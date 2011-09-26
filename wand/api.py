""":mod:`wand.api` --- Low-level interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import platform
import ctypes
import ctypes.util


def load_library():
    """Loads the MagickWand library.

    :returns: the MagickWand library
    :rtype: :class:`ctypes.CDLL`

    """
    return ctypes.CDLL(ctypes.util.find_library('MagickWand'))


library = load_library()

