from attest import Tests, assert_hook, raises

from wand.image import Image
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
def set_get_gravity(wand):
    wand.gravity = 'center'
    assert wand.gravity == 'center'

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

@tests.test
def draw_line(wand):
    gray = Color('#ccc')
    with Image(width=10, height=10, background=gray) as img:
        with Color('#333333') as black:
            wand.fill_color = black
        wand.line((5,5), (7,5))
        wand.draw(img)

        assert img[4,5] == Color('#ccc')
        assert img[5,5] == Color('#333333')
        assert img[6,5] == Color('#333333')
        assert img[7,5] == Color('#333333')
        assert img[8,5] == Color('#ccc')

@tests.test
def draw_text(wand):
    with Image(width=100, height=100, background=Color('#fff')) as img:
        with Drawing() as draw:
            draw.font = asset('League_Gothic.otf')
            draw.font_size = 25
            with Color('#000') as bk:
                draw.fill_color = bk
            draw.gravity = 'west'
            draw.text(0, 0, 'Hello Wand')
            draw.draw(img)

            assert img.signature ==\
            '54d1fc4825ef0bddebb5de88419f05351a8f137828cbae1f767fa4a2ca1bbab4'

if __name__ == '__main__':
    tests.run()