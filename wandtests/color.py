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

