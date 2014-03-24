""":mod:`wand.image` --- Image objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens and manipulates images. Image objects can be used in :keyword:`with`
statement, and these resources will be automatically managed (even if any
error happened)::

    with Image(filename='pikachu.png') as i:
        print('width =', i.width)
        print('height =', i.height)

"""
import collections
import ctypes
import functools
import numbers
import weakref

from . import compat
from .api import MagickPixelPacket, libc, libmagick, library
from .color import Color
from .compat import (binary, binary_type, encode_filename, file_types,
                     string_type, text, xrange)
from .exceptions import WandException
from .resource import DestroyedResourceError, Resource
from .font import Font


__all__ = ('ALPHA_CHANNEL_TYPES', 'CHANNELS', 'COLORSPACE_TYPES',
           'COMPOSITE_OPERATORS', 'EVALUATE_OPS', 'FILTER_TYPES',
           'GRAVITY_TYPES', 'IMAGE_TYPES', 'ORIENTATION_TYPES', 'UNIT_TYPES',
           'BaseImage', 'ChannelDepthDict', 'ChannelImageDict',
           'ClosedImageError', 'HistogramDict', 'Image', 'ImageProperty',
           'Iterator', 'Metadata', 'OptionDict', 'manipulative')


#: (:class:`tuple`) The list of filter types.
#:
#: - ``'undefined'``
#: - ``'point'``
#: - ``'box'``
#: - ``'triangle'``
#: - ``'hermite'``
#: - ``'hanning'``
#: - ``'hamming'``
#: - ``'blackman'``
#: - ``'gaussian'``
#: - ``'quadratic'``
#: - ``'cubic'``
#: - ``'catrom'``
#: - ``'mitchell'``
#: - ``'jinc'``
#: - ``'sinc'``
#: - ``'sincfast'``
#: - ``'kaiser'``
#: - ``'welsh'``
#: - ``'parzen'``
#: - ``'bohman'``
#: - ``'bartlett'``
#: - ``'lagrange'``
#: - ``'lanczos'``
#: - ``'lanczossharp'``
#: - ``'lanczos2'``
#: - ``'lanczos2sharp'``
#: - ``'robidoux'``
#: - ``'robidouxsharp'``
#: - ``'cosine'``
#: - ``'spline'``
#: - ``'sentinel'``
#:
#: .. seealso::
#:
#:    `ImageMagick Resize Filters`__
#:       Demonstrates the results of resampling images using the various
#:       resize filters and blur settings available in ImageMagick.
#:
#:    __ http://www.imagemagick.org/Usage/resize/
FILTER_TYPES = ('undefined', 'point', 'box', 'triangle', 'hermite', 'hanning',
                'hamming', 'blackman', 'gaussian', 'quadratic', 'cubic',
                'catrom', 'mitchell', 'jinc', 'sinc', 'sincfast', 'kaiser',
                'welsh', 'parzen', 'bohman', 'bartlett', 'lagrange', 'lanczos',
                'lanczossharp', 'lanczos2', 'lanczos2sharp', 'robidoux',
                'robidouxsharp', 'cosine', 'spline', 'sentinel')

#: (:class:`tuple`) The list of composition operators
#:
#: - ``'undefined'``
#: - ``'no'``
#: - ``'add'``
#: - ``'atop'``
#: - ``'blend'``
#: - ``'bumpmap'``
#: - ``'change_mask'``
#: - ``'clear'``
#: - ``'color_burn'``
#: - ``'color_dodge'``
#: - ``'colorize'``
#: - ``'copy_black'``
#: - ``'copy_blue'``
#: - ``'copy'``
#: - ``'copy_cyan'``
#: - ``'copy_green'``
#: - ``'copy_magenta'``
#: - ``'copy_opacity'``
#: - ``'copy_red'``
#: - ``'copy_yellow'``
#: - ``'darken'``
#: - ``'dst_atop'``
#: - ``'dst'``
#: - ``'dst_in'``
#: - ``'dst_out'``
#: - ``'dst_over'``
#: - ``'difference'``
#: - ``'displace'``
#: - ``'dissolve'``
#: - ``'exclusion'``
#: - ``'hard_light'``
#: - ``'hue'``
#: - ``'in'``
#: - ``'lighten'``
#: - ``'linear_light'``
#: - ``'luminize'``
#: - ``'minus'``
#: - ``'modulate'``
#: - ``'multiply'``
#: - ``'out'``
#: - ``'over'``
#: - ``'overlay'``
#: - ``'plus'``
#: - ``'replace'``
#: - ``'saturate'``
#: - ``'screen'``
#: - ``'soft_light'``
#: - ``'src_atop'``
#: - ``'src'``
#: - ``'src_in'``
#: - ``'src_out'``
#: - ``'src_over'``
#: - ``'subtract'``
#: - ``'threshold'``
#: - ``'xor'``
#: - ``'divide'``
#:
#: .. versionchanged:: 0.3.0
#:    Renamed from :const:`COMPOSITE_OPS` to :const:`COMPOSITE_OPERATORS`.
#:
#: .. seealso::
#:
#:    `Compositing Images`__ ImageMagick v6 Examples
#:       Image composition is the technique of combining images that have,
#:       or do not have, transparency or an alpha channel.
#:       This is usually performed using the IM :program:`composite` command.
#:       It may also be performed as either part of a larger sequence of
#:       operations or internally by other image operators.
#:
#:    `ImageMagick Composition Operators`__
#:       Demonstrates the results of applying the various composition
#:       composition operators.
#:
#:    __ http://www.imagemagick.org/Usage/compose/
#:    __ http://www.rubblewebs.co.uk/imagemagick/operators/compose.php
COMPOSITE_OPERATORS = (
    'undefined', 'no', 'add', 'atop', 'blend', 'bumpmap', 'change_mask',
    'clear', 'color_burn', 'color_dodge', 'colorize', 'copy_black',
    'copy_blue', 'copy', 'copy_cyan', 'copy_green', 'copy_magenta',
    'copy_opacity', 'copy_red', 'copy_yellow', 'darken', 'dst_atop', 'dst',
    'dst_in', 'dst_out', 'dst_over', 'difference', 'displace', 'dissolve',
    'exclusion', 'hard_light', 'hue', 'in', 'lighten', 'linear_light',
    'luminize', 'minus', 'modulate', 'multiply', 'out', 'over', 'overlay',
    'plus', 'replace', 'saturate', 'screen', 'soft_light', 'src_atop', 'src',
    'src_in', 'src_out', 'src_over', 'subtract', 'threshold', 'xor', 'divide'
)

#: (:class:`dict`) The dictionary of channel types.
#:
#: - ``'undefined'``
#: - ``'red'``
#: - ``'gray'``
#: - ``'cyan'``
#: - ``'green'``
#: - ``'magenta'``
#: - ``'blue'``
#: - ``'yellow'``
#: - ``'alpha'``
#: - ``'opacity'``
#: - ``'black'``
#: - ``'index'``
#: - ``'composite_channels'``
#: - ``'all_channels'``
#: - ``'true_alpha'``
#: - ``'rgb_channels'``
#: - ``'gray_channels'``
#: - ``'sync_channels'``
#: - ``'default_channels'``
#:
#: .. seealso::
#:
#:    `ImageMagick Color Channels`__
#:       Lists the various channel types with descriptions of each
#:
#:    __ http://www.imagemagick.org/Magick++/Enumerations.html#ChannelType
CHANNELS = dict(undefined=0, red=1, gray=1, cyan=1, green=2, magenta=2,
                blue=4, yellow=4, alpha=8, opacity=8, black=32, index=32,
                composite_channels=47, all_channels=134217727, true_alpha=64,
                rgb_channels=128, gray_channels=128, sync_channels=256,
                default_channels=134217719)

#: (:class:`tuple`) The list of evaluation operators
#:
#: - ``'undefined'``
#: - ``'add'``
#: - ``'and'``
#: - ``'divide'``
#: - ``'leftshift'``
#: - ``'max'``
#: - ``'min'``
#: - ``'multiply'``
#: - ``'or'``
#: - ``'rightshift'``
#: - ``'set'``
#: - ``'subtract'``
#: - ``'xor'``
#: - ``'pow'``
#: - ``'log'``
#: - ``'threshold'``
#: - ``'thresholdblack'``
#: - ``'thresholdwhite'``
#: - ``'gaussiannoise'``
#: - ``'impulsenoise'``
#: - ``'laplaciannoise'``
#: - ``'multiplicativenoise'``
#: - ``'poissonnoise'``
#: - ``'uniformnoise'``
#: - ``'cosine'``
#: - ``'sine'``
#: - ``'addmodulus'``
#: - ``'mean'``
#: - ``'abs'``
#: - ``'exponential'``
#: - ``'median'``
#: - ``'sum'``
#:
#: .. seealso::
#:
#:    `ImageMagick Image Evaluation Operators`__
#:       Describes the MagickEvaluateImageChannel method and lists the
#:       various evaluations operators
#:
#:    __ http://www.magickwand.org/MagickEvaluateImage.html
EVALUATE_OPS = ('undefined', 'add', 'and', 'divide', 'leftshift', 'max',
                'min', 'multiply', 'or', 'rightshift', 'set', 'subtract',
                'xor', 'pow', 'log', 'threshold', 'thresholdblack',
                'thresholdwhite', 'gaussiannoise', 'impulsenoise',
                'laplaciannoise', 'multiplicativenoise', 'poissonnoise',
                'uniformnoise', 'cosine', 'sine', 'addmodulus', 'mean',
                'abs', 'exponential', 'median', 'sum')

#: (:class:`tuple`) The list of colorspaces.
#:
#: - ``'undefined'``
#: - ``'rgb'``
#: - ``'gray'``
#: - ``'transparent'``
#: - ``'ohta'``
#: - ``'lab'``
#: - ``'xyz'``
#: - ``'ycbcr'``
#: - ``'ycc'``
#: - ``'yiq'``
#: - ``'ypbpr'``
#: - ``'yuv'``
#: - ``'cmyk'``
#: - ``'srgb'``
#: - ``'hsb'``
#: - ``'hsl'``
#: - ``'hwb'``
#: - ``'rec601luma'``
#: - ``'rec601ycbcr'``
#: - ``'rec709luma'``
#: - ``'rec709ycbcr'``
#: - ``'log'``
#: - ``'cmy'``
#: - ``'luv'``
#: - ``'hcl'``
#: - ``'lch'``
#: - ``'lms'``
#: - ``'lchab'``
#: - ``'lchuv'``
#: - ``'scrgb'``
#: - ``'hsi'``
#: - ``'hsv'``
#: - ``'hclp'``
#: - ``'ydbdr'``
#:
#: .. seealso::
#:
#:    `ImageMagick Color Management`__
#:       Describes the ImageMagick color management operations
#:
#:    __ http://www.imagemagick.org/script/color-management.php
#:
#: .. versionadded:: 0.3.4
COLORSPACE_TYPES = ('undefined', 'rgb', 'gray', 'transparent', 'ohta', 'lab',
                    'xyz', 'ycbcr', 'ycc', 'yiq', 'ypbpr', 'yuv', 'cmyk',
                    'srgb', 'hsb', 'hsl', 'hwb', 'rec601luma', 'rec601ycbcr',
                    'rec709luma', 'rec709ycbcr', 'log', 'cmy', 'luv', 'hcl',
                    'lch', 'lms', 'lchab', 'lchuv', 'scrgb', 'hsi', 'hsv',
                    'hclp', 'ydbdr')

