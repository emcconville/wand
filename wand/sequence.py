""":mod:`wand.sequence` --- Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import contextlib
import functools
import numbers

from .api import library
from .image import BaseImage, ClosedImageError, ImageProperty


class Sequence(ImageProperty, collections.MutableSequence):

    def __init__(self, image):
        super(Sequence, self).__init__(image)
        self.instances = []

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
            if instance is not None and instance.index is not None:
                return instance
        else:
            number_to_extend = index - instances_length + 1
            instances.extend(None for _ in xrange(number_to_extend))
        instance = SingleImage(self.image.wand, index)
        self.instances[index] = instance
        return instance

    def __setitem__(self, index, image):
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        with self.index_context(index) as index:
            library.MagickRemoveImage(self.image.wand)
            library.MagickAddImage(self.image.wand, image.wand)
            instances = self.instances
            if index < len(instances):  # detach
                instance = instances[index]
                instance.index = None
                instances[index] = None

    def __delitem__(self, index):
        with self.index_context(index) as index:
            library.MagickRemoveImage(self.image.wand)
            instances = self.instances
            if index < len(instances):  # detach
                instance = instances[index]
                instance.index = None
                del instances[index]

    def insert(self, index, image):
        index = self.validate_position(index)
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        if index == 0:
            tmp_idx = self.current_index
            try:
                library.MagickSetFirstIterator(self.image.wand)
                library.MagickAddImage(self.image.wand, image.wand)
            finally:
                self.current_index = tmp_idx
        else:
            with self.index_context(index - 1):
                library.MagickAddImage(self.image.wand, image.wand)
        instances = self.instances
        if index < len(instances):  # reallocate
            for instance in instances[index:]:
                if instance is not None:
                    instance.index += 1
            instances.insert(index, None)

    def append(self, image):
        if not isinstance(image, BaseImage):
            raise TypeError('image must be an instance of wand.image.'
                            'BaseImage, not ' + repr(image))
        wand = self.image.wand
        tmp_idx = self.current_index
        try:
            library.MagickSetLastIterator(wand)
            if isinstance(image, SingleImage):
                with image.clone() as cloned:
                    library.MagickAddImage(wand, cloned.wand)
            else:
                library.MagickAddImage(wand, image.wand)
        finally:
            self.current_index = tmp_idx

    def extend(self, images):
        tmp_idx = self.current_index
        wand = self.image.wand
        try:
            library.MagickSetLastIterator(self.image.wand)
            if isinstance(images, type(self)):
                library.MagickAddImage(wand, images.image.wand)
            else:
                for image in images:
                    if isinstance(image, SingleImage):
                        with image.clone() as cloned:
                            library.MagickAddImage(wand, cloned.wand)
                    elif not isinstance(image, BaseImage):
                        raise TypeError(
                            'images must consist of only instances of '
                            'wand.image.BaseImage, not ' + repr(image)
                        )
                    else:
                        library.MagickAddImage(wand, image.wand)
        finally:
            self.current_index = tmp_idx


class SingleImage(BaseImage):

    def __init__(self, wand, index):
        self.index = index
        super(SingleImage, self).__init__(wand)

    def __getattribute__(self, name):
        this = super(SingleImage, self)
        if name.startswith('c_') or name in ('resource', 'wand', 'index'):
            return this.__getattribute__(name)
        wand = self.wand
        tmp_idx = library.MagickGetIteratorIndex(wand)
        library.MagickSetIteratorIndex(wand, self.index)
        value = this.__getattribute__(name)
        library.MagickSetIteratorIndex(wand, tmp_idx)
        if callable(value):
            @functools.wraps(value)
            def patched(*args, **kwargs):
                tmp_idx = library.MagickGetIteratorIndex(wand)
                library.MagickSetIteratorIndex(wand, self.index)
                result = value(*args, **kwargs)
                library.MagickSetIteratorIndex(wand, tmp_idx)
                return result
            return patched
        return value

    @property
    def wand(self):
        if self.index is None:
            raise ClosedImageError(repr(self) + ' is detached')
        return super(SingleImage, self).wand

    @wand.setter
    def wand(self, wand):
        self.resource = wand

    @wand.deleter
    def wand(self):
        del self.resource

    def clone_wand(self):
        image = library.GetImageFromMagickWand(self.wand)
        exc = library.AcquireExceptionInfo()
        cloned = library.CloneImages(image, str(self.index), exc)
        library.DestroyExceptionInfo(exc)
        return library.NewMagickWandFromImage(cloned)
