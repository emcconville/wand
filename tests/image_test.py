# -*- coding: utf-8 -*-
import codecs
import io
import os
import os.path
import shutil
import struct
import sys
import tempfile
import warnings

from pytest import mark, raises

from wand.image import ClosedImageError, Image, IMAGE_LAYER_METHOD
from wand.color import Color
from wand.compat import PY3, string_type, text, text_type
from wand.exceptions import OptionError, MissingDelegateError
from wand.font import Font

try:
    filesystem_encoding = sys.getfilesystemencoding()
except RuntimeError:
    unicode_filesystem_encoding = False
else:
    try:
        codec_info = codecs.lookup(filesystem_encoding)
    except LookupError:
        unicode_filesystem_encoding = False
    else:
        unicode_filesystem_encoding = codec_info.name in (
            'utf-8', 'utf-16', 'utf-16-be', 'utf-16-le',
            'utf-32', 'utf-32-be', 'utf-32-le',
            'mbcs'  # for Windows
        )


def test_empty_image():
    with Image() as img:
        assert img.size == (0, 0)
        assert repr(img) == '<wand.image.Image: (empty)>'


def test_image_invalid_params():
    with raises(TypeError):
        Image(image=Image(), width=100, height=100)
    with raises(TypeError):
        Image(image=Image(), blob=b"blob")
    with raises(TypeError):
        Image(image=b"blob")


def test_blank_image():
    gray = Color('#ccc')
    transparent = Color('transparent')
    with raises(TypeError):
        Image(width=0, height=0)
    with Image(width=20, height=10) as img:
        assert img[10, 5] == transparent
    with Image(width=20, height=10, background=gray) as img:
        assert img.size == (20, 10)
        assert img[10, 5] == gray


def test_raw_image(fx_asset):
    b = b"".join([struct.pack("BBB", i, j, 0)
                  for i in range(256) for j in range(256)])
    with raises(ValueError):
        Image(blob=b, depth=6)
    with raises(TypeError):
        Image(blob=b, depth=8, width=0, height=0, format="RGB")
    with raises(TypeError):
        Image(blob=b, depth=8, width=256, height=256, format=1)
    with Image(blob=b, depth=8, width=256, height=256, format="RGB") as img:
        assert img.size == (256, 256)
        assert img[0, 0] == Color('#000000')
        assert img[255, 255] == Color('#ffff00')
        assert img[64, 128] == Color('#804000')
    with Image(filename=str(fx_asset.join('blob.rgb')),
               depth=8, width=256, height=256, format="RGB") as img:
        assert img.size == (256, 256)
        assert img[0, 0] == Color('#000000')
        assert img[255, 255] == Color('#ffff00')
        assert img[64, 128] == Color('#804000')


def test_clear_image(fx_asset):
    with Image() as img:
        img.read(filename=str(fx_asset.join('mona-lisa.jpg')))
        assert img.size == (402, 599)
        img.clear()
        assert img.size == (0, 0)
        img.read(filename=str(fx_asset.join('beach.jpg')))
        assert img.size == (800, 600)


def test_read_from_filename(fx_asset):
    with Image() as img:
        img.read(filename=str(fx_asset.join('mona-lisa.jpg')))
        assert img.width == 402
        img.clear()
        with fx_asset.join('mona-lisa.jpg').open('rb') as f:
            img.read(file=f)
            assert img.width == 402
            img.clear()
        blob = fx_asset.join('mona-lisa.jpg').read('rb')
        img.read(blob=blob)
        assert img.width == 402


@mark.skipif(not unicode_filesystem_encoding,
             reason='Unicode filesystem encoding needed')
def test_read_from_unicode_filename(fx_asset, tmpdir):
    """https://github.com/dahlia/wand/issues/122"""
    filename = '모나리자.jpg'
    if not PY3:
        filename = filename.decode('utf-8')
    path = os.path.join(text_type(tmpdir), filename)  # workaround py.path bug
    shutil.copyfile(str(fx_asset.join('mona-lisa.jpg')), path)
    with Image() as img:
        img.read(filename=text(path))
        assert img.width == 402


