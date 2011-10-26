""":mod:`wand.api` --- Low-level interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import os.path
import platform
import ctypes
import ctypes.util


def load_library():
    """Loads the MagickWand library.

    :returns: the MagickWand library
    :rtype: :class:`ctypes.CDLL`

    """
    libpath = None
    try:
        magick_home = os.environ['MAGICK_HOME']
    except KeyError:
        pass
    else:
        system = platform.system()
        if system == 'Windows':
            libpath = 'CORE_RL_wand_.dll',
        elif system == 'Darwin':
            libpath = 'lib', 'libMagickWand.dylib'
        else:
            libpath = 'lib', 'libMagickWand.so'
        libpath = os.path.join(magick_home, *libpath)
    if libpath is None:
        libpath = ctypes.util.find_library('MagickWand')
    return ctypes.CDLL(libpath)


#: (:class:`ctypes.CDLL`) The MagickWand library.
library = load_library()

