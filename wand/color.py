""":mod:`wand.color` --- Colors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from .api import library
from .resource import Resource


class Color(Resource):
    """Color."""

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