def test_new_from_file(fx_asset):
    """Opens an image from the file object."""
    with fx_asset.join('mona-lisa.jpg').open('rb') as f:
        with Image(file=f) as img:
            assert img.width == 402
    with raises(ClosedImageError):
        img.wand
    strio = io.BytesIO(fx_asset.join('mona-lisa.jpg').read('rb'))
    with Image(file=strio) as img:
        assert img.width == 402
    strio.close()
    with raises(ClosedImageError):
        img.wand
    with raises(TypeError):
        Image(file='not file object')


def test_new_from_filename(fx_asset):
    """Opens an image through its filename."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand
    with raises(IOError):
        Image(filename=str(fx_asset.join('not-exists.jpg')))


@mark.skipif(not unicode_filesystem_encoding,
             reason='Unicode filesystem encoding needed')
def test_new_from_unicode_filename(fx_asset, tmpdir):
    """https://github.com/dahlia/wand/issues/122"""
    filename = '모나리자.jpg'
    if not PY3:
        filename = filename.decode('utf-8')
    path = os.path.join(text_type(tmpdir), filename)  # workaround py.path bug
    shutil.copyfile(str(fx_asset.join('mona-lisa.jpg')), path)
    with Image(filename=text(path)) as img:
        assert img.width == 402


def test_new_from_blob(fx_asset):
    """Opens an image from blob."""
    blob = fx_asset.join('mona-lisa.jpg').read('rb')
    with Image(blob=blob) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand


def test_new_with_format(fx_asset):
    blob = fx_asset.join('google.ico').read('rb')
    with raises(Exception):
        Image(blob=blob)
    with Image(blob=blob, format='ico') as img:
        assert img.size == (16, 16)


def test_clone(fx_asset):
    """Clones the existing image."""
    funcs = (lambda img: Image(image=img),
             lambda img: img.clone())
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        for func in funcs:
            with func(img) as cloned:
                assert img.wand is not cloned.wand
                assert img.size == cloned.size
            with raises(ClosedImageError):
                cloned.wand
    with raises(ClosedImageError):
        img.wand


def test_save_to_filename(fx_asset):
    """Saves an image to the filename."""
    savefile = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as orig:
        orig.save(filename=savefile)
        with raises(IOError):
            orig.save(filename=os.path.join(savefile, 'invalid.jpg'))
        with raises(TypeError):
            orig.save(filename=1234)
    assert os.path.isfile(savefile)
    with Image(filename=savefile) as saved:
        assert saved.size == (402, 599)
    os.remove(savefile)


@mark.skipif(not unicode_filesystem_encoding,
             reason='Unicode filesystem encoding needed')
def test_save_to_unicode_filename(fx_asset, tmpdir):
    filename = '모나리자.jpg'
    if not PY3:
        filename = filename.decode('utf-8')
    path = os.path.join(text_type(tmpdir), filename)  # workaround py.path bug
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as orig:
        orig.save(filename=path)
    with Image(filename=path) as img:
        assert img.width == 402


def test_save_to_file(fx_asset):
    """Saves an image to the Python file object."""
    buffer = io.BytesIO()
    with tempfile.TemporaryFile() as savefile:
        with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as orig:
            orig.save(file=savefile)
            orig.save(file=buffer)
            with raises(TypeError):
                orig.save(file='filename')
            with raises(TypeError):
                orig.save(file=1234)
        savefile.seek(0)
        with Image(file=savefile) as saved:
            assert saved.size == (402, 599)
        buffer.seek(0)
        with Image(file=buffer) as saved:
            assert saved.size == (402, 599)
    buffer.close()


