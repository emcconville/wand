""":mod:`wand.drawing` --- Drawings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import ctypes
import numbers

from .api import library, MagickPixelPacket
from .color import Color
from .image import Image
from .resource import Resource

__all__ = ('TEXT_ALIGN_TYPES', 'TEXT_DECORATION_TYPES', 'TEXT_GRAVITY_TYPES',
           'Drawing')


TEXT_ALIGN_TYPES = 'undefined', 'left', 'center', 'right'
TEXT_DECORATION_TYPES = ('undefined', 'no', 'underline', 'overline',
                         'line_through')
TEXT_GRAVITY_TYPES = ('forget', 'north_west', 'north',
                      'north_east', 'west', 'center', 'east', 'south_west',
                      'south', 'south_east', 'static')


class Drawing(Resource):
    """Drawing"""

    c_is_resource = library.IsDrawingWand
    c_destroy_resource = library.DestroyDrawingWand
    c_get_exception = library.DrawGetException
    c_clear_exception = library.DrawClearException

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
            raise TypeError('expected a string, not ' + repr(font))
        library.DrawSetFont(self.resource, font)

    @property
    def font_size(self):
        return library.DrawGetFontSize(self.resource)

    @font_size.setter
    def font_size(self, size):
        if not isinstance(size, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(size))
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
        if not isinstance(align, basestring):
            raise TypeError('expected a string, not ' + repr(align))
        elif align not in TEXT_ALIGN_TYPES:
            raise ValueError('expected a string from TEXT_ALIGN_TYPES, not ' +
                             repr(align))
        library.DrawSetTextAlignment(self.resource,
                                     TEXT_ALIGN_TYPES.index(align))

    @property
    def text_antialias(self):
        result = library.DrawGetTextAntialias(self.resource)
        return bool(result)

    @text_antialias.setter
    def text_antialias(self, value):
        library.DrawSetTextAntialias(self.resource, bool(value))

    @property
    def text_decoration(self):
        text_decoration_index = library.DrawGetTextDecoration(self.resource)
        if not text_decoration_index:
            self.raise_exception()
        return TEXT_DECORATION_TYPES[text_decoration_index]

    @text_decoration.setter
    def text_decoration(self, decoration):
        if not isinstance(decoration, basestring):
            raise TypeError('expected a string, not ' + repr(decoration))
        elif decoration not in TEXT_DECORATION_TYPES:
            raise ValueError('expected a string from TEXT_DECORATION_TYPES, '
                             'not ' + repr(decoration))
        library.DrawSetTextDecoration(self.resource,
                                      TEXT_DECORATION_TYPES.index(decoration))

    @property
    def text_encoding(self):
        return library.DrawGetTextEncoding(self.resource)

    @text_encoding.setter
    def text_encoding(self, encoding):
        if encoding is not None and not isinstance(encoding, basestring):
            raise TypeError('expected a string, not ' + repr(encoding))
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
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterlineSpacing(self.resource, spacing)

    @property
    def text_interword_spacing(self):
        return library.DrawGetTextInterwordSpacing(self.resource)

    @text_interword_spacing.setter
    def text_interword_spacing(self, spacing):
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterwordSpacing(self.resource, spacing)

    @property
    def text_kerning(self):
        return library.DrawGetTextKerning(self.resource)

    @text_kerning.setter
    def text_kerning(self, kerning):
        if not isinstance(kerning, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(kerning))
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
            raise TypeError('expected a wand.color.Color object, not ' +
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
        if not isinstance(value, basestring):
            raise TypeError('expected a string, not ' + repr(value))
        elif value not in TEXT_GRAVITY_TYPES:
            raise ValueError('expected a string from TEXT_GRAVITY_TYPES, not '
                             + repr(value))
        library.DrawSetGravity(self.resource, TEXT_GRAVITY_TYPES.index(value))

    def clear(self):
        library.ClearDrawingWand(self.resource)

    def draw(self, image):
        if not isinstance(image, Image):
            raise TypeError('image must be a wand.image.Image instance, not '
                            + repr(image))
        res = library.MagickDrawImage(image.wand, self.resource)
        if not res:
            self.raise_exception()

    def line(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        library.DrawLine(self.resource, start_x, start_y, end_x, end_y)

    def text(self, x, y, body):
        if not isinstance(x, numbers.Integral) or x < 0:
            exc = ValueError if x < 0 else TypeError
            raise exc('x must be a natural number, not ' + repr(x))
        elif not isinstance(y, numbers.Integral) or y < 0:
            exc = ValueError if y < 0 else TypeError
            raise exc('y must be a natural number, not ' + repr(x))
        elif not isinstance(body, basestring):
            raise TypeError('body must be a string, not ' + repr(body))
        elif not body:
            raise ValueError('body string cannot be empty')
        if self.text_encoding:
            body = body.encode(self.text_encoding)
        body_p = ctypes.create_string_buffer(body)
        library.DrawAnnotation(
            self.resource, x, y,
            ctypes.cast(body_p,ctypes.POINTER(ctypes.c_ubyte))
        )
