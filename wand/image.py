""":mod:`wand.image` --- Image objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens and manipulates images. Image objects can be used in :keyword:`with`
statement, and these resources will be automatically managed (even if any
error happened)::

    with Image(filename='pikachu.png') as i:
        print 'width =', i.width
        print 'height =', i.height

"""
from .api import library
from .resource import increment_refcount, decrement_refcount


__all__ = 'Image', 'ClosedImageError'


class Image(object):
    """An image object.

    :param image: makes an exact copy of the ``image``
    :type image: :class:`Image`
    :param filename: opens an image of the ``filename``
    :type filename: :class:`basestring`

    """

    __slots__ = '_wand',

    def __init__(self, image=None, filename=None):
        args = image, filename
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
                library.MagickReadImage(self.wand, filename)
        except:
            decrement_refcount()
            raise

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

    def save(self, filename):
        """Saves the image into the ``filename``.

        :param filename: a filename to write to
        :type filename: :class:`basename`

        """
        if not isinstance(filename, basestring):
            raise TypeError('filename must be a string, not ' + repr(filename))
        library.MagickWriteImage(self.wand, filename)


class ClosedImageError(ReferenceError, AttributeError):
    """An error that rises when some code tries access to an already closed
    image.

    """

