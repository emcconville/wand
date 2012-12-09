# -*- coding: utf-8 -*-

from .api import library
from .image import Image


class Sequence(object):
    """
    MagickWand's image sequences manager.

    :param image: An `Image` instance
    :type image: :class:`Image`
    """

    def __init__(self, image, clone_by_default=True):
        if not isinstance(image, Image):
            raise TypeError('expected a wand.image.Image instance, '
                            'not ' + repr(image))

        if not image.has_sequence():
            raise ValueError("Current image does not have secuence.")

        self.image = image
        self.clone = clone_by_default

    def __len__(self):
        return library.MagickGetNumberImages(self.image.wand)

    def __getitem__(self, index):
        if self.clone:
            image = self.image.clone()
        else:
            image = self.image

        library.MagickSetIteratorIndex(image.wand, index)
        return image

    def get_current_index(self):
        return library.MagickGetIteratorIndex(self.image.wand)

    def append(self, image):
        self.insert(len(self) - 1, image)

    def insert(self, index, image):
        if not isinstance(image, Image):
            raise TypeError('expected a wand.image.Image instance, '
                            'not ' + repr(image))

        if not 0 <= index < len(self):
            raise TypeError('value could be between 0 and %s' % len(self))

        current_index = self.get_current_index()
        library.MagickSetIteratorIndex(self.image.wand, index)
        library.MagickAddImage(self.image.wand, image.wand)
        library.MagickSetIteratorIndex(self.image.wand, current_index)
