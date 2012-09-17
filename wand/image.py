""":mod:`wand.image` --- Image objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens and manipulates images. Image objects can be used in :keyword:`with`
statement, and these resources will be automatically managed (even if any
error happened)::

    with Image(filename='pikachu.png') as i:
        print 'width =', i.width
        print 'height =', i.height

"""
import collections
import ctypes
import numbers
import platform
import types

from .api import MagickPixelPacket, libc, libmagick, library
from .color import Color
from .resource import DestroyedResourceError, Resource


__all__ = ('ALPHA_CHANNEL_TYPES', 'CHANNELS', 'COMPOSITE_OPS', 'EVALUATE_OPS',
           'FILTER_TYPES', 'IMAGE_TYPES', 'UNIT_TYPES', 'ClosedImageError',
           'Image', 'Iterator')


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
#: .. seealso::
#:
#:    `ImageMagick Composition Operators`__
#:       Demonstrates the results of applying the various composition
#:       composition operators.
#:
#:    __ http://www.rubblewebs.co.uk/imagemagick/operators/compose.php
COMPOSITE_OPS = ('undefined', 'no', 'add', 'atop', 'blend', 'bumpmap',
                 'change_mask', 'clear', 'color_burn', 'color_dodge',
                 'colorize', 'copy_black', 'copy_blue', 'copy', 'copy_cyan',
                 'copy_green', 'copy_magenta', 'copy_opacity', 'copy_red',
                 'copy_yellow', 'darken', 'dst_atop', 'dst', 'dst_in',
                 'dst_out', 'dst_over', 'difference', 'displace',
                 'dissolve', 'exclusion', 'hard_light', 'hue', 'in',
                 'lighten', 'linear_light', 'luminize', 'minus', 'modulate',
                 'multiply', 'out', 'over', 'overlay', 'plus', 'replace',
                 'saturate', 'screen', 'soft_light', 'src_atop', 'src',
                 'src_in', 'src_out', 'src_over', 'subtract', 'threshold',
                 'xor', 'divide')

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

#: (:class:`tuple`) The list of alpha chanell types
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

#: (:class:`tuple`) The list of resolution unit types
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


