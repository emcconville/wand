""":mod:`wand.color` --- Colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from .api import library
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

    """

    c_is_resource = library.IsPixelWand
    c_destroy_resource = library.DestroyPixelWand
    c_get_exception = library.PixelGetException
    c_clear_exception = library.PixelClearException

    __slots__ = 'string', 'c_resource', 'allocated'

    def __init__(self, string):
        self.string = string
        self.allocated = 0

    def __getinitargs__(self):
        return self.string,

    def __enter__(self):
        if not self.allocated:
            with self.allocate():
                self.resource = library.NewPixelWand()
                library.PixelSetColor(self.resource, self.string)
        self.allocated += 1
        return Resource.__enter__(self)

    def __exit__(self, type, value, traceback):
        self.allocated -= 1
        if not self.allocated:
            Resource.__exit__(self, type, value, traceback)

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        with self as this:
            with other:
                a = this.resource
                b = other.resource
                alpha = library.PixelGetAlpha
                return bool(library.IsPixelWandSimilar(a, b, 0) and
                            alpha(a) == alpha(b))

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