#: (:class:`tuple`) The list of alpha channel types
#:
#: - ``'undefined'``
#: - ``'activate'``
#: - ``'background'``
#: - ``'copy'``
#: - ``'deactivate'``
#: - ``'extract'``
#: - ``'opaque'``
#: - ``'reset'``
#: - ``'set'``
#: - ``'shape'``
#: - ``'transparent'``
#: - ``'flatten'``
#: - ``'remove'``
#:
#: .. seealso::
#:    `ImageMagick Image Channel`__
#:       Describes the SetImageAlphaChannel method which can be used
#:       to modify alpha channel. Also describes AlphaChannelType
#:
#:    __ http://www.imagemagick.org/api/channel.php#SetImageAlphaChannel
ALPHA_CHANNEL_TYPES = ('undefined', 'activate', 'background', 'copy',
                       'deactivate', 'extract', 'opaque', 'reset', 'set',
                       'shape', 'transparent', 'flatten', 'remove')

#: (:class:`tuple`) The list of image types
#:
#: - ``'undefined'``
#: - ``'bilevel'``
#: - ``'grayscale'``
#: - ``'grayscalematte'``
#: - ``'palette'``
#: - ``'palettematte'``
#: - ``'truecolor'``
#: - ``'truecolormatte'``
#: - ``'colorseparation'``
#: - ``'colorseparationmatte'``
#: - ``'optimize'``
#: - ``'palettebilevelmatte'``
#:
#: .. seealso::
#:
#:    `ImageMagick Image Types`__
#:       Describes the MagickSetImageType method which can be used
#:       to set the type of an image
#:
#:    __ http://www.imagemagick.org/api/magick-image.php#MagickSetImageType
IMAGE_TYPES = ('undefined', 'bilevel', 'grayscale', 'grayscalematte',
               'palette', 'palettematte', 'truecolor', 'truecolormatte',
               'colorseparation', 'colorseparationmatte', 'optimize',
               'palettebilevelmatte')

#: (:class:`tuple`) The list of resolution unit types.
#:
#: - ``'undefined'``
#: - ``'pixelsperinch'``
#: - ``'pixelspercentimeter'``
#:
#: .. seealso::
#:
#:    `ImageMagick Image Units`__
#:       Describes the MagickSetImageUnits method which can be used
#:       to set image units of resolution
#:
#:    __ http://www.imagemagick.org/api/magick-image.php#MagickSetImageUnits
UNIT_TYPES = 'undefined', 'pixelsperinch', 'pixelspercentimeter'

#: (:class:`tuple`) The list of :attr:`~BaseImage.gravity` types.
#:
#: .. versionadded:: 0.3.0
GRAVITY_TYPES = ('forget', 'north_west', 'north', 'north_east', 'west',
                 'center', 'east', 'south_west', 'south', 'south_east',
                 'static')

#: (:class:`tuple`) The list of :attr:`~BaseImage.orientation` types.
#:
#: .. versionadded:: 0.3.0
ORIENTATION_TYPES = ('undefined', 'top_left', 'top_right', 'bottom_right',
                     'bottom_left', 'left_top', 'right_top', 'right_bottom',
                     'left_bottom')

#: (:class:`collections.Set`) The set of available :attr:`~BaseImage.options`.
#:
#: .. versionadded:: 0.3.0
#:
#: .. versionchanged:: 0.3.4
#:    Added ``'jpeg:sampling-factor'`` option.
OPTIONS = frozenset(['fill', 'jpeg:sampling-factor'])

#: (:class:`tuple`) The list of :attr:`Image.compression` types.
#:
#: .. versionadded:: 0.3.6
COMPRESSION_TYPES = (
    'undefined', 'b44a', 'b44', 'bzip', 'dxt1', 'dxt3', 'dxt5', 'fax',
    'group4',
    'jbig1',        # ISO/IEC std 11544 / ITU-T rec T.82
    'jbig2',        # ISO/IEC std 14492 / ITU-T rec T.88
    'jpeg2000',     # ISO/IEC std 15444-1
    'jpeg', 'losslessjpeg',
    'lzma',         # Lempel-Ziv-Markov chain algorithm
    'lzw', 'no', 'piz', 'pxr24', 'rle', 'zip', 'zips'
)