def test_save_full_animated_gif_to_file(fx_asset):
    """Save all frames of an animated to a Python file object."""
    temp_filename = os.path.join(tempfile.mkdtemp(), 'savetest.gif')
    orig_filename = str(fx_asset.join('nocomments.gif'))
    with open(temp_filename, 'w+b') as fp:
        with Image(filename=orig_filename) as orig:
            orig.save(file=fp)
    assert os.path.isfile(temp_filename)
    with Image(filename=orig_filename) as orig:
        with Image(filename=temp_filename) as temp:
            assert len(orig.sequence) == len(temp.sequence)
    os.remove(temp_filename)


def test_save_error(fx_asset):
    filename = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    fileobj = io.BytesIO()
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as orig:
        with raises(TypeError):
            orig.save()
        with raises(TypeError):
            orig.save(filename=filename, file=fileobj)


def test_make_blob(fx_asset):
    """Makes a blob string."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with Image(blob=img.make_blob('png')) as img2:
            assert img2.size == (402, 599)
            assert img2.format == 'PNG'
        assert img.format == 'JPEG'
        with raises(TypeError):
            img.make_blob(123)
    svg = b'''
    <svg width="100px" height="100px">
        <circle cx="100" cy="50" r="40" stroke="black"
         stroke-width="2" fill="red" />
    </svg>
    '''
    with Image(blob=svg, format='svg') as img:
        assert img.size == (100, 100)
        assert img.format in ('SVG', 'MVG')
        img.format = 'PNG'
        assert img.size == (100, 100)
        assert img.format == 'PNG'
        png = img.make_blob()
    with Image(blob=png, format='png') as img:
        assert img.size == (100, 100)
        assert img.format == 'PNG'


def test_size(fx_asset):
    """Gets the image size."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.size == (402, 599)
        assert img.width == 402
        assert img.height == 599
        assert len(img) == 599


def test_get_resolution(fx_asset):
    """Gets image resolution."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.resolution == (72, 72)


def test_set_resolution_01(fx_asset):
    """Sets image resolution."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.resolution = (100, 100)
        assert img.resolution == (100, 100)


def test_set_resolution_02(fx_asset):
    """Sets image resolution with integer as parameter."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.resolution = 100
        assert img.resolution == (100, 100)


def test_set_resolution_03(fx_asset):
    """Sets image resolution on constructor"""
    with Image(filename=str(fx_asset.join('sample.pdf')),
               resolution=(100, 100)) as img:
        assert img.resolution == (100, 100)


def test_set_resolution_04(fx_asset):
    """Sets image resolution on constructor with integer as parameter."""
    with Image(filename=str(fx_asset.join('sample.pdf')),
               resolution=100) as img:
        assert img.resolution == (100, 100)


def test_get_units(fx_asset):
    """Gets the image resolution units."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert img.units == "pixelsperinch"
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.units == "undefined"


def test_set_units(fx_asset):
    """Sets the image resolution units."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        img.units = "pixelspercentimeter"
        assert img.units == "pixelspercentimeter"


def test_get_virtual_pixel(fx_asset):
    """Gets image virtual pixel"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.virtual_pixel == "undefined"


def test_set_virtual_pixel(fx_asset):
    """Sets image virtual pixel"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.virtual_pixel = "tile"
        assert img.virtual_pixel == "tile"
        with raises(ValueError):
            img.virtual_pixel = "nothing"


def test_get_colorspace(fx_asset):
    """Gets the image colorspace"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.colorspace.endswith('rgb')


def test_set_colorspace(fx_asset):
    """Sets the image colorspace"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.colorspace = 'cmyk'
        assert img.colorspace == 'cmyk'


def test_get_depth(fx_asset):
    """Gets the image depth"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.depth == 8


def test_set_depth(fx_asset):
    """Sets the image depth"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.depth = 16
        assert img.depth == 16


def test_get_format(fx_asset):
    """Gets the image format."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.format == 'JPEG'
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        assert img.format == 'PNG'


def test_set_format(fx_asset):
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


def test_get_type(fx_asset):
    """Gets the image type."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.type == "truecolor"
        img.alpha_channel = True
        assert img.type == "truecolormatte"


def test_set_type(fx_asset):
    """Sets the image type."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        img.type = "grayscale"
        assert img.type == "grayscale"


