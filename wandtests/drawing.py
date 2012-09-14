from attest import Tests, assert_hook, raises

from wand.color import Color
from wand.api import library, MagickPixelPacket
from wand.drawing import Drawing

from .image import asset
import ctypes

tests = Tests()

@tests.context
def drawing_wand():
    with Drawing() as wand:
        yield wand

@tests.test
def is_drawing_wand(wand):
    assert library.IsDrawingWand(wand.drawing_wand) == 1

@tests.test
def set_get_font(wand):
    wand.font = asset('League_Gothic.otf')
    assert wand.font == asset('League_Gothic.otf')

@tests.test
def set_get_font_size(wand):
    wand.font_size = 22.2
    assert wand.font_size == 22.2

@tests.test
def set_get_fill_color(wand):
    with Color('#333333') as black:
        wand.fill_color = black
    assert wand.fill_color == Color('#333333')

@tests.test
def set_get_text_alignment(wand):
    wand.text_alignment = 'center'
    assert wand.text_alignment == 'center'

@tests.test
def set_get_text_antialias(wand):
    wand.text_antialias = True
    assert wand.text_antialias is True

@tests.test
def set_get_text_decoration(wand):
    wand.text_decoration = 'underline'
    assert wand.text_decoration == 'underline'

@tests.test
def set_get_text_encoding(wand):
    wand.text_encoding = 'UTF-8'
    assert wand.text_encoding == 'UTF-8'

@tests.test
def set_get_text_interline_spacing(wand):
    wand.text_interline_spacing = 10.11
    assert wand.text_interline_spacing == 10.11

@tests.test
def set_get_text_interword_spacing(wand):
    wand.text_interword_spacing = 5.55
    assert wand.text_interword_spacing == 5.55

@tests.test
def set_get_text_kerning(wand):
    wand.text_kerning = 10.22
    assert wand.text_kerning == 10.22

@tests.test
def set_get_text_under_color(wand):
    with Color('#333333') as black:
        wand.text_under_color = black
    assert wand.text_under_color == Color('#333333')

@tests.test
def clone_drawing_wand(wand):
    wand.text_kerning = 10.22

    funcs = (lambda img: Drawing(drawing_wand=wand),
             lambda img: wand.clone())
    for func in funcs:
        with func(wand) as cloned:
            assert wand.drawing_wand is not cloned.drawing_wand
            assert wand.text_kerning == cloned.text_kerning

@tests.test
def clear_drawing_wand(wand):
    wand.text_kerning = 10.22
    assert wand.text_kerning == 10.22

    wand.clear()
    assert wand.text_kerning == 0

if __name__ == '__main__':
    tests.run()