def manipulative(function):
    """Mark the operation manipulating itself instead of returning new one."""
    @functools.wraps(function)
    def wrapped(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        self.dirty = True
        return result
    return wrapped


class BaseImage(Resource):
    """The abstract base of :class:`Image` (container) and
    :class:`~wand.sequence.SingleImage`.  That means the most of
    operations, defined in this abstract classs, are possible for
    both :class:`Image` and :class:`~wand.sequence.SingleImage`.

    .. versionadded:: 0.3.0

    """

    #: (:class:`OptionDict`) The mapping of internal option settings.
    #:
    #: .. versionadded:: 0.3.0
    #:
    #: .. versionchanged:: 0.3.4
    #:    Added ``'jpeg:sampling-factor'`` option.
    options = None

    #: (:class:`collections.Sequence`) The list of
    #: :class:`~wand.sequence.SingleImage`\ s that the image contains.
    #:
    #: .. versionadded:: 0.3.0
    sequence = None

    #: (:class:`bool`) Whether the image is changed or not.
    dirty = None

    c_is_resource = library.IsMagickWand
    c_destroy_resource = library.DestroyMagickWand
    c_get_exception = library.MagickGetException
    c_clear_exception = library.MagickClearException

    __slots__ = '_wand',

    def __init__(self, wand):
        self.wand = wand
        self.channel_images = ChannelImageDict(self)
        self.channel_depths = ChannelDepthDict(self)
        self.options = OptionDict(self)
        self.dirty = False

    @property
    def wand(self):
        """Internal pointer to the MagickWand instance. It may raise
        :exc:`ClosedImageError` when the instance has destroyed already.

        """
        try:
            return self.resource
        except DestroyedResourceError:
            raise ClosedImageError(repr(self) + ' is closed already')

    @wand.setter
    def wand(self, wand):
        try:
            self.resource = wand
        except TypeError:
            raise TypeError(repr(wand) + ' is not a MagickWand instance')

    @wand.deleter
    def wand(self):
        del self.resource

    def clone(self):
        """Clones the image. It is equivalent to call :class:`Image` with
        ``image`` parameter. ::

            with img.clone() as cloned:
                # manipulate the cloned image
                pass

        :returns: the cloned new image
        :rtype: :class:`Image`

        .. versionadded:: 0.1.1

        """
        return Image(image=self)

    def __len__(self):
        return self.height

    def __iter__(self):
        return Iterator(image=self)

    def __getitem__(self, idx):
        if (not isinstance(idx, string_type) and
            isinstance(idx, collections.Iterable)):
            idx = tuple(idx)
            d = len(idx)
            if not (1 <= d <= 2):
                raise ValueError('index cannot be {0}-dimensional'.format(d))
            elif d == 2:
                x, y = idx
                x_slice = isinstance(x, slice)
                y_slice = isinstance(y, slice)
                if x_slice and not y_slice:
                    y = slice(y, y + 1)
                elif not x_slice and y_slice:
                    x = slice(x, x + 1)
                elif not (x_slice or y_slice):
                    if not (isinstance(x, numbers.Integral) and
                            isinstance(y, numbers.Integral)):
                        raise TypeError('x and y must be integral, not ' +
                                        repr((x, y)))
                    if x < 0:
                        x += self.width
                    if y < 0:
                        y += self.height
                    if x >= self.width:
                        raise IndexError('x must be less than width')
                    elif y >= self.height:
                        raise IndexError('y must be less than height')
                    elif x < 0:
                        raise IndexError('x cannot be less than 0')
                    elif y < 0:
                        raise IndexError('y cannot be less than 0')
                    with iter(self) as iterator:
                        iterator.seek(y)
                        return iterator.next(x)
                if not (x.step is None and y.step is None):
                    raise ValueError('slicing with step is unsupported')
                elif (x.start is None and x.stop is None and
                      y.start is None and y.stop is None):
                    return self.clone()
                cloned = self.clone()
                try:
                    cloned.crop(x.start, y.start, x.stop, y.stop)
                except ValueError as e:
                    raise IndexError(str(e))
                return cloned
            else:
                return self[idx[0]]
        elif isinstance(idx, numbers.Integral):
            if idx < 0:
                idx += self.height
            elif idx >= self.height:
                raise IndexError('index must be less than height, but got ' +
                                 repr(idx))
            elif idx < 0:
                raise IndexError('index cannot be less than zero, but got ' +
                                 repr(idx))
            with iter(self) as iterator:
                iterator.seek(idx)
                return iterator.next()
        elif isinstance(idx, slice):
            return self[:, idx]
        raise TypeError('unsupported index type: ' + repr(idx))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.signature == other.signature
        return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.signature)

    @property
    def animation(self):
        """(:class:`bool`) Whether the image is animation or not.
        It doesn't only mean that the image has two or more images (frames),
        but all frames are even the same size.  It's about image format,
        not content.  It's :const:`False` even if :mimetype:`image/ico`
        consits of two or more images of the same size.

        For example, it's :const:`False` for :mimetype:`image/jpeg`,
        :mimetype:`image/gif`, :mimetype:`image/ico`.

        If :mimetype:`image/gif` has two or more frames, it's :const:`True`.
        If :mimetype:`image/gif` has only one frame, it's :const:`False`.

        .. versionadded:: 0.3.0

        """
        return False

    @property
    def gravity(self):
        """(:class:`basestring`) The text placement gravity used when
        annotating with text.  It's a string from :const:`GRAVITY_TYPES`
        list.  It also can be set.

        """
        gravity_index = library.MagickGetGravity(self.wand)
        if not gravity_index:
            self.raise_exception()
        return GRAVITY_TYPES[gravity_index]

    @gravity.setter
    @manipulative
    def gravity(self, value):
        if not isinstance(value, string_type):
            raise TypeError('expected a string, not ' + repr(value))
        if value not in GRAVITY_TYPES:
            raise ValueError('expected a string from GRAVITY_TYPES, not '
                             + repr(value))
        library.MagickSetGravity(self.wand, GRAVITY_TYPES.index(value))

    @property
    def font_path(self):
        """(:class:`basestring`) The path of the current font.
        It also can be set.

        """
        return text(library.MagickGetFont(self.wand))

    @font_path.setter
    @manipulative
    def font_path(self, font):
        font = binary(font)
        if library.MagickSetFont(self.wand, font) == False:
            raise ValueError('font is invalid')

    @property
    def font_size(self):
        """(:class:`numbers.Real`) The font size.  It also can be set."""
        return library.MagickGetPointsize(self.wand)

    @font_size.setter
    @manipulative
    def font_size(self, size):
        if not isinstance(size, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(size))
        elif size < 0.0:
            raise ValueError('cannot be less then 0.0, but got ' + repr(size))
        elif library.MagickSetPointsize(self.wand, size) == False:
            raise ValueError('unexpected error is occur')

    @property
    def font_antialias(self):
        return bool(library.MagickGetAntialias(self.wand))

    @font_antialias.setter
    @manipulative
    def font_antialias(self, antialias):
        if not isinstance(antialias, bool):
            raise TypeError('font_antialias must be a bool, not ' +
                            repr(antialias))
        library.MagickSetAntialias(self.wand, antialias)

    @property
    def font(self):
        """(:class:`wand.font.Font`) The current font options."""
        return Font(
            path=text(self.font_path),
            size=self.font_size,
            color=self.font_color,
            antialias=self.font_antialias
        )

    @font.setter
    @manipulative
    def font(self, font):
        if not isinstance(font, Font):
            raise TypeError('font must be a wand.font.Font, not ' + repr(font))
        self.font_path = font.path
        self.font_size = font.size
        self.font_color = font.color
        self.font_antialias = font.antialias

    @property
    def width(self):
        """(:class:`numbers.Integral`) The width of this image."""
        return library.MagickGetImageWidth(self.wand)

    @width.setter
    @manipulative
    def width(self, width):
        if width is not None and not isinstance(width, numbers.Integral):
            raise TypeError('width must be a integral, not ' + repr(width))
        library.MagickSetSize(self.wand, width, self.height)

    @property
    def height(self):
        """(:class:`numbers.Integral`) The height of this image."""
        return library.MagickGetImageHeight(self.wand)

    @height.setter
    @manipulative
    def height(self, height):
        if height is not None and not isinstance(height, numbers.Integral):
            raise TypeError('height must be a integral, not ' + repr(height))
        library.MagickSetSize(self.wand, self.width, height)

    @property
    def orientation(self):
        """(:class:`basestring`) The image orientation.  It's a string from
        :const:`ORIENTATION_TYPES` list.  It also can be set.

        .. versionadded:: 0.3.0

        """
        orientation_index = library.MagickGetImageOrientation(self.wand)
        return ORIENTATION_TYPES[orientation_index]

    @orientation.setter
    @manipulative
    def orientation(self, value):
        if not isinstance(value, string_type):
            raise TypeError('expected a string, not ' + repr(value))
        if value not in ORIENTATION_TYPES:
            raise ValueError('expected a string from ORIENTATION_TYPES, not '
                             + repr(value))
        index = ORIENTATION_TYPES.index(value)
        library.MagickSetImageOrientation(self.wand, index)

    @property
    def font_color(self):
        return Color(self.options['fill'])

    @font_color.setter
    @manipulative
    def font_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('font_color must be a wand.color.Color, not ' +
                            repr(color))
        self.options['fill'] = color.string

    @manipulative
    def caption(self, text, left=0, top=0, width=None, height=None, font=None,
                gravity=None):
        """Writes a caption ``text`` into the position.

        :param text: text to write
        :type text: :class:`basestring`
        :param left: x offset in pixels
        :type left: :class:`numbers.Integral`
        :param right: y offset in pixels
        :type right: :class:`numbers.Integral`
        :param width: width of caption in pixels.
                      default is :attr:`width` of the image
        :type width: :class:`numbers.Integral`
        :param height: height of caption in pixels.
                       default is :attr:`height` of the image
        :type height: :class:`numbers.Integral`
        :param font: font to use.  default is :attr:`font` of the image
        :type font: :class:`wand.font.Font`
        :param gravity: text placement gravity.
                        uses the current :attr:`gravity` setting of the image
                        by default
        :type gravity: :class:`basestring`

        .. versionadded:: 0.3.0

        """
        if not isinstance(left, numbers.Integral):
            raise TypeError('left must be an integer, not ' + repr(left))
        elif not isinstance(top, numbers.Integral):
            raise TypeError('top must be an integer, not ' + repr(top))
        elif width is not None and not isinstance(width, numbers.Integral):
            raise TypeError('width must be an integer, not ' + repr(width))
        elif height is not None and not isinstance(height, numbers.Integral):
            raise TypeError('height must be an integer, not ' + repr(height))
        elif font is not None and not isinstance(font, Font):
            raise TypeError('font must be a wand.font.Font, not ' + repr(font))
        elif gravity is not None and compat.text(gravity) not in GRAVITY_TYPES:
            raise ValueError('invalid gravity value')
        if width is None:
            width = self.width - left
        if height is None:
            height = self.height - top
        with Image() as textboard:
            library.MagickSetSize(textboard.wand, width, height)
            textboard.font = font or self.font
            textboard.gravity = gravity or self.gravity
            with Color('transparent') as background_color:
                library.MagickSetBackgroundColor(textboard.wand,
                                                 background_color.resource)
            textboard.read(filename=b'caption:' + text.encode('utf-8'))
            self.composite(textboard, left, top)


    @property
    def resolution(self):
        """(:class:`tuple`) Resolution of this image.

        .. versionadded:: 0.3.0

        """
        x = ctypes.c_double()
        y = ctypes.c_double()
        r = library.MagickGetImageResolution(self.wand, x, y)
        if not r:
            self.raise_exception()
        return int(x.value), int(y.value)

    @resolution.setter
    @manipulative
    def resolution(self, geometry):
        if isinstance(geometry, collections.Sequence):
            x, y = geometry
        elif isinstance(geometry, numbers.Integral):
            x, y = geometry, geometry
        else:
            raise TypeError('resolution must be a (x, y) pair or an integer '
                            'of the same x/y')
        if self.size == (0, 0):
            r = library.MagickSetResolution(self.wand, x, y)
        else:
            r = library.MagickSetImageResolution(self.wand, x, y)
        if not r:
            self.raise_exception()

    @property
    def size(self):
        """(:class:`tuple`) The pair of (:attr:`width`, :attr:`height`)."""
        return self.width, self.height

    @property
    def units(self):
        """(:class:`basestring`) The resolution units of this image."""
        r = library.MagickGetImageUnits(self.wand)
        return UNIT_TYPES[text(r)]

    @units.setter
    @manipulative
    def units(self, units):
        if not isinstance(units, string_type) or units not in UNIT_TYPES:
            raise TypeError('Unit value must be a string from wand.images.'
                            'UNIT_TYPES, not ' + repr(units))
        r = library.MagickSetImageUnits(self.wand, UNIT_TYPES.index(units))
        if not r:
            self.raise_exception()

    @property
    def colorspace(self):
        """(:class:`basestring`) The image colorspace.

        Defines image colorspace as in :const:`COLORSPACE_TYPES` enumeration.

        It may raise :exc:`ValueError` when the colorspace is unknown.

        .. versionadded:: 0.3.4

        """
        colorspace_type_index = library.MagickGetImageColorspace(self.wand)
        if not colorspace_type_index:
            self.raise_exception()
        return COLORSPACE_TYPES[text(colorspace_type_index)]

    @colorspace.setter
    @manipulative
    def colorspace(self, colorspace_type):
        if not isinstance(colorspace_type, string_type) \
            or colorspace_type not in COLORSPACE_TYPES:
            raise TypeError('Colorspace value must be a string from '
                            'COLORSPACE_TYPES, not ' + repr(colorspace_type))
        r = library.MagickSetImageColorspace(self.wand,
                                    COLORSPACE_TYPES.index(colorspace_type))
        if not r:
            self.raise_exception()

    @property
    def depth(self):
        """(:class:`numbers.Integral`) The depth of this image.

        .. versionadded:: 0.2.1

        """
        return library.MagickGetImageDepth(self.wand)

    @depth.setter
    @manipulative
    def depth(self, depth):
        r = library.MagickSetImageDepth(self.wand, depth)
        if not r:
            raise self.raise_exception()

    @property
    def type(self):
        """(:class:`basestring`) The image type.

        Defines image type as in :const:`IMAGE_TYPES` enumeration.

        It may raise :exc:`ValueError` when the type is unknown.

        .. versionadded:: 0.2.2

        """
        image_type_index = library.MagickGetImageType(self.wand)
        if not image_type_index:
            self.raise_exception()
        return IMAGE_TYPES[text(image_type_index)]

    @type.setter
    @manipulative
    def type(self, image_type):
        if not isinstance(image_type, string_type) \
            or image_type not in IMAGE_TYPES:
            raise TypeError('Type value must be a string from IMAGE_TYPES'
                            ', not ' + repr(image_type))
        r = library.MagickSetImageType(self.wand,
                                       IMAGE_TYPES.index(image_type))
        if not r:
            self.raise_exception()

    @property
    def compression_quality(self):
        """(:class:`numbers.Integral`) Compression quality of this image.

        .. versionadded:: 0.2.0

        """
        return library.MagickGetImageCompressionQuality(self.wand)

    @compression_quality.setter
    @manipulative
    def compression_quality(self, quality):
        """Set compression quality for the image.

        :param quality: new compression quality setting
        :type quality: :class:`numbers.Integral`

        """
        if not isinstance(quality, numbers.Integral):
            raise TypeError('compression quality must be a natural '
                            'number, not ' + repr(quality))
        r = library.MagickSetImageCompressionQuality(self.wand, quality)
        if not r:
            raise ValueError('Unable to set compression quality to ' +
                             repr(quality))

    @property
    def signature(self):
        """(:class:`str`) The SHA-256 message digest for the image pixel
        stream.

        .. versionadded:: 0.1.9

        """
        signature = library.MagickGetImageSignature(self.wand)
        return text(signature.value)

    @property
    def alpha_channel(self):
        """(:class:`bool`) Get state of image alpha channel.
        It can also be used to enable/disable alpha channel.

        .. versionadded:: 0.2.1

        .. todo::

           Support other states than ``''activatealphachannel'``
           or ``'deactivatealphachannel'``.

        """
        return bool(library.MagickGetImageAlphaChannel(self.wand))

    @alpha_channel.setter
    @manipulative
    def alpha_channel(self, alpha):
        if alpha == True:
            act = ALPHA_CHANNEL_TYPES.index('activate')
        elif alpha == False:
            act = ALPHA_CHANNEL_TYPES.index('deactivate')
        else:
            raise TypeError('alpha_channel must be bool, not ' +
                            repr(alpha))
        r = library.MagickSetImageAlphaChannel(self.wand, act)
        if r:
            return r
        self.raise_exception()

    @property
    def background_color(self):
        """(:class:`wand.color.Color`) The image background color.
        It can also be set to change the background color.

        .. versionadded:: 0.1.9

        """
        pixel = library.NewPixelWand()
        result = library.MagickGetImageBackgroundColor(self.wand, pixel)
        if result:
            size = ctypes.sizeof(MagickPixelPacket)
            buffer = ctypes.create_string_buffer(size)
            library.PixelGetMagickColor(pixel, buffer)
            return Color(raw=buffer)
        self.raise_exception()

    @background_color.setter
    @manipulative
    def background_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            result = library.MagickSetImageBackgroundColor(self.wand,
                                                           color.resource)
            if not result:
                self.raise_exception()

    @property
    def quantum_range(self):
        """(:class:`int`) The maxumim value of a color channel that is
        supported by the imagemgick library.

        .. versionadded:: 0.2.0

        """
        result = ctypes.c_size_t()
        library.MagickGetQuantumRange(ctypes.byref(result))
        return result.value

    @property
    def histogram(self):
        """(:class:`HistogramDict`) The mapping that represents the histogram.
        Keys are :class:`~wand.color.Color` objects, and values are
        the number of pixels.

        .. versionadded:: 0.3.0

        """
        return HistogramDict(self)

    @manipulative
    def crop(self, left=0, top=0, right=None, bottom=None,
             width=None, height=None, reset_coords=True):
        """Crops the image in-place.

        .. sourcecode:: text

           +--------------------------------------------------+
           |              ^                         ^         |
           |              |                         |         |
           |             top                        |         |
           |              |                         |         |
           |              v                         |         |
           | <-- left --> +-------------------+  bottom       |
           |              |             ^     |     |         |
           |              | <-- width --|---> |     |         |
           |              |           height  |     |         |
           |              |             |     |     |         |
           |              |             v     |     |         |
           |              +-------------------+     v         |
           | <--------------- right ---------->               |
           +--------------------------------------------------+

        :param left: x-offset of the cropped image. default is 0
        :type left: :class:`numbers.Integral`
        :param top: y-offset of the cropped image. default is 0
        :type top: :class:`numbers.Integral`
        :param right: second x-offset of the cropped image.
                      default is the :attr:`width` of the image.
                      this parameter and ``width`` parameter are exclusive
                      each other
        :type right: :class:`numbers.Integral`
        :param bottom: second y-offset of the cropped image.
                       default is the :attr:`height` of the image.
                       this parameter and ``height`` parameter are exclusive
                       each other
        :type bottom: :class:`numbers.Integral`
        :param width: the :attr:`width` of the cropped image.
                      default is the :attr:`width` of the image.
                      this parameter and ``right`` parameter are exclusive
                      each other
        :type width: :class:`numbers.Integral`
        :param height: the :attr:`height` of the cropped image.
                       default is the :attr:`height` of the image.
                       this parameter and ``bottom`` parameter are exclusive
                       each other
        :type height: :class:`numbers.Integral`
        :param reset_coords:
           optional flag. If set, after the rotation, the coordinate frame
           will be relocated to the upper-left corner of the new image.
           By default is `True`.
        :type reset_coords: :class:`bool`
        :raises exceptions.ValueError:
           when one or more arguments are invalid

        .. note::

           If you want to crop the image but not in-place, use slicing
           operator.

        .. versionchanged:: 0.1.8
           Made to raise :exc:`~exceptions.ValueError` instead of
           :exc:`~exceptions.IndexError` for invalid ``width``/``height``
           arguments.

        .. versionadded:: 0.1.7

        """
        if not (right is None or width is None):
            raise TypeError('parameters right and width are exclusive each '
                            'other; use one at a time')
        elif not (bottom is None or height is None):
            raise TypeError('parameters bottom and height are exclusive each '
                            'other; use one at a time')
        def abs_(n, m, null=None):
            if n is None:
                return m if null is None else null
            elif not isinstance(n, numbers.Integral):
                raise TypeError('expected integer, not ' + repr(n))
            elif n > m:
                raise ValueError(repr(n) + ' > ' + repr(m))
            return m + n if n < 0 else n
        left = abs_(left, self.width, 0)
        top = abs_(top, self.height, 0)
        if width is None:
            right = abs_(right, self.width)
            width = right - left
        if height is None:
            bottom = abs_(bottom, self.height)
            height = bottom - top
        if width < 1:
            raise ValueError('image width cannot be zero')
        elif height < 1:
            raise ValueError('image width cannot be zero')
        elif left == top == 0 and width == self.width and height == self.height:
            return
        if self.animation:
            self.wand = library.MagickCoalesceImages(self.wand)
            library.MagickSetLastIterator(self.wand)
            n = library.MagickGetIteratorIndex(self.wand)
            library.MagickResetIterator(self.wand)
            for i in xrange(0, n + 1):
                library.MagickSetIteratorIndex(self.wand, i)
                library.MagickCropImage(self.wand, width, height, left, top)
                if reset_coords:
                    library.MagickResetImagePage(self.wand, None)
        else:
            library.MagickCropImage(self.wand, width, height, left, top)
            self.raise_exception()
            if reset_coords:
                self.reset_coords()

    def reset_coords(self):
        """Reset the coordinate frame of the image so to the upper-left corner
        is (0, 0) again (crop and rotate operations change it).

        .. versionadded:: 0.2.0

        """
        library.MagickResetImagePage(self.wand, None)

    @manipulative
    def resize(self, width=None, height=None, filter='undefined', blur=1):
        """Resizes the image.

        :param width: the width in the scaled image. default is the original
                      width
        :type width: :class:`numbers.Integral`
        :param height: the height in the scaled image. default is the original
                       height
        :type height: :class:`numbers.Integral`
        :param filter: a filter type to use for resizing. choose one in
                       :const:`FILTER_TYPES`. default is ``'undefined'``
                       which means IM will try to guess best one to use
        :type filter: :class:`basestring`, :class:`numbers.Integral`
        :param blur: the blur factor where > 1 is blurry, < 1 is sharp.
                     default is 1
        :type blur: :class:`numbers.Real`

        .. versionchanged:: 0.2.1
           The default value of ``filter`` has changed from ``'triangle'``
           to ``'undefined'`` instead.

        .. versionchanged:: 0.1.8
           The ``blur`` parameter changed to take :class:`numbers.Real`
           instead of :class:`numbers.Rational`.

        .. versionadded:: 0.1.1

        """
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if not isinstance(width, numbers.Integral):
            raise TypeError('width must be a natural number, not ' +
                            repr(width))
        elif not isinstance(height, numbers.Integral):
            raise TypeError('height must be a natural number, not ' +
                            repr(height))
        elif width < 1:
            raise ValueError('width must be a natural number, not ' +
                             repr(width))
        elif height < 1:
            raise ValueError('height must be a natural number, not ' +
                             repr(height))
        elif not isinstance(blur, numbers.Real):
            raise TypeError('blur must be numbers.Real , not ' + repr(blur))
        elif not isinstance(filter, (string_type, numbers.Integral)):
            raise TypeError('filter must be one string defined in wand.image.'
                            'FILTER_TYPES or an integer, not ' + repr(filter))
        if isinstance(filter, string_type):
            try:
                filter = FILTER_TYPES.index(filter)
            except IndexError:
                raise ValueError(repr(filter) + ' is an invalid filter type; '
                                 'choose on in ' + repr(FILTER_TYPES))
        elif (isinstance(filter, numbers.Integral) and
              not (0 <= filter < len(FILTER_TYPES))):
            raise ValueError(repr(filter) + ' is an invalid filter type')
        blur = ctypes.c_double(float(blur))
        if self.animation:
            self.wand = library.MagickCoalesceImages(self.wand)
            library.MagickSetLastIterator(self.wand)
            n = library.MagickGetIteratorIndex(self.wand)
            library.MagickResetIterator(self.wand)
            for i in xrange(n + 1):
                library.MagickSetIteratorIndex(self.wand, i)
                library.MagickResizeImage(self.wand, width, height,
                                          filter, blur)
            library.MagickSetSize(self.wand, width, height)
        else:
            r = library.MagickResizeImage(self.wand, width, height,
                                          filter, blur)
            library.MagickSetSize(self.wand, width, height)
            if not r:
                self.raise_exception()

    @manipulative
    def sample(self, width=None, height=None):
        """Resizes the image by sampling the pixels.  It's basically quicker
        than :meth:`resize()` except less quality as a tradeoff.

        :param width: the width in the scaled image. default is the original
                      width
        :type width: :class:`numbers.Integral`
        :param height: the height in the scaled image. default is the original
                       height
        :type height: :class:`numbers.Integral`

        .. versionadded:: 0.3.4

        """
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if not isinstance(width, numbers.Integral):
            raise TypeError('width must be a natural number, not ' +
                            repr(width))
        elif not isinstance(height, numbers.Integral):
            raise TypeError('height must be a natural number, not ' +
                            repr(height))
        elif width < 1:
            raise ValueError('width must be a natural number, not ' +
                             repr(width))
        elif height < 1:
            raise ValueError('height must be a natural number, not ' +
                             repr(height))
        if self.animation:
            self.wand = library.MagickCoalesceImages(self.wand)
            library.MagickSetLastIterator(self.wand)
            n = library.MagickGetIteratorIndex(self.wand)
            library.MagickResetIterator(self.wand)
            for i in xrange(n + 1):
                library.MagickSetIteratorIndex(self.wand, i)
                library.MagickSampleImage(self.wand, width, height)
            library.MagickSetSize(self.wand, width, height)
        else:
            r = library.MagickSampleImage(self.wand, width, height)
            library.MagickSetSize(self.wand, width, height)
            if not r:
                self.raise_exception()

    @manipulative
    def transform(self, crop='', resize=''):
        """Transforms the image using :c:func:`MagickTransformImage`,
        which is a convenience function accepting geometry strings to
        perform cropping and resizing.  Cropping is performed first,
        followed by resizing.  Either or both arguments may be omitted
        or given an empty string, in which case the corresponding action
        will not be performed. Geometry specification strings are
        defined as follows:

        A geometry string consists of a size followed by an optional offset.
        The size is specified by one of the options below,
        where **bold** terms are replaced with appropriate integer values:

        **scale**\ ``%``
          Height and width both scaled by specified percentage

        **scale-x**\ ``%x``\ \ **scale-y**\ ``%``
          Height and width individually scaled by specified percentages.
          Only one % symbol is needed.

        **width**
          Width given, height automagically selected to preserve aspect ratio.

        ``x``\ \ **height**
          Height given, width automagically selected to preserve aspect ratio.

        **width**\ ``x``\ **height**
          Maximum values of width and height given; aspect ratio preserved.

        **width**\ ``x``\ **height**\ ``!``
          Width and height emphatically given; original aspect ratio ignored.

        **width**\ ``x``\ **height**\ ``>``
          Shrinks images with dimension(s) larger than the corresponding
          width and/or height dimension(s).

        **width**\ ``x``\ **height**\ ``<``
          Enlarges images with dimensions smaller than the corresponding
          width and/or height dimension(s).

        **area**\ ``@``
          Resize image to have the specified area in pixels.
          Aspect ratio is preserved.

        The offset, which only applies to the cropping geometry string,
        is given by ``{+-}``\ **x**\ ``{+-}``\ **y**\ , that is,
        one plus or minus sign followed by an **x** offset,
        followed by another plus or minus sign, followed by a **y** offset.
        Offsets are in pixels from the upper left corner of the image.
        Negative offsets will cause the corresponding number of pixels to
        be removed from the right or bottom edge of the image, meaning the
        cropped size will be the computed size minus the absolute value
        of the offset.

        For example, if you want to crop your image to 300x300 pixels
        and then scale it by 2x for a final size of 600x600 pixels,
        you can call::

            image.transform('300x300', '200%')

        This method is a fairly thing wrapper for the C API, and does not
        perform any additional checking of the parameters except insofar as
        verifying that they are of the correct type.  Thus, like the C
        API function, the method is very permissive in terms of what
        it accepts for geometry strings; unrecognized strings and
        trailing characters will be ignored rather than raising an error.

        :param crop: A geometry string defining a subregion of the image
                     to crop to
        :type crop: :class:`basestring`
        :param resize: A geometry string defining the final size of the image
        :type resize: :class:`basestring`

        .. seealso::

           `ImageMagick Geometry Specifications`__
              Cropping and resizing geometry for the ``transform`` method are
              specified according to ImageMagick's geometry string format.
              The ImageMagick documentation provides more information about
              geometry strings.

           __ http://www.imagemagick.org/script/command-line-processing.php#geometry

        .. versionadded:: 0.2.2

        """
        # Check that the values given are the correct types.  ctypes will do
        # this automatically, but we can make the error message more friendly
        # here.
        if not isinstance(crop, string_type):
            raise TypeError("crop must be a string, not " + repr(crop))
        if not isinstance(resize, string_type):
            raise TypeError("resize must be a string, not " + repr(resize))
        # Also verify that only ASCII characters are included
        try:
            crop = crop.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('crop must only contain ascii-encodable ' +
                             'characters.')
        try:
            resize = resize.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('resize must only contain ascii-encodable ' +
                             'characters.')
        if self.animation:
            new_wand = library.MagickCoalesceImages(self.wand)
            length = len(self.sequence)
            for i in xrange(length):
                library.MagickSetIteratorIndex(new_wand, i)
                if i:
                    library.MagickAddImage(
                        new_wand,
                        library.MagickTransformImage(new_wand, crop, resize)
                    )
                else:
                    new_wand = library.MagickTransformImage(new_wand,
                                                            crop,
                                                            resize)
            self.sequence.instances = []
        else:
            new_wand = library.MagickTransformImage(self.wand, crop, resize)
        if not new_wand:
            self.raise_exception()
        self.wand = new_wand

    @manipulative
    def liquid_rescale(self, width, height, delta_x=0, rigidity=0):
        """Rescales the image with `seam carving`_, also known as
        image retargeting, content-aware resizing, or liquid rescaling.

        :param width: the width in the scaled image
        :type width: :class:`numbers.Integral`
        :param height: the height in the scaled image
        :type height: :class:`numbers.Integral`
        :param delta_x: maximum seam transversal step.
                        0 means straight seams.  default is 0
        :type delta_x: :class:`numbers.Real`
        :param rigidity: introduce a bias for non-straight seams.
                         default is 0
        :type rigidity: :class:`numbers.Real`
        :raises wand.exceptions.MissingDelegateError:
           when ImageMagick isn't configured ``--with-lqr`` option.

        .. note::

           This feature requires ImageMagick to be configured
           ``--with-lqr`` option.  Or it will raise
           :exc:`~wand.exceptions.MissingDelegateError`:

        .. seealso::

           `Seam carving`_ --- Wikipedia
              The article which explains what seam carving is
              on Wikipedia.

        .. _Seam carving: http://en.wikipedia.org/wiki/Seam_carving

        """
        if not isinstance(width, numbers.Integral):
            raise TypeError('width must be an integer, not ' + repr(width))
        elif not isinstance(height, numbers.Integral):
            raise TypeError('height must be an integer, not ' + repr(height))
        elif not isinstance(delta_x, numbers.Real):
            raise TypeError('delta_x must be a float, not ' + repr(delta_x))
        elif not isinstance(rigidity, numbers.Real):
            raise TypeError('rigidity must be a float, not ' + repr(rigidity))
        library.MagickLiquidRescaleImage(self.wand, int(width), int(height),
                                         float(delta_x), float(rigidity))
        self.raise_exception()

    @manipulative
    def rotate(self, degree, background=None, reset_coords=True):
        """Rotates the image right.  It takes a ``background`` color
        for ``degree`` that isn't a multiple of 90.

        :param degree: a degree to rotate. multiples of 360 affect nothing
        :type degree: :class:`numbers.Real`
        :param background: an optional background color.
                           default is transparent
        :type background: :class:`wand.color.Color`
        :param reset_coords: optional flag. If set, after the rotation, the
            coordinate frame will be relocated to the upper-left corner of
            the new image. By default is `True`.
        :type reset_coords: :class:`bool`

        .. versionadded:: 0.2.0
           The ``reset_coords`` parameter.

        .. versionadded:: 0.1.8

        """
        if background is None:
            background = Color('transparent')
        elif not isinstance(background, Color):
            raise TypeError('background must be a wand.color.Color instance, '
                            'not ' + repr(background))
        if not isinstance(degree, numbers.Real):
            raise TypeError('degree must be a numbers.Real value, not ' +
                            repr(degree))
        with background:
            if self.animation:
                self.wand = library.MagickCoalesceImages(self.wand)
                library.MagickSetLastIterator(self.wand)
                n = library.MagickGetIteratorIndex(self.wand)
                library.MagickResetIterator(self.wand)
                for i in range(0, n + 1):
                    library.MagickSetIteratorIndex(self.wand, i)
                    library.MagickRotateImage(self.wand,
                                              background.resource,
                                              degree)
                    if reset_coords:
                        library.MagickResetImagePage(self.wand, None)
            else:
                result = library.MagickRotateImage(self.wand,
                                                   background.resource,
                                                   degree)
                if not result:
                    self.raise_exception()
                if reset_coords:
                    self.reset_coords()

    @manipulative
    def flip(self):
        """Creates a vertical mirror image by reflecting the pixels around
        the central x-axis.  It manipulates the image in place.

        .. versionadded:: 0.3.0

        """
        result = library.MagickFlipImage(self.wand)
        if not result:
            self.raise_exception()

    @manipulative
    def flop(self):
        """Creates a horizontal mirror image by reflecting the pixels around
        the central y-axis.  It manipulates the image in place.

        .. versionadded:: 0.3.0

        """
        result = library.MagickFlopImage(self.wand)
        if not result:
            self.raise_exception()

    @manipulative
    def transparentize(self, transparency):
        """Makes the image transparent by subtracting some percentage of
        the black color channel.  The ``transparency`` parameter specifies the
        percentage.

        :param transparency: the percentage fade that should be performed on the
                             image, from 0.0 to 1.0
        :type transparency: :class:`numbers.Real`

        .. versionadded:: 0.2.0

        """
        if transparency:
            t = ctypes.c_double(float(self.quantum_range * float(transparency)))
            if t.value > self.quantum_range or t.value < 0:
                raise ValueError('transparency must be a numbers.Real value ' +
                                 'between 0.0 and 1.0')
            # Set the wand to image zero, in case there are multiple images
            # in it
            library.MagickSetIteratorIndex(self.wand, 0)
            # Change the pixel representation of the image
            # to RGB with an alpha channel
            library.MagickSetImageType(self.wand,
                                       IMAGE_TYPES.index('truecolormatte'))
            # Perform the black channel subtraction
            library.MagickEvaluateImageChannel(self.wand,
                                               CHANNELS['opacity'],
                                               EVALUATE_OPS.index('subtract'),
                                               t)
            self.raise_exception()

    @manipulative
    def transparent_color(self, color, alpha, fuzz=0, invert=False):
        """Makes the color ``color`` a transparent color with a tolerance of
        fuzz. The ``alpha`` parameter specify the transparency level and the
        parameter ``fuzz`` specify the tolerance.

        :param color: The color that should be made transparent on the image,
                      color object
        :type color: :class:`wand.color.Color`
        :param alpha: the level of transparency: 1.0 is fully opaque
                      and 0.0 is fully transparent.
        :type alpha: :class:`numbers.Real`
        :param fuzz: By default target must match a particular pixel color
                     exactly. However, in many cases two colors may differ
                     by a small amount. The fuzz member of image defines how
                     much tolerance is acceptable to consider two colors as the
                     same. For example, set fuzz to 10 and the color red at
                     intensities of 100 and 102 respectively are now interpreted
                     as the same color for the color.
        :type fuzz: :class:`numbers.Integral`
        :param invert: Boolean to tell to paint the inverse selection.
        :type invert: :class:`bool`

        .. versionadded:: 0.3.0

        """
        if not isinstance(alpha, numbers.Real):
            raise TypeError('alpha must be an float, not ' + repr(alpha))
        elif not isinstance(fuzz, numbers.Integral):
            raise TypeError('fuzz must be an integer, not ' + repr(fuzz))
        elif not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        library.MagickTransparentPaintImage(self.wand, color.resource,
                                            alpha, fuzz, invert)
        self.raise_exception()

    @manipulative
    def composite(self, image, left, top):
        """Places the supplied ``image`` over the current image, with the top
        left corner of ``image`` at coordinates ``left``, ``top`` of the
        current image.  The dimensions of the current image are not changed.

        :param image: the image placed over the current image
        :type image: :class:`wand.image.Image`
        :param left: the x-coordinate where `image` will be placed
        :type left: :class:`numbers.Integral`
        :param top: the y-coordinate where `image` will be placed
        :type top: :class:`numbers.Integral`

        .. versionadded:: 0.2.0

        """
        if not isinstance(left, numbers.Integral):
            raise TypeError('left must be an integer, not ' + repr(left))
        elif not isinstance(top, numbers.Integral):
            raise TypeError('top must be an integer, not ' + repr(left))
        op = COMPOSITE_OPERATORS.index('over')
        library.MagickCompositeImage(self.wand, image.wand, op,
                                     int(left), int(top))
        self.raise_exception()

    @manipulative
    def composite_channel(self, channel, image, operator, left=0, top=0):
        """Composite two images using the particular ``channel``.

        :param channel: the channel type.  available values can be found
                        in the :const:`CHANNELS` mapping
        :param image: the composited source image.
                      (the receiver image becomes the destination)
        :type image: :class:`Image`
        :param operator: the operator that affects how the composite
                         is applied to the image.  available values
                         can be found in the :const:`COMPOSITE_OPERATORS`
                         list
        :param left: the column offset of the composited source image
        :type left: :class:`numbers.Integral`
        :param top: the row offset of the composited source image
        :type top: :class:`numbers.Integral`
        :raises exceptions.ValueError: when the given ``channel`` or
                                       ``operator`` is invalid

        .. versionadded:: 0.3.0

        """
        if not isinstance(channel, string_type):
            raise TypeError('channel must be a string, not ' +
                            repr(channel))
        elif not isinstance(operator, string_type):
            raise TypeError('operator must be a string, not ' +
                            repr(operator))
        elif not isinstance(left, numbers.Integral):
            raise TypeError('left must be an integer, not ' + repr(left))
        elif not isinstance(top, numbers.Integral):
            raise TypeError('top must be an integer, not ' + repr(left))
        try:
            ch_const = CHANNELS[channel]
        except KeyError:
            raise ValueError(repr(channel) + ' is an invalid channel type'
                             '; see wand.image.CHANNELS dictionary')
        try:
            op =  COMPOSITE_OPERATORS.index(operator)
        except IndexError:
            raise IndexError(repr(operator) + ' is an invalid composite '
                             'operator type; see wand.image.COMPOSITE_'
                             'OPERATORS dictionary')
        library.MagickCompositeImageChannel(self.wand, ch_const, image.wand,
                                            op, int(left), int(top))
        self.raise_exception()

    @manipulative
    def modulate(self, brightness=100.0, saturation=100.0, hue=100.0):
        """Changes the brightness, saturation and hue of an image.
        We modulate the image with the given ``brightness``, ``saturation``
        and ``hue``.

        :param brightness: percentage of brightness
        :type brightness: :class:`numbers.Real`
        :param saturation: percentage of saturation
        :type saturation: :class:`numbers.Real`
        :param hue: percentage of hue rotation
        :type hue: :class:`numbers.Real`

        :raises exceptions.ValueError:
           when one or more arguments are invalid

        .. versionadded:: 0.3.4

        """
        if not isinstance(brightness, numbers.Real):
            raise TypeError('brightness has to be a numbers.Real, not ' +
                            repr(brightness))

        elif not isinstance(saturation, numbers.Real):
            raise TypeError('saturation has to be a numbers.Real, not ' +
                            repr(saturation))

        elif not isinstance(hue, numbers.Real):
            raise TypeError('hue has to be a numbers.Real, not '+
                            repr(hue))
        r = library.MagickModulateImage(
            self.wand,
            ctypes.c_double(brightness),
            ctypes.c_double(saturation),
            ctypes.c_double(hue)
        )
        if not r:
            self.raise_exception()

    @manipulative
    def gaussian_blur(self, radius, sigma):
        """Blurs the image.  We convolve the image with a gaussian operator
        of the given ``radius`` and standard deviation (``sigma``).
        For reasonable results, the ``radius`` should be larger
        than ``sigma``.  Use a ``radius`` of 0 and :meth:`blur()` selects
        a suitable ``radius`` for you.

        :param radius: the radius of the, in pixels,
                       not counting the center pixel
        :type radius: :class:`numbers.Real`
        :param sigma: the standard deviation of the, in pixels
        :type sigma: :class:`numbers.Real`

        .. versionadded:: 0.3.3

        """
        if not isinstance(radius, numbers.Real):
            raise TypeError('radius has to be a numbers.Real, not ' +
                            repr(radius))
        elif not isinstance(sigma, numbers.Real):
            raise TypeError('sigma has to be a numbers.Real, not ' +
                            repr(sigma))
        r = library.MagickGaussianBlurImage(self.wand, radius, sigma)
        if not r:
            self.raise_exception()

    @manipulative
    def unsharp_mask(self, radius, sigma, amount, threshold):
        """Sharpens the image using unsharp mask filter. We convolve the image
        with a Gaussian operator of the given ``radius`` and standard deviation
        (``sigma``). For reasonable results, ``radius`` should be larger than
        ``sigma``. Use a radius of 0 and :meth:`unsharp_mask()`` selects
        a suitable radius for you.

        :param radius: the radius of the Gaussian, in pixels,
                       not counting the center pixel
        :type radius: :class:`numbers.Real`
        :param sigma: the standard deviation of the Gaussian, in pixels
        :type sigma: :class:`numbers.Real`
        :param amount: the percentage of the difference between the original
                       and the blur image that is added back into the original
        :type amount: :class:`numbers.Real`
        :param threshold: the threshold in pixels needed to apply
                          the diffence amount
        :type threshold: :class:`numbers.Real`

        .. versionadded:: 0.3.4

        """
        if not isinstance(radius, numbers.Real):
            raise TypeError('radius has to be a numbers.Real, not ' +
                            repr(radius))
        elif not isinstance(sigma, numbers.Real):
            raise TypeError('sigma has to be a numbers.Real, not ' +
                            repr(sigma))
        elif not isinstance(amount, numbers.Real):
            raise TypeError('amount has to be a numbers.Real, not ' +
                            repr(amount))
        elif not isinstance(threshold, numbers.Real):
            raise TypeError('threshold has to be a numbers.Real, not ' +
                            repr(threshold))
        r = library.MagickUnsharpMaskImage(self.wand, radius, sigma,
                                           amount, threshold)
        if not r:
            self.raise_exception()

    @manipulative
    def watermark(self, image, transparency=0.0, left=0, top=0):
        """Transparentized the supplied ``image`` and places it over the
        current image, with the top left corner of ``image`` at coordinates
        ``left``, ``top`` of the current image.  The dimensions of the
        current image are not changed.

        :param image: the image placed over the current image
        :type image: :class:`wand.image.Image`
        :param transparency: the percentage fade that should be performed on
                             the image, from 0.0 to 1.0
        :type transparency: :class:`numbers.Real`
        :param left: the x-coordinate where `image` will be placed
        :type left: :class:`numbers.Integral`
        :param top: the y-coordinate where `image` will be placed
        :type top: :class:`numbers.Integral`

        .. versionadded:: 0.2.0

        """
        with image.clone() as watermark_image:
            watermark_image.transparentize(transparency)
            self.composite(watermark_image, left=left, top=top)
        self.raise_exception()

    def __repr__(self):
        cls = type(self)
        if getattr(self, 'c_resource', None) is None:
            return '<{0}.{1}: (closed)>'.format(cls.__module__, cls.__name__)
        return '<{0}.{1}: {2} ({3}x{4})>'.format(
            cls.__module__, cls.__name__,
            self.signature[:7], self.width, self.height
        )


