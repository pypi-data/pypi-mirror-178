"""Various utility functions."""
import datetime
import re
import os
import unicodedata
import secrets

# Compat for Python < 3.9
import importlib_resources
import babel
import markdown
import bleach
import gpxpy

from pyramid.i18n import TranslationString as _
from pyramid.httpexceptions import HTTPBadRequest
from markupsafe import Markup
from sqlalchemy import select


ALLOWED_TAGS = (bleach.sanitizer.ALLOWED_TAGS +
                # Allow headings
                ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] +
                ['p'] + ['img'])

ALLOWED_ATTRIBUTES = dict(bleach.sanitizer.ALLOWED_ATTRIBUTES)
ALLOWED_ATTRIBUTES['img'] = ['alt', 'src']

# Arbitrarily chosen, just make sure they are representable
DEFAULT_START_TIME = datetime.datetime(1977, 5, 25, 8, 0)
DEFAULT_END_TIME = datetime.datetime(1985, 7, 3, 8, 0)


_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)


def safe_markdown(md_source):
    """Transform a markdown document into a safe HTML document.

    This uses ``markdown`` to first parse the markdown source into HTML, and
    then ``bleach`` to strip any disallowed HTML tags.

    :param md_source: The markdown source.
    :type md_source: str
    :return: The safe HTML transformed version.
    :rtype: Markup
    """
    html = markdown.markdown(md_source, output_format='html5')
    html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return Markup(html)


def fix_iso_timestamp(timestamp):
    """Fixes an ISO timestamp to make it parseable by
    :meth:`datetime.datetime.fromisoformat`.

    This removes an 'Z' if it exists at the end of the timestamp, and replaces
    it with '+00:00'.

    :param timestamp: The timestamp to fix.
    :type timestamp: str
    :return: The fixed timestamp.
    :rtype: str
    """
    if timestamp.endswith('Z'):
        return timestamp[:-1] + '+00:00'
    return timestamp


def round_timedelta_to_multiple(value, multiples):
    """Round the timedelta `value` to be a multiple of `multiples`.

    :param value: The value to be rounded.
    :type value: datetime.timedelta
    :param multiples: The size of each multiple.
    :type multiples: datetime.timedelta
    :return: The rounded value.
    :rtype: datetime.timedelta
    """
    lower = value.total_seconds() // multiples.total_seconds() * multiples.total_seconds()
    second_offset = value.total_seconds() - lower
    if second_offset < multiples.total_seconds() // 2:
        # Round down
        return datetime.timedelta(seconds=lower)
    # Round up
    return datetime.timedelta(seconds=lower) + multiples


def guess_gpx_timezone(gpx):
    """Guess which timezone the GPX file was recorded in.

    This looks at a few timestamps to see if they have timezone information
    attached, including some known GPX extensions.

    :param gpx: The parsed GPX file to analyse.
    :type gpx: gpxpy.GPX
    :return: The timezone information.
    :rtype: datetime.timezone
    """
    time_bounds = gpx.get_time_bounds()
    times = [
        gpx.time,
        time_bounds.start_time,
        time_bounds.end_time,
    ]
    times = [time for time in times if time]
    # First, we check if any of the timestamps has a timezone attached. Note
    # that some devices save their times in UTC, so we need to look for a
    # timestamp different than UTC.
    for time in times:
        if time.tzinfo and time.tzinfo.utcoffset(time):
            return time.tzinfo

    # Next, we look if there's a "localTime" extension on the track, so we can
    # compare the local time to the time.
    if times:
        for track in gpx.tracks:
            time = times[0]
            local_time = None
            for extension in track.extensions:
                if extension.tag.lower() == 'localtime':
                    local_time = datetime.datetime.fromisoformat(
                        fix_iso_timestamp(extension.text)).replace(tzinfo=None)
                elif extension.tag.lower() == 'time':
                    time = datetime.datetime.fromisoformat(
                        fix_iso_timestamp(extension.text)).replace(tzinfo=None)
            if local_time is not None:
                # We found a pair that we can use!
                offset = local_time - time
                # With all the time madness, luckily most time zones seem to stick
                # to an offset that is a multiple of 15 minutes (see
                # https://en.wikipedia.org/wiki/List_of_UTC_offsets). We try to
                # round the value to the nearest of 15 minutes, to prevent any
                # funky offsets from happening due to slight clock desyncs.
                offset = round_timedelta_to_multiple(offset, datetime.timedelta(minutes=15))
                return datetime.timezone(offset)

    # If all else fails, we assume that we are UTC+00:00
    return datetime.timezone.utc