def test_get_compression(fx_asset):
    """Gets the image compression quality."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.compression_quality == 80


def test_set_compression(fx_asset):
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


def test_strip(fx_asset):
    """Strips the image of all profiles and comments."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        strio = io.BytesIO()
        img.save(file=strio)
        len_unstripped = strio.tell()
        strio.close()
        strio = io.BytesIO()
        img.strip()
        img.save(file=strio)
        len_stripped = strio.tell()
        assert len_unstripped > len_stripped


def test_trim(fx_asset):
    """Remove transparent area around image."""
    with Image(filename=str(fx_asset.join('trimtest.png'))) as img:
        oldx, oldy = img.size
        img.trim()
        newx, newy = img.size
        assert newx < oldx
        assert newy < oldy


def test_trim_fuzz(fx_asset):
    with Image(filename=str(fx_asset.join('trimtest.png'))) as img:
        img.trim()
        trimx, trimy = img.size
        img.trim(fuzz=10000)
        fuzzx, fuzzy = img.size
        assert fuzzx < trimx
        assert fuzzy < trimy


def test_trim_color(fx_asset):
    with Image(filename=str(fx_asset.join('trim-color-test.png'))) as img:
        assert img.size == (100, 100)
        with Color('blue') as blue:
            img.trim(blue)
            assert img.size == (50, 100)
        with Color('srgb(0,255,0)') as green:
            assert (img[0, 0] == img[0, -1] == img[-1, 0] == img[-1, -1] ==
                    green)


def test_get_mimetype(fx_asset):
    """Gets mimetypes of the image."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.mimetype in ('image/jpeg', 'image/x-jpeg')
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        assert img.mimetype in ('image/png', 'image/x-png')


def test_convert(fx_asset):
    """Converts the image format."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with img.convert('png') as converted:
            assert converted.format == 'PNG'
            strio = io.BytesIO()
            converted.save(file=strio)
            strio.seek(0)
            with Image(file=strio) as png:
                assert png.format == 'PNG'
        with raises(ValueError):
            img.convert('HONG')
        with raises(TypeError):
            img.convert(123)


@mark.slow
def test_iterate(fx_asset):
    """Uses iterator."""
    with Color('#000') as black:
        with Color('transparent') as transparent:
            with Image(filename=str(fx_asset.join('croptest.png'))) as img:
                for i, row in enumerate(img):
                    assert len(row) == 300
                    if i % 3:
                        continue  # avoid slowness
                    if 100 <= i < 200:
                        for x, color in enumerate(row):
                            if x % 3:
                                continue  # avoid slowness
                            if 100 <= x < 200:
                                assert color == black
                            else:
                                assert color == transparent
                    else:
                        for color in row:
                            assert color == transparent
                assert i == 299


def test_slice_clone(fx_asset):
    """Clones using slicing."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with img[:, :] as cloned:
            assert img.size == cloned.size


def test_slice_invalid_types(fx_asset):
    """Slicing with invalid types should throw exceptions."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            img['12']
        with raises(TypeError):
            img[1.23]
        with raises(ValueError):
            img[()]
        with raises(ValueError):
            img[:, :, :]
        with raises(ValueError):
            img[::2, :]
        with raises(IndexError):
            img[1:1, :]
        with raises(IndexError):
            img[:, 2:2]
        with raises(TypeError):
            img[100.0:, 100.0]
        with raises(TypeError):
            img['100':, '100']
        with raises(IndexError):
            img[500:, 900]
        with raises(TypeError):
            img['1', 0]
        with raises(TypeError):
            img[1, '0']
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with raises(IndexError):
            img[300, 300]
        with raises(IndexError):
            img[-301, -301]


