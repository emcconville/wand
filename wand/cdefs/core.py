""":mod:`wand.cdefs.core` --- MagickCore definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: ?.?.?
"""
from ctypes import POINTER, c_void_p, c_char_p, c_size_t
from wand.cdefs.wandtypes import c_magick_char_p

__all__ = ('load',)


def load(libmagick):
    """Define MagickCore methods.
    We'll only define the bare-minimum methods to support the MagickWand
    library.

    .. seealso::

        #include <magick/MagickCore.h>
        // Or
        #include <MagickCore/MagickCore.h>

    :param libmagick: the loaded ``MagickCore`` library.
    :type libmagick: :class:`ctypes.CDLL`

    .. versionadded:: 0.?.?

    """
    libmagick.AcquireExceptionInfo.argtypes = []
    libmagick.AcquireExceptionInfo.restype = c_void_p
    libmagick.CloneImages.argtypes = [c_void_p, c_char_p, c_void_p]
    libmagick.CloneImages.restype = c_void_p
    libmagick.DestroyExceptionInfo.argtypes = [c_void_p]
    libmagick.DestroyExceptionInfo.restype = c_void_p
    libmagick.DestroyImage.argtypes = [c_void_p]
    libmagick.DestroyImage.restype = c_void_p
    libmagick.GetNextImageInList.argtypes = [c_void_p]
    libmagick.GetNextImageInList.restype = c_void_p
    libmagick.GetMagickCopyright.argtypes = []
    libmagick.GetMagickCopyright.restype = c_char_p
    libmagick.GetMagickDelegates.argtypes = []
    libmagick.GetMagickDelegates.restype = c_char_p
    libmagick.GetMagickFeatures.argtypes = []
    libmagick.GetMagickFeatures.restype = c_char_p
    try:
        libmagick.GetMagickLicense.argtypes = []
        libmagick.GetMagickLicense.restype = c_char_p
    except AttributeError:
        pass
    libmagick.GetMagickPackageName.argtypes = []
    libmagick.GetMagickPackageName.restype = c_char_p
    libmagick.GetMagickQuantumDepth.argtypes = [POINTER(c_size_t)]
    libmagick.GetMagickQuantumDepth.restype = c_char_p
    libmagick.GetMagickQuantumRange.argtypes = [POINTER(c_size_t)]
    libmagick.GetMagickQuantumRange.restype = c_char_p
    libmagick.GetMagickReleaseDate.argtypes = []
    libmagick.GetMagickReleaseDate.restype = c_char_p
    libmagick.GetMagickVersion.argtypes = [POINTER(c_size_t)]
    libmagick.GetMagickVersion.restype = c_char_p
    libmagick.MagickToMime.argtypes = [c_char_p]
    libmagick.MagickToMime.restype = c_magick_char_p