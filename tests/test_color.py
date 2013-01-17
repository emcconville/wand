from wand.color import Color
import unittest


class ColorTests(unittest.TestCase):
    def test_equals(self):
        """Equality test."""
        assert Color('#fff') == Color('#ffffff') == Color('white')
        assert Color('#000') == Color('#000000') == Color('black')
        assert Color('rgba(0, 0, 0, 0)') == Color('rgba(0, 0, 0, 0)')
        assert Color('rgba(0, 0, 0, 0)') == Color('rgba(1, 1, 1, 0)')


    def test_not_equals(self):
        """Equality test."""
        assert Color('#000') != Color('#fff')
        assert Color('rgba(0, 0, 0, 0)') != Color('rgba(0, 0, 0, 1)')
        assert Color('rgba(0, 0, 0, 1)') != Color('rgba(1, 1, 1, 1)')

