import os.path
import tempfile
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from attest import Tests, assert_hook, raises

from wand.image import ClosedImageError, Image
from wand.color import Color


tests = Tests()


def asset(filename):
    return os.path.join(os.path.dirname(__file__), 'assets', filename)


@tests.test
def new_from_file():
    """Opens an image from the file object."""
    with open(asset('mona-lisa.jpg'), 'rb') as f:
        with Image(file=f) as img:
            assert img.width == 402
    with raises(ClosedImageError):
        img.wand
    with open(asset('mona-lisa.jpg'), 'rb') as f:
        strio = StringIO.StringIO(f.read())
    with Image(file=strio) as img:
        assert img.width == 402
    strio.close()
    with raises(ClosedImageError):
        img.wand
    with raises(TypeError):
        Image(file='not file object')


@tests.test
def new_from_filename():
    """Opens an image through its filename."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand
    with raises(IOError):
        Image(filename=asset('not-exists.jpg'))


@tests.test
def new_from_blob():
    """Opens an image from blob."""
    with open(asset('mona-lisa.jpg'), 'rb') as f:
        blob = f.read()
    with Image(blob=blob) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand


@tests.test
def new_with_format():
    with open(asset('google.ico'), 'rb') as f:
        blob = f.read()
    with raises(Exception):
        Image(blob=blob)
    with Image(blob=blob, format='ico') as img:
        assert img.size == (16, 16)


@tests.test
def clone():
    """Cloens the existing image."""
    funcs = (lambda img: Image(image=img),
             lambda img: img.clone())
    with Image(filename=asset('mona-lisa.jpg')) as img:
        for func in funcs:
            with func(img) as cloned:
                assert img.wand is not cloned.wand
                assert img.size == cloned.size
            with raises(ClosedImageError):
                cloned.wand
    with raises(ClosedImageError):
        img.wand


@tests.test
def save_to_filename():
    """Saves an image to the filename."""
    savefile = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    with Image(filename=asset('mona-lisa.jpg')) as orig:
        orig.save(filename=savefile)
        with raises(IOError):
            orig.save(filename=os.path.join(savefile, 'invalid.jpg'))
        with raises(TypeError):
            orig.save(filename=1234)
    assert os.path.isfile(savefile)
    with Image(filename=savefile) as saved:
        assert saved.size == (402, 599)
    os.remove(savefile)


@tests.test
def save_to_file():
    """Saves an image to the Python file object."""
    buffer = StringIO.StringIO()
    with tempfile.TemporaryFile() as savefile:
        with Image(filename=asset('mona-lisa.jpg')) as orig:
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


@tests.test
def save_error():
    filename = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    fileobj = StringIO.StringIO()
    with Image(filename=asset('mona-lisa.jpg')) as orig:
        with raises(TypeError):
            orig.save()
        with raises(TypeError):
            orig.save(filename=filename, file=fileobj)


@tests.test
def make_blob():
    """Makes a blob string."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with Image(blob=img.make_blob('png')) as img2:
            assert img2.size == (402, 599)
            assert img2.format == 'PNG'
        assert img.format == 'JPEG'
        with raises(TypeError):
            img.make_blob(123)


@tests.test
def size():
    """Gets the image size."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.size == (402, 599)
        assert img.width == 402
        assert img.height == 599
        assert len(img) == 599

@tests.test
def get_depth():
    """Gets the image depth"""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.depth == 8

@tests.test
def set_depth():
    """Sets the image depth"""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        img.depth = 16
        assert img.depth == 16

@tests.test
def get_format():
    """Gets the image format."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.format == 'JPEG'
    with Image(filename=asset('croptest.png')) as img:
        assert img.format == 'PNG'


@tests.test
def set_format():
    """Sets the image format."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        img.format = 'png'
        assert img.format == 'PNG'
        strio = StringIO.StringIO()
        img.save(file=strio)
        strio.seek(0)
        with Image(file=strio) as png:
            assert png.format == 'PNG'
        with raises(ValueError):
            img.format = 'HONG'
        with raises(TypeError):
            img.format = 123


@tests.test
def get_compression():
    """Gets the image compression quality."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.compression_quality == 80


@tests.test
def set_compression():
    """Sets the image compression quality."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        img.compression_quality = 50
        assert img.compression_quality == 50
        strio = StringIO.StringIO()
        img.save(file=strio)
        strio.seek(0)
        with Image(file=strio) as jpg:
            assert jpg.compression_quality == 50
        with raises(TypeError):
            img.compression_quality = 'high'


@tests.test
def strip():
    """Strips the image of all profiles and comments."""
    with Image(filename=asset('beach.jpg')) as img:
        strio = StringIO.StringIO()
        img.save(file=strio)
        len_unstripped = strio.tell()
        strio.truncate(0)
        img.strip()
        img.save(file=strio)
        len_stripped = strio.tell()
        assert len_unstripped > len_stripped


@tests.test
def trim():
    """Remove transparent area around image."""
    with Image(filename=asset('trimtest.png')) as img:
        oldx, oldy = img.size
        print img.trim()
        newx, newy = img.size
        assert newx < oldx
        assert newy < oldy


@tests.test
def get_mimetype():
    """Gets mimetypes of the image."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.mimetype in ('image/jpeg', 'image/x-jpeg')
    with Image(filename=asset('croptest.png')) as img:
        assert img.mimetype in ('image/png', 'image/x-png')


