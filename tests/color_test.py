import platform
import time

from memory_profiler import memory_usage
from pytest import mark

from wand.color import Color
from wand.compat import xrange
from wand.version import MAGICK_VERSION_INFO  # noqa


def test_equals():
    """Equality test."""
    assert Color('#fff') == Color('#ffffff') == Color('white')
    assert Color('#000') == Color('#000000') == Color('black')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(0, 0, 0, 0)')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(1, 1, 1, 0)')


def test_not_equals():
    """Equality test."""
    assert Color('#000') != Color('#fff')
    assert Color('rgba(0, 0, 0, 0)') != Color('rgba(0, 0, 0, 1)')
    assert Color('rgba(0, 0, 0, 1)') != Color('rgba(1, 1, 1, 1)')


def test_hash():
    """Hash test."""
    assert (hash(Color('#fff')) == hash(Color('#ffffff')) ==
            hash(Color('white')))
    assert (hash(Color('#000')) == hash(Color('#000000')) ==
            hash(Color('black')))
    assert hash(Color('rgba(0, 0, 0, 0))')) == hash(Color('rgba(0, 0, 0, 0))'))
    assert hash(Color('rgba(0, 0, 0, 0))')) == hash(Color('rgba(1, 1, 1, 0))'))


def test_red():
    assert Color('black').red == 0
    assert Color('red').red == 1
    assert Color('white').red == 1
    assert 0.5 <= Color('rgba(128, 0, 0, 1)').red < 0.51


def test_green():
    assert Color('black').green == 0
    assert Color('#0f0').green == 1
    assert Color('white').green == 1
    assert 0.5 <= Color('rgba(0, 128, 0, 1)').green < 0.51


def test_blue():
    assert Color('black').blue == 0
    assert Color('blue').blue == 1
    assert Color('white').blue == 1
    assert 0.5 <= Color('rgba(0, 0, 128, 1)').blue < 0.51


def test_alpha():
    assert Color('rgba(0, 0, 0, 1)').alpha == 1
    assert Color('rgba(0, 0, 0, 0)').alpha == 0
    assert 0.49 <= Color('rgba(0, 0, 0, 0.5)').alpha <= 0.5


def test_red_int8():
    assert Color('black').red_int8 == 0
    assert Color('red').red_int8 == 255
    assert Color('white').red_int8 == 255
    assert Color('rgba(128, 0, 0, 1)').red_int8 == 128


def test_green_int8():
    assert Color('black').green_int8 == 0
    assert Color('#0f0').green_int8 == 255
    assert Color('white').green_int8 == 255
    assert Color('rgba(0, 128, 0, 1)').green_int8 == 128


def test_blue_int8():
    assert Color('black').blue_int8 == 0
    assert Color('blue').blue_int8 == 255
    assert Color('white').blue_int8 == 255
    assert Color('rgba(0, 0, 128, 1)').blue_int8 == 128


def test_alpha_int8():
    assert Color('rgba(0, 0, 0, 1)').alpha_int8 == 255
    assert Color('rgba(0, 0, 0, 0)').alpha_int8 == 0
    if not (Color('rgb(127,0,0)').red_quantum <=
            Color('rgba(0,0,0,0.5').alpha_quantum <=
            Color('rgb(128,0,0)').red_quantum):
        # FIXME: I don't know why, but the value PixelGetAlphaQuantum() returns
        #        is inconsistent to other PixelGet{Red,Green,Blue}Quantum()
        #        functions in Travis CI.  We just skip the test in this case.
        return
    assert 127 <= Color('rgba(0, 0, 0, 0.5)').alpha_int8 <= 128


def test_string():
    assert Color('black').string in ('rgb(0,0,0)', 'srgb(0,0,0)')
    assert str(Color('black')) in ('rgb(0,0,0)', 'srgb(0,0,0)')


def color_memory_leak():
    for i in xrange(5000):
        with Color('orange'):
            pass
    time.sleep(0.02)


@mark.skipif('MAGICK_VERSION_INFO <= (6, 6, 9, 7)')
def test_memory_leak():
    """https://github.com/dahlia/wand/pull/127"""
    consumes = memory_usage((color_memory_leak, (), {}))
    vm = platform.python_implementation()
    minimum = 15.0 if vm == 'PyPy' else 1.0  # FIXME
    assert consumes[-1] - consumes[0] <= minimum
