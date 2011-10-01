import os.path
import tempfile
from attest import assert_hook, Tests, raises
from wand.image import Image, ClosedImageError


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
        orig.save(savefile)
    assert os.path.isfile(savefile)
    with Image(filename=savefile) as saved:
        assert saved.size == (402, 599)
    os.remove(savefile)


@tests.test
def size():
    """Gets the image size."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.size == (402, 599)
        assert img.width == 402
        assert img.height == 599


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

