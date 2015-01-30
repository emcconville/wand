import itertools

from pytest import fixture, mark, raises, skip

from wand.image import Image
from wand.color import Color
from wand.compat import nested
from wand.api import library
from wand.drawing import Drawing
from wand.exceptions import WandLibraryVersionError


@fixture
def fx_wand(request):
    wand = Drawing()
    request.addfinalizer(wand.destroy)
    return wand


def test_is_drawing_wand(fx_wand):
    assert library.IsDrawingWand(fx_wand.resource)


def test_set_get_clip_path(fx_wand):
    fx_wand.clip_path = 'M10,10 15,15 10,15 Z'
    assert fx_wand.clip_path == 'M10,10 15,15 10,15 Z'

def test_set_get_clip_rule(fx_wand):
    fx_wand.clip_rule = 'evenodd'
    assert fx_wand.clip_rule == 'evenodd'

def test_set_get_clip_units(fx_wand):
    fx_wand.clip_units = 'object_bounding_box'
    assert fx_wand.clip_units == 'object_bounding_box'

def test_set_get_font(fx_wand, fx_asset):
    fx_wand.font = str(fx_asset.join('League_Gothic.otf'))
    assert fx_wand.font == str(fx_asset.join('League_Gothic.otf'))


def test_set_get_font_size(fx_wand):
    fx_wand.font_size = 22.2
    assert fx_wand.font_size == 22.2


def test_set_get_fill_color(fx_wand):
    with Color('#333333') as black:
        fx_wand.fill_color = black
    assert fx_wand.fill_color == Color('#333333')

def test_set_get_fill_color_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.fill_color = "green"

def test_set_get_fill_opacity(fx_wand):
    fx_wand.fill_opacity = 1.0;
    assert fx_wand.fill_opacity == 1.0

def test_set_get_fill_opacity_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.fill_opacity = "1.5";

def test_set_get_fill_rule(fx_wand):
    valid = 'evenodd'
    notvalid = 'error'
    invalid = (1,2)
    fx_wand.fill_rule = valid
    assert fx_wand.fill_rule == valid
    with raises(ValueError):
        fx_wand.fill_rule = notvalid
    with raises(TypeError):
        fx_wand.fill_rule = invalid
    fx_wand.fill_rule = 'undefined' # reset

def test_set_get_stroke_antialias(fx_wand):
    fx_wand.stroke_antialias = False
    assert fx_wand.stroke_antialias == False

def test_set_get_stroke_color(fx_wand):
    with Color('#333333') as black:
        fx_wand.stroke_color = black
    assert fx_wand.stroke_color == Color('#333333')

def test_set_get_stroke_color_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_color = '#333333'

def test_set_get_stroke_dash_array(fx_wand):
    dash_array = [2, 1, 4, 1]
    fx_wand.stroke_dash_array = dash_array
    assert fx_wand.stroke_dash_array == dash_array

def test_set_get_stroke_dash_offset(fx_wand):
    fx_wand.stroke_dash_offset = 0.5
    assert fx_wand.stroke_dash_offset == 0.5

def test_set_get_stroke_line_cap(fx_wand):
    fx_wand.stroke_line_cap = 'round'
    assert fx_wand.stroke_line_cap == 'round'

def test_set_get_stroke_line_cap_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_line_cap = 0x74321870
    with raises(ValueError):
        fx_wand.stroke_line_cap = 'apples'

def test_set_get_stroke_line_join(fx_wand):
    fx_wand.stroke_line_join = 'miter'
    assert fx_wand.stroke_line_join == 'miter'

def test_set_get_stroke_line_join_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_line_join = 0x74321870
    with raises(ValueError):
        fx_wand.stroke_line_join = 'apples'

def test_set_get_stroke_miter_limit(fx_wand):
    fx_wand.stroke_miter_limit = 5
    assert fx_wand.stroke_miter_limit == 5

def test_set_get_stroke_miter_limit_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_miter_limit = "5"

