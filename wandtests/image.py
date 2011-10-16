import os.path
import contextlib
import tempfile
from attest import assert_hook, Tests, raises
from wand.image import Image, ClosedImageError
from wand.color import Color


tests = Tests()


def asset(filename):
    return os.path.join(os.path.dirname(__file__), 'assets', filename)


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
    with open(asset('mona-lisa.jpg')) as f:
        blob = f.read()
    with Image(blob=blob) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand


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
def save():
    """Saves an image."""
    savefile = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    with Image(filename=asset('mona-lisa.jpg')) as orig:
        orig.save(filename=savefile)
        with raises(IOError):
            orig.save(filename=os.path.join(savefile, 'invalid.jpg'))
    assert os.path.isfile(savefile)
    with Image(filename=savefile) as saved:
        assert saved.size == (402, 599)
    os.remove(savefile)


@tests.test
def make_blob():
    """Makes a blob string."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        with Image(blob=img.make_blob('png')) as img2:
            assert img2.size == (402, 599)
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
        with raises(ValueError):
            img[1:1, :]
        with raises(ValueError):
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
    with Color('#000') as black:
        with Image(filename=asset('croptest.png')) as img:
            with img[100:200, 100:200] as cropped:
                assert cropped.size == (100, 100)
                for row in cropped:
                    for col in row:
                        assert col == black
            with img[150:, :150] as cropped:
                assert cropped.size == (150, 150)
            with img[-200:-100, -200:-100] as cropped:
                assert cropped.size == (100, 100)
            with img[100:200] as cropped:
                assert cropped.size == (300, 100)


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

