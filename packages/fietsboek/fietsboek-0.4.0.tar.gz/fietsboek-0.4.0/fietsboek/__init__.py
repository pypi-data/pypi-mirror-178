"""Fietsboek is a web application to track and share GPX tours.

For more information, see the README or the included documentation.
"""
from pathlib import Path

import importlib_metadata
import redis
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.settings import asbool, aslist
from pyramid.i18n import default_locale_negotiator

from .security import SecurityPolicy
from .data import DataManager
from .pages import Pages
from . import jinja2 as fiets_jinja2


__VERSION__ = importlib_metadata.version('fietsboek')


def locale_negotiator(request):
    """Negotiates the right locale to use.

    This tries the following:
    1. It runs the default negotiator. This allows the locale to be overriden
       by using the _LOCALE_ query parameter.
    2. It uses the `Accept-Language`_ header.

    .. Accept-Language: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language

    :param request: The request for which to get the language.
    :type request: pyramid.request.Request
    :return: The determined locale, or ``None`` if the default should be used.
    :rtype: str
    """
    locale = default_locale_negotiator(request)
    if locale:
        return locale

    installed_locales = request.registry.settings['available_locales']
    sentinel = object()
    negotiated = request.accept_language.lookup(installed_locales, default=sentinel)
    if negotiated is sentinel:
        return None
    return negotiated


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # pylint: disable=unused-argument, import-outside-toplevel, cyclic-import
    from .views import tileproxy
    if settings.get('session_key', '<EDIT THIS>') == '<EDIT THIS>':
        raise ValueError("Please set a session signing key (session_key) in your settings!")

    if 'fietsboek.data_dir' not in settings:
        raise ValueError("Please set a data directory (fietsboek.data_dir) in your settings!")

    def data_manager(request):
        data_dir = request.registry.settings["fietsboek.data_dir"]
        return DataManager(Path(data_dir))

    def redis_(request):
        return redis.from_url(request.registry.settings["redis.url"])

    settings['enable_account_registration'] = asbool(
        settings.get('enable_account_registration', 'false'))
    settings['available_locales'] = aslist(
        settings.get('available_locales', 'en'))
    settings['fietsboek.pages'] = aslist(
        settings.get('fietsboek.pages', ''))
    settings['fietsboek.tile_proxy.disable'] = asbool(
        settings.get('fietsboek.tile_proxy.disable', 'false'))
    settings['thunderforest.maps'] = aslist(
        settings.get('thunderforest.maps', ''))
    settings['fietsboek.default_tile_layers'] = aslist(
        settings.get('fietsboek.default_tile_layers',
                     'osm satellite osmde opentopo topplusopen opensea cycling hiking'))
    settings['fietsboek.tile_layers'] = tileproxy.extract_tile_layers(settings)

    # Load the pages
    page_manager = Pages()
    for path in settings['fietsboek.pages']:
        path = Path(path)
        if path.is_dir():
            page_manager.load_directory(path)
        elif path.is_file():
            page_manager.load_file(path)

    def pages(request):
        return page_manager

    my_session_factory = SignedCookieSessionFactory(settings['session_key'])
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
        config.scan()
        config.add_translation_dirs('fietsboek:locale/')
        config.set_session_factory(my_session_factory)
        config.set_security_policy(SecurityPolicy())
        config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
        config.set_default_csrf_options(require_csrf=True)
        config.set_locale_negotiator(locale_negotiator)
        config.add_request_method(data_manager, reify=True)
        config.add_request_method(pages, reify=True)
        config.add_request_method(redis_, name="redis", reify=True)

    jinja2_env = config.get_jinja2_environment()
    jinja2_env.filters['format_decimal'] = fiets_jinja2.filter_format_decimal
    jinja2_env.filters['format_datetime'] = fiets_jinja2.filter_format_datetime
    jinja2_env.filters['local_datetime'] = fiets_jinja2.filter_local_datetime
    jinja2_env.globals['embed_tile_layers'] = fiets_jinja2.global_embed_tile_layers

    return config.make_wsgi_app()
