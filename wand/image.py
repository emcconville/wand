""":mod:`wand.image` --- Image objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens and manipulates images. Image objects can be used in :keyword:`with`
statement, and these resources will be automatically managed (even if any
error happened)::

    with Image(filename='pikachu.png') as i:
        print 'width =', i.width
        print 'height =', i.height

"""
import numbers
import collections
import ctypes
import os
import sys
import warnings
from . import exceptions
from .api import library
from .resource import increment_refcount, decrement_refcount


__all__ = 'FILTER_TYPES', 'Image', 'ClosedImageError'


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
#:    `ImageMagick Resize Filters
#:    <http://www.dylanbeattie.net/magick/filters/result.html>`_
FILTER_TYPES = ('undefined', 'point', 'box', 'triangle', 'hermite', 'hanning',
                'hamming', 'blackman', 'gaussian', 'quadratic', 'cubic',
                'catrom', 'mitchell', 'lanczos', 'bessel', 'sinc')


class Image(object):
    """An image object.

    :param image: makes an exact copy of the ``image``
    :type image: :class:`Image`
    :param filename: opens an image of the ``filename``
    :type filename: :class:`basestring`

    """

    __slots__ = '_wand',

    def __init__(self, image=None, blob=None, filename=None):
        args = image, blob, filename
        if all(a is None for a in args):
            raise TypeError('missing arguments')
        elif any(a is not None and b is not None
                 for i, a in enumerate(args)
                 for b in args[:i] + args[i + 1:]):
            raise TypeError('parameters are exclusive each other; use only '
                            'one at once')
        increment_refcount()
        try:
            if image is not None:
                if not isinstance(image, Image):
                    raise TypeError('image must be a wand.image.Image '
                                    'instance, not ' + repr(image))
                self.wand = library.CloneMagickWand(image.wand)
            else:
                self.wand = library.NewMagickWand()
                if blob is not None:
                    if not isinstance(blob, collections.Iterable):
                        raise TypeError('blob must be iterable, not ' +
                                        repr(blob))
                    if not isinstance(blob, basestring):
                        blob = ''.join(blob)
                    elif not isinstance(blob, str):
                        blob = str(blob)
                    library.MagickReadImageBlob(self.wand, blob, len(blob))
                elif filename is not None:
                    library.MagickReadImage(self.wand, filename)
                else:
                    raise TypeError('invalid argument(s)')
        except:
            decrement_refcount()
            raise
        self.raise_exception()

    @property
    def wand(self):
        """Internal pointer to the MagickWand instance. It may raise
        :exc:`ClosedImageError` when the instance has destroyed already.

        """
        if self._wand is None:
            raise ClosedImageError(repr(self) + ' is closed already')
        return self._wand

    @wand.setter
    def wand(self, wand):
        if library.IsMagickWand(wand):
            self._wand = wand
        else:
            raise TypeError(repr(wand) + ' is not a MagickWand instance')

    @wand.deleter
    def wand(self):
        library.DestroyMagickWand(self.wand)
        self._wand = None

    def get_exception(self):
        """Gets a current exception instance.

        :returns: a current exception. it can be ``None`` as well if any
                  errors aren't occurred
        :rtype: :class:`wand.exceptions.WandException`

        """
        severity = ctypes.c_int()
        desc = library.MagickGetException(self.wand, ctypes.byref(severity))
        if severity.value == 0:
            return
        library.MagickClearException(self.wand)
        exc_cls = exceptions.TYPE_MAP[severity.value]
        return exc_cls(ctypes.string_at(desc))

    def raise_exception(self, stacklevel=1):
        """Raises an exception or warning if it has occurred."""
        e = self.get_exception()
        if isinstance(e, Warning):
            warnings.warn(e, stacklevel=stacklevel + 1)
        elif isinstance(e, Exception):
            raise e

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """Closes the image explicitly. If you use the image object in
        :keyword:`with` statement, it was called implicitly so don't have to
        call it.

        """
        del self.wand
        decrement_refcount()

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
        :param blur: the blur factor where > 1 is blurry, < 1 is sharp
        :type blur: :class:`numbers.Rational`

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
        elif not isinstance(blur, numbers.Rational):
            raise TypeError('blur must be numbers.Rational, not ' + repr(blur))
        elif not isinstance(filter, (basestring, numbers.Integral)):
            raise TypeError('filter must be one string defined in wand.image.'
                            'FILTER_TYPES or an integer, not ' + repr(filter))
        if isinstance(filter, basestring):
            try:
                filter = FILTER_TYPES.index(filter)
            except IndexError:
                raise ValueError(repr(filter) + ' is an invalid filter type; '
                                 'choose on in ' + repr(FILTET_TYPES))
        elif (isinstance(filter, numbers.Integral) and
              not (0 <= filter < len(FILTER_TYPES))):
            raise ValueError(repr(filter) + ' is an invalid filter type')
        blur = ctypes.c_double(float(blur))
        library.MagickResizeImage(self.wand, width, height, filter, blur)

    def save(self, filename):
        """Saves the image into the ``filename``.

        :param filename: a filename to write to
        :type filename: :class:`basename`

        """
        if not isinstance(filename, basestring):
            raise TypeError('filename must be a string, not ' + repr(filename))
        r = library.MagickWriteImage(self.wand, filename)
        if not r:
            raise self.get_exception()

    def make_blob(self, format):
        """Makes the binary string of the image.

        :param format: the image format to write e.g. ``'png'``, ``'jpeg'``
        :type format: :class:`basestring`
        :returns: a blob (bytes) string
        :rtype: :class:`str`
        :raises: :exc:`ValueError` when ``format`` is invalid

        """
        if not isinstance(format, basestring):
            raise TypeError("format must be a string like 'png' or 'jpeg', "
                            'not ' + repr(format))
        r = library.MagickSetImageFormat(self.wand, str(format).strip().upper())
        if not r:
            raise ValueError('{0!r} is an invalid format'.format(format))
        library.MagickResetIterator(self.wand)
        length = ctypes.c_size_t()
        blob_p = library.MagickGetImageBlob(self.wand, ctypes.byref(length))
        blob = ctypes.string_at(blob_p, length.value)
        library.MagickRelinquishMemory(library.MagickIdentifyImage(self.wand))
        return blob


class ClosedImageError(ReferenceError, AttributeError):
    """An error that rises when some code tries access to an already closed
    image.

    """

