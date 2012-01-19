""":mod:`wand.image` --- Image objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens and manipulates images. Image objects can be used in :keyword:`with`
statement, and these resources will be automatically managed (even if any
error happened)::

    with Image(filename='pikachu.png') as i:
        print 'width =', i.width
        print 'height =', i.height

"""
import types
import numbers
import collections
import ctypes
import platform
from .api import library, libmagick, libc, MagickPixelPacket
from .resource import Resource, DestroyedResourceError
from .color import Color


__all__ = 'FILTER_TYPES', 'Image', 'Iterator', 'ClosedImageError'


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
#: - ``'lanczos'``
#: - ``'bessel'``
#: - ``'sinc'``
#:
#: .. seealso::
#:
#:    `ImageMagick Resize Filters`__
#:       Demonstrates the results of resampling three images using the various
#:       resize filters and blur settings available in ImageMagick,
#:       and the file size of the resulting thumbnail images.
#:
#:    __ http://www.dylanbeattie.net/magick/filters/result.html
FILTER_TYPES = ('undefined', 'point', 'box', 'triangle', 'hermite', 'hanning',
                'hamming', 'blackman', 'gaussian', 'quadratic', 'cubic',
                'catrom', 'mitchell', 'lanczos', 'bessel', 'sinc')


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

    """

    c_is_resource = library.IsMagickWand
    c_destroy_resource = library.DestroyMagickWand
    c_get_exception = library.MagickGetException
    c_clear_exception = library.MagickClearException

    __slots__ = '_wand',

    def __init__(self, image=None, blob=None, file=None, filename=None):
        args = image, blob, file, filename
        if all(a is None for a in args):
            raise TypeError('missing arguments')
        elif any(a is not None and b is not None
                 for i, a in enumerate(args)
                 for b in args[:i] + args[i + 1:]):
            raise TypeError('parameters are exclusive each other; use only '
                            'one at once')
        with self.allocate():
            if image is not None:
                if not isinstance(image, Image):
                    raise TypeError('image must be a wand.image.Image '
                                    'instance, not ' + repr(image))
                self.wand = library.CloneMagickWand(image.wand)
            else:
                self.wand = library.NewMagickWand()
                read = False
                if file is not None:
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
    def mimetype(self):
        """(:class:`basestring`) The MIME type of the image
        e.g. ``'image/jpeg'``, ``'image/png'``.

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

        """
        return library.MagickGetImageSignature(self.wand)

    @property
    def background_color(self):
        """(:class:`wand.color.Color`) The image background color.
        It can also be set to change the background color.

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

        """
        cloned = self.clone()
        cloned.format = format
        return cloned

    def crop(self, left=0, top=0, right=None, bottom=None,
             width=None, height=None):
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

        .. note::

           If you want to crop the image but not in-place, use slicing
           operator.

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

    def resize(self, width=None, height=None, filter='triangle', blur=1):
        """Resizes the image.

        :param width: the width in the scaled image. default is the original
                      width
        :type width: :class:`numbers.Integral`
        :param height: the height in the scaled image. default is the original
                       height
        :type height: :class:`numbers.Integral`
        :param filter: a filter type to use for resizing. choose one in
                       :const:`FILTER_TYPES`. default is ``'triangle'``
        :type filter: :class:`basestring`, :class:`numbers.Integral`
        :param blur: the blur factor where > 1 is blurry, < 1 is sharp.
                     default is 1
        :type blur: :class:`numbers.Real`

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
        library.MagickResizeImage(self.wand, width, height, filter, blur)

    def rotate(self, degree, background=None):
        """Rotates the image. It takes a ``background`` color for ``degree``
        that isn't a multiple of 90.

        :param degree: a degree to rotate. multiples of 360 affect nothing
        :type degree: :class:`numbers.Real`
        :param background: an optional background color.
                           default is transparent
        :type background: :class:`wand.color.Color`

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

    def save(self, file=None, filename=None):
        """Saves the image into the ``file`` or ``filename``. It takes
        only one argument at a time.

        :param file: a file object to write to
        :type file: file object
        :param filename: a filename string to write to
        :type filename: :class:`basename`

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
        """Clones the same iterator."""
        return type(self)(iterator=self)


class ClosedImageError(DestroyedResourceError):
    """An error that rises when some code tries access to an already closed
    image.

    """