def test_set_get_stroke_opacity(fx_wand):
    fx_wand.stroke_opacity = 1.0
    assert fx_wand.stroke_opacity == 1.0

def test_set_get_stroke_opacity_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_opacity = "1.0"

def test_set_get_stroke_width(fx_wand):
    fx_wand.stroke_width = 5
    assert fx_wand.stroke_width == 5

def test_set_get_stroke_width_user_error(fx_wand):
    with raises(TypeError):
        fx_wand.stroke_width = '0.1234'
    with raises(ValueError):
        fx_wand.stroke_width = -1.5

def test_set_get_text_alignment(fx_wand):
    fx_wand.text_alignment = 'center'
    assert fx_wand.text_alignment == 'center'


def set_get_text_antialias(fx_wand):
    fx_wand.text_antialias = True
    assert fx_wand.text_antialias is True


def test_set_get_text_decoration(fx_wand):
    fx_wand.text_decoration = 'underline'
    assert fx_wand.text_decoration == 'underline'

def test_set_get_text_direction(fx_wand):
    try:
        fx_wand.text_direction = 'right_to_left'
        assert fx_wand.text_direction == 'right_to_left'
    except WandLibraryVersionError:
        skip("DrawGetTextDirection not supported by installed drawing library")

def test_set_get_text_encoding(fx_wand):
    fx_wand.text_encoding = 'UTF-8'
    assert fx_wand.text_encoding == 'UTF-8'


def test_set_get_text_interline_spacing(fx_wand):
    fx_wand.text_interline_spacing = 10.11
    assert fx_wand.text_interline_spacing == 10.11


def test_set_get_text_interword_spacing(fx_wand):
    fx_wand.text_interword_spacing = 5.55
    assert fx_wand.text_interword_spacing == 5.55


def test_set_get_text_kerning(fx_wand):
    fx_wand.text_kerning = 10.22
    assert fx_wand.text_kerning == 10.22


def test_set_get_text_under_color(fx_wand):
    with Color('#333333') as black:
        fx_wand.text_under_color = black
    assert fx_wand.text_under_color == Color('#333333')

def test_set_get_vector_graphics(fx_wand):
    fx_wand.stroke_width = 7
    xml = fx_wand.vector_graphics
    assert xml.index("<stroke-width>7</stroke-width>") > 0
    fx_wand.vector_graphics = ('<drawing-wand><stroke-width>'
                               '8</stroke-width></drawing-wand>')
    xml = fx_wand.vector_graphics
    assert xml.index("<stroke-width>8</stroke-width>") > 0


def test_set_get_gravity(fx_wand):
    fx_wand.gravity = 'center'
    assert fx_wand.gravity == 'center'


def test_clone_drawing_wand(fx_wand):
    fx_wand.text_kerning = 10.22
    funcs = (lambda img: Drawing(drawing=fx_wand),
             lambda img: fx_wand.clone())
    for func in funcs:
        with func(fx_wand) as cloned:
            assert fx_wand.resource is not cloned.resource
            assert fx_wand.text_kerning == cloned.text_kerning


def test_clear_drawing_wand(fx_wand):
    fx_wand.text_kerning = 10.22
    assert fx_wand.text_kerning == 10.22
    fx_wand.clear()
    assert fx_wand.text_kerning == 0

def test_draw_arc(fx_asset):
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#000')) as (white, red, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = red
                draw.stroke_color = black
                draw.arc((10, 10), # Start
                         (40, 40), # End
                         (-90, 90)) # Degree
                draw.draw(img)
                assert img[20,25] == white
                assert img[30,25] == red
                assert img[40,25] == black