def test_index_pixel(fx_asset):
    """Gets a pixel."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        assert img[0, 0] == Color('transparent')
        assert img[99, 99] == Color('transparent')
        assert img[100, 100] == Color('black')
        assert img[150, 150] == Color('black')
        assert img[-200, -200] == Color('black')
        assert img[-201, -201] == Color('transparent')


def test_index_row(fx_asset):
    """Gets a row."""
    with Color('transparent') as transparent:
        with Color('black') as black:
            with Image(filename=str(fx_asset.join('croptest.png'))) as img:
                for c in img[0]:
                    assert c == transparent
                for c in img[99]:
                    assert c == transparent
                for i, c in enumerate(img[100]):
                    if 100 <= i < 200:
                        assert c == black
                    else:
                        assert c == transparent
                for i, c in enumerate(img[150]):
                    if 100 <= i < 200:
                        assert c == black
                    else:
                        assert c == transparent
                for i, c in enumerate(img[-200]):
                    if 100 <= i < 200:
                        assert c == black
                    else:
                        assert c == transparent
                for c in img[-201]:
                    assert c == transparent


def test_slice_crop(fx_asset):
    """Crops using slicing."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with img[100:200, 100:200] as cropped:
            assert cropped.size == (100, 100)
            with Color('#000') as black:
                for row in cropped:
                    for col in row:
                        assert col == black
        with img[150:, :150] as cropped:
            assert cropped.size == (150, 150)
        with img[-200:-100, -200:-100] as cropped:
            assert cropped.size == (100, 100)
        with img[100:200] as cropped:
            assert cropped.size == (300, 100)
        assert img.size == (300, 300)
        with raises(IndexError):
            img[:500, :500]
        with raises(IndexError):
            img[290:310, 290:310]


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
        with raises(ValueError):
            img.crop(0, 0, 500, 500)
        with raises(ValueError):
            img.crop(290, 290, 50, 50)
        with raises(ValueError):
            img.crop(290, 290, width=0, height=0)


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


def test_crop_error(fx_asset):
    """Crop errors."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with raises(TypeError):
            img.crop(right=1, width=2)
        with raises(TypeError):
            img.crop(bottom=1, height=2)


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


@mark.slow
def test_distort(fx_asset):
    """Distort image."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with Color('skyblue') as color:
            img.matte_color = color
            img.virtual_pixel = 'tile'
            img.distort('perspective', (0, 0, 20, 60, 90, 0,
                                        70, 63, 0, 90, 5, 83,
                                        90, 90, 85, 88))
            assert img[img.width - 1, 0] == color


def test_distort_error(fx_asset):
    """Distort image with user error"""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(ValueError):
            img.distort('mirror', (1,))
        with raises(TypeError):
            img.distort('perspective', 1)


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
                    assert black == cloned[2, 70] == cloned[35, 37]
                    assert black == cloned[85, 88] == cloned[52, 120]


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


def test_transparent_color(fx_asset):
    """TransparentPaint test"""
    with Image(filename=str(fx_asset.join('rotatetest.gif'))) as img:
        img.alpha_channel = True
        with Color('white') as white:
            img.transparent_color(white, 0.0, 2, 0)
            assert img[75, 50].alpha == 0
            assert img[0, 50].alpha == 1.0


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


def test_equal(fx_asset):
    """Equals (``==``) and not equals (``!=``) operators."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as a:
        with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as a2:
            assert a == a2
            assert not (a != a2)
        with Image(filename=str(fx_asset.join('sasha.jpg'))) as b:
            assert a != b
            assert not (a == b)
        with a.convert('png') as a3:
            assert a == a3
            assert not (a != a3)


def test_object_hash(fx_asset):
    """Gets :func:`hash()` of the image."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        a = hash(img)
        img.format = 'png'
        b = hash(img)
        assert a == b


