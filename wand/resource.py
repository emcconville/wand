""":mod:`wand.resource` --- Global resource management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is the global resource to manage in MagickWand API. This module
implements automatic global resource management through reference counting.

"""
from .api import library


__all__ = ('is_instantiated', 'genesis', 'terminus', 'increment_refcount',
           'decrement_refcount')


def genesis():
    """Instantiates the MagickWand API.

    .. warning::
    
       Don't call this function directly. Use :func:`increment_refcount()` and
       :func:`decrement_refcount()` functions instead.

    """
    library.MagickWandGenesis()


def terminus():
    """Cleans up the MagickWand API.

    .. warning::
    
       Don't call this function directly. Use :func:`increment_refcount()` and
       :func:`decrement_refcount()` functions instead.

    """
    library.MagickWandTerminus()


#: (:class:`numbers.Integral`) The internal integer value that maintains
#: the number of referenced objects.
#:
#: .. warning::
#:
#:    Don't touch this global variable. Use :func:`increment_refcount()` and
#:    :func:`decrement_refcount()` functions instead.
#:
reference_count = 0


def increment_refcount():
    """Increments the :data:`reference_count` and instantiates the MagickWand
    API if it is the first use.

    """
    global reference_count
    if reference_count:
        reference_count += 1
    else:
        genesis()
        reference_count = 1


def decrement_refcount():
    """Decrements the :data:`reference_count` and cleans up the MagickWand
    API if it will be no more used.

    """
    global reference_count
    if not reference_count:
        raise RuntimeError('wand.resource.reference_count is already zero')
    reference_count -= 1
    if not reference_count:
        terminus()