def test_draw_circle(fx_asset):
    with nested(Color('#fff'),
                Color('#000')) as (white, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = black
                draw.circle((25, 25), # Origin
                            (40, 40)) # Perimeter
                draw.draw(img)
                assert img[5,5] == img[45,45] == white
                assert img[25,25] == black

def test_draw_comment():
    comment = 'pikachu\'s\ ghost'
    with nested(Image(width=1, height=1), Drawing()) as (img, draw):
        draw.comment(comment)
        draw(img)
        blob = img.make_blob(format="svg")
        assert blob.index(comment) > 0

def test_draw_color():
    with nested(Color('#fff'),
                Color('#000')) as (white, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = black
                draw.color(25,25,'floodfill')
                draw.draw(img)
                assert img[25,25] == black

def test_draw_color_user_error():
    with Drawing() as draw:
        with raises(TypeError):
            draw.color()
        with raises(TypeError):
            draw.color(1, 2, 4)
        with raises(ValueError):
            draw.color(1, 2, 'apples')

def test_draw_ellipse(fx_wand):
    gray, red = Color('#ccc'), Color('#f00')
    with Image(width=50, height=50, background=gray) as img:
        with Drawing() as draw:
            draw.fill_color = red
            draw.ellipse((25,25), # origin
                         (20,10)) # radius
            draw.draw(img)
            assert img[25,10] == gray
            assert img[45,25] == red

def test_draw_line(fx_wand):
    gray = Color('#ccc')
    with Image(width=10, height=10, background=gray) as img:
        with Color('#333333') as black:
            fx_wand.fill_color = black
        fx_wand.line((5,5), (7,5))
        fx_wand.draw(img)
        assert img[4,5] == Color('#ccc')
        assert img[5,5] == Color('#333333')
        assert img[6,5] == Color('#333333')
        assert img[7,5] == Color('#333333')
        assert img[8,5] == Color('#ccc')

def test_draw_matte():
    with nested(Color('#fff'),
                Color('transparent')) as (white, transparent):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_opacity = 0
                draw.matte(25,25,'floodfill')
                draw.draw(img)
                assert img[25,25] == transparent

def test_draw_matte_user_error():
    with Drawing() as draw:
        with raises(TypeError):
            draw.matte()
        with raises(TypeError):
            draw.matte(1, 2, 4)
        with raises(ValueError):
            draw.matte(1, 2, 'apples')

def test_draw_point():
    with nested(Color('#fff'), Color('#000')) as (white, black):
        with Image(width=5, height=5, background=white) as img:
            with Drawing() as draw:
                draw.stroke_color = black
                draw.point(2,2)
                draw.draw(img)
                assert img[2,2] == black

def test_draw_polygon(fx_wand):
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw.polygon([(10,10),
                              (40,25),
                              (10,40)])
                draw.draw(img)
                assert img[10,25] == red
                assert img[25,25] == blue
                assert img[35,15] == img[35,35] == white

def test_draw_polyline(fx_wand):
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw.polyline([(10,10),
                              (40,25),
                              (10,40)])
                draw.draw(img)
                assert img[10,25] == img[25,25] == blue
                assert img[35,15] == img[35,35] == white

def test_draw_push_pop():
    with Drawing() as draw:
        draw.stroke_width = 2
        draw.push()
        draw.stroke_width = 3
        assert 3 == draw.stroke_width
        draw.pop()
        assert 2 == draw.stroke_width

def test_draw_bezier(fx_wand):
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw.bezier([(10,10),
                             (10,40),
                             (40,10),
                             (40,40)])
                draw.draw(img)
                assert img[10,10] == img[25,25] == img[40,40] == red
                assert img[34,32] == img[15,18] == blue
                assert img[34,38] == img[15,12] == white

def test_path_curve():
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw = (draw.path_start()
                        .path_move(to=(0,25), relative=True)
                        .path_curve(to=(25,25), controls=((0, 0), (25, 0)))
                        .path_curve(to=(25,0), controls=((0, 25), (25, 25)), relative=True)
                        .path_finish())
                draw.draw(img)
                assert img[25,25] == red
                assert img[35,35] == img[35,35] == blue
                assert img[35,15] == img[15,35] == white

def test_path_curve_user_error():
    with Drawing() as draw:
        with raises(TypeError):
            draw.path_curve(to=(5,7))
        with raises(TypeError):
            draw.path_curve(controls=(5,7))

def test_path_curve_to_quadratic_bezier():
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw = (draw.path_start()
                        .path_move(to=(0, 25), relative=True)
                        .path_curve_to_quadratic_bezier(to=(50, 25), control=(25, 50))
                        .path_curve_to_quadratic_bezier(to=(-20, -20), control=(-25, 0), relative=True)
                        .path_finish())
                draw.draw(img)
                assert img[30,5] == red

def test_path_curve_to_quadratic_bezier_smooth():
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw = (draw.path_start()
                        .path_curve_to_quadratic_bezier(to=(25, 25), control=(25, 25))
                        .path_curve_to_quadratic_bezier(to=( 10, -10), smooth=True, relative=True)
                        .path_curve_to_quadratic_bezier(to=( 35, 35), smooth=True, relative=False)
                        .path_curve_to_quadratic_bezier(to=(-10, -10), smooth=True, relative=True)
                        .path_finish())
                draw.draw(img)
                assert img[25,25] == red
                assert img[30,30] == blue

def test_path_curve_quadratic_bezier_user_error():
    with Drawing() as draw:
        with raises(TypeError):
            draw.path_curve_to_quadratic_bezier()
        with raises(TypeError):
            draw.path_curve_to_quadratic_bezier(to=(5,6))

def test_draw_path_elliptic_arc():
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw = (draw.path_start()
                        .path_move(to=(25,0))
                        .path_elliptic_arc(to=(25, 50), radius=(15, 25))
                        .path_elliptic_arc(to=(0,-15), radius=(5, 5), clockwise=False, relative=True)
                        .path_close()
                        .path_finish())
                draw.draw(img)
                assert img[25,35] == img[25,20] == red
                assert img[15,25] == img[30,45] == blue


def test_draw_path_elliptic_arc_user_error():
    with Drawing() as draw:
        with raises(TypeError):
            draw.path_elliptic_arc(to=(5,7))
        with raises(TypeError):
            draw.path_elliptic_arc(radius=(5,7))

def test_draw_path_line():
    with nested(Color('#fff'),
                Color('#f00'),
                Color('#00f')) as (white, red, blue):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.fill_color = blue
                draw.stroke_color = red
                draw = (draw.path_start()
                        .path_move(to=( 5, 5))
                        .path_move(to=( 5, 5), relative=True)
                        .path_line(to=(40, 40))
                        .path_line(to=( 0,-10), relative=True)
                        .path_horizontal_line(x=45)
                        .path_vertical_line(y=25)
                        .path_horizontal_line(x=-5, relative=True)
                        .path_vertical_line(y=-5, relative=True)
                        .path_finish())
                draw.draw(img)
                assert img[40,40] == img[40,30] == red
                assert img[45,25] == img[40,20] == red

def test_draw_path_line_user_error():
    with Drawing() as draw:
        # Test missing value
        with raises(TypeError):
            draw.path_line()
        with raises(TypeError):
            draw.path_horizontal_line()
        with raises(TypeError):
            draw.path_vertical_line()

def test_draw_move_user_error():
    with Drawing() as draw:
        # Test missing value
        with raises(TypeError):
            draw.path_move()

@mark.parametrize('kwargs', itertools.product(
    [('right', 40), ('width', 30)],
    [('bottom', 40), ('height', 30)]
))
def test_draw_rectangle(kwargs, display, fx_wand):
    with nested(Color('#fff'),
                Color('#333'),
                Color('#ccc')) as (white, black, gray):
        with Image(width=50, height=50, background=white) as img:
            fx_wand.stroke_width = 2
            fx_wand.fill_color = black
            fx_wand.stroke_color = gray
            fx_wand.rectangle(left=10, top=10, **dict(kwargs))
            fx_wand.draw(img)
            display(img)
            assert img[7, 7] == img[7, 42] == img[42, 7] == \
                   img[42, 42] == img[0, 0] == img[49, 49] == white
            assert img[12, 12] == img[12, 38] == img[38, 12] == \
                   img[38, 38] == black

def test_draw_rotate():
    with nested(Color('#fff'),
                Color('#000')) as (white, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.stroke_color = black
                draw.rotate(45)
                draw.line((3, 3), (35, 35))
                draw.draw(img)
                assert img[0,49] == black

def test_draw_skew():
    with nested(Color('#fff'),
                Color('#000')) as (white, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.stroke_color = black
                draw.skew(x=11,y=-24)
                draw.line((3, 3), (35, 35))
                draw.draw(img)
                assert img[43,42] == black

def test_draw_translate():
    with nested(Color('#fff'),
                Color('#000')) as (white, black):
        with Image(width=50, height=50, background=white) as img:
            with Drawing() as draw:
                draw.stroke_color = black
                draw.translate(x=5, y=5)
                draw.line((3, 3), (35, 35))
                draw.draw(img)
                assert img[40,40] == black

def test_draw_text(fx_asset):
    with Color('#fff') as white:
        with Image(width=100, height=100, background=white) as img:
            with Drawing() as draw:
                draw.font = str(fx_asset.join('League_Gothic.otf'))
                draw.font_size = 25
                with Color('#000') as bk:
                    draw.fill_color = bk
                draw.gravity = 'west'
                draw.text(0, 0, 'Hello Wand')
                draw.draw(img)
            assert (img[0, 0] == img[0, -1] == img[-1, 0] == img[-1, -1] ==
                    img[0, 39] == img[0, 57] == img[77, 39] == img[77, 57] ==
                    white)
            assert (img[2, 40] == img[2, 57] == img[75, 40] == img[75, 57] ==
                    Color('black'))


def test_get_font_metrics_test(fx_asset):
    with Image(width=144, height=192, background=Color('#fff')) as img:
        with Drawing() as draw:
            draw.font = str(fx_asset.join('League_Gothic.otf'))
            draw.font_size = 13
            nm1 = draw.get_font_metrics(img, 'asdf1234')
            nm2 = draw.get_font_metrics(img, 'asdf1234asdf1234')
            nm3 = draw.get_font_metrics(img, 'asdf1234\nasdf1234')
            assert nm1.character_width == draw.font_size
            assert nm1.text_width < nm2.text_width
            assert nm2.text_width <= nm3.text_width
            assert nm2.text_height == nm3.text_height
            m1 = draw.get_font_metrics(img, 'asdf1234', True)
            m2 = draw.get_font_metrics(img, 'asdf1234asdf1234', True)
            m3 = draw.get_font_metrics(img, 'asdf1234\nasdf1234', True)
            assert m1.character_width == draw.font_size
            assert m1.text_width < m2.text_width
            assert m2.text_width > m3.text_width
            assert m2.text_height < m3.text_height

def test_viewbox(fx_asset):
  with Drawing() as draw:
    with raises(TypeError):
      draw.viewbox(None, None, None, None)
    with raises(TypeError):
      draw.viewbox(10, None, None, None)
    with raises(TypeError):
      draw.viewbox(10, 10, None, None)
    with raises(TypeError):
      draw.viewbox(10, 10, 100, None)
    draw.viewbox(10, 10, 100, 100)

def test_regression_issue_163(tmpdir):
    """https://github.com/dahlia/wand/issues/163"""
    unicode_char = b'\xce\xa6'.decode('utf-8')
    with Drawing() as draw:
        with Image(width=500, height=500) as image:
            draw.font_size = 20
            draw.gravity = 'south_west'
            draw.text(0, 0, unicode_char)
            draw(image)
            image.save(filename=str(tmpdir.join('out.jpg')))
