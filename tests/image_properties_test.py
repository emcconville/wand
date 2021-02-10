# -*- coding: utf-8 -*-
#
# These test cover the Image attributes that directly map to C-API functions.
#
import io
import numbers
from pytest import mark, raises

from wand.color import Color
from wand.compat import string_type
from wand.font import Font
from wand.image import Image
from wand.version import MAGICK_VERSION_NUMBER


def test_alpha_channel_get(fx_asset):
    """Checks if image has alpha channel."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        assert img.alpha_channel is True
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.alpha_channel is False


def test_alpha_channel_set(fx_asset):
    """Sets alpha channel to off."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        if MAGICK_VERSION_NUMBER < 0x700:
            enable_option = 'on'
            disable_option = False
        else:
            enable_option = 'associate'
            disable_option = 'disassociate'
        img.alpha_channel = enable_option
        assert img.alpha_channel is True
        img.alpha_channel = disable_option
        assert img.alpha_channel is False
        img.alpha_channel = 'opaque'
        assert img[0, 0].alpha == 1.0
        with raises(ValueError):
            img.alpha_channel = 'watermark'


def test_artifacts():
    with Image(filename='rose:') as img:
        img.artifacts['key'] = 'value'
        assert 'date:create' in img.artifacts
        assert img.artifacts['key'] == 'value'
        assert img.artifacts['not_a_value'] is None
        _ = len(img.artifacts)
        for _ in img.artifacts.items():
            pass
        del img.artifacts['key']


def test_background_color_get(fx_asset):
    """Gets the background color."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert Color('white') == img.background_color


def test_background_color_set(fx_asset):
    """Sets the background color."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with Color('red') as color:
            img.background_color = color
            assert img.background_color == color
        img.background_color = 'green'
        assert img.background_color == Color('green')


def test_border_color():
    green = Color('green')
    with Image(filename='rose:') as img:
        img.border_color = 'green'
        assert img.border_color == green


@mark.xfail(MAGICK_VERSION_NUMBER >= 0x700,
            reason="Channel traits are not implemented in IM7.")