class Image(BaseImage):
    """An image object.

    :param image: makes an exact copy of the ``image``
    :type image: :class:`Image`
    :param blob: opens an image of the ``blob`` byte array
    :type blob: :class:`str`
    :param file: opens an image of the ``file`` object
    :type file: file object
    :param filename: opens an image of the ``filename`` string
    :type filename: :class:`basestring`
    :param format: forces filename to  buffer.``format`` to help
                   imagemagick detect the file format. Used only in
                   ``blob`` or ``file`` cases
    :type format: :class:`basestring`
    :param width: the width of new blank image.
    :type width: :class:`numbers.Integral`
    :param height: the height of new blank imgage.
    :type height: :class:`numbers.Integral`
    :param background: an optional background color.
                       default is transparent
    :type background: :class:`wand.color.Color`
    :param resolution: set a resolution value (dpi),
        usefull for vectorial formats (like pdf)
    :type resolution: :class:`collections.Sequence`,
                      :Class:`numbers.Integral`

    .. versionadded:: 0.1.5
       The ``file`` parameter.

    .. versionadded:: 0.1.1
       The ``blob`` parameter.

    .. versionadded:: 0.2.1
       The ``format`` parameter.

    .. versionadded:: 0.2.2
       The ``width``, ``height``, ``background`` parameters.

    .. versionadded:: 0.3.0
       The ``resolution`` parameter.

    .. describe:: [left:right, top:bottom]

       Crops the image by its ``left``, ``right``, ``top`` and ``bottom``,
       and then returns the cropped one. ::

           with img[100:200, 150:300] as cropped:
               # manipulated the cropped image
               pass

       Like other subscriptable objects, default is 0 or its width/height::

           img[:, :]        #--> just clone
           img[:100, 200:]  #--> equivalent to img[0:100, 200:img.height]

       Negative integers count from the end (width/height)::

           img[-70:-50, -20:-10]
           #--> equivalent to img[width-70:width-50, height-20:height-10]

       :returns: the cropped image
       :rtype: :class:`Image`

       .. versionadded:: 0.1.2

    """

    #: (:class:`Metadata`) The metadata mapping of the image.  Read only.
    #:
    #: .. versionadded:: 0.3.0
    metadata = None

    #: (:class:`ChannelImageDict`) The mapping of separated channels
    #: from the image. ::
    #:
    #:     with image.channel_images['red'] as red_image:
    #:         display(red_image)
    channel_images = None

    #: (:class:`ChannelDepthDict`) The mapping of channels to their depth.
    #: Read only.
    #:
    #: .. versionadded:: 0.3.0
    channel_depths = None

    def __init__(self, image=None, blob=None, file=None, filename=None,
                 format=None, width=None, height=None, background=None,
                 resolution=None):
        new_args = width, height, background
        open_args = image, blob, file, filename
        if (any(a is not None for a in new_args) and
            any(a is not None for a in open_args)):
            raise TypeError('blank image parameters cant be used with image '
                            'opening parameters')
        elif any(a is not None and b is not None
                 for i, a in enumerate(open_args)
                 for b in open_args[:i] + open_args[i + 1:]):
            raise TypeError('parameters are exclusive each other; use only '
                            'one at once')
        elif not (format is None or isinstance(format, string_type)):
            raise TypeError('format must be a string, not ' + repr(format))
        with self.allocate():
            if image is None:
                wand = library.NewMagickWand()
                super(Image, self).__init__(wand)
            if width is not None and height is not None:
                self.blank(width, height, background)
            elif image is not None:
                if not isinstance(image, BaseImage):
                    raise TypeError('image must be a wand.image.Image '
                                    'instance, not ' + repr(image))
                elif format:
                    raise TypeError('format option cannot be used with image '
                                    'nor filename')
                wand = library.CloneMagickWand(image.wand)
                super(Image, self).__init__(wand)
            else:
                if format:
                    format = binary(format)
                if file is not None:
                    if format:
                        library.MagickSetFilename(self.wand,
                                                  b'buffer.' + format)
                    self.read(file=file, resolution=resolution)
                if blob is not None:
                    if format:
                        library.MagickSetFilename(self.wand,
                                                  b'buffer.' + format)
                    self.read(blob=blob, resolution=resolution)
                elif filename is not None:
                    if format:
                        raise TypeError(
                            'format option cannot be used with image '
                            'nor filename'
                        )
                    self.read(filename=filename, resolution=resolution)
            self.metadata = Metadata(self)
            from .sequence import Sequence
            self.sequence = Sequence(self)
        self.raise_exception()

    def read(self, file=None, filename=None, blob=None, resolution=None):
        """Read new image into Image() object.

        :param blob: reads an image from the ``blob`` byte array
        :type blob: :class:`str`
        :param file: reads an image from the ``file`` object
        :type file: file object
        :param filename: reads an image from the ``filename`` string
        :type filename: :class:`basestring`
        :param resolution: set a resolution value (DPI),
                           usefull for vectorial formats (like PDF)
        :type resolution: :class:`collections.Sequence`,
                          :class:`numbers.Integral`

        .. versionadded:: 0.3.0

        """
        r = None
        # Resolution must be set after image reading.
        if resolution is not None:
            if (isinstance(resolution, collections.Sequence) and
                len(resolution) == 2):
                library.MagickSetResolution(self.wand, *resolution)
            elif isinstance(resolution, numbers.Integral):
                library.MagickSetResolution(self.wand, resolution, resolution)
            else:
                raise TypeError('resolution must be a (x, y) pair or an '
                                'integer of the same x/y')
        if file is not None:
            if (isinstance(file, file_types) and
                hasattr(libc, 'fdopen')):
                fd = libc.fdopen(file.fileno(), file.mode)
                r = library.MagickReadImageFile(self.wand, fd)
            elif not callable(getattr(file, 'read', None)):
                raise TypeError('file must be a readable file object'
                                ', but the given object does not '
                                'have read() method')
            else:
                blob = file.read()
                file = None
        if blob is not None:
            if not isinstance(blob, collections.Iterable):
                raise TypeError('blob must be iterable, not ' +
                                repr(blob))
            if not isinstance(blob, binary_type):
                blob = b''.join(blob)
            r = library.MagickReadImageBlob(self.wand, blob, len(blob))
        elif filename is not None:
            filename = encode_filename(filename)
            r = library.MagickReadImage(self.wand, filename)
        if not r:
            self.raise_exception()

    def close(self):
        """Closes the image explicitly. If you use the image object in
        :keyword:`with` statement, it was called implicitly so don't have to
        call it.

        .. note::

           It has the same functionality of :attr:`destroy()` method.

        """
        self.destroy()

    def clear(self):
        """Clears resources associated with the image, leaving the image blank,
        and ready to be used with new image.

        .. versionadded:: 0.3.0

        """
        library.ClearMagickWand(self.wand)

    @property
    def format(self):
        """(:class:`basestring`) The image format.

        If you want to convert the image format, just reset this property::

            assert isinstance(img, wand.image.Image)
            img.format = 'png'

        It may raise :exc:`ValueError` when the format is unsupported.

        .. seealso::

           `ImageMagick Image Formats`__
              ImageMagick uses an ASCII string known as *magick* (e.g. ``GIF``)
              to identify file formats, algorithms acting as formats,
              built-in patterns, and embedded profile types.

           __ http://www.imagemagick.org/script/formats.php

        .. versionadded:: 0.1.6

        """
        fmt = library.MagickGetImageFormat(self.wand)
        if bool(fmt):
            return text(fmt.value)
        self.raise_exception()

    @format.setter
    def format(self, fmt):
        if not isinstance(fmt, string_type):
            raise TypeError("format must be a string like 'png' or 'jpeg'"
                            ', not ' + repr(fmt))
        fmt = fmt.strip()
        r = library.MagickSetImageFormat(self.wand, binary(fmt.upper()))
        if not r:
            raise ValueError(repr(fmt) + ' is unsupported format')
        r = library.MagickSetFilename(self.wand,
                                      b'buffer.' + binary(fmt.lower()))
        if not r:
            self.raise_exception()

    @property
    def mimetype(self):
        """(:class:`basestring`) The MIME type of the image
        e.g. ``'image/jpeg'``, ``'image/png'``.

        .. versionadded:: 0.1.7

        """
        rp = libmagick.MagickToMime(binary(self.format))
        if not bool(rp):
            self.raise_exception()
        mimetype = rp.value
        return text(mimetype)

    @property
    def animation(self):
        return self.mimetype == 'image/gif' and len(self.sequence) > 1

    @property
    def compression(self):
        """(:class:`basestring`) The type of image compression.
        It's a string from :const:`COMPRESSION_TYPES` list.
        It also can be set.

        .. versionadded:: 0.3.6

        """
        compression_index = libmagick.MagickGetImageCompression(self.wand)
        return COMPRESSION_TYPES[compression_index]

    @compression.setter
    def compression(self, value):
        if not isinstance(value, string_type):
            raise TypeError('expected a string, not ' + repr(value))
        if value not in COMPRESSION_TYPES:
            raise ValueError('expected a string from COMPRESSION_TYPES, not '
                             + repr(value))
        library.MagickSetImageCompression(
            self.wand,
            COMPRESSION_TYPES.index(value)
        )

    def blank(self, width, height, background=None):
        """Creates blank image.

        :param width: the width of new blank image.
        :type width: :class:`numbers.Integral`
        :param height: the height of new blank imgage.
        :type height: :class:`numbers.Integral`
        :param background: an optional background color.
                           default is transparent
        :type background: :class:`wand.color.Color`
        :returns: blank image
        :rtype: :class:`Image`

        .. versionadded:: 0.3.0

        """
        if not isinstance(width, numbers.Integral) or width < 1:
            raise TypeError('width must be a natural number, not ' +
                            repr(width))
        if not isinstance(height, numbers.Integral) or height < 1:
            raise TypeError('height must be a natural number, not ' +
                            repr(height))
        if background is not None and not isinstance(background, Color):
            raise TypeError('background must be a wand.color.Color '
                            'instance, not ' + repr(background))
        if background is None:
            background = Color('transparent')
        with background:
            r = library.MagickNewImage(self.wand, width, height,
                                   background.resource)
            if not r:
                self.raise_exception()
        return self

    def convert(self, format):
        """Converts the image format with the original image maintained.
        It returns a converted image instance which is new. ::

            with img.convert('png') as converted:
                converted.save(filename='converted.png')

        :param format: image format to convert to
        :type format: :class:`basestring`
        :returns: a converted image
        :rtype: :class:`Image`
        :raises: :exc:`ValueError` when the given ``format`` is unsupported

        .. versionadded:: 0.1.6

        """
        cloned = self.clone()
        cloned.format = format
        return cloned

    def save(self, file=None, filename=None):
        """Saves the image into the ``file`` or ``filename``. It takes
        only one argument at a time.

        :param file: a file object to write to
        :type file: file object
        :param filename: a filename string to write to
        :type filename: :class:`basename`

        .. versionadded:: 0.1.5
           The ``file`` parameter.

        .. versionadded:: 0.1.1

        """
        if file is None and filename is None:
            raise TypeError('expected an argument')
        elif file is not None and filename is not None:
            raise TypeError('expected only one argument; but two passed')
        elif file is not None:
            if isinstance(file, string_type):
                raise TypeError('file must be a writable file object, '
                                'but {0!r} is a string; did you want '
                                '.save(filename={0!r})?'.format(file))
            elif isinstance(file, file_types) and hasattr(libc, 'fdopen'):
                fd = libc.fdopen(file.fileno(), file.mode)
                if len(self.sequence) > 1:
                    r = library.MagickWriteImagesFile(self.wand, fd)
                else:
                    r = library.MagickWriteImageFile(self.wand, fd)
                libc.fflush(fd)
                if not r:
                    self.raise_exception()
            else:
                if not callable(getattr(file, 'write', None)):
                    raise TypeError('file must be a writable file object, '
                                    'but it does not have write() method: ' +
                                    repr(file))
                file.write(self.make_blob())
        else:
            if not isinstance(filename, string_type):
                raise TypeError('filename must be a string, not ' +
                                repr(filename))
            filename = encode_filename(filename)
            if len(self.sequence) > 1:
                r = library.MagickWriteImages(self.wand, filename, True)
            else:
                r = library.MagickWriteImage(self.wand, filename)
            if not r:
                self.raise_exception()

    def make_blob(self, format=None):
        """Makes the binary string of the image.

        :param format: the image format to write e.g. ``'png'``, ``'jpeg'``.
                       it is omittable
        :type format: :class:`basestring`
        :returns: a blob (bytes) string
        :rtype: :class:`str`
        :raises: :exc:`ValueError` when ``format`` is invalid

        .. versionchanged:: 0.1.6
           Removed a side effect that changes the image :attr:`format`
           silently.

        .. versionadded:: 0.1.5
           The ``format`` parameter became optional.

        .. versionadded:: 0.1.1

        """
        if format is not None:
            with self.convert(format) as converted:
                return converted.make_blob()
        library.MagickResetIterator(self.wand)
        length = ctypes.c_size_t()
        blob_p = None
        if len(self.sequence) > 1:
            blob_p = library.MagickGetImagesBlob(self.wand,
                                                 ctypes.byref(length))
        else:
            blob_p = library.MagickGetImageBlob(self.wand, ctypes.byref(length))
        if blob_p and length.value:
            blob = ctypes.string_at(blob_p, length.value)
            library.MagickRelinquishMemory(blob_p)
            return blob
        self.raise_exception()

    def strip(self):
        """Strips an image of all profiles and comments.

        .. versionadded:: 0.2.0

        """
        result = library.MagickStripImage(self.wand)
        if not result:
            self.raise_exception()

    def trim(self, color=None, fuzz=0):
        """Remove solid border from image. Uses top left pixel as a guide
        by default, or you can also specify the ``color`` to remove.

        :param color: the border color to remove.
                      if it's omitted top left pixel is used by default
        :type color: :class:`~wand.color.Color`
        :param fuzz: Defines how much tolerance is acceptable to consider
                     two colors as the same.
        :type fuzz: :class:`numbers.Integral`

        .. versionadded:: 0.3.0
           Optional ``color`` and ``fuzz`` parameters.

        .. versionadded:: 0.2.1

        """
        with color or self[0, 0] as color:
            self.border(color, 1, 1)
        result = library.MagickTrimImage(self.wand, fuzz)
        if not result:
            self.raise_exception()

    def border(self, color, width, height):
        """Surrounds the image with a border.

        :param bordercolor: the border color pixel wand
        :type image: :class:`~wand.color.Color`
        :param width: the border width
        :type width: :class:`numbers.Integral`
        :param height: the border height
        :type height: :class:`numbers.Integral`

        .. versionadded:: 0.3.0

        """
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            result = library.MagickBorderImage(self.wand, color.resource,
                                               width, height)
        if not result:
            self.raise_exception()

    def normalize(self, channel=None):
        """Normalize color channels.

        :param channel: the channel type.  available values can be found
                        in the :const:`CHANNELS` mapping.  If ``None``,
                        normalize all channels.
        :type channel: :class:`basestring`

        """
        if channel:
            try:
                ch_const = CHANNELS[channel]
            except KeyError:
                raise ValueError(repr(channel) + ' is an invalid channel type'
                                 '; see wand.image.CHANNELS dictionary')
            r = library.MagickNormalizeImageChannel(self.wand, ch_const)
        else:
            r = library.MagickNormalizeImage(self.wand)
        if not r:
            self.raise_exception()

    def _repr_png_(self):
        with self.convert('png') as cloned:
            return cloned.make_blob()

    def __repr__(self):
        cls = type(self)
        if getattr(self, 'c_resource', None) is None:
            return '<{0}.{1}: (closed)>'.format(cls.__module__, cls.__name__)
        return '<{0}.{1}: {2} {3!r} ({4}x{5})>'.format(
            cls.__module__, cls.__name__,
            self.signature[:7], self.format, self.width, self.height
        )


