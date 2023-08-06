"""Tile proxying layer.

While this might slow down the initial load (as we now load everything through
fietsboek), we can cache the OSM tiles per instance, and we can provide better
access control for services like thunderforest.com.

Additionally, this protects the users' IP, as only fietsboek can see it.
"""
import datetime
import random
import logging
import re
from enum import Enum
from typing import NamedTuple
from itertools import chain

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPGatewayTimeout

import requests
from requests.exceptions import ReadTimeout

from .. import __VERSION__


class LayerType(Enum):
    """Enum to distinguish base layers and overlay layers."""
    BASE = "base"
    OVERLAY = "overlay"


class LayerAccess(Enum):
    """Enum discerning whether a layer is publicly accessible or restriced to
    logged-in users.

    Note that in the future, a finer-grained distinction might be possible.
    """
    PUBLIC = "public"
    RESTRICTED = "restricted"


class TileSource(NamedTuple):
    """Represents a remote server that can provide tiles to us."""
    key: str
    """Key to indicate this source in URLs."""
    name: str
    """Human-readable name of the source."""
    url_template: str
    """URL with placeholders."""
    layer_type: LayerType
    """Type of this layer."""
    zoom: int
    """Max zoom of this layer."""
    access: LayerAccess
    """Access restrictions to use this layer."""
    attribution: str
    """Attribution string."""


LOGGER = logging.getLogger(__name__)


def _href(url, text):
    return f'<a href="{url}" target="_blank">{text}</a>'


_jb_copy = _href("https://www.j-berkemeier.de/GPXViewer", "GPXViewer")


DEFAULT_TILE_LAYERS = [
    # Main base layers
    TileSource(
        'osm',
        'OSM',
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        LayerType.BASE,
        19,
        LayerAccess.PUBLIC,
        ''.join([
            _jb_copy, ' | Map data &copy; ',
            _href("https://www.openstreetmap.org/", "OpenStreetMap"), ' and contributors ',
            _href("https://creativecommons.org/licenses/by-sa/2.0/", "CC-BY-SA"),
        ]),
    ),
    TileSource(
        'satellite',
        'Satellit',
        'https://server.arcgisonline.com/ArcGIS/rest/services/'
        'World_Imagery/MapServer/tile/{z}/{y}/{x}',
        LayerType.BASE,
        21,
        LayerAccess.PUBLIC,
        ''.join([
            _jb_copy, ' | Map data &copy; ', _href("https://www.esri.com", "Esri"),
            ', i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, ',
            'IGP, UPR-EGP, and the GIS User Community',
        ]),
    ),
    TileSource(
        'osmde',
        'OSMDE',
        'https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png',
        LayerType.BASE,
        19,
        LayerAccess.PUBLIC,
        ''.join([
            _jb_copy, ' | Map data &copy; ',
            _href("https://www.openstreetmap.org/", "OpenStreetMap"), ' and contributors ',
            _href("https://creativecommons.org/licenses/by-sa/2.0/", "CC-BY-SA")
        ]),
    ),
    TileSource(
        'opentopo',
        'Open Topo',
        'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        LayerType.BASE,
        17,
        LayerAccess.PUBLIC,
        ''.join([
            _jb_copy,
            ' | Kartendaten: © OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © ',
            _href("https://opentopomap.org/about", "OpenTopoMap"), ' (CC-BY-SA)',
        ]),
    ),
    TileSource(
        'topplusopen',
        'TopPlusOpen',
        'https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/'
        '1.0.0/web/default/WEBMERCATOR/{z}/{y}/{x}.png',
        LayerType.BASE,
        18,
        LayerAccess.PUBLIC,
        ''.join([
            _jb_copy, ' | Kartendaten: © ',
            _href("https://www.bkg.bund.de/SharedDocs/Produktinformationen"
                  "/BKG/DE/P-2017/170922-TopPlus-Web-Open.html",
                  "Bundesamt für Kartographie und Geodäsie"),
        ]),
    ),

    # Overlay layers
    TileSource(
        'opensea',
        'OpenSea',
        'https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
        LayerType.OVERLAY,
        None,
        LayerAccess.PUBLIC,
        'Kartendaten: © <a href="http://www.openseamap.org">OpenSeaMap</a> contributors',
    ),
    TileSource(
        'hiking',
        'Hiking',
        'https://tile.waymarkedtrails.org/hiking/{z}/{x}/{y}.png',
        LayerType.OVERLAY,
        None,
        LayerAccess.PUBLIC,
        f'&copy; {_href("http://waymarkedtrails.org", "Sarah Hoffmann")} '
        f'({_href("https://creativecommons.org/licenses/by-sa/3.0/", "CC-BY-SA")})',
    ),
    TileSource(
        'cycling',
        'Cycling',
        'https://tile.waymarkedtrails.org/cycling/{z}/{x}/{y}.png',
        LayerType.OVERLAY,
        None,
        LayerAccess.PUBLIC,
        f'&copy; {_href("http://waymarkedtrails.org", "Sarah Hoffmann")} '
        f'({_href("https://creativecommons.org/licenses/by-sa/3.0/", "CC-BY-SA")})',
    ),
]

