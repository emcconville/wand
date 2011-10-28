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

library.NewMagickWand.restype = ctypes.c_void_p

library.DestroyMagickWand.argtypes = [ctypes.c_void_p]
library.DestroyMagickWand.restype = ctypes.c_void_p

library.CloneMagickWand.argtypes = [ctypes.c_void_p]
library.CloneMagickWand.restype = ctypes.c_void_p

library.IsMagickWand.argtypes = [ctypes.c_void_p]

library.MagickGetException.argtypes = [ctypes.c_void_p,
                                       ctypes.POINTER(ctypes.c_int)]
library.MagickGetException.restype = ctypes.c_char_p

library.MagickClearException.argtypes = [ctypes.c_void_p]

library.MagickReadImageBlob.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_size_t]

library.MagickReadImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

library.MagickReadImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

library.MagickSetImageFormat.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

library.MagickGetImageBlob.argtypes = [ctypes.c_void_p,
                                       ctypes.POINTER(ctypes.c_size_t)]
library.MagickGetImageBlob.restype = ctypes.POINTER(ctypes.c_ubyte)

library.MagickWriteImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

library.MagickWriteImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

library.MagickGetImageWidth.argtypes = [ctypes.c_void_p]
library.MagickGetImageWidth.restype = ctypes.c_size_t

library.MagickGetImageHeight.argtypes = [ctypes.c_void_p]
library.MagickGetImageHeight.restype = ctypes.c_size_t

library.MagickCropImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                    ctypes.c_size_t, ctypes.c_ssize_t,
                                    ctypes.c_ssize_t]

library.MagickResizeImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                      ctypes.c_size_t, ctypes.c_int,
                                      ctypes.c_double]

library.MagickResetIterator.argtypes = [ctypes.c_void_p]

library.MagickIdentifyImage.argtypes = [ctypes.c_void_p]
library.MagickIdentifyImage.restype = ctypes.c_char_p

library.MagickRelinquishMemory.argtypes = [ctypes.c_void_p]
library.MagickRelinquishMemory.restype = ctypes.c_void_p

library.NewPixelIterator.argtypes = [ctypes.c_void_p]
library.NewPixelIterator.restype = ctypes.c_void_p

library.DestroyPixelIterator.argtypes = [ctypes.c_void_p]
library.DestroyPixelIterator.restype = ctypes.c_void_p

library.ClonePixelIterator.argtypes = [ctypes.c_void_p]
library.ClonePixelIterator.restype = ctypes.c_void_p

library.IsPixelIterator.argtypes = [ctypes.c_void_p]

library.PixelGetIteratorException.argtypes = [ctypes.c_void_p,
                                              ctypes.POINTER(ctypes.c_int)]
library.PixelGetIteratorException.restype = ctypes.c_char_p

library.PixelClearIteratorException.argtypes = [ctypes.c_void_p]

library.PixelSetFirstIteratorRow.argtypes = [ctypes.c_void_p]

library.PixelSetIteratorRow.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t]

library.PixelGetNextIteratorRow.argtypes = [ctypes.c_void_p,
                                            ctypes.POINTER(ctypes.c_size_t)]
library.PixelGetNextIteratorRow.restype = ctypes.POINTER(ctypes.c_void_p)

library.NewPixelWand.restype = ctypes.c_void_p

library.DestroyPixelWand.argtypes = [ctypes.c_void_p]
library.DestroyPixelWand.restype = ctypes.c_void_p

library.IsPixelWand.argtypes = [ctypes.c_void_p]

library.PixelGetException.argtypes = [ctypes.c_void_p,
                                      ctypes.POINTER(ctypes.c_int)]
library.PixelGetException.restype = ctypes.c_char_p

library.PixelClearException.argtypes = [ctypes.c_void_p]

library.IsPixelWandSimilar.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                       ctypes.c_double]

library.PixelSetColor.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

library.PixelGetColorAsString.argtypes = [ctypes.c_void_p]
library.PixelGetColorAsString.restype = ctypes.c_char_p

library.PixelGetAlpha.argtypes = [ctypes.c_void_p]
library.PixelGetAlpha.restype = ctypes.c_double

#: (:class:`ctypes.CDLL`) The C standard library.
libc = None

if platform.system() == 'Windows':
    libc = ctypes.cdll.msvcrt
elif platform.system() == 'Darwin':
    libc = ctypes.cdll.LoadLibrary('libc.dylib')
else:
    libc = ctypes.cdll.LoadLibrary('libc.so.6')

libc.fdopen.argtypes = [ctypes.c_int, ctypes.c_char_p]
libc.fdopen.restype = ctypes.c_void_p

