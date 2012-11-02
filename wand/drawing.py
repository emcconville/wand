""":mod:`wand.drawing` --- Drawings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import ctypes
import numbers

from .api import library, MagickPixelPacket
from .color import Color
from .resource import Resource

TEXT_ALIGN_TYPES = 'undefined', 'left', 'center', 'right'
TEXT_DECORATION_TYPES = ('undefined', 'no', 'underline', 'overline',
                         'line_through')
TEXT_GRAVITY_TYPES = ('forget', 'north_west', 'north',
                      'north_east', 'west', 'center', 'east', 'south_west',
                      'south', 'south_east', 'static')

__all__ = ('TEXT_ALIGN_TYPES', 'TEXT_DECORATION_TYPES', 'TEXT_GRAVITY_TYPES',
           'Drawing')


class Drawing(Resource):
    """Drawing"""

    c_is_resource = library.IsDrawingWand
    c_destroy_resource = library.DestroyDrawingWand
    c_get_exception = library.DrawGetException
    c_clear_exception = library.DrawClearException

    __slots__ = 'c_resource'

    def __init__(self, drawing_wand=None):
        with self.allocate():
            if not drawing_wand:
                wand = library.NewDrawingWand()
            else:
                wand = library.CloneDrawingWand(drawing_wand.resource)
            self.resource = wand

    def clone(self):
        return type(self)(drawing_wand=self)

    @property
    def font(self):
        return library.DrawGetFont(self.resource)

    @font.setter
    def font(self, font):
        if not isinstance(font, basestring):
            raise TypeError('font must be a basestring object, not ' +
                            repr(font))
        library.DrawSetFont(self.resource, font)

    @property
    def font_size(self):
        return library.DrawGetFontSize(self.resource)

    @font_size.setter
    def font_size(self, size):
        if not isinstance(size, numbers.Number):
            raise TypeError('expected a number, but got ' + repr(size))
        elif size < 0.0:
            raise ValueError('cannot be less then 0.0, but got ' + repr(size))
        library.DrawSetFontSize(self.resource, size)

    @property
    def fill_color(self):
        pixel = library.NewPixelWand()
        library.DrawGetFillColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @fill_color.setter
    def fill_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetFillColor(self.resource, color.resource)

    @property
    def text_alignment(self):
        text_alignment_index = library.DrawGetTextAlignment(self.resource)
        if not text_alignment_index:
            self.raise_exception()
        return TEXT_ALIGN_TYPES[text_alignment_index]

    @text_alignment.setter
    def text_alignment(self, align):
        if (not isinstance(align, basestring) or
            align not in TEXT_ALIGN_TYPES):
            raise TypeError('align value must be a string from ' +
                            'TEXT_ALIGN_TYPES, not ' + repr(align))
        library.DrawSetTextAlignment(self.resource,
                                     TEXT_ALIGN_TYPES.index(align))

    @property
    def text_antialias(self):
        result = library.DrawGetTextAntialias(self.resource)
        return True if result == 1 else False

    @text_antialias.setter
    def text_antialias(self, value):
        if not isinstance(value, bool):
            raise TypeError('value must be a boolean, not ' +
                            repr(value))
        library.DrawSetTextAntialias(self.resource, 1 if value is True else 0)

    @property
    def text_decoration(self):
        text_decoration_index = library.DrawGetTextDecoration(self.resource)
        if not text_decoration_index:
            self.raise_exception()
        return TEXT_DECORATION_TYPES[text_decoration_index]

    @text_decoration.setter
    def text_decoration(self, decoration):
        if (not isinstance(decoration, basestring) or
            decoration not in TEXT_DECORATION_TYPES):
            raise TypeError('fecoration value must be a string from ' +
                            'TEXT_DECORATION_TYPES, not ' + repr(decoration))
        library.DrawSetTextDecoration(self.resource,
                                      TEXT_DECORATION_TYPES.index(decoration))

    @property
    def text_encoding(self):
        return library.DrawGetTextEncoding(self.resource)

    @text_encoding.setter
    def text_encoding(self, encoding):
        if encoding is not None and not isinstance(encoding, basestring):
            raise TypeError('encoding must be a basestring object, not ' + 
                            repr(encoding))
        elif encoding is None:
            # encoding specify an empty string to set text encoding
            # to system's default.
            encoding = ''
        library.DrawSetTextEncoding(self.resource, encoding)

    @property
    def text_interline_spacing(self):
        return library.DrawGetTextInterlineSpacing(self.resource)

    @text_interline_spacing.setter
    def text_interline_spacing(self, spacing):
        if not isinstance(spacing, numbers.Number):
            raise TypeError('expeted a number, but got ' + repr(spacing))
        library.DrawSetTextInterlineSpacing(self.resource, spacing)

    @property
    def text_interword_spacing(self):
        return library.DrawGetTextInterwordSpacing(self.resource)

    @text_interword_spacing.setter
    def text_interword_spacing(self, spacing):
        if not isinstance(spacing, numbers.Number):
            raise TypeError('expeted a number, but got ' + repr(spacing))
        library.DrawSetTextInterwordSpacing(self.resource, spacing)

    @property
    def text_kerning(self):
        return library.DrawGetTextKerning(self.resource)

    @text_kerning.setter
    def text_kerning(self, kerning):
        if not isinstance(kerning, numbers.Number):
            raise TypeError('expeted a number, but got ' + repr(kerning))
        library.DrawSetTextKerning(self.resource, kerning)

    @property
    def text_under_color(self):
        pixel = library.NewPixelWand()
        library.DrawGetTextUnderColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @text_under_color.setter
    def text_under_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetTextUnderColor(self.resource, color.resource)

    @property
    def gravity(self):
        gravity_index = library.DrawGetGravity(self.resource)
        if not gravity_index:
            self.raise_exception()
        return TEXT_GRAVITY_TYPES[gravity_index]

    @gravity.setter
    def gravity(self, value):
        if (not isinstance(value, basestring) or
            value not in TEXT_GRAVITY_TYPES):
            raise TypeError('gravity value must be a string from ' +
                            'TEXT_GRAVITY_TYPES, not ' + repr(value))
        library.DrawSetGravity(self.resource, TEXT_GRAVITY_TYPES.index(value))


    def clear(self):
        library.ClearDrawingWand(self.resource)

    def draw(self, image):
        res = library.MagickDrawImage(image.wand, self.resource)
        if not res:
            self.raise_exception()

    def line(self, start, end):
        if not isinstance(start, tuple) or len(start) != 2:
            raise TypeError('start must be a 2-dimensional tuple')
        if not isinstance(end, tuple) or len(end) != 2:
            raise TypeError('end must be a 2-dimensional tuple')
        library.DrawLine(self.resource, start[0], start[1], end[0], end[1])

    def text(self, x, y, body):
        if not isinstance(x, numbers.Integral) or x < 0:
            raise TypeError('x must be a natural number, not ' + repr(x))
        if not isinstance(y, numbers.Integral) or y < 0:
            raise TypeError('y must be a natural number, not ' + repr(x))
        if not isinstance(body, basestring) or len(body) < 1:
            raise TypeError('body must be a string, not ' + repr(body))
        if self.text_encoding:
            body = body.encode(self.text_encoding)
        body_p = ctypes.create_string_buffer(body)
        library.DrawAnnotation(
            self.resource, x, y,
            ctypes.cast(body_p,ctypes.POINTER(ctypes.c_ubyte))
        )
