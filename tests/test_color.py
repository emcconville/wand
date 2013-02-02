import unittest
from wand.color import Color


class ColorTests(unittest.TestCase):
    def test_equals(self):
        """Equality test."""

        self.assertEqual(Color('#fff'), Color('#ffffff'))
        self.assertEqual(Color('#ffffff'), Color('white'))

        self.assertEqual(Color('#000'), Color('#000000'))
        self.assertEqual(Color('#000000'), Color('black'))

        self.assertEqual(Color('rgba(0, 0, 0, 0)'), Color('rgba(0, 0, 0, 0)'))
        self.assertEqual(Color('rgba(0, 0, 0, 0)'), Color('rgba(1, 1, 1, 0)'))


    def test_not_equals(self):
        """Equality test."""

        self.assertNotEqual(Color('#000'), Color('#fff'))
        self.assertNotEqual(Color('rgba(0, 0, 0, 0)'), Color('rgba(0, 0, 0, 1)'))
        self.assertNotEqual(Color('rgba(0, 0, 0, 1)'), Color('rgba(1, 1, 1, 1)'))
