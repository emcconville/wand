from attest import Tests, assert_hook, raises

from wand.color import Color


tests = Tests()


@tests.test
def equals():
    """Equality test."""
    assert Color('#fff') == Color('#ffffff') == Color('white')
    assert Color('#000') == Color('#000000') == Color('black')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(0, 0, 0, 0)')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(1, 1, 1, 0)')


@tests.test
def not_equals():
    """Equality test."""
    assert Color('#000') != Color('#fff')
    assert Color('rgba(0, 0, 0, 0)') != Color('rgba(0, 0, 0, 1)')
    assert Color('rgba(0, 0, 0, 1)') != Color('rgba(1, 1, 1, 1)')


@tests.test
def red():
    assert Color('black').red == 0
    assert Color('red').red == 1
    assert Color('white').red == 1
    assert 0.5 <= Color('rgba(128, 0, 0, 1)').red < 0.51


@tests.test
def green():
    assert Color('black').green == 0
    assert Color('#0f0').green == 1
    assert Color('white').green == 1
    assert 0.5 <= Color('rgba(0, 128, 0, 1)').green < 0.51


@tests.test
def blue():
    assert Color('black').blue == 0
    assert Color('blue').blue == 1
    assert Color('white').blue == 1
    assert 0.5 <= Color('rgba(0, 0, 128, 1)').blue < 0.51
