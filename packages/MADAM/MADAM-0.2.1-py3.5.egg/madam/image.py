import io
from enum import Enum

from bidict import bidict
import piexif
import PIL.ExifTags
import PIL.Image

from madam.core import operator, OperatorError
from madam.core import Asset, Processor, MetadataProcessor, UnsupportedFormatError


class ExifProcessor(MetadataProcessor):
    """
    Represents a metadata processor that supports Exif data.
    """
    @property
    def format(self):
        return 'exif'

    def read(self, file):
        data = file.read()
        try:
            exif = piexif.load(data)
        except ValueError:
            raise UnsupportedFormatError()
        exif_stripped_from_empty_entries = {key: value for (key, value) in exif.items() if value}
        return exif_stripped_from_empty_entries

    def strip(self, file):
        data = file.read()
        essence_without_metadata_as_stream = io.BytesIO()
        piexif.remove(data, essence_without_metadata_as_stream)
        return essence_without_metadata_as_stream

    def combine(self, file, exif):
        file_with_exif = io.BytesIO()
        piexif.insert(piexif.dump(exif), file.read(), new_file=file_with_exif)
        return file_with_exif


class ResizeMode(Enum):
    """
    Represents a behavior for image resize operations.
    """
    #: Resized image exactly matches the specified dimensions
    EXACT = 0
    #: Resized image is resized to fit completely into the specified dimensions
    FIT = 1
    #: Resized image is resized to completely fill the specified dimensions
    FILL = 2


class FlipOrientation(Enum):
    """
    Represents an axis for image flip operations.
    """
    #: Horizontal axis
    HORIZONTAL = 0
    #: Vertical axis
    VERTICAL = 1


class PillowProcessor(Processor):
    """
    Represents a processor that uses Pillow as a backend.
    """
    def __init__(self):
        super().__init__()
        self.__mime_type_to_pillow_type = bidict({
            'image/jpeg': 'JPEG',
            'image/png': 'PNG'
        })

    def _read(self, file):
        image = PIL.Image.open(file)
        metadata = dict(
            mime_type=self.__mime_type_to_pillow_type.inv[image.format],
            width=image.width,
            height=image.height
        )
        file.seek(0)
        asset = Asset(file, **metadata)
        return asset

    def _can_read(self, file):
        try:
            PIL.Image.open(file)
            file.seek(0)
            return True
        except IOError:
            return False
        except:
            raise ValueError('Error when reading file-like object: %r' % file)

    @operator
    def resize(self, asset, width, height, mode=ResizeMode.EXACT):
        """
        Creates a new Asset whose essence is resized according to the specified parameters.

        :param asset: Asset to be resized
        :param width: target width
        :param height: target height
        :param mode: resize behavior
        :return: Asset with resized essence
        """
        image = PIL.Image.open(asset.essence)
        width_delta = width - image.width
        height_delta = height - image.height
        resized_width = width
        resized_height = height
        if mode in (ResizeMode.FIT, ResizeMode.FILL):
            if mode == ResizeMode.FIT and width_delta < height_delta or \
               mode == ResizeMode.FILL and width_delta > height_delta:
                resize_factor = width / image.width
            else:
                resize_factor = height / image.height
            resized_width = round(resize_factor * image.width)
            resized_height = round(resize_factor * image.height)
        resized_image = image.resize((resized_width, resized_height),
                                     resample=PIL.Image.LANCZOS)
        resized_asset = self._image_to_asset(resized_image)
        return resized_asset

    def _image_to_asset(self, image):
        image_buffer = io.BytesIO()
        image.save(image_buffer, 'JPEG')
        image_buffer.seek(0)
        asset = self._read(image_buffer)
        return asset

    def _rotate(self, asset, rotation):
        """
        Creates a new image asset from specified asset whose essence is rotated
        by the specified rotation.

        :param asset: Image asset to be rotated
        :param rotation: One of ``PIL.Image.FLIP_LEFT_RIGHT``,
        ``PIL.Image.FLIP_TOP_BOTTOM``, ``PIL.Image.ROTATE_90``,
        ``PIL.Image.ROTATE_180``, ``PIL.Image.ROTATE_270``, or
        ``PIL.Image.TRANSPOSE``
        :return: New image asset with rotated essence
        """
        image = PIL.Image.open(asset.essence)
        transposed_image = image.transpose(rotation)
        transposed_asset = self._image_to_asset(transposed_image)
        return transposed_asset

    @operator
    def transpose(self, asset):
        """
        Creates a new image asset whose essence is the transpose of the
        specified asset's essence.

        :param asset: Image asset whose essence is to be transposed
        :return: New image asset with transposed essence
        """
        return self._rotate(asset, PIL.Image.TRANSPOSE)

    @operator
    def flip(self, asset, orientation):
        """
        Creates a new asset whose essence is flipped according the specified orientation.

        :param asset: Asset whose essence is to be flipped
        :param orientation: axis of the flip operation
        :return: Asset with flipped essence
        """
        if orientation == FlipOrientation.HORIZONTAL:
            flip_orientation = PIL.Image.FLIP_LEFT_RIGHT
        else:
            flip_orientation = PIL.Image.FLIP_TOP_BOTTOM
        return self._rotate(asset, flip_orientation)

    @operator
    def auto_orient(self, asset):
        """
        Creates a new asset whose essence is rotated according to the Exif orientation.

        :param asset: Asset with Exif metadata
        :return: Asset with rotated essence
        """
        orientation = asset.metadata['exif']['0th'][piexif.ImageIFD.Orientation]
        if orientation == 1:
            oriented_asset = Asset(asset.essence, metadata={})
        elif orientation == 2:
            oriented_asset = self.flip(orientation=FlipOrientation.HORIZONTAL)(asset)
        elif orientation == 3:
            oriented_asset = self._rotate(asset, PIL.Image.ROTATE_180)
        elif orientation == 4:
            oriented_asset = self.flip(orientation=FlipOrientation.VERTICAL)(asset)
        elif orientation == 5:
            oriented_asset = self.flip(orientation=FlipOrientation.VERTICAL)(self._rotate(asset, PIL.Image.ROTATE_90))
        elif orientation == 6:
            oriented_asset = self._rotate(asset, PIL.Image.ROTATE_270)
        elif orientation == 7:
            oriented_asset = self.flip(orientation=FlipOrientation.HORIZONTAL)(self._rotate(asset, PIL.Image.ROTATE_90))
        elif orientation == 8:
            oriented_asset = self._rotate(asset, PIL.Image.ROTATE_90)
        else:
            raise OperatorError('Unable to correct image orientation with value %s' % orientation)

        return oriented_asset

    @operator
    def convert(self, asset, mime_type):
        """
        Creates a new asset of the specified MIME type from the essence of the
        specified asset.

        :param asset: Asset whose contents will be converted
        :param mime_type: Target MIME type
        :return: New asset with converted essence
        """
        pil_format = self.__mime_type_to_pillow_type[mime_type]
        try:
            image = PIL.Image.open(asset.essence)
            converted_essence_data = io.BytesIO()
            image.save(converted_essence_data, pil_format)
        except (IOError, KeyError) as pil_error:
            raise OperatorError('Could not convert image: %s', pil_error)
        converted_essence_data.seek(0)

        converted_asset = Asset(converted_essence_data, mime_type=mime_type)
        return converted_asset
