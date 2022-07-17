# -*- coding: utf-8 -*-
#
# These test cover the Image methods that directly map to C-API function calls.
#
import io
import warnings

from pytest import mark, raises

from wand.color import Color
from wand.exceptions import (MissingDelegateError, OptionError,
                             WandRuntimeError)
from wand.image import Image
from wand.font import Font
from wand.version import MAGICK_VERSION_NUMBER


def test_adaptive_blur():
    with Image(filename='rose:') as img:
        was = img.signature
        img.adaptive_blur(8, 3)
        assert was != img.signature
        was = img.signature
        img.adaptive_blur(8, 3, channel='red')
        assert was != img.signature


def test_adaptive_resize():
    with Image(filename='rose:') as img:
        img.adaptive_resize(140, 92)
        assert 140, 92 == img.size
    with Image(filename='rose:') as img:
        _, h = img.size
        img.adaptive_resize(columns=140)
        assert img.size == (140, h)
        img.adaptive_resize(rows=92)
        assert img.size == (140, 92)


@mark.skipif(MAGICK_VERSION_NUMBER < 0x690,
             reason='-adaptive-sharpen fixed in version 6.8.9-2')
def test_adaptive_sharpen():
    with Image(width=100, height=100, pseudo='plasma:') as img:
        was = img.signature
        img.adaptive_sharpen(15, 3)
        assert was != img.signature
    with Image(width=100, height=100, pseudo='plasma:') as img:
        was = img.signature
        img.adaptive_sharpen(15, 3, channel='red')
        assert was != img.signature


def test_adaptive_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        offset = 0.1 * img.quantum_range
        img.adaptive_threshold(15, 15, offset)
        assert was != img.signature


def test_annotate(fx_asset):
    from wand.drawing import Drawing
    with Image(filename='rose:') as img:
        was = img.signature
        with Drawing() as ctx:
            ctx.font = str(fx_asset.join('League_Gothic.otf'))
            ctx.font_size = 32
            img.annotate('Hello', ctx, left=10, baseline=img.height-10)
        assert was != img.signature
    with raises(TypeError):
        with Image(filename='rose:') as img:
            img.annotate('Hello', 0xDEADBEEF)


def test_auto_gamma():
    with Image(filename='rose:') as img:
        was = img.signature
        img.auto_gamma()
        assert was != img.signature


def test_auto_level():
    with Image(filename='rose:') as img:
        was = img.signature
        img.auto_level()
        assert was != img.signature


