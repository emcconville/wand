""":mod:`wand.font` --- Font
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 0.1.2

"""
import ctypes
import numbers

from .color import Color

__all__ = 'Font',


class Font(object):
    raw_path = None
    raw_size = None
    raw_color = None
    raw_antialias = None

    def __init__(self, path=None, size=None, color=None, antialias=None):
        if path is not None:
            self.path = path
        if size is not None:
            self.size = size
        if color is not None:
            self.color = color
        if antialias is not None:
            self.antialias = antialias

    @property
    def path(self):
        return self.raw_path

    @path.setter
    def path(self, path):
        if not isinstance(path, basestring):
            raise TypeError('path must be a string, not ' + repr(path))
        self.raw_path = path

    @property
    def size(self):
        return self.raw_size

    @size.setter
    def size(self, size):
        if not isinstance(size, numbers.Real):
            raise TypeError('size must be a real number, not ' + repr(size))
        self.raw_size = size

    @property
    def color(self):
        return self.raw_color

    @color.setter
    def color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color, not ' + repr(color))
        self.raw_color = color

    @property
    def antialias(self):
        return self.raw_antialias

    @antialias.setter
    def antialias(self, antialias):
        if not isinstance(antialias, bool):
            raise TypeError('antialias must be a bool, not ' + repr(antialias))
        self.raw_antialias = antialias
