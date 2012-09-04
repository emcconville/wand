from attest import Tests, assert_hook, raises

from wand.color import Color
from wand.api import library, MagickPixelPacket

from .image import asset
import ctypes

tests = Tests()

def color_from_pixel(pixel):
    result_color = None
    size = ctypes.sizeof(MagickPixelPacket)
    buffer = ctypes.create_string_buffer(size)
    library.PixelGetMagickColor(pixel, buffer)
    return Color(raw=buffer)

@tests.context
def drawing_wand():
    wand = library.NewDrawingWand()
    try:
        yield wand
    finally:
        library.DestroyDrawingWand(wand)

@tests.test
def set_get_font(wand):
    library.DrawSetFont(wand, asset('League_Gothic.otf'))
    assert library.DrawGetFont(wand) == asset('League_Gothic.otf')

@tests.test
def set_get_font_size(wand):
    library.DrawSetFontSize(wand, 22.0)
    assert library.DrawGetFontSize(wand) == 22.0

@tests.test
def set_get_fill_color(wand):
    with Color('#333333') as black:
        library.DrawSetFillColor(wand, black.resource)

    pixel = library.NewPixelWand()
    library.DrawGetFillColor(wand, pixel)

    result_color = color_from_pixel(pixel)
    assert result_color == Color('#333333')

@tests.test
def set_get_text_alignment(wand):
    library.DrawSetTextAlignment(wand, 2)
    assert library.DrawGetTextAlignment(wand) == 2

@tests.test
def set_get_text_antialias(wand):
    library.DrawSetTextAntialias(wand, 1)
    assert library.DrawGetTextAntialias(wand) == 1

@tests.test
def set_get_text_decoration(wand):
    library.DrawSetTextDecoration(wand, 2)
    assert library.DrawGetTextDecoration(wand) == 2

@tests.test
def set_get_text_encoding(wand):
    library.DrawSetTextEncoding(wand, 'UTF-8')
    assert library.DrawGetTextEncoding(wand) == 'UTF-8'

@tests.test
def set_get_text_interline_spacing(wand):
    library.DrawSetTextInterlineSpacing(wand, 10.0)
    assert library.DrawGetTextInterlineSpacing(wand) == 10.0

@tests.test
def set_get_text_kerning(wand):
    library.DrawSetTextKerning(wand, 10.0)
    assert library.DrawGetTextKerning(wand) == 10.0

@tests.test
def set_get_text_under_color(wand):
    with Color('#333333') as black:
        library.DrawSetTextUnderColor(wand, black.resource)

    pixel = library.NewPixelWand()
    library.DrawGetTextUnderColor(wand, pixel)

    result_color = color_from_pixel(pixel)
    assert result_color == Color('#333333')

if __name__ == '__main__':
    tests.run()