def test_channel_depths(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as i:
        assert dict(i.channel_depths) == {
            'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
            'undefined': 1, 'composite_channels': 8, 'index': 1,
            'rgb_channels': 8, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
            'default_channels': 8, 'black': 1, 'cyan': 8,
            'all_channels': 8, 'green': 8, 'magenta': 8, 'red': 8,
            'gray_channels': 8, 'rgb': 8
        }
    with Image(filename=str(fx_asset.join('google.ico'))) as i:
        assert dict(i.channel_depths) == {
            'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
            'undefined': 1, 'composite_channels': 8, 'index': 1,
            'rgb_channels': 8, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
            'default_channels': 8, 'black': 1, 'cyan': 8, 'all_channels': 8,
            'green': 8, 'magenta': 8, 'red': 8, 'gray_channels': 8, 'rgb': 8
        }


def test_channel_images(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as i:
        i.format = 'png'
        channels = ('opacity', 'alpha',)
        # Only include TrueAlphaChannel if IM6, as its deprecated & unused
        # in IM7.
        if MAGICK_VERSION_NUMBER < 0x700:
            channels = channels + ('true_alpha',)
        for name in channels:
            expected_path = str(fx_asset.join('channel_images', name + '.png'))
            with Image(filename=expected_path) as expected:
                if MAGICK_VERSION_NUMBER >= 0x700:
                    # With IM7, channels are dynamic & influence signatures.
                    # We'll need to compare the first channel of the expected
                    # PNG with the extracted channel.
                    first_channel = expected.channel_images['red']
                    assert i.channel_images[name] == first_channel
                else:
                    assert i.channel_images[name] == expected


def test_colors(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as img:
        assert img.colors == 2


def test_colorspace_get(fx_asset):
    """Gets the image colorspace"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.colorspace.endswith('rgb')


def test_colorspace_set(fx_asset):
    """Sets the image colorspace"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.colorspace = 'cmyk'
        assert img.colorspace == 'cmyk'


def test_compose(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.compose == 'over'
        img.compose = 'blend'
        assert img.compose == 'blend'
        with raises(TypeError):
            img.compose = 0xDEADBEEF
        with raises(ValueError):
            img.compose = 'none'


def test_compression(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        # Legacy releases/library asserted ``'group4'`` compression type.
        # IM 7 will correctly report ``'jpeg'``, but ``'group4'`` should
        # still be apart of regression acceptance.
        assert img.compression in ('group4', 'jpeg')
        img.compression = 'zip'
        assert img.compression == 'zip'
        with raises(TypeError):
            img.compression = 0x60


def test_compression_quality_get(fx_asset):
    """Gets the image compression quality."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.compression_quality == 80


def test_compression_quality_set(fx_asset):
    """Sets the image compression quality."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.compression_quality = 50
        assert img.compression_quality == 50
        strio = io.BytesIO()
        img.save(file=strio)
        strio.seek(0)
        with Image(file=strio) as jpg:
            assert jpg.compression_quality == 50
        with raises(TypeError):
            img.compression_quality = 'high'


def test_delay_set_get(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img:
        img.delay = 10
        assert img.delay == 10


def test_depth_get(fx_asset):
    """Gets the image depth"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.depth == 8


def test_depth_set(fx_asset):
    """Sets the image depth"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.depth = 16
        assert img.depth == 16


def test_dispose(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img:
        assert img.dispose == 'none'
        img.dispose = 'background'
        assert img.dispose == 'background'


def test_font_set(fx_asset):
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        font = Font(
            path=str(fx_asset.join('League_Gothic.otf')),
            color=Color('gold'),
            size=12,
            antialias=False
        )
        img.font = font
        assert img.font_path == font.path
        assert img.font_size == font.size
        assert img.font_color == font.color
        assert img.antialias == font.antialias
        assert img.font == font
        assert repr(img.font)
        fontStroke = Font(
            path=str(fx_asset.join('League_Gothic.otf')),
            stroke_color=Color('ORANGE'),
            stroke_width=1.5
        )
        img.font = fontStroke
        assert img.stroke_color == fontStroke.stroke_color
        assert img.stroke_width == fontStroke.stroke_width
        img.font_color = 'gold'
        assert img.font_color == Color('gold')
        img.stroke_color = 'gold'
        assert img.stroke_color == Color('gold')
        fontColor = Font(
            path=str(fx_asset.join('League_Gothic.otf')),
            color='YELLOW',
            stroke_color='PINK'
        )
        img.font = fontColor
        assert img.font_color == Color('YELLOW')
        assert img.stroke_color == Color('PINK')
        with raises(ValueError):
            img.font_size = -99


def test_format_get(fx_asset):
    """Gets the image format."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.format == 'JPEG'
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        assert img.format == 'PNG'


def test_format_set(fx_asset):
    """Sets the image format."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.format = 'png'
        assert img.format == 'PNG'
        strio = io.BytesIO()
        img.save(file=strio)
        strio.seek(0)
        with Image(file=strio) as png:
            assert png.format == 'PNG'
        with raises(ValueError):
            img.format = 'HONG'
        with raises(TypeError):
            img.format = 123


def test_fuzz():
    with Image(filename='rose:') as img:
        assert img.fuzz == 0.0
        img.fuzz = img.quantum_range
        assert img.fuzz == img.quantum_range


def test_gravity_set():
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        img.gravity = 'center'
        assert img.gravity == 'center'


def test_histogram(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as a:
        h = a.histogram
        assert len(h) == 2
        assert frozenset(h) == frozenset([
            Color('srgb(0,255,0'),
            Color('srgb(0,0,255')
        ])
        assert dict(h) == {
            Color('srgb(0,255,0'): 5000,
            Color('srgb(0,0,255'): 5000,
        }
        assert Color('white') not in h
        assert Color('srgb(0,255,0)') in h
        assert Color('srgb(0,0,255)') in h
        assert h[Color('srgb(0,255,0)')] == 5000
        assert h[Color('srgb(0,0,255)')] == 5000


def test_interlace_scheme_get(fx_asset):
    with Image(filename='rose:') as img:
        expected = 'no'
        assert img.interlace_scheme == expected


def test_interlace_scheme_set(fx_asset):
    with Image(filename='rose:') as img:
        expected = 'plane'
        img.interlace_scheme = expected
        assert img.interlace_scheme == expected


def test_interpolate_method_get(fx_asset):
    with Image(filename='rose:') as img:
        expected = 'undefined'
        assert img.interpolate_method == expected


def test_interpolate_method_set(fx_asset):
    with Image(filename='rose:') as img:
        expected = 'spline'
        img.interpolate_method = expected
        assert img.interpolate_method == expected


def test_kurtosis():
    with Image(filename='rose:') as img:
        kurtosis = img.kurtosis
        assert isinstance(kurtosis, numbers.Real)
        assert kurtosis != 0.0


def test_length_of_bytes():
    with Image(filename='rose:') as img:
        assert img.length_of_bytes > 0
        img.resample(300, 300)
        assert img.length_of_bytes == 0


def test_loop(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img:
        assert img.loop == 0
        img.loop = 1
        assert img.loop == 1


def test_matte_color(fx_asset):
    with Image(filename='rose:') as img:
        with Color('navy') as color:
            img.matte_color = color
            assert img.matte_color == color
            with raises(TypeError):
                img.matte_color = False
        img.matte_color = 'orange'
        assert img.matte_color == Color('orange')


def test_mean():
    with Image(filename='rose:') as img:
        mean = img.mean
        assert isinstance(mean, numbers.Real)
        assert mean != 0.0


def test_metadata(fx_asset):
    """Test metadata api"""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert 52 <= len(img.metadata) <= 55
        for key in img.metadata:
            assert isinstance(key, string_type)
        assert 'exif:ApertureValue' in img.metadata
        assert 'exif:UnknownValue' not in img.metadata
        assert img.metadata['exif:ApertureValue'] == '192/32'
        assert img.metadata.get('exif:UnknownValue', "IDK") == "IDK"


def test_mimetype(fx_asset):
    """Gets mimetypes of the image."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.mimetype in ('image/jpeg', 'image/x-jpeg')
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        assert img.mimetype in ('image/png', 'image/x-png')


def test_minima_maxima():
    with Image(filename='rose:') as img:
        min_q = img.minima
        max_q = img.maxima
        assert min_q < max_q


def test_orientation_get(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.orientation == 'undefined'

    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert img.orientation == 'top_left'


def test_orientation_set(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        img.orientation = 'bottom_right'
        assert img.orientation == 'bottom_right'


def test_page_basic(fx_asset):
    with Image(filename=str(fx_asset.join('watermark.png'))) as img1:
        assert img1.page == (640, 480, 0, 0)
        assert img1.page_width == 640
        assert img1.page_height == 480
        assert img1.page_x == 0
        assert img1.page_y == 0
        with raises(TypeError):
            img1.page = 640


def test_page_offset(fx_asset):
    with Image(filename=str(fx_asset.join('watermark-offset.png'))) as img1:
        assert img1.page == (640, 480, 12, 13)
        assert img1.page_width == 640
        assert img1.page_height == 480
        assert img1.page_x == 12
        assert img1.page_y == 13


def test_page_setter(fx_asset):
    with Image(filename=str(fx_asset.join('watermark.png'))) as img1:
        assert img1.page == (640, 480, 0, 0)
        img1.page = (640, 480, 0, 0)
        assert img1.page == (640, 480, 0, 0)
        img1.page = (640, 480, 12, 13)
        assert img1.page == (640, 480, 12, 13)
        img1.page = (640, 480, -12, 13)
        assert img1.page == (640, 480, -12, 13)
        img1.page = (640, 480, 12, -13)
        assert img1.page == (640, 480, 12, -13)
        img1.page = (6400, 4800, 2, 3)
        assert img1.page == (6400, 4800, 2, 3)


def test_page_setter_items(fx_asset):
    with Image(filename=str(fx_asset.join('watermark.png'))) as img1:
        assert img1.page == (640, 480, 0, 0)
        img1.page_width = 6400
        assert img1.page == (6400, 480, 0, 0)
        img1.page_height = 4800
        assert img1.page == (6400, 4800, 0, 0)
        img1.page_x = 12
        assert img1.page == (6400, 4800, 12, 0)
        img1.page_y = 13
        assert img1.page == (6400, 4800, 12, 13)
        img1.page_x = -12
        assert img1.page == (6400, 4800, -12, 13)
        img1.page_y = -13
        assert img1.page == (6400, 4800, -12, -13)


def test_page_setter_papersize():
    with Image(filename='rose:') as img:
        img.page = 'a4'
        assert img.page == (595, 842, 0, 0)
        img.page = 'badvalue'
        assert img.page == (0, 0, 0, 0)


def test_primary_points(fx_asset):
    with Image(filename='rose:') as img:
        blue = [d/2 for d in img.blue_primary]
        img.blue_primary = blue
        assert blue == list(img.blue_primary)
        green = [d/2 for d in img.green_primary]
        img.green_primary = green
        assert green == list(img.green_primary)
        red = [d/2 for d in img.red_primary]
        img.red_primary = red
        assert red == list(img.red_primary)
        white = [d/2 for d in img.white_point]
        img.white_point = white
        assert white == list(img.white_point)
        with raises(TypeError):
            img.blue_primary = 0xDEADBEEF
        with raises(TypeError):
            img.green_primary = 0xDEADBEEF
        with raises(TypeError):
            img.red_primary = 0xDEADBEEF
        with raises(TypeError):
            img.white_point = 0xDEADBEEF


def test_profiles(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert len(img.profiles) == 1
        assert 'exif' in [d for d in img.profiles]
        exif_data = img.profiles['exif']
        assert exif_data is not None
        del img.profiles['exif']
        assert img.profiles['exif'] is None
        img.profiles['exif'] = exif_data
        assert img.profiles['exif'] == exif_data
        with raises(TypeError):
            img.profiles[0xDEADBEEF]
        with raises(TypeError):
            del img.profiles[0xDEADBEEF]
        with raises(TypeError):
            img.profiles[0xDEADBEEF] = 0xDEADBEEF
        with raises(TypeError):
            img.profiles['exif'] = 0xDEADBEEF


def test_rendering_intent(fx_asset):
    with Image(filename=str(fx_asset.join('trimtest.png'))) as img:
        assert img.rendering_intent == 'perceptual'
        img.rendering_intent = 'relative'
        assert img.rendering_intent == 'relative'


def test_resolution_get(fx_asset):
    """Gets image resolution."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.resolution == (72, 72)


def test_resolution_set_01(fx_asset):
    """Sets image resolution."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.resolution = (100, 100)
        assert img.resolution == (100, 100)


def test_resolution_set_02(fx_asset):
    """Sets image resolution with integer as parameter."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.resolution = 100
        assert img.resolution == (100, 100)


def test_resolution_set_03():
    """Sets image resolution on constructor"""
    with Image(filename='rose:', resolution=(100, 100)) as img:
        assert img.resolution == (100, 100)


def test_resolution_set_04():
    """Sets image resolution on constructor with integer as parameter."""
    with Image(filename='rose:', resolution=100) as img:
        assert img.resolution == (100, 100)


def test_sampling_factors():
    with Image(filename='rose:') as img:
        img.sampling_factors = "4:2:2"
        assert img.sampling_factors == (2, 1)
        with raises(TypeError):
            img.sampling_factors = {}


def test_scene():
    with Image(filename='rose:') as img:
        img.scene = 4
        assert img.scene == 4


def test_signature(fx_asset):
    """Gets the image signature."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with fx_asset.join('mona-lisa.jpg').open('rb') as f:
            with Image(file=f) as same:
                assert img.signature == same.signature
        with img.convert('png') as same:
            assert img.signature == same.signature
        with Image(filename=str(fx_asset.join('beach.jpg'))) as diff:
            assert img.signature != diff.signature


def test_size(fx_asset):
    """Gets the image size."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.size == (402, 599)
        assert img.width == 402
        assert img.height == 599
        assert len(img) == 599


def test_skewness():
    with Image(filename='rose:') as img:
        skewness = img.skewness
        assert isinstance(skewness, numbers.Real)
        assert skewness != 0.0


def test_standard_deviation():
    with Image(filename='rose:') as img:
        standard_deviation = img.standard_deviation
        assert isinstance(standard_deviation, numbers.Real)
        assert standard_deviation != 0.0


def test_stroke_color_user_error():
    with Image(filename='rose:') as img:
        img.stroke_color = 'green'
        img.stroke_color = None
        assert img.stroke_color is None
        with raises(TypeError):
            img.stroke_color = 0xDEADBEEF


def test_type_get(fx_asset):
    """Gets the image type."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.type == "truecolor"
        img.alpha_channel = True
        if MAGICK_VERSION_NUMBER < 0x700:
            expected = "truecolormatte"
        else:
            expected = "truecoloralpha"
        assert img.type == expected


def test_type_set(fx_asset):
    """Sets the image type."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.type = "grayscale"
        assert img.type == "grayscale"


def test_ticks_per_second(fx_asset):
    with Image(filename=str(fx_asset.join('nocomments.gif'))) as img:
        assert img.ticks_per_second == 100
        img.ticks_per_second = 10
        assert img.ticks_per_second == 10


def test_units_get(fx_asset):
    """Gets the image resolution units."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert img.units == "pixelsperinch"
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.units == "undefined"


def test_units_set(fx_asset):
    """Sets the image resolution units."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        img.units = "pixelspercentimeter"
        assert img.units == "pixelspercentimeter"


def test_virtual_pixel_get(fx_asset):
    """Gets image virtual pixel"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.virtual_pixel == "undefined"


def test_virtual_pixel_set(fx_asset):
    """Sets image virtual pixel"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.virtual_pixel = "tile"
        assert img.virtual_pixel == "tile"
        with raises(ValueError):
            img.virtual_pixel = "nothing"