TTL = datetime.timedelta(days=7)
"""Time to live of cached tiles."""

TIMEOUT = datetime.timedelta(seconds=1.5)
"""Timeout when requesting new tiles from a source server."""

PUNISHMENT_TTL = datetime.timedelta(minutes=10)
"""Block-out period after too many requests of a server have timed out."""

PUNISHMENT_THRESHOLD = 10
"""Block a provider after that many requests have timed out."""


@view_config(route_name='tile-proxy', http_cache=3600)
def tile_proxy(request):
    """Requests the given tile from the proxy.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    if request.registry.settings.get("fietsboek.tile_proxy.disable"):
        raise HTTPBadRequest("Tile proxying is disabled")

    provider = request.matchdict['provider']
    tile_sources = {source.key: source for source in sources_for(request)}
    if provider not in tile_sources:
        raise HTTPBadRequest("Invalid provider")

    x, y, z = (int(request.matchdict['x']), int(request.matchdict['y']),
               int(request.matchdict['z']))
    cache_key = f"tile:{provider}-{x}-{y}-{z}"
    content_type = "image/png"

    cached = request.redis.get(cache_key)
    if cached is not None:
        return Response(cached, content_type=content_type)

    timeout_tracker = f"provider-timeout:{provider}"
    if int(request.redis.get(timeout_tracker) or "0") > PUNISHMENT_THRESHOLD:
        # We've gotten too many timeouts from this provider recently, so avoid
        # contacting it in the first place.
        LOGGER.debug("Aborted attempt to contact %s due to previous timeouts", provider)
        raise HTTPGatewayTimeout(f"Avoiding request to {provider}")

    url = tile_sources[provider].url_template.format(x=x, y=y, z=z, s=random.choice("abc"))
    headers = {
        "user-agent": f"Fietsboek-Tile-Proxy/{__VERSION__}",
    }
    from_mail = request.registry.settings.get('email.from')
    if from_mail:
        headers["from"] = from_mail

    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT.total_seconds())
    except ReadTimeout:
        LOGGER.debug("Proxy timeout when accessing %r", url)
        request.redis.incr(timeout_tracker)
        request.redis.expire(timeout_tracker, PUNISHMENT_TTL)
        raise HTTPGatewayTimeout(f"No response in time from {provider}") from None
    else:
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            LOGGER.info("Proxy request failed for %s: %s", provider, exc)
            return Response(f"Failed to get tile from {provider}",
                            status_code=resp.status_code)
        request.redis.set(cache_key, resp.content, ex=TTL)
        return Response(resp.content, content_type=resp.headers.get("Content-type", content_type))


def sources_for(request):
    """Returns all eligible tile sources for the given request.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: A list of tile sources.
    :rtype: list[TileSource]
    """
    settings = request.registry.settings
    return [
        source for source in chain(
            (default_layer for default_layer in DEFAULT_TILE_LAYERS
             if default_layer.key in settings["fietsboek.default_tile_layers"]),
            settings["fietsboek.tile_layers"]
        )
        if source.access == LayerAccess.PUBLIC or request.identity is not None
    ]


def extract_tile_layers(settings):
    """Extract all defined tile layers from the settings.

    :param settings: The application settings.
    :type settings: dict
    :return: A list of extracted tile sources.
    :rtype: list[TileSource]
    """
    layers = []
    layers.extend(_extract_thunderforest(settings))
    layers.extend(_extract_user_layers(settings))
    return layers


def _extract_thunderforest(settings):
    # Thunderforest Shortcut!
    tf_api_key = settings.get("thunderforest.api_key")
    if tf_api_key:
        tf_access = LayerAccess(settings.get("thunderforest.access", "restricted"))
        tf_attribution = ' | '.join([
            _jb_copy,
            _href("https://www.thunderforest.com/", "Thunderforest"),
            _href("https://www.openstreetmap.org/", "OpenStreetMap"),
        ])
        for tf_map in settings["thunderforest.maps"]:
            url = (f"https://tile.thunderforest.com/{tf_map}/"
                   f"{{z}}/{{x}}/{{y}}.png?apikey={tf_api_key}")
            yield TileSource(
                f"tf-{tf_map}", f"TF {tf_map.title()}", url,
                LayerType.BASE, 22, tf_access, tf_attribution,
            )


def _extract_user_layers(settings):
    # Any other custom maps
    for key in settings.keys():
        match = re.match("^fietsboek\\.tile_layer\\.([A-Za-z0-9_-]+)$", key)
        if not match:
            continue

        provider_id = match.group(1)
        name = settings[key]
        url = settings[f"{key}.url"]
        layer_type = LayerType(settings.get(f"{key}.type", "base"))
        zoom = int(settings.get(f"{key}.zoom", 22))
        attribution = settings.get(f"{key}.attribution", _jb_copy)
        access = LayerAccess(settings.get(f"{key}.access", "public"))

        yield TileSource(provider_id, name, url, layer_type, zoom, access, attribution)
