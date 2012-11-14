""":mod:`wand.api` --- Low-level interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionchanged:: 0.1.10
   Changed to throw :exc:`~exceptions.ImportError` instead of
   :exc:`~exceptions.AttributeError` when the shared library fails to load.

"""
import ctypes
import ctypes.util
import os
import os.path
import platform

__all__ = 'load_library', 'MagickPixelPacket', 'library', 'libmagick', 'libc'


def load_library():
    """Loads the MagickWand library.

    :returns: the MagickWand library and the ImageMagick library

    """
    libpath = None
    system = platform.system()

    magick_home = os.environ.get('MAGICK_HOME')
    if magick_home:
        if system == 'Windows':
            libpath = 'CORE_RL_wand_.dll',
        elif system == 'Darwin':
            libpath = 'lib', 'libMagickWand.dylib',
        else:
            libpath = 'lib', 'libMagickWand.so',
        libpath = os.path.join(magick_home, *libpath)
    else:
        if system == 'Windows':
            libpath = ctypes.util.find_library('CORE_RL_wand_')
        else:
            libpath = ctypes.util.find_library('MagickWand')
    libwand = ctypes.CDLL(libpath)

    if system == 'Windows':
        # On Windows, the API is split between two libs. On other platforms,
        # it's all contained in one.
        libmagick_filename = 'CORE_RL_magick_'
        if magick_home:
            libmagick_path = os.path.join(magick_home,
                                          libmagick_filename + '.dll')
        else:
            libmagick_path = ctypes.util.find_library(libmagick_filename)
        libmagick = ctypes.CDLL(libmagick_path)
        return libwand, libmagick

    return libwand, libwand


if not hasattr(ctypes, 'c_ssize_t'):
    if ctypes.sizeof(ctypes.c_uint) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_int
    elif ctypes.sizeof(ctypes.c_ulong) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_long
    elif ctypes.sizeof(ctypes.c_ulonglong) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_longlong


class MagickPixelPacket(ctypes.Structure):

    _fields_ = [('storage_class', ctypes.c_int),
                ('colorspace', ctypes.c_int),
                ('matte', ctypes.c_int),
                ('fuzz', ctypes.c_double),
                ('depth', ctypes.c_size_t),
                ('red', ctypes.c_double),
                ('green', ctypes.c_double),
                ('blue', ctypes.c_double),
                ('opacity', ctypes.c_double),
                ('index', ctypes.c_double)]


libraries = load_library()

#: (:class:`ctypes.CDLL`) The MagickWand library.
library = libraries[0]

#: (:class:`ctypes.CDLL`) The ImageMagick library.  It is the same with
#: :data:`library` on platforms other than Windows.
#:
#: .. versionadded:: 0.1.10
libmagick = libraries[1]