@tests.test
def convert():
    """Converts the image format."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with img.convert('png') as converted:
            assert converted.format == 'PNG'
            strio = StringIO.StringIO()
            converted.save(file=strio)
            strio.seek(0)
            with Image(file=strio) as png:
                assert png.format == 'PNG'
        with raises(ValueError):
            img.convert('HONG')
        with raises(TypeError):
            img.convert(123)


@tests.test
def iterate():
    """Uses iterator."""
    with Color('#000') as black:
        with Color('transparent') as transparent:
            with Image(filename=asset('croptest.png')) as img:
                for i, row in enumerate(img):
                    assert len(row) == 300
                    if i % 3:
                        continue # avoid slowness
                    if 100 <= i < 200:
                        for x, color in enumerate(row):
                            if x % 3:
                                continue # avoid slowness
                            if 100 <= x < 200:
                                assert color == black
                            else:
                                assert color == transparent
                    else:
                        for color in row:
                            assert color == transparent
                assert i == 299


@tests.test
def slice_clone():
    """Clones using slicing."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with img[:,:] as cloned:
            assert img.size == cloned.size


@tests.test
def slice_invalid_types():
    """Slicing with invalid types should throw exceptions."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
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
    with Image(filename=asset('croptest.png')) as img:
        with raises(IndexError):
            img[300, 300]
        with raises(IndexError):
            img[-301, -301]


@tests.test
def index_pixel():
    """Gets a pixel."""
    with Image(filename=asset('croptest.png')) as img:
        assert img[0, 0] == Color('transparent')
        assert img[99, 99] == Color('transparent')
        assert img[100, 100] == Color('black')
        assert img[150, 150] == Color('black')
        assert img[-200, -200] == Color('black')
        assert img[-201, -201] == Color('transparent')


@tests.test
def index_row():
    """Gets a row."""
    with Color('transparent') as transparent:
        with Color('black') as black:
            with Image(filename=asset('croptest.png')) as img:
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


@tests.test
def slice_crop():
    """Crops using slicing."""
    with Image(filename=asset('croptest.png')) as img:
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


@tests.test
def crop():
    """Crops in-place."""
    with Image(filename=asset('croptest.png')) as img:
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


@tests.test
def crop_error():
    """Crop errors."""
    with Image(filename=asset('croptest.png')) as img:
        with raises(TypeError):
            img.crop(right=1, width=2)
        with raises(TypeError):
            img.crop(bottom=1, height=2)


@tests.test
def resize():
    """Resizes the image."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with img.clone() as a:
            assert a.size == (402, 599)
            a.resize(100, 100)
            assert a.size == (100, 100)
        with img.clone() as b:
            assert b.size == (402, 599)
            b.resize(height=100)
            assert b.size == (402, 100)
        with img.clone() as c:
            assert c.size == (402, 599)
            c.resize(width=100)
            assert c.size == (100, 599)


@tests.test
def resize_errors():
    """Resizing errors."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with raises(TypeError):
            img.resize(width='100')
        with raises(TypeError):
            img.resize(height='100')
        with raises(ValueError):
            img.resize(width=0)
        with raises(ValueError):
            img.resize(height=0)
        with raises(ValueError):
            img.resize(width=-5)
        with raises(ValueError):
            img.resize(height=-5)


@tests.test
def rotate():
    """Rotates an image."""
    with Image(filename=asset('rotatetest.gif')) as img:
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


@tests.test
def signature():
    """Gets the image signature."""
    sig = '763774301b62cf9ea033b661f5136fbda7e8de96254aec3dd0dff63c05413a1e'
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.signature == sig
        img.format = 'png'
        assert img.signature == sig


@tests.test
def equal():
    """Equals (``==``) and not equals (``!=``) operators."""
    with Image(filename=asset('mona-lisa.jpg')) as a:
        with Image(filename=asset('mona-lisa.jpg')) as a2:
            assert a == a2
            assert not (a != a2)
        with Image(filename=asset('sasha.jpg')) as b:
            assert a != b
            assert not (a == b)
        with a.convert('png') as a3:
            assert a == a3
            assert not (a != a3)


@tests.test
def object_hash():
    """Gets :func:`hash()` of the image."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        a = hash(img)
        img.format = 'png'
        b = hash(img)
        assert a == b


@tests.test
def get_background_color():
    """Gets the background color."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert Color('white') == img.background_color


@tests.test
def set_background_color():
    """Sets the background color."""
    with Image(filename=asset('croptest.png')) as img:
        with Color('transparent') as color:
            img.background_color = color
            assert img.background_color == color


@tests.test
def watermark():
    """Adds  watermark to an image."""
    with Image(filename=asset('beach.jpg')) as img:
        with Image(filename=asset('watermark.png')) as wm:
            img.watermark(wm, 0.3)
            with Image(filename=asset('marked.png')) as marked:
                msg = 'img = {0!r}, marked = {1!r}'.format(
                    img.signature, marked.signature)
                assert img == marked, msg


@tests.test
def reset_coords():
    """Reset the coordinate frame so to the upper-left corner of
    the image is (0, 0) again.

    """
    with Image(filename=asset('sasha.jpg')) as img:
            img.rotate(45, reset_coords=True)
            img.crop(0, 0, 170, 170)
            with Image(filename=asset('resettest.png')) as control:
                msg = 'img = {0!r}, control = {1!r}'.format(
                    img.signature, control.signature)
                assert img == control, msg