def tour_metadata(gpx_data):
    """Calculate the metadata of the tour.

    Returns a dict with ``length``, ``uphill``, ``downhill``, ``moving_time``,
    ``stopped_time``, ``max_speed``, ``avg_speed``, ``start_time`` and
    ``end_time``.

    :param gpx_data: The GPX data of the tour.
    :type gpx_data: str
    :return: A dictionary with the computed values.
    :rtype: dict
    """
    gpx = gpxpy.parse(gpx_data)
    timezone = guess_gpx_timezone(gpx)
    uphill, downhill = gpx.get_uphill_downhill()
    moving_data = gpx.get_moving_data()
    time_bounds = gpx.get_time_bounds()
    try:
        avg_speed = moving_data.moving_distance / moving_data.moving_time
    except ZeroDivisionError:
        avg_speed = 0.0
    return {
        'length': gpx.length_3d(),
        'uphill': uphill,
        'downhill': downhill,
        'moving_time': moving_data.moving_time,
        'stopped_time': moving_data.stopped_time,
        'max_speed': moving_data.max_speed,
        'avg_speed': avg_speed,
        'start_time': (time_bounds.start_time or DEFAULT_START_TIME).astimezone(timezone),
        'end_time': (time_bounds.end_time or DEFAULT_END_TIME).astimezone(timezone),
    }


def mps_to_kph(mps):
    """Converts meters/second to kilometers/hour.

    :param mps: Input meters/second.
    :type mps: float
    :return: The converted km/h value.
    :rtype: float
    """
    return mps / 1000 * 60 * 60


def month_name(request, month):
    """Returns the localized name for the month with the given number.

    :param request: The pyramid request.
    :type request: pyramid.request.Request
    :param month: Number of the month, 1 = January.
    :type month: int
    :return: The localized month name.
    :rtype: str
    """
    assert 1 <= month <= 12
    locale = babel.Locale.parse(request.localizer.locale_name)
    return locale.months["stand-alone"]["wide"][month]


def random_link_secret(nbytes=20):
    """Safely generates a secret suitable for the link share.

    The returned string consists of characters that are safe to use in a URL.

    :param nbytes: Number of random bytes to use.
    :type nbytes: int
    :return: A randomly drawn string.
    :rtype: str
    """
    return secrets.token_urlsafe(nbytes)


def retrieve_multiple(dbsession, model, params, name):
    """Parses a reply to retrieve multiple database objects.

    This is usable for arrays sent by HTML forms, for example to retrieve all
    badges or all tagged friends.

    If an object could not be found, this raises a
    :class:`~pyramid.httpexceptions.HTTPBadRequest`.

    :raises pyramid.httpexceptions.HTTPBadRequest: If an object could not be
        found.
    :param dbsession: The database session.
    :type dbsession: sqlalchemy.orm.session.Session
    :param model: The model class to retrieve.
    :type model: class
    :param params: The form parameters.
    :type params: webob.multidict.NestedMultiDict
    :param name: Name of the parameter to look for.
    :type name: str
    :return: A list of elements found.
    :rtype: list[model]
    """
    objects = []
    for obj_id in params.getall(name):
        if not obj_id:
            continue
        query = select(model).filter_by(id=obj_id)
        obj = dbsession.execute(query).scalar_one_or_none()
        if obj is None:
            raise HTTPBadRequest()
        objects.append(obj)
    return objects


def check_password_constraints(password, repeat_password=None):
    """Verifies that the password constraints match for the given password.

    This is usually also verified client-side, but for people that bypass the
    client side verification and the API, this is re-implemented here.

    If ``repeat_password`` is given, this also verifies that the two passwords
    match.

    :raises ValueError: If the verification of the constraints failed. The
        first arg of the error will be a
        :class:`~pyramid.i18n.TranslationString` with the message of why the
        verification failed.
    :param password: The password which to verify.
    :type password: str
    :param repeat_password: The password repeat.
    :type repeat_password: str
    """
    if repeat_password is not None:
        if repeat_password != password:
            raise ValueError(_("password_constraint.mismatch"))
    if len(password) < 8:
        raise ValueError(_("password_constraint.length"))


def read_localized_resource(locale_name, path, raise_on_error=False):
    """Reads a localized resource.

    Localized resources are located in the ``fietsboek/locale/**`` directory.
    Note that ``path`` may contain slashes.

    If the resource could not be found, a placeholder string is returned instead.

    :param locale_name: Name of the locale.
    :type locale_name: str
    :param raise_on_error: Raise an error instead of returning a placeholder.
    :type raise_on_error: bool
    :raises FileNotFoundError: If the path could not be found and
        ``raise_on_error`` is ``True``.
    :return: The text content of the resource.
    :rtype: str
    """
    locales = [locale_name]
    # Second chance: If the locale is a specific form of a more general
    # locale, try the general locale as well.
    if "_" in locale_name:
        locales.append(locale_name.split("_", 1)[0])

    for locale in locales:
        locale_dir = importlib_resources.files('fietsboek') / 'locale' / locale
        resource_path = locale_dir / path
        try:
            return resource_path.read_text()
        except (FileNotFoundError, ModuleNotFoundError, NotADirectoryError):
            pass
    if raise_on_error:
        raise FileNotFoundError(f"Resource {path!r} not found")
    return f"{locale_name}:{path}"


def secure_filename(filename):
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.
    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    :param filename: the filename to secure
    :type filename: str
    :return: The secure filename.
    :rtype: str
    """
    # Taken from
    # https://github.com/pallets/werkzeug/blob/main/src/werkzeug/utils.py

    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".", maxsplit=1)[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename
