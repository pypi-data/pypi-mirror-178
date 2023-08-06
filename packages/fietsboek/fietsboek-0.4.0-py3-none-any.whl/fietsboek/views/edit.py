"""Views for editing a track."""
import re
import logging
import datetime
from collections import namedtuple

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy import select

from .. import models, util
from ..models.track import Visibility, TrackType


ImageEmbed = namedtuple("ImageEmbed", "name url description")

LOGGER = logging.getLogger(__name__)


@view_config(route_name='edit', renderer='fietsboek:templates/edit.jinja2',
             permission='track.edit', request_method='GET')
def edit(request):
    """Renders the edit form.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    track = request.context
    badges = request.dbsession.execute(select(models.Badge)).scalars()
    badges = [(badge in track.badges, badge) for badge in badges]

    images = []
    for image in request.data_manager.images(track.id):
        metadata = request.dbsession.execute(
                select(models.ImageMetadata).filter_by(track=track, image_name=image)
            ).scalar_one_or_none()
        if metadata:
            description = metadata.description
        else:
            description = ""
        img_src = request.route_url("image", track_id=track.id, image_name=image)
        images.append(ImageEmbed(image, img_src, description))

    return {
        'track': track,
        'badges': badges,
        'images': images,
    }


@view_config(route_name='edit', permission='track.edit', request_method='POST')
def do_edit(request):
    """Endpoint for saving the edited data.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    # pylint: disable=duplicate-code
    track = request.context

    user_friends = request.identity.get_friends()
    badges = util.retrieve_multiple(request.dbsession, models.Badge, request.params, "badge[]")
    tagged_people = util.retrieve_multiple(request.dbsession, models.User,
                                           request.params, "tagged-friend[]")

    if any(user not in track.tagged_people and user not in user_friends for user in tagged_people):
        return HTTPBadRequest()

    tz_offset = datetime.timedelta(minutes=int(request.params["date-tz"]))
    date = datetime.datetime.fromisoformat(request.params["date"])
    track.date = date.replace(tzinfo=datetime.timezone(tz_offset))

    track.tagged_people = tagged_people
    track.title = request.params["title"]
    track.visibility = Visibility[request.params["visibility"]]
    track.type = TrackType[request.params["type"]]
    track.description = request.params["description"]
    track.badges = badges
    tags = request.params.getall("tag[]")
    track.sync_tags(tags)

    edit_images(request, request.context)

    return HTTPFound(request.route_url('details', track_id=track.id))


def edit_images(request, track):
    """Edit the images from the given request.

    This deletes and adds images and image descriptions as needed, based on the
    image[...] and image-description[...] fields.

    :param request: The request:
    :type request: pyramid.request.Request
    :param track: The track to edit.
    :type track: fietsboek.models.track.Track
    """

    # Delete requested images
    for image in request.params.getall("delete-image[]"):
        request.data_manager.delete_image(track.id, image)
        image_meta = request.dbsession.execute(
                select(models.ImageMetadata).filter_by(track_id=track.id, image_name=image)
            ).scalar_one_or_none()
        LOGGER.debug("Deleted image %s %s (metadata: %s)", track.id, image, image_meta)
        if image_meta:
            request.dbsession.delete(image_meta)

    # Add new images
    set_descriptions = set()
    for param_name, image in request.params.items():
        match = re.match("image\\[(\\d+)\\]$", param_name)
        if not match:
            continue
        # Sent for the multi input
        if image == b"":
            continue

        upload_id = match.group(1)
        image_name = request.data_manager.add_image(track.id, image.file, image.filename)
        image_meta = models.ImageMetadata(track=track, image_name=image_name)
        image_meta.description = request.params.get(f"image-description[{upload_id}]", "")
        request.dbsession.add(image_meta)
        LOGGER.debug("Uploaded image %s %s", track.id, image_name)
        set_descriptions.add(upload_id)

    images = request.data_manager.images(track.id)
    # Set image descriptions
    for param_name, description in request.params.items():
        match = re.match("image-description\\[(.+)\\]$", param_name)
        if not match:
            continue
        image_id = match.group(1)
        # Descriptions that we already set while adding new images can be
        # ignored
        if image_id in set_descriptions:
            continue
        # Did someone give us a wrong ID?!
        if image_id not in images:
            LOGGER.info("Got a ghost image description for track %s: %s", track.id, image_id)
            continue
        image_meta = models.ImageMetadata.get_or_create(request.dbsession, track, image_id)
        image_meta.description = description
        request.dbsession.add(image_meta)
