""":mod:`wand.sequence` --- Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import contextlib
import functools
import numbers

from .api import library
from .image import BaseImage, ClosedImageError, ImageProperty
from .version import MAGICK_VERSION_INFO


class Sequence(ImageProperty, collections.MutableSequence):

    def __init__(self, image):
        super(Sequence, self).__init__(image)
        self.instances = []

    def __del__(self):
        for instance in self.instances:
            if instance is not None:
                instance.c_resource = None

    @property
    def current_index(self):
        """(:class:`numbers.Integral`) The current index of
        its internal iterator.

        .. note::

           It's only for internal use.

        """
        return library.MagickGetIteratorIndex(self.image.wand)

    @current_index.setter
    def current_index(self, index):
        library.MagickSetIteratorIndex(self.image.wand, index)

    @contextlib.contextmanager
    def index_context(self, index):
        """Scoped setter of :attr:`current_index`.  Should be
        used for :keyword:`with` statement e.g.::

            with image.sequence.index_context(3):
                print image.size

        .. note::

           It's only for internal use.

        """
        index = self.validate_position(index)
        tmp_idx = self.current_index
        self.current_index = index
        yield index
        self.current_index = tmp_idx

    def __len__(self):
        return library.MagickGetNumberImages(self.image.wand)

    def validate_position(self, index):
        if not isinstance(index, numbers.Integral):
            raise TypeError('index must be integer, not ' + repr(index))
        length = len(self)
        if index >= length or index < -length:
            raise IndexError(
                'out of index: {0} (total: {1})'.format(index, length)
            )
        if index < 0:
            index += length
        return index

    def __getitem__(self, index):
        index = self.validate_position(index)
        instances = self.instances
        instances_length = len(instances)
        if index < instances_length:
            instance = instances[index]
            if instance is not None:
                return instance
        else:
            number_to_extend = index - instances_length + 1
            instances.extend(None for _ in xrange(number_to_extend))
        wand = self.image.wand
        tmp_idx = library.MagickGetIteratorIndex(wand)
        library.MagickSetIteratorIndex(wand, index)
        image = library.GetImageFromMagickWand(wand)
        exc = library.AcquireExceptionInfo()
        single_image = library.CloneImages(image, str(index), exc)
        library.DestroyExceptionInfo(exc)
        single_wand = library.NewMagickWandFromImage(single_image)
        library.MagickSetIteratorIndex(wand, tmp_idx)
        instance = SingleImage(single_wand)
        self.instances[index] = instance
        return instance

    def __setitem__(self, index, image):
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        with self.index_context(index) as index:
            library.MagickRemoveImage(self.image.wand)
            library.MagickAddImage(self.image.wand, image.wand)

    def __delitem__(self, index):
        with self.index_context(index) as index:
            library.MagickRemoveImage(self.image.wand)
            del self.instances[index]

    def insert(self, index, image):
        index = self.validate_position(index)
        instances = self.instances
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        if index == 0:
            tmp_idx = self.current_index
            self_wand = self.image.wand
            wand = image.wand
            try:
                # Prepending image into the list using MagickSetFirstIterator()
                # and MagickAddImage() had not worked properly, but was fixed
                # since 6.7.6-0 (rev7106).
                if MAGICK_VERSION_INFO >= (6, 7, 6, 0):
                    library.MagickSetFirstIterator(self_wand)
                    library.MagickAddImage(self_wand, wand)
                else:
                    self.current_index = 0
                    with self.image.clone() as clone:
                        i = len(clone.sequence) - 1
                        while i > 0:
                            del clone.sequence[i]
                            i -= 1
                        library.MagickAddImage(self_wand, clone.wand)
                    self.current_index = 0
                    library.MagickAddImage(self_wand, wand)
                    self.current_index = 0
                    library.MagickRemoveImage(self_wand)
            finally:
                self.current_index = tmp_idx
        else:
            with self.index_context(index - 1):
                library.MagickAddImage(self.image.wand, image.wand)
        self.instances.insert(index, None)

    def append(self, image):
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        wand = self.image.wand
        tmp_idx = self.current_index
        try:
            library.MagickSetLastIterator(wand)
            library.MagickAddImage(wand, image.sequence[0].wand)
        finally:
            self.current_index = tmp_idx
        self.instances.append(None)

    def extend(self, images):
        tmp_idx = self.current_index
        wand = self.image.wand
        try:
            library.MagickSetLastIterator(self.image.wand)
            if isinstance(images, type(self)):
                library.MagickAddImage(wand, images.image.wand)
            else:
                for image in images:
                    if not isinstance(image, BaseImage):
                        raise TypeError(
                            'images must consist of only instances of '
                            'wand.image.BaseImage, not ' + repr(image)
                        )
                    library.MagickAddImage(wand, image.wand)
        finally:
            self.current_index = tmp_idx


class SingleImage(BaseImage):

    def __repr__(self):
        cls = type(self)
        if getattr(self, 'c_resource', None) is None:
            return '<{0}.{1}: (closed)>'.format(cls.__module__, cls.__name__)
        return '<{0}.{1}: {2} ({3}x{4})>'.format(
            cls.__module__, cls.__name__,
            self.signature[:7], self.width, self.height
        )