class Iterator(Resource, collections.Iterator):
    """Row iterator for :class:`Image`. It shouldn't be instantiated
    directly; instead, it can be acquired through :class:`Image` instance::

        assert isinstance(image, wand.image.Image)
        iterator = iter(image)

    It doesn't iterate every pixel, but rows. For example::

        for row in image:
            for col in row:
                assert isinstance(col, wand.color.Color)
                print(col)

    Every row is a :class:`collections.Sequence` which consists of
    one or more :class:`wand.color.Color` values.

    :param image: the image to get an iterator
    :type image: :class:`Image`

    .. versionadded:: 0.1.3

    """

    c_is_resource = library.IsPixelIterator
    c_destroy_resource = library.DestroyPixelIterator
    c_get_exception = library.PixelGetIteratorException
    c_clear_exception = library.PixelClearIteratorException

    def __init__(self, image=None, iterator=None):
        if image is not None and iterator is not None:
            raise TypeError('it takes only one argument at a time')
        with self.allocate():
            if image is not None:
                if not isinstance(image, Image):
                    raise TypeError('expected a wand.image.Image instance, '
                                    'not ' + repr(image))
                self.resource = library.NewPixelIterator(image.wand)
                self.height = image.height
            else:
                if not isinstance(iterator, Iterator):
                    raise TypeError('expected a wand.image.Iterator instance, '
                                    'not ' + repr(iterator))
                self.resource = library.ClonePixelIterator(iterator.resource)
                self.height = iterator.height
        self.raise_exception()
        self.cursor = 0

    def __iter__(self):
        return self

    def seek(self, y):
        if not isinstance(y, numbers.Integral):
            raise TypeError('expected an integer, but got ' + repr(y))
        elif y < 0:
            raise ValueError('cannot be less than 0, but got ' + repr(y))
        elif y > self.height:
            raise ValueError('canot be greater than height')
        self.cursor = y
        if y == 0:
            library.PixelSetFirstIteratorRow(self.resource)
        else:
            if not library.PixelSetIteratorRow(self.resource, y - 1):
                self.raise_exception()

    def __next__(self, x=None):
        if self.cursor >= self.height:
            self.destroy()
            raise StopIteration()
        self.cursor += 1
        width = ctypes.c_size_t()
        pixels = library.PixelGetNextIteratorRow(self.resource,
                                                 ctypes.byref(width))
        get_color = library.PixelGetMagickColor
        struct_size = ctypes.sizeof(MagickPixelPacket)
        if x is None:
            r_pixels = [None] * width.value
            for x in xrange(width.value):
                pc = pixels[x]
                packet_buffer = ctypes.create_string_buffer(struct_size)
                get_color(pc, packet_buffer)
                r_pixels[x] = Color(raw=packet_buffer)
            return r_pixels
        packet_buffer = ctypes.create_string_buffer(struct_size)
        get_color(pixels[x], packet_buffer)
        return Color(raw=packet_buffer)

    next = __next__  # Python 2 compatibility

    def clone(self):
        """Clones the same iterator.

        """
        return type(self)(iterator=self)