def test_get_alpha_channel(fx_asset):
    """Checks if image has alpha channel."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        assert img.alpha_channel is True
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert img.alpha_channel is False


def test_set_alpha_channel(fx_asset):
    """Sets alpha channel to off."""
    with Image(filename=str(fx_asset.join('watermark.png'))) as img:
        img.alpha_channel = 'on'
        assert img.alpha_channel is True
        img.alpha_channel = False
        assert img.alpha_channel is False
        img.alpha_channel = 'opaque'
        assert img[0, 0].alpha == 1.0
        with raises(ValueError):
            img.alpha_channel = 'watermark'


def test_get_background_color(fx_asset):
    """Gets the background color."""
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        assert Color('transparent') == img.background_color


def test_set_background_color(fx_asset):
    """Sets the background color."""
    with Image(filename=str(fx_asset.join('croptest.png'))) as img:
        with Color('red') as color:
            img.background_color = color
            assert img.background_color == color


def test_set_get_matte_color(fx_asset):
    with Image(filename='rose:') as img:
        with Color('navy') as color:
            img.matte_color = color
            assert img.matte_color == color
            with raises(TypeError):
                img.matte_color = False


def test_transparentize(fx_asset):
    with Image(filename=str(fx_asset.join('croptest.png'))) as im:
        with Color('transparent') as transparent:
            with Color('black') as black:
                assert im[99, 100] == transparent
                assert im[100, 100] == black
                im.transparentize(0.3)
                assert im[99, 100] == transparent
                with im[100, 100] as c:
                    assert c.red == c.green == c.blue == 0
                    assert 0.69 < c.alpha < 0.71


def test_watermark(fx_asset):
    """Adds  watermark to an image."""
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        with Image(filename=str(fx_asset.join('watermark.png'))) as wm:
            a = img[70, 83]
            b = img[70, 84]
            c = img[623, 282]
            d = img[622, 281]
            img.watermark(wm, 0.3)
            assert img[70, 83] == a
            assert img[70, 84] != b
            assert img[623, 282] == c
            assert img[622, 281] != d


def test_reset_coords(fx_asset):
    """Reset the coordinate frame so to the upper-left corner of
    the image is (0, 0) again.

    """
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
            img.rotate(45, reset_coords=True)
            img.crop(0, 0, 170, 170)
            assert img[85, 85] == Color('transparent')


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


def test_channel_depths(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as i:
        assert dict(i.channel_depths) == {
            'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
            'undefined': 1, 'composite_channels': 8, 'index': 1,
            'rgb_channels': 1, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
            'default_channels': 8, 'black': 1, 'cyan': 8,
            'all_channels': 8, 'green': 8, 'magenta': 8, 'red': 8,
            'gray_channels': 1
        }
    with Image(filename=str(fx_asset.join('google.ico'))) as i:
        assert dict(i.channel_depths) == {
            'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
            'undefined': 1, 'composite_channels': 8, 'index': 1,
            'rgb_channels': 1, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
            'default_channels': 8, 'black': 1, 'cyan': 8, 'all_channels': 8,
            'green': 8, 'magenta': 8, 'red': 8, 'gray_channels': 1
        }


def test_channel_images(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as i:
        i.format = 'png'
        for name in 'opacity', 'alpha', 'true_alpha':
            expected_path = str(fx_asset.join('channel_images', name + '.png'))
            with Image(filename=expected_path) as expected:
                assert i.channel_images[name] == expected


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
        with orig.clone() as img:
            with Color('black') as color:
                with Image(width=w // 2, height=h // 2,
                           background=color) as cimg:
                    img.composite_channel('red', cimg, 'copy_red',
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


def test_compare(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as orig:
        with Image(filename=str(fx_asset.join('watermark_beach.jpg'))) as img:
            cmp_img, err = orig.compare(img, 'absolute')
            cmp_img, err = orig.compare(img, 'mean_absolute')
            cmp_img, err = orig.compare(img, 'root_mean_square')


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


def test_caption_without_font(fx_asset):
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        with raises(TypeError):
            img.caption(
                'Test message',
                left=5, top=144,
                width=134, height=20,
                gravity='center'
            )


def test_setfont(fx_asset):
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
        assert img.font_antialias == font.antialias
        assert img.font == font


def test_setgravity():
    with Image(width=144, height=192, background=Color('#1e50a2')) as img:
        img.gravity = 'center'
        assert img.gravity == 'center'


def test_negate_default(display, fx_asset):
    def test(c1, c2):
        assert (c1.red_int8 + c2.red_int8 == 255 and
                c1.green_int8 + c2.green_int8 == 255 and
                c1.blue_int8 + c2.blue_int8 == 255)
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        display(img)
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        img.negate()
        test(left_top, img[0, 0])
        test(left_bottom, img[0, -1])
        test(right_top, img[-1, 0])
        test(right_bottom, img[-1, -1])


def test_threshold(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        top = int(img.height * 0.25)
        btm = int(img.height * 0.75)
        print(img[0, top], img[0, btm])
        img.threshold(0.5)
        print(img[0, top], img[0, btm])
        with img[0, top] as white:
            assert white.red_int8 == white.green_int8 == white.blue_int8 == 255
        with img[0, btm] as black:
            assert black.red_int8 == black.green_int8 == black.blue_int8 == 0


def test_threshold_channel(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        top = int(img.height * 0.25)
        btm = int(img.height * 0.75)
        print(img[0, top], img[0, btm])
        img.threshold(0.0, 'red')
        img.threshold(0.5, 'green')
        img.threshold(1.0, 'blue')
        print(img[0, top], img[0, btm])
        # The top half of the image should be yellow, and the bottom half red.
        with img[0, top] as yellow:
            assert (yellow.red_int8 == yellow.green_int8 == 255 and
                    yellow.blue_int8 == 0)
        with img[0, btm] as red:
            assert (red.red_int8 == 255 and
                    red.green_int8 == red.blue_int8 == 0)


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


def test_normalize_default(display, fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        display(img)
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        print(left_top, left_bottom, right_top, right_bottom)
        img.normalize()
        display(img)
        print(img[0, 0], img[0, -1], img[-1, 0], img[-1, -1])
        assert img[0, 0] != left_top
        assert img[0, -1] != left_bottom
        assert img[-1, 0] != right_top
        assert img[-1, -1] != right_bottom
        with img[0, 0] as left_top:
            assert left_top.red == left_top.green == left_top.blue == 1
        with img[-1, -1] as right_bottom:
            assert (right_bottom.red == right_bottom.green ==
                    right_bottom.blue == 0)


def test_normalize_channel(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        left_top = img[0, 0]
        left_bottom = img[0, -1]
        right_top = img[-1, 0]
        right_bottom = img[-1, -1]
        img.normalize('red')
        assert img[0, 0] != left_top
        assert img[0, -1] != left_bottom
        assert img[-1, 0] != right_top
        assert img[-1, -1] != right_bottom
        # Normalizing the 'red' channel of gray_range.jpg should result in
        # top,left red channel == 255, and lower left red channel == 0
        assert img[0, 0].red_int8 == 255
        assert img[0, -1].red_int8 == 0
        # Just for fun, make sure we haven't altered any other color channels.
        for chan in ('blue', 'green'):
            c = chan + '_int8'
            assert getattr(img[0, 0], c) == getattr(left_top, c)
            assert getattr(img[0, -1], c) == getattr(left_bottom, c)
            assert getattr(img[-1, 0], c) == getattr(right_top, c)
            assert getattr(img[-1, -1], c) == getattr(right_bottom, c)


def test_level_default(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the levels to make this image entirely black
        img.level(1, 1)
        with img[0, 0] as dark:
            assert dark.red_int8 <= dark.green_int8 <= dark.blue_int8 <= 0
        with img[0, -1] as dark:
            assert dark.red_int8 <= dark.green_int8 <= dark.blue_int8 <= 0
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        # Adjust the levels to make this image entirely white
        img.level(0, 0)
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
            img.level(1, 1, channel=chan)
            assert(getattr(img[0, 0], c) <= 0)
            assert(getattr(img[0, -1], c) <= 0)
        with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
            # Adjust each channel level to make it entirely white
            img.level(0, 0, channel=chan)
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


def test_equalize(fx_asset):
    with Image(filename=str(fx_asset.join('gray_range.jpg'))) as img:
        print(img[0, 0], img[0, -1])
        img.equalize()
        print(img[0, 0], img[0, -1])
        # The top row should be nearly white, and the bottom nearly black.
        with img[0, 0] as light:
            assert light.red_int8 >= light.green_int8 >= light.blue_int8 >= 250
        with img[0, -1] as dark:
            assert dark.red_int8 <= dark.green_int8 <= dark.blue_int8 <= 5


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


def test_frame_error(fx_asset):
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        with raises(TypeError):
            img.frame(width='one')
        with raises(TypeError):
            img.frame(height=3.5)
        with raises(TypeError):
            img.frame(matte='green')
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
        with raises(AttributeError):
            with empty_wand.fx('8'):
                pass
    with Image(filename='rose:') as xc:
        with raises(OptionError):
            with xc.fx('/0'):
                pass
        with raises(TypeError):
            with xc.fx(('p[0,0]',)):
                pass
        with raises(ValueError):
            with xc.fx('p[0,0]', True):
                pass


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


def test_get_orientation(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.orientation == 'undefined'

    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        assert img.orientation == 'top_left'


def test_set_orientation(fx_asset):
    with Image(filename=str(fx_asset.join('beach.jpg'))) as img:
        img.orientation = 'bottom_right'
        assert img.orientation == 'bottom_right'


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


def test_gaussian_blur(fx_asset, display):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.gaussian_blur(30, 10)
        after = img[100, 100]
        assert before != after
        assert 0.84 <= after.red <= 0.851
        assert 0.74 <= after.green <= 0.75
        assert 0.655 <= after.blue < 0.67


def test_modulate(fx_asset, display):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.modulate(120, 120, 120)
        after = img[100, 100]
        assert before != after
        assert 0.98 <= after.red <= 0.99
        assert 0.98 <= after.green <= 0.99
        assert 0.96 <= after.blue <= 0.97


def test_unsharp_mask(fx_asset, display):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        before = img[100, 100]
        img.unsharp_mask(1.1, 1, 0.5, 0.001)
        after = img[100, 100]
        assert before != after
        assert 0.89 <= after.red <= 0.90
        assert 0.82 <= after.green <= 0.83
        assert 0.72 <= after.blue < 0.74


def test_compression(fx_asset):
    with Image(filename=str(fx_asset.join('sasha.jpg'))) as img:
        assert img.compression == 'group4'


def test_issue_150(fx_asset, tmpdir):
    """Should not be terminated with segmentation fault.

    https://github.com/dahlia/wand/issues/150

    """
    with Image(filename=str(fx_asset.join('tiger_hd-1920x1080.jpg'))) as img:
        img.format = 'pjpeg'
        with open(str(tmpdir.join('out.jpg')), 'wb') as f:
            img.save(file=f)


@mark.slow
def test_quantize(fx_asset):
    number_colors = 64
    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
        colors = set([color for row in img for color in row])
        assert len(colors) > number_colors

    with Image(filename=str(fx_asset.join('mona-lisa.jpg'))) as img:
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
        colors = set([color for row in img for color in row])
        assert colors
        assert len(colors) <= number_colors


def test_transform_colorspace(fx_asset):
    with Image(filename=str(fx_asset.join('cmyk.jpg'))) as img:
        with raises(TypeError):
            img.transform_colorspace('unknown')

        img.transform_colorspace('srgb')
        assert img.colorspace == 'srgb'


def test_merge_layers_basic(fx_asset):
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
        for method in IMAGE_LAYER_METHOD + ('', 'junk'):
            if method in ['merge', 'flatten', 'mosaic']:
                continue  # skip the valid ones
            with raises(TypeError):
                img.merge_layers(method)


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


def test_page_basic(fx_asset):
    with Image(filename=str(fx_asset.join('watermark.png'))) as img1:
        assert img1.page == (640, 480, 0, 0)
        assert img1.page_width == 640
        assert img1.page_height == 480
        assert img1.page_x == 0
        assert img1.page_y == 0


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
