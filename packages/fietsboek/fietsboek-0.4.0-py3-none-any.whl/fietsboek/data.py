"""Data manager for fietsboek.

Data are objects that belong to a track (such as images), but are not stored in
the database itself. This module makes access to such data objects easier.
"""
import random
import string
import shutil
import uuid
import logging

from .util import secure_filename


LOGGER = logging.getLogger(__name__)


def generate_filename(filename):
    """Generates a safe-to-use filename for uploads.

    If possible, tries to keep parts of the original filename intact, such as
    the extension.

    :param filename: The original filename.
    :type filename: str
    :return: The generated filename.
    :rtype: str
    """
    if filename:
        good_name = secure_filename(filename)
        if good_name:
            random_prefix = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
            return f"{random_prefix}_{good_name}"

    return str(uuid.uuid4())


class DataManager:
    """Data manager.

    The data manager is usually provided as ``request.data_manager`` and can be
    used to access track's images and other on-disk data.

    :ivar data_dir: Path to the data folder.
    :vartype data_dir: pathlib.Path
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def _track_data_dir(self, track_id):
        return self.data_dir / "tracks" / str(track_id)

    def images(self, track_id):
        """Returns a list of images that belong to a track.

        :param track_id: Numerical ID of the track.
        :type track_id: int
        :return: A list of image IDs.
        :rtype: list[str]
        """
        image_dir = self._track_data_dir(track_id) / "images"
        if not image_dir.exists():
            return []
        images = []
        for image in image_dir.iterdir():
            images.append(image.name)
        return images

    def purge(self, track_id):
        """Purge all data pertaining to the given track.

        This function logs errors but raises no exception, as such it can
        always be used to clean up after a track.

        :param track_id: The ID of the track.
        :type track_id: int
        """
        def log_error(_, path, exc_info):
            LOGGER.warning("Failed to remove %s", path, exc_info=exc_info)

        path = self._track_data_dir(track_id)
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=False, onerror=log_error)

    def image_path(self, track_id, image_id):
        """Returns a path to a saved image.

        :raises FileNotFoundError: If the given image could not be found.
        :param track_id: ID of the track.
        :type track_id: int
        :param image_id: ID of the image.
        :type image_id: str
        :return: A path pointing to the requested image.
        :rtype: pathlib.Path
        """
        image = self._track_data_dir(track_id) / "images" / secure_filename(image_id)
        if not image.exists():
            raise FileNotFoundError("The requested image does not exist")
        return image

    def add_image(self, track_id, image, filename=None):
        """Saves an image to a track.

        :param track_id: ID of the track.
        :type track_id: int
        :param image: The image, as a file-like object to read from.
        :type image: file
        :param filename: The image's original filename.
        :type filename: str
        :return: The ID of the saved image.
        :rtype: str
        """
        image_dir = self._track_data_dir(track_id) / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        filename = generate_filename(filename)
        path = image_dir / filename
        with open(path, "wb") as fobj:
            shutil.copyfileobj(image, fobj)

        return filename

    def delete_image(self, track_id, image_id):
        """Deletes an image from a track.

        :raises FileNotFoundError: If the given image could not be found.
        :param track_id: ID of the track.
        :type track_id: int
        :param image_id: ID of the image.
        :type image_id: str
        """
        # Be sure to not delete anything else than the image file
        image_id = secure_filename(image_id)
        if '/' in image_id or '\\' in image_id:
            return
        path = self.image_path(track_id, image_id)
        path.unlink()
