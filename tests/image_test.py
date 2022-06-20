# -*- coding: utf-8 -*-
#
# These tests cover the basic I/O & pythonic interfaces of the Image class.
#
import codecs
import io
import os
import os.path
import shutil
import struct
import sys
import tempfile

from pytest import mark, raises

from wand.image import ClosedImageError, Image
from wand.color import Color
from wand.compat import PY3, text, text_type
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

try:
    import numpy as np
except ImportError:
    np = None


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
    with raises(ValueError):
        Image(width=0, height=0)
    with Image(width=20, height=10) as img:
        assert img[10, 5] == transparent
    with Image(width=20, height=10, background=gray) as img:
        assert img.size == (20, 10)
        assert img[10, 5] == gray
    with Image(width=20, height=10, background='#ccc') as img:
        assert img.size == (20, 10)
        assert img[10, 5] == gray


def test_raw_image(fx_asset):
    b = b"".join([struct.pack("BBB", i, j, 0)
                  for i in range(256) for j in range(256)])
    with raises(ValueError):
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
    """https://github.com/emcconville/wand/issues/122"""
    filename = '모나리자.jpg'
    if not PY3:
        filename = filename.decode('utf-8')
    path = os.path.join(text_type(tmpdir), filename)  # workaround py.path bug
    shutil.copyfile(str(fx_asset.join('mona-lisa.jpg')), path)
    with Image() as img:
        img.read(filename=text(path))
        assert img.width == 402


def test_read_with_colorspace(fx_asset):
    fpath = str(fx_asset.join('cmyk.jpg'))
    with Image(filename=fpath,
               colorspace='srgb',
               units='pixelspercentimeter') as img:
        assert img.units == 'pixelspercentimeter'


def test_read_with_extract():
    with Image(filename='rose:', extract="10x10+10+10") as img:
        assert (10, 10) == img.size
    with Image() as img:
        img.read(filename='rose:', extract="10x10+10+10")
        assert (10, 10) == img.size


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
    """https://github.com/emcconville/wand/issues/122"""
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


def test_new_from_pseudo(fx_asset):
    with Image() as img:
        img.pseudo(10, 10, 'xc:none')
        assert img.size == (10, 10)


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


def test_image_add():
    with Image(filename='rose:') as a:
        with Image(filename='rose:') as b:
            a.image_add(b)
        assert a.iterator_length() == 2
    with raises(TypeError):
        with Image(filename='rose:') as img:
            img.image_add(0xdeadbeef)


def test_image_get():
    with Image(filename='rose:') as img:
        with img.image_get() as i:
            assert isinstance(i, Image)


def test_image_remove():
    with Image(filename='null:') as empty:
        empty.image_remove()
        assert empty.iterator_length() == 0


def test_image_set():
    with Image(filename='null:') as a:
        with Image(filename='rose:') as b:
            a.image_set(b)
        assert a.iterator_length() == 1


def test_image_swap():
    with Image(width=1, height=1, background='red') as a:
        a.read(filename='xc:green')
        a.read(filename='xc:blue')
        was = a.iterator_get()
        a.image_swap(0, 2)
        assert a.iterator_get() == was
    with raises(TypeError):
        a.image_swap('a', 'b')


def test_ping_from_filename(fx_asset):
    file_path = str(fx_asset.join('mona-lisa.jpg'))
    with Image.ping(filename=file_path) as img:
        assert img.size == (402, 599)


def test_ping_from_blob(fx_asset):
    blob = fx_asset.join('mona-lisa.jpg').read('rb')
    with Image.ping(blob=blob) as img:
        assert img.size == (402, 599)


def test_ping_from_file(fx_asset):
    with fx_asset.join('mona-lisa.jpg').open('rb') as fd:
        with Image.ping(file=fd) as img:
            assert img.size == (402, 599)


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
    pbm = b'''P1
    4 4
    0 1 0 1
    1 0 1 0
    0 1 0 1
    1 0 1 0
    '''
    png = None
    with Image(blob=pbm, format='pbm') as img:
        assert img.size == (4, 4)
        img.format = 'PNG'
        png = img.make_blob()
    with Image(blob=png, format='png') as img:
        assert img.size == (4, 4)
        assert img.format == 'PNG'