class ImageProperty(object):
    """The mixin class to maintain a weak reference to the parent
    :class:`Image` object.

    .. versionadded:: 0.3.0

    """

    def __init__(self, image):
        if not isinstance(image, BaseImage):
            raise TypeError('expected a wand.image.BaseImage instance, '
                            'not ' + repr(image))
        self._image = weakref.ref(image)

    @property
    def image(self):
        """(:class:`Image`) The parent image.

        It ensures that the parent :class:`Image`, which is held in a weak
        reference, still exists.  Returns the dereferenced :class:`Image`
        if it does exist, or raises a :exc:`ClosedImageError` otherwise.

        :exc: `ClosedImageError` when the parent Image has been destroyed

        """
        # Dereference our weakref and check that the parent Image stil exists
        image = self._image()
        if image is not None:
            return image
        raise ClosedImageError(
            'parent Image of {0!r} has been destroyed'.format(self)
        )

class OptionDict(ImageProperty, collections.MutableMapping):
    """Mutable mapping of the image internal options.  See available
    options in :const:`OPTIONS` constant.

    .. versionadded:: 0.3.0

    """

    def __iter__(self):
        return iter(OPTIONS)

    def __len__(self):
        return len(OPTIONS)

    def __getitem__(self, key):
        if not isinstance(key, string_type):
            raise TypeError('option name must be a string, not ' + repr(key))
        if key not in OPTIONS:
            raise ValueError('invalid option: ' + repr(key))
        image = self.image
        return text(library.MagickGetOption(image.wand, binary(key)))

    def __setitem__(self, key, value):
        if not isinstance(key, string_type):
            raise TypeError('option name must be a string, not ' + repr(key))
        if not isinstance(value, string_type):
            raise TypeError('option value must be a string, not ' +
                            repr(value))
        if key not in OPTIONS:
            raise ValueError('invalid option: ' + repr(key))
        image = self.image
        library.MagickSetOption(image.wand, binary(key), binary(value))

    def __delitem__(self, key):
        self[key] = ''