class Image(Resource):
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


    .. versionadded:: 0.1.5
       The ``file`` parameter.

    .. versionadded:: 0.1.1
       The ``blob`` parameter.

    .. versionadded:: 0.2.1
       The ``format`` parameter.

    .. versionadded:: 0.2.2
       The ``width``, ``height``, ``background`` parameters.

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

    c_is_resource = library.IsMagickWand
    c_destroy_resource = library.DestroyMagickWand
    c_get_exception = library.MagickGetException
    c_clear_exception = library.MagickClearException

    __slots__ = '_wand',

    def __init__(self, image=None, blob=None, file=None, filename=None,
                 format=None, width=None, height=None, background=None):
        new_args = width, height, background
        open_args = image, blob, file, filename

        if (any(a is not None for a in new_args) and
            any(a is not None for a in open_args)):
            raise TypeError('blank image parameters cant be used with image '
                            'opening parameters')
        elif all(a is None for a in open_args):
            # Create a blank image
            if not isinstance(width, numbers.Integral) or width < 1:
                raise TypeError('width must be a natural number, not ' +
                                repr(width))
            if not isinstance(height, numbers.Integral) or height < 1:
                raise TypeError('height must be a natural number, not ' +
                                repr(height))
            if background is not None and not isinstance(background, Color):
                raise TypeError('background must be a wand.color.Color '
                                'instance, not ' + repr(background))
        elif any(a is not None and b is not None
                 for i, a in enumerate(open_args)
                 for b in open_args[:i] + open_args[i + 1:]):
            raise TypeError('parameters are exclusive each other; use only '
                            'one at once')
        elif not (format is None or isinstance(format, basestring)):
            raise TypeError('format must be a string, not ' + repr(format))
        with self.allocate():
            if width is not None and height is not None:
                if background is None:
                    background = Color('transparent')
                self.wand = library.NewMagickWand()
                with background:
                    library.MagickNewImage(self.wand, width, height,
                                           background.resource)
            elif image is not None:
                if not isinstance(image, Image):
                    raise TypeError('image must be a wand.image.Image '
                                    'instance, not ' + repr(image))
                elif format:
                    raise TypeError('format option cannot be used with image '
                                    'nor filename')
                self.wand = library.CloneMagickWand(image.wand)
            else:
                self.wand = library.NewMagickWand()
                read = False
                if file is not None:
                    if format:
                        library.MagickSetFilename(self.wand,
                                                  'buffer.' + format)
                    if (isinstance(file, types.FileType) and
                        hasattr(libc, 'fdopen')):
                        fd = libc.fdopen(file.fileno(), file.mode)
                        library.MagickReadImageFile(self.wand, fd)
                        read = True
                    elif not callable(getattr(file, 'read', None)):
                        raise TypeError('file must be a readable file object'
                                        ', but the given object does not '
                                        'have read() method')
                    else:
                        blob = file.read()
                        file = None
                if blob is not None:
                    if format:
                        library.MagickSetFilename(self.wand,
                                                  'buffer.' + format)
                    if not isinstance(blob, collections.Iterable):
                        raise TypeError('blob must be iterable, not ' +
                                        repr(blob))
                    if not isinstance(blob, basestring):
                        blob = ''.join(blob)
                    elif not isinstance(blob, str):
                        blob = str(blob)
                    library.MagickReadImageBlob(self.wand, blob, len(blob))
                    read = True
                elif filename is not None:
                    if format:
                        raise TypeError(
                            'format option cannot be used with image '
                            'nor filename'
                        )
                    library.MagickReadImage(self.wand, filename)
                    read = True
                if not read:
                    raise TypeError('invalid argument(s)')
        self.raise_exception()

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

    def close(self):
        """Closes the image explicitly. If you use the image object in
        :keyword:`with` statement, it was called implicitly so don't have to
        call it.

        .. note::

           It has the same functionality of :attr:`destroy()` method.

        """
        self.destroy()

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
        return type(self)(image=self)

    def __len__(self):
        return self.height

    def __iter__(self):
        return Iterator(image=self)

    def __getitem__(self, idx):
        if (not isinstance(idx, basestring) and
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
    def width(self):
        """(:class:`numbers.Integral`) The width of this image."""
        return library.MagickGetImageWidth(self.wand)

    @property
    def height(self):
        """(:class:`numbers.Integral`) The height of this image."""
        return library.MagickGetImageHeight(self.wand)

    @property
    def size(self):
        """(:class:`tuple`) The pair of (:attr:`width`, :attr:`height`)."""
        return self.width, self.height

    @property
    def units(self):
        """(:class:`basestring`) The resolution units of this image."""
        r = library.MagickGetImageUnits(self.wand)
        return UNIT_TYPES[r]

    @units.setter
    def units(self, units):
        if not isinstance(units, basestring) or units not in UNIT_TYPES: 
            raise TypeError('Unit value must be a string from wand.images.'
                            'UNIT_TYPES, not ' + repr(units))
        r = library.MagickSetImageUnits(self.wand, UNIT_TYPES.index(units))
        if not r:
            self.raise_exception()

    @property
    def depth(self):
        """(:class:`numbers.Integral`) The depth of this image.

        .. versionadded:: 0.2.1

        """
        return library.MagickGetImageDepth(self.wand)

    @depth.setter
    def depth(self, depth):
        r = library.MagickSetImageDepth(self.wand, depth)
        if not r:
            raise self.raise_exception()

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
        if fmt:
            return fmt
        self.raise_exception()

    @format.setter
    def format(self, fmt):
        if not isinstance(fmt, basestring):
            raise TypeError("format must be a string like 'png' or 'jpeg'"
                            ', not ' + repr(fmt))
        r = library.MagickSetImageFormat(self.wand, fmt.strip().upper())
        if not r:
            raise ValueError(repr(fmt) + ' is unsupported format')

    @property
    def type(self):
        """(:class:`basestring`) The image type.

        Defines image type as in wand.image.IMAGE_TYPES enumeration.

        It may raise :exc:`ValueError` when the type is unknown.

        .. versionadded:: 0.2.2

        """
        image_type_index = library.MagickGetImageType(self.wand)
        if not image_type_index:
            self.raise_exception()
        return IMAGE_TYPES[image_type_index]

    @type.setter
    def type(self, image_type):
        if not isinstance(image_type, basestring) \
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
    def mimetype(self):
        """(:class:`basestring`) The MIME type of the image
        e.g. ``'image/jpeg'``, ``'image/png'``.

        .. versionadded:: 0.1.7

        """
        rp = libmagick.MagickToMime(self.format)
        if not rp:
            self.raise_exception()
        mimetype = ctypes.string_at(rp)
        if platform.system() != 'Windows':
            # FIXME: On Windows, the above free() makes access violation
            #        reading error.  This conditional free() is of course
            #        *not* the right solution, but I currently can't
            #        understand why.
            libc.free(rp)
        return mimetype

    @property
    def signature(self):
        """(:class:`str`) The SHA-256 message digest for the image pixel
        stream.

        .. versionadded:: 0.1.9

        """
        return library.MagickGetImageSignature(self.wand)

    @property
    def alpha_channel(self):
        """(:class:`bool`) Get state of image alpha channel.
        It can also be used to enable/disable alpha channel.

        .. versionadded:: 0.2.1

        .. todo::

           Support other states than ``''activatealphachannel'``
           or ``'deactivatealphachannel'``.

        """
        return library.MagickGetImageAlphaChannel(self.wand)

    @alpha_channel.setter
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

    @property
    def quantum_range(self):
        """(:class:`int`) The maxumim value of a color channel that is
        supported by the imagemgick library.

        .. versionadded:: 0.2.0

        """
        result = ctypes.c_size_t()
        library.MagickGetQuantumRange(ctypes.byref(result))
        return result.value

    @background_color.setter
    def background_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            result = library.MagickSetImageBackgroundColor(self.wand,
                                                           color.resource)
            if not result:
                self.raise_exception()

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
        elif not isinstance(filter, (basestring, numbers.Integral)):
            raise TypeError('filter must be one string defined in wand.image.'
                            'FILTER_TYPES or an integer, not ' + repr(filter))
        if isinstance(filter, basestring):
            try:
                filter = FILTER_TYPES.index(filter)
            except IndexError:
                raise ValueError(repr(filter) + ' is an invalid filter type; '
                                 'choose on in ' + repr(FILTER_TYPES))
        elif (isinstance(filter, numbers.Integral) and
              not (0 <= filter < len(FILTER_TYPES))):
            raise ValueError(repr(filter) + ' is an invalid filter type')
        blur = ctypes.c_double(float(blur))
        r = library.MagickResizeImage(self.wand, width, height, filter, blur)
        if not r:
            self.raise_exception()

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
        if not isinstance(crop, basestring):
            raise TypeError("crop must be a string, not " + repr(crop))
        if not isinstance(resize, basestring):
            raise TypeError("resize must be a string, not " + repr(resize))
        # Also verify that only ASCII characters are included
        try:
            crop.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('crop must only contain ascii-encodable ' +
                             'characters.')
        try:
            resize.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('resize must only contain ascii-encodable ' +
                             'characters.')
        new_wand = library.MagickTransformImage(self.wand, crop, resize)
        if not new_wand:
            self.raise_exception()
        self.wand = new_wand

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
            result = library.MagickRotateImage(self.wand,
                                               background.resource,
                                               degree)
        if not result:
            self.raise_exception()
        if reset_coords:
            self.reset_coords()

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
            # Set the wand to image zero, in case there are multiple images in it
            library.MagickSetIteratorIndex(self.wand, 0)
            # Change the pixel representation of the image
            # to RGB with an alpha channel
            library.MagickSetImageType(self.wand,
                                       IMAGE_TYPES.index('truecolormatte'))
            # Perform the black channel subtraction
            library.MagickEvaluateImageChannel(self.wand,
                                               CHANNELS['black'],
                                               EVALUATE_OPS.index('subtract'),
                                               t)
            self.raise_exception()

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
        library.MagickCompositeImage(self.wand, image.wand,
                                     COMPOSITE_OPS.index('over'), left, top)
        self.raise_exception()

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
            self.composite(watermark_image, left, top)
        self.raise_exception()

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
            if isinstance(file, types.FileType) and hasattr(libc, 'fdopen'):
                fd = libc.fdopen(file.fileno(), file.mode)
                r = library.MagickWriteImageFile(self.wand, fd)
                if not r:
                    self.raise_exception()
            else:
                if not callable(getattr(file, 'write', None)):
                    raise TypeError('file must be a writable file object, '
                                    'but it does not have write() method: ' +
                                    repr(file))
                file.write(self.make_blob())
        else:
            if not isinstance(filename, basestring):
                raise TypeError('filename must be a string, not ' +
                                repr(filename))
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

    def trim(self):
        """Remove solid border from image. Uses top left pixel as a guide.

        .. versionadded:: 0.2.1

        """
        result = library.MagickTrimImage(self.wand)
        if not result:
            self.raise_exception()

class Iterator(Resource, collections.Iterator):
    """Row iterator for :class:`Image`. It shouldn't be instantiated
    directly; instead, it can be acquired through :class:`Image` instance::

        assert isinstance(image, wand.image.Image)
        iterator = iter(image)

    It doesn't iterate every pixel, but rows. For example::

        for row in image:
            for col in row:
                assert isinstance(col, wand.color.Color)
                print col

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

    def next(self, x=None):
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

    def clone(self):
        """Clones the same iterator.

        """
        return type(self)(iterator=self)


class ClosedImageError(DestroyedResourceError):
    """An error that rises when some code tries access to an already closed
    image.

    """