def test_montage():
    with Image() as base:
        for label in ['foo', 'bar', 'baz']:
            with Image(width=10, height=10, pseudo='plasma:') as img:
                img.options['label'] = label
                base.image_add(img)
        style = Font('monospace', 16, 'blue', False, 'orange')
        base.montage(font=style, tile="2x2", thumbnail="16x16", mode="frame",
                     frame="5x5")
        assert base.iterator_length() == 1


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
                    if i % 30:
                        continue  # avoid slowness
                    if 100 <= i < 200:
                        for x, color in enumerate(row):
                            if x % 30:
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


def test_index_pixel_set(fx_asset):
    with Image(filename='rose:') as img:
        with Color('black') as dot:
            img[0, 0] = dot
            assert img[0, 0] == dot
            img[0, 0] = 'black'
            assert img[0, 0] == dot
        img.colorspace = 'gray'
        with Color('gray50') as dot:
            img[0, 0] = dot
            assert img[0, 0] == dot
        img.colorspace = 'cmyk'
        with Color('cmyk(255, 0, 0, 0') as dot:
            img[0, 0] = dot
            assert img[0, 0] == dot
        with raises(TypeError):
            img[0, 0] = 1
        with raises(TypeError):
            img[0xDEADBEEF] = Color('black')
        with raises(ValueError):
            img[1, 2, 3] = Color('black')
        with raises(TypeError):
            img[0.5, "d"] = Color('black')


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


def test_issue_150(fx_asset, tmpdir):
    """Should not be terminated with segmentation fault.

    https://github.com/emcconville/wand/issues/150

    """
    with Image(filename=str(fx_asset.join('tiger_hd-1920x1080.jpg'))) as img:
        img.format = 'pjpeg'
        with open(str(tmpdir.join('out.jpg')), 'wb') as f:
            img.save(file=f)


@mark.skipif(np is None, reason='Numpy not available.')
def test_from_array():
    # From float values.
    rand = np.random.rand(10, 10, 4)
    # We should have a 10x10 image with RGBA data created.
    with Image.from_array(rand) as img:
        assert img.size == (10, 10)
        assert img.alpha_channel
    # From char values
    red8 = np.zeros([10, 10, 3], dtype=np.uint8)
    red8[:, :] = [0xFF, 0x00, 0x00]
    # We should have a RED image.
    with Image.from_array(red8) as img:
        assert img[0, 0] == Color('#F00')
    # From short values.
    green16 = np.zeros([10, 10, 3], dtype=np.uint16)
    green16[:, :] = [0x0000, 0xFFFF, 0x0000]
    # We should have a GREEN image.
    with Image.from_array(green16) as img:
        assert img[0, 0] == Color('#00FF00')


@mark.skipif(np is None, reason='Numpy not available.')
def test_array_interface():
    with Image(filename='rose:') as img:
        img.alpha_channel = 'off'
        array = np.array(img)
        assert array.shape == (46, 70, 3)
    with Image(filename='rose:') as img:
        img.alpha_channel = 'off'
        img.transform_colorspace('gray')
        array = np.array(img)
        assert array.shape == (46, 70, 1)
    with Image(filename='rose:') as img:
        img.alpha_channel = 'off'
        img.transform_colorspace('cmyk')
        array = np.array(img)
        assert array.shape == (46, 70, 4)


@mark.skipif(np is None, reason='Numpy not available.')
def test_numpy_array_hairpinning():
    with Image(filename='rose:') as left:
        with Image.from_array(left) as right:
            assert left.size == right.size


def test_data_url():
    with Image(filename='rose:') as img:
        img.format = 'PNG'
        data = img.data_url()
        assert data.startswith('data:image/png;base64,')