try:
    library.NewMagickWand.restype = ctypes.c_void_p

    library.MagickNewImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                       ctypes.c_int, ctypes.c_void_p]

    library.DestroyMagickWand.argtypes = [ctypes.c_void_p]
    library.DestroyMagickWand.restype = ctypes.c_void_p

    library.CloneMagickWand.argtypes = [ctypes.c_void_p]
    library.CloneMagickWand.restype = ctypes.c_void_p

    library.IsMagickWand.argtypes = [ctypes.c_void_p]

    library.MagickGetException.argtypes = [ctypes.c_void_p,
                                           ctypes.POINTER(ctypes.c_int)]
    library.MagickGetException.restype = ctypes.c_char_p

    library.MagickClearException.argtypes = [ctypes.c_void_p]

    library.MagickSetFilename.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickReadImageBlob.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                            ctypes.c_size_t]

    library.MagickReadImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickReadImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageFormat.argtypes = [ctypes.c_void_p]
    library.MagickGetImageFormat.restype = ctypes.c_char_p

    library.MagickSetImageFormat.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    libmagick.MagickToMime.argtypes = [ctypes.c_char_p]
    libmagick.MagickToMime.restype = ctypes.POINTER(ctypes.c_char)

    library.MagickGetImageSignature.argtypes = [ctypes.c_void_p]
    library.MagickGetImageSignature.restype = ctypes.c_char_p

    library.MagickGetImageProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    library.MagickGetImageProperty.restype = ctypes.c_char_p

    library.MagickGetImageProperties.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_char_p,
                                                 ctypes.POINTER(ctypes.c_size_t)]
    library.MagickGetImageProperties.restype = ctypes.POINTER(ctypes.c_char_p)

    library.MagickSetImageProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                               ctypes.c_char_p]

    library.MagickDeleteImageProperty.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_char_p]
    library.MagickGetImageBackgroundColor.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_void_p]

    library.MagickSetImageBackgroundColor.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_void_p]

    library.MagickGetImageAlphaChannel.argtypes = [ctypes.c_void_p]
    library.MagickGetImageAlphaChannel.restype = ctypes.c_size_t

    library.MagickSetImageAlphaChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int]

    library.MagickGetImageBlob.argtypes = [ctypes.c_void_p,
                                           ctypes.POINTER(ctypes.c_size_t)]
    library.MagickGetImageBlob.restype = ctypes.POINTER(ctypes.c_ubyte)

    library.MagickWriteImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickWriteImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageWidth.argtypes = [ctypes.c_void_p]
    library.MagickGetImageWidth.restype = ctypes.c_size_t

    library.MagickGetImageHeight.argtypes = [ctypes.c_void_p]
    library.MagickGetImageHeight.restype = ctypes.c_size_t

    library.MagickGetImageUnits.argtypes = [ctypes.c_void_p]

    library.MagickSetImageUnits.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickGetImageDepth.argtypes = [ctypes.c_void_p]
    library.MagickGetImageDepth.restype = ctypes.c_size_t

    library.MagickSetImageDepth.argtypes = [ctypes.c_void_p]

    library.MagickCropImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                        ctypes.c_size_t, ctypes.c_ssize_t,
                                        ctypes.c_ssize_t]

    library.MagickResetImagePage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickResizeImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t, ctypes.c_int,
                                          ctypes.c_double]

    library.MagickTransformImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                             ctypes.c_char_p]
    library.MagickTransformImage.restype = ctypes.c_void_p

    library.MagickRotateImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
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

    library.PixelGetMagickColor.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.PixelSetMagickColor.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.PixelSetColor.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.PixelGetColorAsString.argtypes = [ctypes.c_void_p]
    library.PixelGetColorAsString.restype = ctypes.c_char_p

    library.PixelGetAlpha.argtypes = [ctypes.c_void_p]
    library.PixelGetAlpha.restype = ctypes.c_double

    library.MagickGetQuantumRange.argtypes = [ctypes.POINTER(ctypes.c_size_t)]

    library.MagickSetIteratorIndex.argtypes = [ctypes.c_void_p,
                                               ctypes.c_ssize_t]

    library.MagickGetImageType.argtypes = [ctypes.c_void_p]
    
    library.MagickSetImageType.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickEvaluateImageChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int,
                                                   ctypes.c_int,
                                                   ctypes.c_double]

    library.MagickCompositeImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                             ctypes.c_int, ctypes.c_ssize_t,
                                             ctypes.c_ssize_t]

    library.MagickGetImageCompressionQuality.argtypes = [ctypes.c_void_p]
    library.MagickGetImageCompressionQuality.restype = ctypes.c_ssize_t

    library.MagickSetImageCompressionQuality.argtypes = [ctypes.c_void_p,
                                                         ctypes.c_ssize_t]

    library.MagickStripImage.argtypes = [ctypes.c_void_p]

    library.MagickTrimImage.argtypes = [ctypes.c_void_p]

    libmagick.GetMagickVersion.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
    libmagick.GetMagickVersion.restype = ctypes.c_char_p

    libmagick.GetMagickReleaseDate.argtypes = []
    libmagick.GetMagickReleaseDate.restype = ctypes.c_char_p

    library.NewDrawingWand.restype = ctypes.c_void_p

    library.CloneDrawingWand.argtypes = [ctypes.c_void_p]
    library.CloneDrawingWand.restype = ctypes.c_void_p

    library.DestroyDrawingWand.argtypes = [ctypes.c_void_p]
    library.DestroyDrawingWand.restype = ctypes.c_void_p

    library.IsDrawingWand.argtypes = [ctypes.c_void_p]
    library.IsDrawingWand.restype = ctypes.c_int

    library.DrawGetException.argtypes = [ctypes.c_void_p,
                                         ctypes.POINTER(ctypes.c_int)]
    library.DrawGetException.restype = ctypes.c_char_p

    library.DrawClearException.argtypes = [ctypes.c_void_p]
    library.DrawClearException.restype = ctypes.c_int

    library.DrawSetFont.argtypes = [ctypes.c_void_p,
                                    ctypes.c_char_p]
    library.DrawSetFont.restype = None

    library.DrawSetFontSize.argtypes = [ctypes.c_void_p,
                                        ctypes.c_double]
    library.DrawSetFontSize.restype = None

    library.DrawSetFillColor.argtypes = [ctypes.c_void_p,
                                         ctypes.c_void_p]
    library.DrawSetFillColor.restype = None

    library.DrawSetTextAlignment.argtypes = [ctypes.c_void_p,
                                             ctypes.c_int]
    library.DrawSetTextAlignment.restype = None

    library.DrawSetTextAntialias.argtypes = [ctypes.c_void_p,
                                             ctypes.c_int]
    library.DrawSetTextAntialias.restype = None

    library.DrawSetTextDecoration.argtypes = [ctypes.c_void_p,
                                              ctypes.c_int]
    library.DrawSetTextDecoration.restype = None

    library.DrawSetTextEncoding.argtypes = [ctypes.c_void_p,
                                            ctypes.c_char_p]
    library.DrawSetTextEncoding.restype = None

    library.DrawSetTextInterlineSpacing.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_double]
    library.DrawSetTextInterlineSpacing.restype = None

    library.DrawSetTextInterwordSpacing.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_double]
    library.DrawSetTextInterwordSpacing.restype = None

    library.DrawSetTextKerning.argtypes = [ctypes.c_void_p,
                                           ctypes.c_double]
    library.DrawSetTextKerning.restype = None

    library.DrawSetTextUnderColor.argtypes = [ctypes.c_void_p,
                                              ctypes.c_void_p]
    library.DrawSetTextUnderColor.restype = None

    library.DrawGetFillColor.argtypes = [ctypes.c_void_p,
                                         ctypes.c_void_p]
    library.DrawGetFillColor.restype = None

    library.DrawGetFont.argtypes = [ctypes.c_void_p]
    library.DrawGetFont.restype = ctypes.c_char_p

    library.DrawGetFontSize.argtypes = [ctypes.c_void_p]
    library.DrawGetFontSize.restype = ctypes.c_double

    library.DrawGetTextAlignment.argtypes = [ctypes.c_void_p]
    library.DrawGetTextAlignment.restype = ctypes.c_int

    library.DrawGetTextAntialias.argtypes = [ctypes.c_void_p]
    library.DrawGetTextAntialias.restype = ctypes.c_int

    library.DrawGetTextDecoration.argtypes = [ctypes.c_void_p]
    library.DrawGetTextDecoration.restype = ctypes.c_int

    library.DrawGetTextEncoding.argtypes = [ctypes.c_void_p]
    library.DrawGetTextEncoding.restype = ctypes.c_char_p

    library.DrawGetTextInterlineSpacing.argtypes = [ctypes.c_void_p]
    library.DrawGetTextInterlineSpacing.restype = ctypes.c_double

    library.DrawGetTextInterwordSpacing.argtypes = [ctypes.c_void_p]
    library.DrawGetTextInterwordSpacing.restype = ctypes.c_double

    library.DrawGetTextKerning.argtypes = [ctypes.c_void_p]
    library.DrawGetTextKerning.restype = ctypes.c_double

    library.DrawGetTextUnderColor.argtypes = [ctypes.c_void_p,
                                              ctypes.c_void_p]
    library.DrawGetTextUnderColor.restype = None

    library.DrawSetGravity.argtypes = [ctypes.c_void_p,
                                       ctypes.c_int]
    library.DrawSetGravity.restype = None

    library.DrawGetGravity.argtypes = [ctypes.c_void_p]
    library.DrawGetGravity.restype = ctypes.c_int

    library.MagickAnnotateImage.argtypes = [ctypes.c_void_p,
                                            ctypes.c_void_p,
                                            ctypes.c_double,
                                            ctypes.c_double,
                                            ctypes.c_double,
                                            ctypes.c_char_p]
    library.MagickAnnotateImage.restype = ctypes.c_int

    library.ClearDrawingWand.argtypes = [ctypes.c_void_p]
    library.ClearDrawingWand.restype = None

    library.MagickDrawImage.argtypes = [ctypes.c_void_p,
                                        ctypes.c_void_p]
    library.MagickDrawImage.restype = ctypes.c_int

    library.DrawLine.argtypes = [ctypes.c_void_p,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double]
    library.DrawLine.restype = None

    library.DrawAnnotation.argtypes = [ctypes.c_void_p,
                                       ctypes.c_double,
                                       ctypes.c_double,
                                       ctypes.POINTER(ctypes.c_ubyte)]
    library.DrawAnnotation.restype = None

    library.MagickQueryFontMetrics.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p,
                                               ctypes.c_char_p]
    library.MagickQueryFontMetrics.restype = ctypes.POINTER(ctypes.c_double)

    library.MagickQueryMultilineFontMetrics.argtypes = [ctypes.c_void_p,
                                                        ctypes.c_void_p,
                                                        ctypes.c_char_p]
    library.MagickQueryMultilineFontMetrics.restype = ctypes.POINTER(ctypes.c_double)


except AttributeError:
    raise ImportError('MagickWand shared library not found or incompatible')

#: (:class:`ctypes.CDLL`) The C standard library.
libc = None

if platform.system() == 'Windows':
    libc = ctypes.CDLL(ctypes.util.find_msvcrt())
else:
    if platform.system() == 'Darwin':
        libc = ctypes.cdll.LoadLibrary('libc.dylib')
    elif platform.system() == 'FreeBSD':
        libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
    else:
        libc = ctypes.cdll.LoadLibrary('libc.so.6')
    libc.fdopen.argtypes = [ctypes.c_int, ctypes.c_char_p]
    libc.fdopen.restype = ctypes.c_void_p

libc.free.argtypes = [ctypes.c_void_p]