def test_auto_orientation(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        # if orientation is undefined nothing should be changed
        before = img[100, 100]
        img.auto_orient()
        after = img[100, 100]
        assert before == after
        assert img.orientation == 'top_left'

    with Image(filename=str(fx_asset.join('orientationtest.jpg'))) as original:
        with original.clone() as img:
            # now we should get a flipped image
            assert img.orientation == 'bottom_left'
            before = img[100, 100]
            img.auto_orient()
            after = img[100, 100]
            assert before != after
            assert img.orientation == 'top_left'

            assert img[0, 0] == original[0, -1]
            assert img[0, -1] == original[0, 0]
            assert img[-1, 0] == original[-1, -1]
            assert img[-1, -1] == original[-1, 0]


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Auto Threshold requires ImageMagick-7.0.8.')
def test_auto_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        img.auto_threshold()
        assert was != img.signature


def test_black_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        img.black_threshold(Color('gray(50%)'))
        img.black_threshold('gray(50%)')
        assert was != img.signature
        with raises(TypeError):
            img.white_threshold(0xDEADBEEF)


def test_blue_shift():
    with Image(filename='rose:') as img:
        was = img.signature
        img.blue_shift(1.5)
        assert was != img.signature
        with raises(TypeError):
            img.blue_shift('NaN')


def test_blur(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.blur(30, 10)
        after = img[100, 100]
        assert before != after
    with Image(filename='rose:') as img:
        was = img.signature
        img.blur(30, 10, 'red')
        assert was != img.signature


def test_border(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        with Color('red') as color:
            img.border(color, 2, 5)
            assert (img[0, 0] == img[0, -1] == img[-1, 0] == img[-1, -1] ==
                    img[1, 4] == img[1, -5] == img[-2, 4] == img[-2, -5] ==
                    color)
            assert img[2, 5] == left_top
            assert img[2, -6] == left_bottom
            assert img[-3, 5] == right_top
            assert img[-3, -6] == right_bottom
    with Image(filename='rose:') as img:
        was = img.signature
        img.border('pink', 2, 5)
        assert was != img.signature


def test_brightness_contrast():
    with Image(filename='rose:') as img:
        was = img.signature
        img.brightness_contrast(-10.0, 50)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.brightness_contrast(-10.0, 50, 'red')
        assert was != img.signature


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason="Canny requires ImageMagick-7.0.8")
def test_canny(fx_asset):
    with Image(filename='rose:') as img:
        img.transform_colorspace('gray')
        was = img.signature
        img.canny(1, 3)
        assert was != img.signature


def test_caption(fx_asset):
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        font = Font(
            path=str(fx_asset.join('League_Gothic.otf')),
            color=Color("gold"),
            size=12,
            antialias=False
        )
        img.caption(
            'Test message',
            font=font,
            left=5, top=144,
            width=134, height=20,
            gravity='center'
        )


def test_caption_without_font():
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        with raises(TypeError):
            img.caption(
                'Test message',
                left=5, top=144,
                width=134, height=20,
                gravity='center'
            )


def test_charcoal():
    with Image(filename='rose:') as img:
        img.transform_colorspace('gray')
        was = img.signature
        img.charcoal(1, 2)
        assert was != img.signature


def test_chop():
    with Image(filename='rose:') as img:
        w, h = img.size
        img.chop(10, 10, 10, 10)
        assert img.width == (w - 10)
        assert img.height == (h - 10)


def test_chop_gravity():
    with Image(filename='rose:') as img:
        img.chop(width=10, height=10, gravity='south_east')
        assert (60, 36, 0, 0) == img.page
    with raises(ValueError):
        with Image(filename='rose:') as img:
            img.chop(x=10, gravity='north')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x709,
             reason="Clahe requires Imagemagick-7.0.9.")
def test_clahe():
    with Image(filename='rose:') as img:
        was = img.signature
        img.clahe(10, 10, 128, 3)
        assert was != img.signature


def test_clamp():
    with Image(filename='rose:') as img:
        assert img.clamp(channel='red')


def test_clut(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        with Image(img) as clut:
            clut.unique_colors()
            clut.flop()
            img.clut(clut)
            assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        with Image(img) as clut:
            clut.unique_colors()
            clut.flop()
            img.clut(clut, channel='red')
            assert was != img.signature
        with raises(TypeError):
            img.clut(0xDEADBEEF)


def test_coalesce(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img1:
        with Image(img1) as img2:
            img2.coalesce()
            assert img1.signature != img2.signature
            assert img1.size == img2.size


def test_color_decision_list():
    ccc = """
    <ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.2">
        <ColorCorrection id="cc03345">
            <SOPNode>
                <Slope> 0.9 1.2 0.5 </Slope>
                <Offset> 0.4 -0.5 0.6 </Offset>
                <Power> 1.0 0.8 1.5 </Power>
            </SOPNode>
            <SATNode>
                <Saturation> 0.85 </Saturation>
            </SATNode>
        </ColorCorrection>
    </ColorCorrectionCollection>
    """
    with Image(filename='rose:') as img:
        was = img.signature
        assert img.color_decision_list(ccc)
        assert was != img.signature
    with Image(filename='rose:') as img:
        assert img.cdl(ccc)


def test_color_map(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as img:
        img.type = 'palette'
        assert img[0, 0] == img.color_map(0)
        orange = Color('ORANGE')
        assert orange == img.color_map(0, orange)
        assert orange == img.color_map(0, 'ORANGE')
        assert orange == img.color_map(0)
        with raises(TypeError):
            img.color_map('NaN')
        with raises(TypeError):
            img.color_map(0, 0xDEADBEEF)
        with raises(ValueError):
            img.color_map(-1, orange)


def test_color_matrix():
    with Image(filename='rose:') as img:
        was = img.signature
        matrix = [
            [0.9, 0.0, 0.0],
            [0.0, 0.9, 0.0],
            [0.0, 0.0, 1.3]
        ]
        img.color_matrix(matrix)
        assert was != img.signature
        with raises(TypeError):
            img.color_matrix(0xDEADBEEF)
        with raises(TypeError):
            img.color_matrix((0, 0, 0, 0, 0))
        with raises(ValueError):
            img.color_matrix([[1, 0], [0, 1, 0]])


@mark.skipif(MAGICK_VERSION_NUMBER < 0x70A,
             reason='Color Threshold requires ImageMagick-7.0.10')
def test_color_threshold():
    with Image(width=100, height=100, pseudo='plasma:') as img:
        was = img.signature
        img.color_threshold(start='#000', stop='#ccc')
        assert was != img.signature


def test_colorize():
    with Image(filename='rose:') as img:
        was = img.signature
        img.colorize('blue', 'blue')
        assert was != img.signature
        with raises(TypeError):
            img.colorize(0xDEADBEEF, Color('blue'))
        with raises(TypeError):
            img.colorize(Color('blue'), 0xDEADBEEF)


def test_combine():
    with Image() as img:
        img.pseudo(width=1, height=1, pseudo='xc:grey100')
        img.pseudo(width=1, height=1, pseudo='xc:grey50')
        img.pseudo(width=1, height=1, pseudo='xc:grey0')
        assert len(img.sequence) == 3
        img.colorspace = 'rgb'
        img.combine()
        assert len(img.sequence) == 1
        pixel = img[0, 0]
        assert pixel.red > pixel.green > pixel.blue


def test_compare(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        with Image(filename=str(fx_asset.join('watermark_beach.jpg'))) as img:
            cmp_img, err = orig.compare(img, 'absolute',
                                        highlight=Color('orange'),
                                        lowlight=Color('gray90'))
            del cmp_img, err
            cmp_img, err = orig.compare(img, 'mean_absolute')
            del cmp_img, err
            cmp_img, err = orig.compare(img, 'root_mean_square')
            del cmp_img, err


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason="Complex requires ImageMagick-7.0.8.")
def test_complex():
    with Image(width=1, height=1, pseudo='xc:gray25') as a:
        with Image(width=1, height=1, pseudo='xc:gray50') as b:
            a.sequence.append(b)
            with a.complex('add') as img:
                assert 2 == len(img.sequence)


def test_composite(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        with orig.clone() as img:
            with Image(filename=str(fx_asset.join('watermark.png'))) as fg:
                img.composite(fg, 5, 10)
            # These pixels should not be changed:
            assert img[0, 0] == orig[0, 0]
            assert img[0, img.height - 1] == orig[0, orig.height - 1]
            assert img[img.width - 1, 0] == orig[orig.width - 1, 0]
            assert (img[img.width - 1, img.height - 1] ==
                    orig[orig.width - 1, img.height - 1])
            # These pixels should be the almost black:
            assert img[70, 100].red <= 1
            assert img[70, 100].green <= 1
            assert img[70, 100].blue <= 1
            assert img[130, 100].red <= 1
            assert img[130, 100].green <= 1
            assert img[130, 100].blue <= 1


def test_composite_arguments():
    with Image(filename='rose:') as img:
        base = img.signature
        left = base
        right = base
        with img.clone() as img1:
            with Image(width=img.width,
                       height=img.height,
                       pseudo='gradient:') as mask:
                img1.composite(mask, operator='blend')
            left = img1.signature
            assert base != left
        with img.clone() as img2:
            with Image(width=img.width,
                       height=img.height,
                       pseudo='gradient:') as mask:
                img2.composite(mask, operator='blend', arguments='7,7')
            right = img2.signature
            assert base != right
        assert left != right


def test_composite_gravity():
    green = Color('GREEN')
    red = Color('RED')
    with Image(width=100, height=100, background=green) as src:
        with Image(width=10, height=10, background=red) as dst:
            src.composite(dst, gravity='east')
        assert src[0, 50] == green
        assert src[99, 50] == red


def test_composite_channel(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        w, h = orig.size
        left = w // 4
        top = h // 4
        right = left * 3 - 1
        bottom = h // 4 * 3 - 1
        # List of (x, y) points that shouldn't be changed:
        outer_points = [
            (0, 0), (0, h - 1), (w - 1, 0), (w - 1, h - 1),
            (left, top - 1), (left - 1, top), (left - 1, top - 1),
            (right, top - 1), (right + 1, top), (right + 1, top - 1),
            (left, bottom + 1), (left - 1, bottom), (left - 1, bottom + 1),
            (right, bottom + 1), (right + 1, bottom), (right + 1, bottom + 1)
        ]
        if MAGICK_VERSION_NUMBER < 0x700:
            channel_name = 'red'
        else:
            channel_name = 'default_channels'
        with orig.clone() as img:
            with Color('black') as color:
                with Image(width=w // 2, height=h // 2,
                           background=color) as cimg:
                    img.composite_channel(channel_name, cimg, 'copy_red',
                                          w // 4, h // 4)
            # These points should be not changed:
            for point in outer_points:
                assert orig[point] == img[point]
            # Inner pixels should lost its red color (red becomes 0)
            for point in zip([left, right], [top, bottom]):
                with orig[point] as oc:
                    with img[point] as ic:
                        assert not ic.red
                        assert ic.green == oc.green
                        assert ic.blue == oc.blue


def test_composite_channel_arguments():
    channel_name = 'default_channels'
    with Image(filename='rose:') as img:
        base = img.signature
        left = base
        right = base
        with img.clone() as img1:
            with Image(width=img.width,
                       height=img.height,
                       pseudo='gradient:') as mask:
                img1.composite_channel(channel_name, mask, 'blend')
            left = img1.signature
            assert base != left
        with img.clone() as img2:
            with Image(width=img.width,
                       height=img.height,
                       pseudo='gradient:') as mask:
                img2.composite_channel(channel_name, mask, 'blend',
                                       arguments='7,7')
            right = img2.signature
            assert base != right
        assert left != right


def test_composite_channel_gravity():
    green = Color('GREEN')
    red = Color('RED')
    channel_name = 'default_channels'
    with Image(width=100, height=100, background=green) as src:
        with Image(width=10, height=10, background=red) as dst:
            src.composite_channel(channel_name, dst, 'over', gravity='east')
        assert src[0, 50] == green
        assert src[99, 50] == red


def test_concat():
    with Image(filename='rose:') as img:
        img.read(filename='rose:')
        with Image(img) as row:
            row.concat()
            assert row.size == (140, 46)
        with Image(img) as row:
            row.concat(True)
            assert row.size == (70, 92)


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Connected Components requires ImageMagick-7.0.8.')
def test_connected_components(fx_asset):
    with Image(filename=str(fx_asset.join('ccobject.png'))) as img:
        objects = img.connected_components()
        assert 2 == len(objects)


def test_contrast():
    with Image(filename='rose:') as img:
        was = img.signature
        img.contrast()
        assert was != img.signature


def test_contrast_stretch(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        img.contrast_stretch(0.15)
        with img[0, 10] as left_top:
            assert left_top.red_int8 == 255
        with img[0, 90] as left_bottom:
            assert left_bottom.red_int8 == 0
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        img.contrast_stretch(0.15, channel='red')
        with img[0, 10] as left_top:
            assert left_top.red_int8 == 255
        with img[0, 90] as left_bottom:
            assert left_bottom.red_int8 == 0


def test_contrast_stretch_user_error(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with raises(TypeError):
            img.contrast_stretch('NaN')
        with raises(TypeError):
            img.contrast_stretch(0.1, 'NaN')
        with raises(ValueError):
            img.contrast_stretch(0.1, channel='Not a channel')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x70A,
             reason='Convex Hull requires ImageMagick-7.0.10.')
def test_convex_hull(fx_asset):
    fpath = str(fx_asset.join('horizon_sunset_border2.jpg'))
    with Image(filename=fpath) as img:
        points = img.convex_hull(background='black')
        assert len(points) > 0


def test_crop(fx_asset):
    """Crops in-place."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(100, 100, 200, 200)
            assert cropped.size == (100, 100)
            with Color('#000') as black:
                for row in cropped:
                    for col in row:
                        assert col == black
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(100, 100, width=100, height=100)
            assert cropped.size == (100, 100)
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(left=150, bottom=150)
            assert cropped.size == (150, 150)
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(left=150, height=150)
            assert cropped.size == (150, 150)
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(-200, -200, -100, -100)
            assert cropped.size == (100, 100)
        with img.clone() as cropped:
            assert cropped.size == img.size
            cropped.crop(top=100, bottom=200)
            assert cropped.size == (300, 100)
        with img.clone() as cropped:
            width, height = img.size
            assert cropped.crop(left=0, top=0, width=width, height=height)
        with raises(ValueError):
            img.crop(0, 0, 500, 500)
        with raises(ValueError):
            img.crop(290, 290, 50, 50)
        with raises(ValueError):
            img.crop(290, 290, width=0, height=0)


def test_crop_error(fx_asset):
    """Crop errors."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with raises(TypeError):
            img.crop(right=1, width=2)
        with raises(TypeError):
            img.crop(bottom=1, height=2)


def test_crop_gif(tmpdir, fx_asset):
    with Image(filename=str(fx_asset.join('nocomments-delay-100.gif'))) as img:
        with img.clone() as d:
            assert d.size == (350, 197)
            for s in d.sequence:
                assert s.delay == 100
            d.crop(50, 50, 200, 150)
            d.save(filename=str(tmpdir.join('50_50_200_150.gif')))
        with Image(filename=str(tmpdir.join('50_50_200_150.gif'))) as d:
            assert len(d.sequence) == 46
            assert d.size == (150, 100)
            for s in d.sequence:
                assert s.delay == 100
    tmpdir.remove()


def test_crop_gravity(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        width = int(img.width / 3)
        height = int(img.height / 3)
        mid_width = int(width / 2)
        mid_height = int(height / 2)
        with img.clone() as center:
            center.crop(width=width, height=height, gravity='center')
            assert center[mid_width, mid_height] == Color('black')
        with img.clone() as northwest:
            northwest.crop(width=width, height=height, gravity='north_west')
            assert northwest[mid_width, mid_height] == Color('transparent')
        with img.clone() as southeast:
            southeast.crop(width=width, height=height, gravity='south_east')
            assert southeast[mid_width, mid_height] == Color('transparent')


def test_crop_gravity_error(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with raises(TypeError):
            img.crop(gravity='center')
        with raises(ValueError):
            img.crop(width=1, height=1, gravity='nowhere')


def test_crop_issue367(fx_asset):
    with Image(filename='rose:') as img:
        expected = img.size
        for gravity in ('north_west', 'north', 'north_east',
                        'west', 'center', 'east',
                        'south_west', 'south', 'south_east',):
            with Image(img) as actual:
                actual.crop(width=200, height=200, gravity=gravity)
                assert actual.size == expected


def test_cycle_color_map(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as img:
        img.type = 'palette'
        lime = img[0, 0]
        img.cycle_color_map(1)
        assert img[-1, 0] == lime
        img.cycle_color_map(-1)
        assert img[0, 0] == lime
        with raises(TypeError):
            img.cycle_color_map('NaN')


def test_deskew(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.deskew(0.4 * img.quantum_range)
        assert was != img.signature


def test_despeckle(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.despeckle()
        assert was != img.signature


@mark.slow
def test_distort(fx_asset):
    """Distort image."""
    with Image(filename=str(fx_asset.join('checks.png'))) as img:
        with Color('skyblue') as color:
            img.matte_color = color
            img.virtual_pixel = 'tile'
            img.distort('perspective', (0, 0, 20, 60, 90, 0, 70, 63,
                                        0, 90, 5, 83, 90, 90, 85, 88))
            assert img[img.width - 1, 0] == color


def test_distort_error(fx_asset):
    """Distort image with user error"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(ValueError):
            img.distort('mirror', (1,))
        with raises(TypeError):
            img.distort('perspective', 1)


def test_edge(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.edge(1.5)
        assert was != img.signature


def test_emboss(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.emboss(1.5, 0.25)
        assert was != img.signature


def test_encipher_decipher():
    with Image(filename='rose:') as img:
        img.depth = 8  # Safety
        was = img.signature
        img.encipher(passphrase='secret')
        assert was != img.signature
        img.decipher(passphrase='secret')
        assert was == img.signature


def test_enhance(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.enhance()
        assert was != img.signature


def test_equalize(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        img.equalize()
        # The top row should be nearly white, and the bottom nearly black.
        with img[0, 0] as light:
            assert light.red >= light.green >= light.blue >= 0.9
        with img[0, -1] as dark:
            assert dark.red <= dark.green <= dark.blue <= 0.1
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        was = img.signature
        img.equalize(channel='red')
        assert was != img.signature


def test_evaluate(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with img.clone() as percent_img:
            fifty_percent = percent_img.quantum_range * 0.5
            percent_img.evaluate('set', fifty_percent)
            with percent_img[10, 10] as gray:
                assert abs(gray.red - Color('gray50').red) < 0.01
        with img.clone() as literal_img:
            literal_img.evaluate('divide', 2, channel='red')
            with img[0, 0] as org_color:
                expected_color = (org_color.red_int8 * 0.5)
                with literal_img[0, 0] as actual_color:
                    assert abs(expected_color - actual_color.red_int8) < 1


def test_evaluate_user_error(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with raises(ValueError):
            img.evaluate(operator='Nothing')
        with raises(TypeError):
            img.evaluate(operator='set', value='NaN')
        with raises(ValueError):
            img.evaluate(operator='set', value=1.0, channel='Not a channel')


def test_export_pixels(fx_asset):
    with Image(filename=str(fx_asset.join('pixels.png'))) as img:
        img.depth = 8  # Not need, but want to match import.
        data = img.export_pixels(x=0, y=0, width=4, height=1,
                                 channel_map='RGBA', storage='char')
        expected = [0xFF, 0x00, 0x00, 0xFF,
                    0x00, 0xFF, 0x00, 0xFF,
                    0x00, 0x00, 0xFF, 0xFF,
                    0x00, 0x00, 0x00, 0x00]
        assert data == expected
        # Test Bad value
        with raises(TypeError):
            img.export_pixels(x='NaN')
        with raises(TypeError):
            img.export_pixels(y='NaN')
        with raises(TypeError):
            img.export_pixels(width='NaN')
        with raises(TypeError):
            img.export_pixels(height='NaN')
        with raises(TypeError):
            img.export_pixels(channel_map=0xDEADBEEF)
        with raises(ValueError):
            img.export_pixels(channel_map='NaN')
        with raises(ValueError):
            img.export_pixels(storage='NaN')


def test_export_pixels_issue_413():
    x = 10
    y = 10
    width = 20
    height = 10
    with Image(width=50, height=50, background=Color('GREEN')) as img:
        export = img.export_pixels(x=x, y=y,
                                   width=width, height=height)
        assert export
        export = img.export_pixels(x=x, y=y,
                                   width=width + x, height=height + y)
        assert export


def test_extent(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with img.clone() as extended:
            assert extended.size == img.size
            extended.extent(width=500)
            assert extended.width == 500
            assert extended.height == img.height

        with img.clone() as extended:
            assert extended.size == img.size
            extended.extent(height=500)
            assert extended.width == img.width
            assert extended.height == 500

        with raises(ValueError):
            img.extent(width=-10)

        with raises(ValueError):
            img.extent(height=-10)


def test_extent_gravity():
    with Image(filename='rose:') as img:
        img.extent(width=10, height=10, gravity='south_east')
        assert (10, 10, 0, 0) == img.page
        img.extent(width=100, height=100, gravity='center')
        assert (100, 100, 0, 0) == img.page
    with raises(ValueError):
        with Image(filename='rose:') as img:
            img.extent(x=10, gravity='north')


def test_features():
    with Image(filename='rose:') as img:
        cf = img.features(10)
        assert 'red' in cf
        assert 'contrast' in cf['red']
        assert 'horizontal' in cf['red']['contrast']


def test_flip(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        with img.clone() as flipped:
            flipped.flip()
            assert flipped[0, 0] == img[0, -1]
            assert flipped[0, -1] == img[0, 0]
            assert flipped[-1, 0] == img[-1, -1]
            assert flipped[-1, -1] == img[-1, 0]


def test_flop(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        with img.clone() as flopped:
            flopped.flop()
            assert flopped[0, 0] == img[-1, 0]
            assert flopped[-1, 0] == img[0, 0]
            assert flopped[0, -1] == img[-1, -1]
            assert flopped[-1, -1] == img[0, -1]


@mark.fft
def test_forward_fourier_transform():
    with Image(filename='rose:') as img:
        was = img.signature
        img.forward_fourier_transform()
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.fft()
        assert was != img.signature


def test_frame(fx_asset):
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.frame(width=4, height=4)
        assert img[0, 0] == img[-1, -1]
        assert img[-1, 0] == img[0, -1]
    with Color('green') as green:
        with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
            img.frame(matte=green, width=2, height=2)
            assert img[0, 0] == green
            assert img[-1, -1] == green
        with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
            img.frame(matte='green', width=2, height=2)
            assert img[0, 0] == green
            assert img[-1, -1] == green


def test_frame_error(fx_asset):
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            img.frame(width='one')
        with raises(TypeError):
            img.frame(height=3.5)
        with raises(TypeError):
            img.frame(inner_bevel=None)
        with raises(TypeError):
            img.frame(outer_bevel='large')


def test_function(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        img.function(function='polynomial',
                     arguments=(4, -4, 1))
        assert img[150, 150] == Color('white')
        img.function(function='sinusoid',
                     arguments=(1,),
                     channel='red')
        assert abs(img[150, 150].red - Color('#80FFFF').red) < 0.01


def test_function_error(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with raises(ValueError):
            img.function('bad function', 1)
        with raises(TypeError):
            img.function('sinusoid', 1)
        with raises(ValueError):
            img.function('sinusoid', (1,), channel='bad channel')


def test_fx(fx_asset):
    with Image(width=2, height=2, background=Color('black')) as xc1:
        # NavyBlue == #000080
        with xc1.fx('0.5019', channel='blue') as xc2:
            assert abs(xc2[0, 0].blue - Color('navy').blue) < 0.0001

    with Image(width=2, height=1, background=Color('white')) as xc1:
        with xc1.fx('0') as xc2:
            assert xc2[0, 0].red == 0


def test_fx_error(fx_asset):
    with Image() as empty_wand:
        with raises(WandRuntimeError):
            with empty_wand.fx('8') as _:
                pass
    with Image(filename='rose:') as xc:
        with raises(OptionError):
            with xc.fx('NULL'):
                pass
        with raises(TypeError):
            with xc.fx(('p[0,0]',)):
                pass
        with raises(TypeError):
            with xc.fx('p[0,0]', True):
                pass


def test_gamma(fx_asset):
    # Value under 1.0 is darker, and above 1.0 is lighter
    middle_point = 75, 50
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with img.clone() as lighter:
            lighter.gamma(1.5)
            assert img[middle_point].red < lighter[middle_point].red
        with img.clone() as darker:
            darker.gamma(0.5)
            assert img[middle_point].red > darker[middle_point].red


def test_gamma_channel(fx_asset):
    # Value under 1.0 is darker, and above 1.0 is lighter
    middle_point = 75, 50
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with img.clone() as lighter:
            lighter.gamma(1.5, channel='red')
            assert img[middle_point].red < lighter[middle_point].red
        with img.clone() as darker:
            darker.gamma(0.5, channel='red')
            assert img[middle_point].red > darker[middle_point].red


def test_gamma_user_error(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with raises(TypeError):
            img.gamma('NaN;')
        with raises(ValueError):
            img.gamma(0.0, 'no channel')


def test_gaussian_blur(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.gaussian_blur(30, 10)
        after = img[100, 100]
        assert before != after
        assert 0.84 <= after.red <= 0.851
        assert 0.74 <= after.green <= 0.75
        assert 0.655 <= after.blue < 0.67
    with Image(filename='rose:') as img:
        was = img.signature
        img.gaussian_blur(30, 10, channel='red')
        assert was != img.signature


def test_get_image_distortion(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        with Image(filename=str(fx_asset.join('watermark_beach.jpg'))) as img:
            err = orig.get_image_distortion(img, 'absolute')
            assert err >= 0.0


def test_hald_clut(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        with Image(filename='hald:3') as hald:
            hald.gamma(0.367)
            img.hald_clut(hald)
        assert was != img.signature
        was = img.signature
        with Image(filename='hald:3') as hald:
            hald.gamma(0.367)
            img.hald_clut(hald, channel='red')
        assert was != img.signature
        with raises(TypeError):
            img.hald_clut(0xDEADBEEF)


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Hough Lines requires ImageMagick-7.0.8.')
def test_hough_lines(fx_asset):
    with Image(filename=str(fx_asset.join('ccobject.png'))) as img:
        was = img.signature
        img.hough_lines(width=3, height=3)
        assert was != img.signature


def test_implode(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.implode(amount=1.0)
        assert was != img.signature


def test_import_pixels(fx_asset):
    data = [0xFF, 0x00, 0x00, 0xFF,
            0x00, 0xFF, 0x00, 0xFF,
            0x00, 0x00, 0xFF, 0xFF,
            0x00, 0x00, 0x00, 0x00]
    with Image(width=4, height=1, background=Color('BLACK')) as dst:
        dst.depth = 8  # For safety
        with Image(filename=str(fx_asset.join('pixels.png'))) as expected:
            expected.depth = 8  # For safety
            dst.import_pixels(x=0, y=0, width=4, height=1,
                              channel_map='RGBA', storage='char',
                              data=data)
            assert dst.signature == expected.signature
        with raises(TypeError):
            dst.import_pixels(x='NaN')
        with raises(TypeError):
            dst.import_pixels(y='NaN')
        with raises(TypeError):
            dst.import_pixels(width='NaN')
        with raises(TypeError):
            dst.import_pixels(height='NaN')
        with raises(TypeError):
            dst.import_pixels(channel_map=0xDEADBEEF)
        with raises(ValueError):
            dst.import_pixels(channel_map='NaN')
        with raises(ValueError):
            dst.import_pixels(storage='NaN')
        with raises(TypeError):
            dst.import_pixels(data=0xDEADBEEF)
        with raises(ValueError):
            dst.import_pixels(data=[0x00, 0xFF])


def test_import_pixels_issue_413():
    x = 10
    y = 10
    width = 20
    height = 10
    with Image(width=50, height=50, background=Color('GREEN')) as img:
        blank = [0xFF] * 600
        img.import_pixels(x=x, y=y,
                          width=width, height=height,
                          channel_map='RGB',
                          data=blank)
        assert img
        blank = [0xFF] * 1800
        img.import_pixels(x=x, y=y,
                          width=width + x, height=height + y,
                          channel_map='RGB',
                          data=blank)
        assert img


@mark.fft
def test_inverse_fourier_transform(fx_asset):
    with Image(filename=str(fx_asset.join('ccobject_magnitude.png'))) as a:
        was = a.signature
        with Image(filename=str(fx_asset.join('ccobject_phase.png'))) as b:
            a.inverse_fourier_transform(b)
        assert was != a.signature
    with Image(filename=str(fx_asset.join('ccobject_magnitude.png'))) as a:
        with Image(filename=str(fx_asset.join('ccobject_phase.png'))) as b:
            assert a.ift(b)
    with raises(TypeError):
        with Image(filename=str(fx_asset.join('ccobject_magnitude.png'))) as a:
            a.inverse_fourier_transform(0xDEADBEEF)


def test_iterator(fx_asset):
    with Image(filename=str(fx_asset.join('animation.gif'))) as img:
        length = img.iterator_length()
        assert length == 4
        img.iterator_reset()
        idx = img.iterator_get()
        assert idx == 0
        while img.iterator_next():
            pass
        idx = img.iterator_get()
        assert idx == 3
        img.iterator_first()
        idx = img.iterator_get()
        assert idx == 0
        img.iterator_last()
        while img.iterator_previous():
            pass
        idx = img.iterator_get()
        assert idx == 0
        img.iterator_set(2)
        idx = img.iterator_get()
        assert idx == 2


@mark.skipif(MAGICK_VERSION_NUMBER < 0x70B,
             reason='Kmeans requires ImageMagick-7.0.11')
def test_kmeans():
    with Image(filename='rose:') as img:
        was = img.signature
        img.kmeans(64)
        assert was != img.signature


def test_kurtosis_channel():
    with Image(filename='rose:') as img:
        r = img.kurtosis_channel('red')
        assert len(r) == 2
        with raises(ValueError):
            img.kurtosis_channel('unknown')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Kuwahara requires ImageMagick-7.0.8.')
def test_kuwahara():
    with Image(filename='rose:') as img:
        was = img.signature
        img.kuwahara(3.0)
        assert was != img.signature


def test_label(fx_asset):
    font_path = str(fx_asset.join('League_Gothic.otf'))
    with Image(filename='rose:') as img:
        was = img.signature
        img.label('a', left=0, top=0, font=Font(font_path, 12))
        now = img.signature
        assert now != was
        img.label('b', font=Font(font_path, 12), gravity='south')
        assert img.signature != now
    with raises(TypeError):
        with Image(filename='rose:') as img:
            img.label('x')


def test_level(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the levels to make this image entirely black
        img.level(black=0.99, white=1.0)
        with img[0, 0] as dark:
            assert dark.red_int8 <= dark.green_int8 <= dark.blue_int8 <= 0
        with img[0, -1] as dark:
            assert dark.red_int8 <= dark.green_int8 <= dark.blue_int8 <= 0
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the levels to make this image entirely white
        img.level(0, 0.01)
        with img[0, 0] as light:
            assert light.red_int8 >= light.green_int8 >= light.blue_int8 >= 255
        with img[0, -1] as light:
            assert light.red_int8 >= light.green_int8 >= light.blue_int8 >= 255
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the image's gamma to darken its midtones
        img.level(gamma=0.5)
        with img[0, len(img) // 2] as light:
            assert light.red_int8 <= light.green_int8 <= light.blue_int8 <= 65
            assert light.red_int8 >= light.green_int8 >= light.blue_int8 >= 60
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the image's gamma to lighten its midtones
        img.level(0, 1, 2.5)
        with img[0, len(img) // 2] as light:
            assert light.red_int8 <= light.green_int8 <= light.blue_int8 <= 195
            assert light.red_int8 >= light.green_int8 >= light.blue_int8 >= 190


def test_level_channel(fx_asset):
    for chan in ('red', 'green', 'blue'):
        c = chan + '_int8'
        with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
            # Adjust each channel level to make it entirely black
            img.level(0.99, 1.0, channel=chan)
            assert(getattr(img[0, 0], c) <= 0)
            assert(getattr(img[0, -1], c) <= 0)
        with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
            # Adjust each channel level to make it entirely white
            img.level(0.0, 0.01, channel=chan)
            assert(getattr(img[0, 0], c) >= 255)
            assert(getattr(img[0, -1], c) >= 255)
        with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
            # Adjust each channel's gamma to darken its midtones
            img.level(gamma=0.5, channel=chan)
            with img[0, len(img) // 2] as light:
                assert(getattr(light, c) <= 65)
                assert(getattr(light, c) >= 60)
        with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
            # Adjust each channel's gamma to lighten its midtones
            img.level(0, 1, 2.5, chan)
            with img[0, len(img) // 2] as light:
                assert(getattr(light, c) >= 190)
                assert(getattr(light, c) <= 195)


def test_level_user_error(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with raises(TypeError):
            img.level(black='NaN')
        with raises(TypeError):
            img.level(white='NaN')
        with raises(TypeError):
            img.level(gamma='NaN')
        with raises(ValueError):
            img.level(channel='404')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Levelize requires ImageMagick-7.0.8.')
def test_levelize():
    with Image(filename='rose:') as img:
        was = img.signature
        img.levelize(3.0)
        assert was != img.signature


def test_linear_stretch(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        img.linear_stretch(black_point=0.15,
                           white_point=0.15)
        with img[0, 10] as left_top:
            assert left_top.red_int8 == 255
        with img[0, 90] as left_bottom:
            assert left_bottom.red_int8 == 0


def test_linear_stretch_user_error(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        with raises(TypeError):
            img.linear_stretch(white_point='NaN',
                               black_point=0.5)
        with raises(TypeError):
            img.linear_stretch(white_point=0.5,
                               black_point='NaN')


def test_liquid_rescale(fx_asset):
    def assert_equal_except_alpha(a, b):
        with a:
            with b:
                assert (a.red == b.red and
                        a.green == b.green and
                        a.blue == b.blue)
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        with orig.clone() as img:
            try:
                img.liquid_rescale(600, 600)
            except MissingDelegateError:
                warnings.warn('skip liquid_rescale test; has no LQR delegate')
            else:
                assert img.size == (600, 600)
                for x in 0, -1:
                    for y in 0, -1:
                        assert_equal_except_alpha(img[x, y], img[x, y])


@mark.skipif(MAGICK_VERSION_NUMBER < 0x693,
             reason='Local Contrast not supported.')
def test_local_contrast():
    with Image(filename='rose:') as img:
        was = img.signature
        img.local_contrast()
        assert was != img.signature


def test_mean_channel():
    with Image(filename='rose:') as img:
        r = img.mean_channel('red')
        assert len(r) == 2
        with raises(ValueError):
            img.mean_channel('unknown')


def test_magnify():
    with Image(filename='rose:') as img:
        expected = img.width * 2
        img.magnify()
        assert expected == img.width


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Mean Shift requires ImageMagick-7.0.8.')
def test_mean_shift():
    with Image(filename='rose:') as img:
        was = img.signature
        img.mean_shift(width=5, height=5)
        assert was != img.signature


def test_merge_layers(fx_asset):
    for method in ['merge', 'flatten', 'mosaic']:
        with Image(filename=str(fx_asset.join('cmyk.jpg'))) as img1:
            orig_size = img1.size
            with Image(filename=str(fx_asset.join('cmyk.jpg'))) as img2:
                img1.sequence.append(img2)
                assert len(img1.sequence) == 2
                img1.merge_layers(method)
                assert len(img1.sequence) == 1
                assert img1.size == orig_size


def test_merge_layers_bad_method(fx_asset):
    with Image(filename=str(fx_asset.join('cmyk.jpg'))) as img:
        for method in ('', 'mosaic' 'junk'):
            with raises(ValueError):
                img.merge_layers(method)
        with raises(TypeError):
            img.merge_layers(None)


def test_merge_layers_method_flatten(fx_asset):
    with Image(width=16, height=16) as img1:
        img1.background_color = Color('black')
        img1.alpha_channel = False
        with Image(width=32, height=32) as img2:
            img2.background_color = Color('white')
            img2.alpha_channel = False
            img2.transform(crop='16x16+8+8')
            img1.sequence.append(img2)
            img1.merge_layers('flatten')
            assert img1.size == (16, 16)


def test_merge_layers_method_merge(fx_asset):
    with Image(width=16, height=16) as img1:
        img1.background_color = Color('black')
        img1.alpha_channel = False
        with Image(width=32, height=32) as img2:
            img2.background_color = Color('white')
            img2.alpha_channel = False
            img2.transform(crop='16x16+8+8')
            img1.sequence.append(img2)
            img1.merge_layers('merge')
            assert img1.size == (24, 24)


def test_merge_layers_method_merge_neg_offset(fx_asset):
    with Image(width=16, height=16) as img1:
        img1.background_color = Color('black')
        img1.alpha_channel = False
        with Image(width=16, height=16) as img2:
            img2.background_color = Color('white')
            img2.alpha_channel = False
            img2.page = (16, 16, -8, -8)
            img1.sequence.append(img2)
            img1.merge_layers('merge')
            assert img1.size == (24, 24)


def test_merge_layers_method_mosaic(fx_asset):
    with Image(width=16, height=16) as img1:
        img1.background_color = Color('black')
        img1.alpha_channel = False
        with Image(width=32, height=32) as img2:
            img2.background_color = Color('white')
            img2.alpha_channel = False
            img2.transform(crop='16x16+8+8')
            img1.sequence.append(img2)
            img1.merge_layers('mosaic')
            assert img1.size == (24, 24)


def test_merge_layers_method_mosaic_neg_offset(fx_asset):
    with Image(width=16, height=16) as img1:
        img1.background_color = Color('black')
        img1.alpha_channel = False
        with Image(width=16, height=16) as img2:
            img2.background_color = Color('white')
            img2.alpha_channel = False
            img2.page = (16, 16, -8, -8)
            img1.sequence.append(img2)
            img1.merge_layers('mosaic')
            assert img1.size == (16, 16)


@mark.skipif(MAGICK_VERSION_NUMBER < 0x70A,
             reason='Minimum Bounding Box requires ImageMagick-7.0.10.')
def test_minimum_bounding_box():
    with Image(filename='wizard:') as img:
        img.fuzz = 0.1 * img.quantum_range
        img.background_color = 'white'
        mbr = img.minimum_bounding_box()
        assert img.width > mbr.get('width', img.width)
        assert img.height > mbr.get('height', img.height)


def test_mode(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.mode(5)
        assert was != img.signature


def test_modulate(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.modulate(120, 120, 120)
        after = img[100, 100]
        assert before != after


def test_morphology_builtin(fx_asset):
    known = []
    args = (('erode', 'ring'),
            ('dilate', 'disk:5'),
            ('open', 'octagon'),
            ('smooth', 'rectangle:0x-1'),
            ('thinning', 'edges'),
            ('distance', 'euclidean:4,10!'),
            ('thicken', 'unity:x5'),
            ('close', 'manhattan:20x25%'),
            ('hit_and_miss', 'chebyshev:5.0'))
    for arg in args:
        with Image(filename='rose:') as img:
            img.morphology(*arg)
            assert img.signature not in known
            known.append(img.signature)
    with Image(filename='rose:') as img:
        with raises(TypeError):
            img.morphology(method=0xDEADBEEF)
        with raises(TypeError):
            img.morphology(method='close',
                           kernel=0xDEADBEEF)
        with raises(TypeError):
            img.morphology(method='close',
                           kernel='1:0',
                           iterations='p')


def test_morphology_user_defined(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.morphology(method='dilate',
                       kernel='3x3: 0.3,0.6,0.3 0.6,1.0,0.6 0.3,0.6,0.3')
        assert was != img.signature
        was = img.signature
        img.morphology(method='dilate',
                       kernel='3x3: 0.3,0.6,0.3 0.6,1.0,0.6 0.3,0.6,0.3',
                       channel='red')
        assert was != img.signature
        with raises(ValueError):
            img.morphology(method='dilate',
                           kernel='junk:0')


def test_motion_blur():
    with Image(filename='rose:') as img:
        was = img.signature
        img.motion_blur(8, 6, 45)
        result = img.signature
        assert was != result
        was = result
        img.motion_blur(8, 6, -45, channel='blue')
        assert was != img.signature


def test_negate_default(fx_asset):
    def test(c1, c2):
        assert (c1.red_int8 + c2.red_int8 == 255 and
                c1.green_int8 + c2.green_int8 == 255 and
                c1.blue_int8 + c2.blue_int8 == 255)
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        img.negate()
        test(left_top, img[0, 0])
        test(left_bottom, img[0, -1])
        test(right_top, img[-1, 0])
        test(right_bottom, img[-1, -1])
        assert img.negate(False, 'red')
        with raises(ValueError):
            img.negate(True, 'unknown')


def test_noise():
    with Image(filename='rose:') as img:
        was = img.signature
        img.noise('gaussian', 1.0)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.noise('gaussian', 1.0, channel='red')
        assert was != img.signature


def test_normalize(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        img.normalize()
        assert img[0, 0] != left_top
        assert img[0, -1] != left_bottom
        assert img[-1, 0] != right_top
        assert img[-1, -1] != right_bottom
        with img[0, 0] as left_top:
            assert left_top.red == left_top.green == left_top.blue == 1
        with img[-1, -1] as right_bottom:
            assert (right_bottom.red == right_bottom.green ==
                    right_bottom.blue == 0)
        with raises(ValueError):
            img.normalize('unknown')


def test_normalize_channel(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        was = img.signature
        img.normalize('red')
        assert was != img.signature


def test_oil_paint():
    with Image(filename='rose:') as img:
        was = img.signature
        img.oil_paint(5)
        assert was != img.signature


def test_opaque_paint():
    pink = Color('pink')
    white = Color('white')
    with Image(filename='WIZARD:') as img:
        img.opaque_paint(target=white, fill=pink,
                         fuzz=0.25*img.quantum_range)
        assert img[0, 0] == pink
    with Image(filename='WIZARD:') as img:
        img.opaque_paint(target='white', fill='pink',
                         fuzz=0.25*img.quantum_range, invert=True)
        assert img[0, 0] == white
    with Image(filename='WIZARD:') as img:
        was = img.signature
        img.opaque_paint(target='white', fill='pink',
                         fuzz=0.25*img.quantum_range, channel='red')
        assert was != img.signature


def test_optimize_layers(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img1:
        with Image(img1) as img2:
            img2.optimize_layers()
            assert img1.signature != img2.signature
            assert img1.size == img2.size


def test_optimize_transparency(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img1:
        with Image(img1) as img2:
            try:
                img2.optimize_transparency()
                assert img1.signature != img2.signature
                assert img1.size == img2.size
            except AttributeError as e:
                warnings.warn('MagickOptimizeImageTransparency not '
                              'present on system. ' + repr(e))


def test_ordered_dither():
    with Image(filename='rose:') as img:
        was = img.signature
        img.ordered_dither('o3x3')
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.ordered_dither('o3x3', channel='red')
        assert was != img.signature


def test_parse_meta_geometry():
    with Image(filename='rose:') as img:
        w, h, x, y = img.parse_meta_geometry('200%')
        assert (w, h, x, y) == (140, 92, 0, 0)
        with raises(ValueError):
            img.parse_meta_geometry('junk')


def test_percent_escape(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert 'sasha.jpg 204x247' == img.percent_escape('%f %wx%h')


def test_polaroid(fx_asset):
    # For testing polaroid method, we can't really identify if somethings
    # has changed correctly.
    with Image(filename='rose:') as img:
        img.polaroid()
    with Image(filename='rose:') as img:
        img.polaroid(caption='hello')
    with Image(filename='rose:') as img:
        font = Font(str(fx_asset.join('League_Gothic.otf')), 12,
                    Color('orange'), True, Color('pink'), 1)
        img.polaroid(caption='hello', font=font)
        with raises(TypeError):
            img.polaroid(caption='hello', font='League_Gothic.otf')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Polynomial requires ImageMagick-7.0.8.')
def test_polynomial():
    with Image(filename='rose:') as img:
        was = img.signature
        img.polynomial(arguments=(0.5, 1.0))
        assert was != img.signature


def test_posterize(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        was = img.signature
        img.posterize(levels=16, dither='no')
        assert was != img.signature
        with raises(TypeError):
            img.posterize(levels='16')
        with raises(ValueError):
            img.posterize(levels=16, dither='manhatten')


@mark.slow
def test_quantize(fx_asset):
    number_colors = 64
    with Image(width=100, height=100, pseudo='PLASMA:') as img:
        assert img.colors > number_colors

    with Image(width=100, height=100, pseudo='PLASMA:') as img:
        with raises(TypeError):
            img.quantize(str(number_colors), 'undefined', 0, True, True)

        with raises(TypeError):
            img.quantize(number_colors, 0, 0, True, True)

        with raises(TypeError):
            img.quantize(number_colors, 'undefined', 'depth', True, True)

        with raises(TypeError):
            img.quantize(number_colors, 'undefined', 0, 1, True)

        with raises(TypeError):
            img.quantize(number_colors, 'undefined', 0, True, 1)

        img.quantize(number_colors, 'undefined', 0, True, True)
        assert img.colors <= number_colors


def test_random_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        img.random_threshold(low=0.4, high=0.6)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.random_threshold(low=0.4, high=0.6, channel='red')
        assert was != img.signature


def test_range_channel():
    with Image(filename='rose:') as img:
        minima, maxima = img.range_channel('red')
        assert minima < maxima
        with raises(ValueError):
            img.range_channel('unknown')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Range Threshold requires ImageMagick-7.0.8.')
def test_range_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        img.range_threshold(20, 40, 60, 80)
        assert was != img.signature
        # Smoke test
        img.range_threshold(20)
        img.range_threshold(20, 40)
        img.range_threshold(20, 40, 60)


def test_region():
    with Image(filename='rose:') as src:
        w, h, x, y = src.page
        with src.region() as dst:
            assert (w, h) == dst.size
        with src.region(width=w//2, height=h//2, x=x//2, y=y//2) as dst:
            assert (w//2, h//2) == dst.size
    with Image(filename='rose:') as src:
        with src.region(width=10, height=10, gravity='south_east') as dst:
            assert (70, 46, 60, 36) == dst.page
            assert (10, 10) == dst.size
    with raises(ValueError):
        with Image(filename='rose:') as img:
            with img.region(x=10, gravity='center') as _:
                pass


def test_remap(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        trim_path = str(fx_asset.join('trim-color-test.png'))
        with Image(filename=trim_path) as palette:
            img.remap(palette)
        assert was != img.signature
        with raises(TypeError):
            img.remap(0xDEADBEEF)
        with raises(TypeError):
            img.remap(img, method=0xDEADBEEF)
        with raises(ValueError):
            img.remap(img, method='none')


@mark.parametrize(('density', 'expected_size'), [
    ((72, 72), (800, 600)),
    ((36, 36), (400, 300)),
    ((144, 144), (1600, 1200)),
    ((None, 36), (800, 300)),
    ((36, None), (400, 600)),
])
def test_resample(density, expected_size, fx_asset):
    """Resample (Adjust number of pixels at the given density) the image."""
    xr, yr = density
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        img.units = "pixelspercentimeter"
        assert img.resolution == (72, 72)
        img.resample(xr, yr)
        # Expect ``None`` values to match ImageMagick's default 72 resolution.
        if xr is None:
            xr = 72
        if yr is None:
            yr = 72
        assert img.resolution == (xr, yr)
        assert img.size == expected_size


def test_resample_errors(fx_asset):
    """Sampling errors."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            img.resample(x_res='100')
        with raises(TypeError):
            img.resample(y_res='100')
        with raises(ValueError):
            img.resample(x_res=0)
        with raises(ValueError):
            img.resample(y_res=0)
        with raises(ValueError):
            img.resample(x_res=-5)
        with raises(ValueError):
            img.resample(y_res=-5)


@mark.parametrize(('method'), [
    ('resize'),
    ('sample'),
])
def test_resize_and_sample(method, fx_asset):
    """Resizes/Samples the image."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with img.clone() as a:
            assert a.size == (402, 599)
            getattr(a, method)(100, 100)
            assert a.size == (100, 100)
        with img.clone() as b:
            assert b.size == (402, 599)
            getattr(b, method)(height=100)
            assert b.size == (402, 100)
        with img.clone() as c:
            assert c.size == (402, 599)
            getattr(c, method)(width=100)
            assert c.size == (100, 599)


@mark.parametrize(('method'), [
    ('resize'),
    ('sample'),
])
def test_resize_and_sample_errors(method, fx_asset):
    """Resizing/Sampling errors."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            getattr(img, method)(width='100')
        with raises(TypeError):
            getattr(img, method)(height='100')
        with raises(ValueError):
            getattr(img, method)(width=0)
        with raises(ValueError):
            getattr(img, method)(height=0)
        with raises(ValueError):
            getattr(img, method)(width=-5)
        with raises(ValueError):
            getattr(img, method)(height=-5)


@mark.slow
@mark.parametrize(('method'), [
    ('resize'),
    ('sample'),
])
def test_resize_and_sample_gif(method, tmpdir, fx_asset):
    with Image(filename=str(fx_asset.join('nocomments-delay-100.gif'))) as img:
        assert len(img.sequence) == 46
        with img.clone() as a:
            assert a.size == (350, 197)
            assert a.sequence[0].delay == 100
            for s in a.sequence:
                assert s.delay == 100
            getattr(a, method)(175, 98)
            a.save(filename=str(tmpdir.join('175_98.gif')))
        with Image(filename=str(tmpdir.join('175_98.gif'))) as a:
            assert len(a.sequence) == 46
            assert a.size == (175, 98)
            for s in a.sequence:
                assert s.delay == 100
        with img.clone() as b:
            assert b.size == (350, 197)
            for s in b.sequence:
                assert s.delay == 100
            getattr(b, method)(height=100)
            b.save(filename=str(tmpdir.join('350_100.gif')))
        with Image(filename=str(tmpdir.join('350_100.gif'))) as b:
            assert len(b.sequence) == 46
            assert b.size == (350, 100)
            for s in b.sequence:
                assert s.delay == 100
        with img.clone() as c:
            assert c.size == (350, 197)
            for s in c.sequence:
                assert s.delay == 100
            getattr(c, method)(width=100)
            c.save(filename=str(tmpdir.join('100_197.gif')))
        with Image(filename=str(tmpdir.join('100_197.gif'))) as c:
            assert len(c.sequence) == 46
            assert c.size == (100, 197)
            for s in c.sequence:
                assert s.delay == 100
    tmpdir.remove()


def test_roll():
    with Image(filename='rose:') as img:
        was = img.signature
        img.roll(x=-15, y=15)
        assert was != img.signature


@mark.slow
def test_rotate(fx_asset):
    """Rotates an image."""
    with Image(filename=str(fx_asset.join('rotatetest.gif'))) as img:
        assert 150 == img.width
        assert 100 == img.height
        with img.clone() as cloned:
            cloned.rotate(360)
            assert img.size == cloned.size
            with Color('black') as black:
                assert black == cloned[0, 50] == cloned[74, 50]
                assert black == cloned[0, 99] == cloned[74, 99]
            with Color('white') as white:
                assert white == cloned[75, 50] == cloned[75, 99]
        with img.clone() as cloned:
            cloned.rotate(90)
            assert 100 == cloned.width
            assert 150 == cloned.height
            with Color('black') as black:
                with Color('white') as white:
                    for y, row in enumerate(cloned):
                        for x, col in enumerate(row):
                            if y < 75 and x < 50:
                                assert col == black
                            else:
                                assert col == white
        with Color('red') as bg:
            with img.clone() as cloned:
                cloned.rotate(45, bg)
                assert 176 <= cloned.width == cloned.height <= 178
                assert bg == cloned[0, 0] == cloned[0, -1]
                assert bg == cloned[-1, 0] == cloned[-1, -1]
                with Color('black') as black:
                    # Until we implement antialiasing, we need to evaluate
                    # pixels next to corners.
                    assert black == cloned[5, 70]
                    assert black == cloned[36, 39]
                    assert black == cloned[85, 88]
                    assert black == cloned[53, 120]
        with Color('red') as bg:
            with img.clone() as cloned:
                cloned.rotate(45, 'red')
                assert 176 <= cloned.width == cloned.height <= 178
                assert bg == cloned[0, 0] == cloned[0, -1]
                assert bg == cloned[-1, 0] == cloned[-1, -1]
                with Color('black') as black:
                    # Until we implement antialiasing, we need to evaluate
                    # pixels next to corners.
                    assert black == cloned[5, 70]
                    assert black == cloned[36, 39]
                    assert black == cloned[85, 88]
                    assert black == cloned[53, 120]


@mark.slow
def test_rotate_gif(tmpdir, fx_asset):
    with Image(filename=str(fx_asset.join('nocomments-delay-100.gif'))) as img:
        for s in img.sequence:
            assert s.delay == 100
        with img.clone() as e:
            assert e.size == (350, 197)
            e.rotate(90)
            for s in e.sequence:
                assert s.delay == 100
            e.save(filename=str(tmpdir.join('rotate_90.gif')))
        with Image(filename=str(tmpdir.join('rotate_90.gif'))) as e:
            assert e.size == (197, 350)
            assert len(e.sequence) == 46
            for s in e.sequence:
                assert s.delay == 100
    tmpdir.remove()


def test_rotate_reset_coords(fx_asset):
    """Reset the coordinate frame so to the upper-left corner of
    the image is (0, 0) again.

    """
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        img.rotate(45, reset_coords=True)
        img.crop(0, 0, 170, 170)
        assert img[85, 85] == Color('transparent')


@mark.skipif(MAGICK_VERSION_NUMBER < 0x688,
             reason="Not supported until after ImageMagick-6.8.8")
def test_rotational_blur():
    with Image(filename='rose:') as img:
        was = img.signature
        img.rotational_blur(45.0)
        now = img.signature
        assert was != now
        was = now
        img.rotational_blur(180, 'blue')
        assert was != img.signature


def test_scale():
    with Image(filename='rose:') as img:
        width, height = img.size
        img.scale(2, 3)
        assert width*2, height*3 == img.size


def test_selective_blur():
    with Image(filename='rose:') as img:
        was = img.signature
        img.selective_blur(8, 3, 0.1 * img.quantum_range)
        assert was != img.signature
        was = img.signature
        img.selective_blur(8, 3, 0.1 * img.quantum_range, channel='red')
        assert was != img.signature


def test_sepia_tone():
    with Image(filename='rose:') as img:
        was = img.signature
        img.sepia_tone(threshold=0.8)
        assert was != img.signature


def test_shade(fx_asset):
    with Image(filename='rose:') as img:
        was = img.signature
        img.shade(gray=False, azimuth=10.0, elevation=10.0)
        assert was != img.signature
        with raises(TypeError):
            img.shade(azimuth='hello')
        with raises(TypeError):
            img.shade(elevation='hello')


def test_shadow():
    with Image(filename='rose:') as img:
        was = img.size
        img.shadow(alpha=5.0, sigma=1.25, x=10, y=10)
        assert was != img.size
        with raises(TypeError):
            img.shadow(alpha='hello')
        with raises(TypeError):
            img.shadow(sigma='hello')
        with raises(TypeError):
            img.shadow(x=None)
        with raises(TypeError):
            img.shadow(y=None)


def test_sharpen():
    with Image(filename='rose:') as img:
        was = img.signature
        img.sharpen(radius=10.0, sigma=2.0)
        assert was != img.signature
        with raises(TypeError):
            img.sharpen(radius='hello')
        with raises(TypeError):
            img.sharpen(sigma='hello')
    with Image(filename='rose:') as img:
        was = img.signature
        img.sharpen(radius=10.0, sigma=2.0, channel='red')
        assert was != img.signature


def test_shave():
    with Image(filename='rose:') as img:
        was = img.size
        img.shave(10, 10)
        assert was != img.size
        with raises(TypeError):
            img.shave(None, 10)
        with raises(TypeError):
            img.shave(10, None)


def test_shear():
    with Image(filename='rose:') as img:
        was = img.signature
        img.shear(background='green', x=10, y=10)
        assert was != img.signature


def test_sigmoidal_contrast():
    with Image(filename='rose:') as img:
        was = img.signature
        img.sigmoidal_contrast(sharpen=True,
                               strength=3,
                               midpoint=0.65 * img.quantum_range)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.sigmoidal_contrast(sharpen=True,
                               strength=3,
                               midpoint=0.65 * img.quantum_range,
                               channel='red')
        assert was != img.signature


def test_similarity():
    with Image(filename='rose:') as img:
        with img.clone() as sub_img:
            location, diff = img.similarity(sub_img)
            assert location['top'] == 0 and location['left'] == 0
            assert diff < 0.001
        with raises(TypeError):
            img.similarity(0xDEADBEEF)


def test_sketch():
    with Image(filename='rose:') as img:
        was = img.signature
        img.sketch(5.0, 3.0, 45.0)
        assert was != img.signature


def test_smush():
    with Image(filename='rose:') as img:
        width, height = img.size
        with img.clone() as a:
            with img.clone() as b:
                a.sequence.append(b)
                a.smush(False, 10)
                assert a.size == (width * 2 + 10, height)
        with img.clone() as a:
            with img.clone() as b:
                a.sequence.append(b)
                a.smush(True, 0)
                assert a.size == (width, height * 2)
        with raises(TypeError):
            img.smush(0xDEADBEEF, '0x0')


def test_solarize():
    with Image(filename='rose:') as img:
        was = img.signature
        img.alpha_channel = 'off'  # Needed for IM-7
        img.solarize(0.5 * img.quantum_range)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.alpha_channel = 'off'  # Needed for IM-7
        img.solarize(0.5 * img.quantum_range, channel='red')
        assert was != img.signature


def test_sparse_color():
    with Image(width=10, height=10, background=Color('WHITE')) as img:
        colors = {'#F00': (0, 0), '#00F': (9, 9)}
        img.sparse_color('barycentric', colors)
        assert img[0, 0] == Color('#F00')
        assert img[9, 9] == Color('#00F')
        with raises(TypeError):
            img.sparse_color(0xDEADBEEF, colors)
        with raises(TypeError):
            img.sparse_color('barycentric', 0xDEADBEEF)
        with raises(TypeError):
            img.sparse_color('barycentric', colors, channel_mask='red')


def test_splice():
    green = Color('GREEN')
    with Image(filename='rose:') as img:
        width, height = img.size
        img.background_color = green
        img.splice(10, 10, 10, 10)
        assert width+10, height+10 == img.size
        assert img[15, 15] == green
    with Image(filename='rose:') as img:
        was = img.signature
        img.splice(width=10, height=10, gravity='center')
        assert img.signature != was
    with raises(ValueError):
        with Image(filename='rose:') as img:
            img.splice(width=10, height=10, x=10, gravity='center')


def test_spread():
    with Image(filename='rose:') as img:
        was = img.signature
        img.spread(8.0)
        assert was != img.signature


def test_statistic():
    with Image(filename='rose:') as img:
        was = img.signature
        img.statistic('median', 5, 5)
        assert was != img.signature
    with Image(filename='rose:') as img:
        was = img.signature
        img.statistic('median', 5, 5, channel='red')
        assert was != img.signature


def test_stegano():
    with Image(filename='wizard:') as img:
        was = img.signature
        with Image(filename='rose:') as watermark:
            img.stegano(watermark)
        assert was != img.signature
        with raises(TypeError):
            img.stegano(0xDEADBEEF)


def test_strip(fx_asset):
    """Strips the image of all profiles and comments."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        strio = io.BytesIO()
        img.save(file=strio)
        len_original = strio.tell()
        strio.close()
        strio = io.BytesIO()
        img.strip()
        img.save(file=strio)
        len_stripped = strio.tell()
        assert len_original > len_stripped


def test_swirl():
    with Image(filename='rose:') as img:
        was = img.signature
        img.swirl(degree=90)
        assert was != img.signature


def test_texture():
    with Image(filename='rose:') as img:
        was = img.signature
        with Image(width=1, height=10, pseudo='gradient:') as tile:
            img.texture(tile)
        assert was != img.signature
        with raises(TypeError):
            img.texture(0xDEADBEEF)


def test_threshold(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        top = int(img.height * 0.25)
        btm = int(img.height * 0.75)
        img.threshold(0.5)
        with img[0, top] as white:
            assert white.red_int8 == white.green_int8 == white.blue_int8 == 255
        with img[0, btm] as black:
            assert black.red_int8 == black.green_int8 == black.blue_int8 == 0
        with raises(ValueError):
            img.threshold(0.5, channel='unknown')


def test_threshold_channel(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        was = img.signature
        img.threshold(0.0, 'red')
        img.threshold(0.5, 'green')
        img.threshold(1.0, 'blue')
        assert was != img.signature


def test_thumbnail():
    with Image(filename='rose:') as img:
        img.thumbnail(50, 20)
        assert (50, 20) == img.size
    with Image(filename='rose:') as img:
        img.thumbnail(width=50)
        assert (50, img.height) == img.size
    with Image(filename='rose:') as img:
        img.thumbnail(height=20)
        assert (img.width, 20) == img.size


def test_tint():
    with Image(filename='rose:') as img:
        was = img.signature
        img.tint('blue', 'blue')
        assert was != img.signature
        with raises(TypeError):
            img.colorize(0xDEADBEEF, Color('blue'))
        with raises(TypeError):
            img.colorize(Color('blue'), 0xDEADBEEF)


@mark.parametrize(('args', 'kwargs', 'expected_size'), [
    ((), {'resize': '200%'}, (1600, 1200)),
    ((), {'resize': '200%x100%'}, (1600, 600)),
    ((), {'resize': '1200'}, (1200, 900)),
    ((), {'resize': 'x300'}, (400, 300)),
    ((), {'resize': '400x600'}, (400, 300)),
    ((), {'resize': '1000x1200^'}, (1600, 1200)),
    ((), {'resize': '100x100!'}, (100, 100)),
    ((), {'resize': '400x500>'}, (400, 300)),
    ((), {'resize': '1200x3000<'}, (1200, 900)),
    ((), {'resize': '120000@'}, (400, 300)),
    ((), {'crop': '300x300'}, (300, 300)),
    ((), {'crop': '300x300+100+100'}, (300, 300)),
    ((), {'crop': '300x300-150-150'}, (150, 150)),
    (('300x300', '200%'), {}, (600, 600)),
])
def test_transform(args, kwargs, expected_size, fx_asset):
    """Transforms (crops and resizes with geometry strings) the image."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert img.size == (800, 600)
        img.transform(*args, **kwargs)
        assert img.size == expected_size


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason="Crop by aspect-ration requires ImageMagick-7.0.8")
def test_transform_aspect_crop(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        img.transform(crop='16:9')
        assert img.size == (800, 450)


def test_transform_colorspace(fx_asset):
    with Image(filename=str(fx_asset.join('cmyk.jpg'))) as img:
        with raises(TypeError):
            img.transform_colorspace(0xDEADBEEF)
        with raises(ValueError):
            img.transform_colorspace('unknown')

        img.transform_colorspace('srgb')
        assert img.colorspace == 'srgb'


def test_transform_errors(fx_asset):
    """Tests errors raised by invalid parameters for transform."""
    unichar = b'\xe2\x9a\xa0'.decode('utf-8')
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            img.transform(crop=500)
        with raises(TypeError):
            img.transform(resize=500)
        with raises(TypeError):
            img.transform(500, 500)
        with raises(ValueError):
            img.transform(crop=unichar)
        with raises(ValueError):
            img.transform(resize=unichar)


def test_transform_gif(tmpdir, fx_asset):
    filename = str(tmpdir.join('test_transform_gif.gif'))
    with Image(filename=str(fx_asset.join('nocomments-delay-100.gif'))) as img:
        assert len(img.sequence) == 46
        assert img.size == (350, 197)
        for single in img.sequence:
            assert single.delay == 100
        img.transform(resize='175x98!')
        assert len(img.sequence) == 46
        assert img.size == (175, 98)
        for single in img.sequence:
            assert single.size == (175, 98)
            assert single.delay == 100
        img.save(filename=filename)
    with Image(filename=filename) as gif:
        assert len(gif.sequence) == 46
        assert gif.size == (175, 98)
        for single in gif.sequence:
            assert single.size == (175, 98)
            assert single.delay == 100
    tmpdir.remove()


def test_transparent_color(fx_asset):
    """TransparentPaint test
    .. versionchanged:: 0.5.0
       Alpha channel must be enabled with ``'set'``, previously ``True``.
       See docstring in :meth:`wand.image.BaseImage.alpha_channel`.
    """
    with Image(filename=str(fx_asset.join('rotatetest.gif'))) as img:
        img.alpha_channel = 'set'
        with Color('white') as white:
            img.transparent_color(white, 0.0, 2, 0)
            assert img[75, 50].alpha == 0
            assert img[0, 50].alpha == 1.0
    with Image(filename=str(fx_asset.join('rotatetest.gif'))) as img:
        img.alpha_channel = 'set'
        img.transparent_color('white', 0.0, 2, 0)
        assert img[75, 50].alpha == 0
        assert img[0, 50].alpha == 1.0


def test_transparentize(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as im:
        with Color('transparent') as transparent:
            with Color('black') as black:
                assert im[99, 100] == transparent
                assert im[100, 100] == black
                im.transparentize(0.3)
                im.clamp()
                assert im[99, 100].alpha_int8 == transparent.alpha_int8
                with im[100, 100] as c:
                    assert c.red == c.green == c.blue == 0
                    assert 0.69 < c.alpha < 0.71
        with raises(ValueError):
            im.transparentize(-9)


def test_transpose(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        with img.clone() as transposed:
            transposed.transpose()
            assert transposed[501, 501] == Color('srgb(205,196,179)')


def test_transverse(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        with img.clone() as transversed:
            transversed.transverse()
            assert transversed[500, 500] == Color('srgb(96,136,185)')


def test_trim(fx_asset):
    """Remove transparent area around image."""
    with Image(filename=str(fx_asset.join('trimtest.png'))) as img:
        old_x, old_y = img.size
        img.trim()
        new_x, new_y = img.size
        assert new_x < old_x
        assert new_y < old_y


def test_trim_color(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as img:
        assert img.size == (100, 100)
        with Color('blue') as blue:
            img.trim(blue)
            assert img.size == (50, 100)
        img.trim('blue')
        assert img.size == (50, 100)
        with Color('srgb(0,255,0)') as green:
            assert (img[0, 0] == img[0, -1] == img[-1, 0] == img[-1, -1] ==
                    green)


def test_trim_fuzz(fx_asset):
    with Image(filename=str(fx_asset.join('trimtest.png'))) as img:
        img.trim()
        trim_x, trim_y = img.size
        img.trim(fuzz=10000)
        fuzz_x, fuzz_y = img.size
        assert fuzz_x < trim_x
        assert fuzz_y < trim_y


@mark.skipif(MAGICK_VERSION_NUMBER < 0x709,
             reason='Trim by percent-background requires ImagesMagick-7.0.9')
def test_trim_percent_background(fx_asset):
    # TODO - Find a better test image to demonstrate trim ranges.
    fpath = str(fx_asset.join('horizon_sunset_border2.jpg'))
    with Image(filename=fpath) as img:
        was = img.size
        img.trim(fuzz=0.0, percent_background=0.0, background_color='black')
        assert img.size != was
    with Image(filename=fpath) as img:
        was = img.size
        img.trim(fuzz=0.0, percent_background=0.5, background_color='black')
        assert img.size != was


def test_trim_reset_coords():
    with Image(filename='logo:') as img:
        page = img.page
        img.trim(reset_coords=True)
        assert page != img.page


def test_unique_colors():
    with Image(filename='rose:') as img:
        was = img.signature
        img.unique_colors()
        assert was != img.signature


def test_unsharp_mask(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.unsharp_mask(1.1, 1, 0.5, 0.001)
        after = img[100, 100]
        assert before != after
    with Image(filename='rose:') as img:
        was = img.signature
        img.unsharp_mask(1.1, 1, 0.5, 0.001, channel='red')
        assert was != img.signature


def test_vignette():
    with Image(filename='rose:') as img:
        was = img.signature
        img.vignette(radius=3, sigma=3)
        assert was != img.signature


def test_watermark(fx_asset):
    """Adds  watermark to an image."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        was = img.signature
        with Image(filename=str(fx_asset.join('watermark.png'))) as wm:
            img.watermark(wm, 0.3)
            assert was != img.signature


def test_wave():
    with Image(filename='rose:') as img:
        was = img.size
        img.wave(amplitude=img.height, wave_length=img.width/2)
        assert was != img.size
        with raises(TypeError):
            img.wave(amplitude='img height')
        with raises(TypeError):
            img.wave(wave_length='img height')
        with raises(TypeError):
            img.wave(method=0xDEADBEEF)


@mark.skipif(MAGICK_VERSION_NUMBER < 0x708,
             reason='Wavelet Denoise requires ImageMagick-7.0.8.')
def test_wavelet_denoise():
    with Image(filename='rose:') as img:
        was = img.signature
        img.wavelet_denoise(0.2, 0.3)
        assert was != img.signature


@mark.skipif(MAGICK_VERSION_NUMBER < 0x70B,
             reason='White balance requires ImageMagick-7.0.11')
def test_white_balance():
    with Image(filename='rose:') as img:
        was = img.signature
        img.white_balance()
        assert was != img.signature


def test_white_threshold():
    with Image(filename='rose:') as img:
        was = img.signature
        img.white_threshold(Color('gray(50%)'))
        assert was != img.signature
        assert img.white_threshold('gray(50%)')
        with raises(TypeError):
            img.white_threshold(0xDEADBEEF)