class Metadata(ImageProperty, collections.Mapping):
    """Class that implements dict-like read-only access to image metadata
    like EXIF or IPTC headers.

    :param image: an image instance
    :type image: :class:`Image`

    .. note::

       You don't have to use this by yourself.
       Use :attr:`Image.metadata` property instead.

    .. versionadded:: 0.3.0

    """

    def __init__(self, image):
        if not isinstance(image, Image):
            raise TypeError('expected a wand.image.Image instance, '
                            'not ' + repr(image))
        super(Metadata, self).__init__(image)

    def __getitem__(self, k):
        """
        :param k: Metadata header name string.
        :type k: :class:`basestring`
        :returns: a header value string
        :rtype: :class:`str`
        """
        image = self.image
        if not isinstance(k, string_type):
            raise TypeError('k must be a string, not ' + repr(k))
        v = library.MagickGetImageProperty(image.wand, binary(k))
        if bool(v) is False:
            raise KeyError(k)
        value = v.value
        return text(value)

    def __iter__(self):
        image = self.image
        num = ctypes.c_size_t()
        props_p = library.MagickGetImageProperties(image.wand, b'', num)
        props = [text(props_p[i]) for i in xrange(num.value)]
        library.MagickRelinquishMemory(props_p)
        return iter(props)

    def __len__(self):
        image = self.image
        num = ctypes.c_size_t()
        props_p = library.MagickGetImageProperties(image.wand, b'', num)
        library.MagickRelinquishMemory(props_p)
        return num.value


