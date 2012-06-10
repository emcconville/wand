""":mod:`wand.color` --- Colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 0.1.2

"""
import ctypes

from .api import MagickPixelPacket, library
from .resource import Resource

__all__ = 'Color',


class Color(Resource):
    """Color value.

    Unlike any other objects in Wand, its resource management can be
    implicit when it used outside of :keyword:`with` block. In these case,
    its resource are allocated for every operation which requires a resource
    and destroyed immediately. Of course it is inefficient when the
    operations are much, so to avoid it, you should use color objects
    inside of :keyword:`with` block explicitly e.g.::

        red_count = 0
        with Color('#f00') as red:
            with Image(filename='image.png') as img:
                for row in img:
                    for col in row:
                        if col == red:
                            red_count += 1

    :param string: a color namel string e.g. ``'rgb(255, 255, 255)'``,
                   ``'#fff'``, ``'white'``. see `ImageMagick Color Names`_
                   doc also
    :type string: :class:`basestring`

    .. seealso::

       `ImageMagick Color Names`_
          The color can then be given as a color name (there is a limited
          but large set of these; see below) or it can be given as a set
          of numbers (in decimal or hexadecimal), each corresponding to
          a channel in an RGB or RGBA color model. HSL, HSLA, HSB, HSBA,
          CMYK, or CMYKA color models may also be specified. These topics
          are briefly described in the sections below.

    .. _ImageMagick Color Names: http://www.imagemagick.org/script/color.php

    .. describe:: == (other)

       Equality operator.

       :param other: a color another one
       :type color: :class:`Color`
       :returns: ``True`` only if two images equal.
       :rtype: :class:`bool`

    """

    c_is_resource = library.IsPixelWand
    c_destroy_resource = library.DestroyPixelWand
    c_get_exception = library.PixelGetException
    c_clear_exception = library.PixelClearException

    __slots__ = 'raw', 'c_resource', 'allocated'

    def __init__(self, string=None, raw=None):
        if (string is None and raw is None or
            string is not None and raw is not None):
            raise TypeError('expected one argument')
        elif raw is None:
            pixel = library.NewPixelWand()
            library.PixelSetColor(pixel, string)
            raw = ctypes.create_string_buffer(
                ctypes.sizeof(MagickPixelPacket)
            )
            library.PixelGetMagickColor(pixel, raw)
        self.raw = raw
        self.allocated = 0

    def __getinitargs__(self):
        return self.string, None

    def __enter__(self):
        if not self.allocated:
            with self.allocate():
                self.resource = library.NewPixelWand()
                library.PixelSetMagickColor(self.resource, self.raw)
        self.allocated += 1
        return Resource.__enter__(self)

    def __exit__(self, type, value, traceback):
        self.allocated -= 1
        if not self.allocated:
            Resource.__exit__(self, type, value, traceback)

    @property
    def string(self):
        """(:class:`basestring`) The string representation of the color."""
        with self as this:
            return library.PixelGetColorAsString(self.resource)

    @staticmethod
    def c_equals(a, b):
        """Raw level version of equality test function for two pixels.

        :param a: a pointer to PixelWand to compare
        :type a: :class:`ctypes.c_void_p`
        :param b: a pointer to PixelWand to compare
        :type b: :class:`ctypes.c_void_p`
        :returns: ``True`` only if two pixels equal
        :rtype: :class:`bool`

        .. note::

           It's only for internal use. Don't use it directly.
           Use ``==`` operator of :class:`Color` instead.

        """
        alpha = library.PixelGetAlpha
        return bool(library.IsPixelWandSimilar(a, b, 0) and
                    alpha(a) == alpha(b))

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        with self as this:
            with other:
                return self.c_equals(this.resource, other.resource)

    def __ne__(self, other):
        return not (self == other)

    @property
    def red(self):
        with self:
            return library.PixelGetRedQuantum(self.resource)

    @property
    def green(self):
        with self:
            return library.PixelGetGreenQuantum(self.resource)

    @property
    def blue(self):
        with self:
            return library.PixelGetBlueQuantum(self.resource)

    def __str__(self):
        return self.string

    def __repr__(self):
        c = type(self)
        return '{0}.{1}({2!r})'.format(c.__module__, c.__name__, self.string)