class ChannelImageDict(ImageProperty, collections.Mapping):
    """The mapping table of separated images of the particular channel
    from the image.

    :param image: an image instance
    :type image: :class:`Image`

    .. note::

       You don't have to use this by yourself.
       Use :attr:`Image.channel_images` property instead.

    .. versionadded:: 0.3.0

    """

    def __iter__(self):
        return iter(CHANNELS)

    def __len__(self):
        return len(CHANNELS)

    def __getitem__(self, channel):
        c = CHANNELS[channel]
        img = self.image.clone()
        succeeded = library.MagickSeparateImageChannel(img.wand, c)
        if not succeeded:
            try:
                img.raise_exception()
            except WandException:
                img.close()
                raise
        return img


class ChannelDepthDict(ImageProperty, collections.Mapping):
    """The mapping table of channels to their depth.

    :param image: an image instance
    :type image: :class:`Image`

    .. note::

       You don't have to use this by yourself.
       Use :attr:`Image.channel_depths` property instead.

    .. versionadded:: 0.3.0

    """

    def __iter__(self):
        return iter(CHANNELS)

    def __len__(self):
        return len(CHANNELS)

    def __getitem__(self, channel):
        c = CHANNELS[channel]
        depth = library.MagickGetImageChannelDepth(self.image.wand, c)
        return int(depth)


class HistogramDict(collections.Mapping):
    """Specialized mapping object to represent color histogram.
    Keys are colors, and values are the number of pixels.

    :param image: the image to get its histogram
    :type image: :class:`BaseImage`

    .. versionadded:: 0.3.0

    """

    def __init__(self, image):
        self.size = ctypes.c_size_t()
        self.pixels = library.MagickGetImageHistogram(
            image.wand,
            ctypes.byref(self.size)
        )
        self.counts = None

    def __len__(self):
        if self.counts is None:
            return self.size.value
        return len(self.counts)

    def __iter__(self):
        if self.counts is None:
            pixels = self.pixels
            string = library.PixelGetColorAsString
            return (Color(string(pixels[i]).value)
                    for i in xrange(self.size.value))
        return iter(Color(string=c) for c in self.counts)

    def __getitem__(self, color):
        if self.counts is None:
            string = library.PixelGetColorAsNormalizedString
            pixels = self.pixels
            count = library.PixelGetColorCount
            self.counts = dict(
                (text(string(pixels[i]).value), count(pixels[i]))
                for i in xrange(self.size.value)
            )
            del self.size, self.pixels
        return self.counts[color.normalized_string]


class ClosedImageError(DestroyedResourceError):
    """An error that rises when some code tries access to an already closed
    image.

    """
