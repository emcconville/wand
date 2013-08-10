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
import sys
import platform

__all__ = ('MagickPixelPacket', 'c_magick_char_p', 'library', 'libc',
           'libmagick', 'load_library')


class c_magick_char_p(ctypes.c_char_p):
    """This subclass prevents the automatic conversion behavior of
    :class:`ctypes.c_char_p`, allowing memory to be properly freed in the
    destructor.  It must only be used for non-const character pointers
    returned by ImageMagick functions.

    """

    def __del__(self):
        """Relinquishes memory allocated by ImageMagick.
        We don't need to worry about checking for ``NULL`` because
        :c:func:`MagickRelinquishMemory` does that for us.
        Note alslo that :class:`ctypes.c_char_p` has no
        :meth:`~object.__del__` method, so we don't need to
        (and indeed can't) call the superclass destructor.

        """
        library.MagickRelinquishMemory(self)


def find_library(suffix=''):
    """Finds library path to try loading.  The result paths are not
    guarenteed that they exist.

    :param suffix: optional suffix e.g. ``'-Q16'``
    :type suffix: :class:`basestring`
    :returns: a pair of libwand and libmagick paths.  they can be the same.
              path can be ``None`` as well
    :rtype: :class:`tuple`

    """
    libwand = None
    system = platform.system()
    magick_home = os.environ.get('MAGICK_HOME')
    if magick_home:
        if system == 'Windows':
            libwand = 'CORE_RL_wand_{0}.dll'.format(suffix),
        elif system == 'Darwin':
            libwand = 'lib', 'libMagickWand{0}.dylib'.format(suffix),
        else:
            libwand = 'lib', 'libMagickWand{0}.so'.format(suffix),
        libwand = os.path.join(magick_home, *libwand)
    else:
        if system == 'Windows':
            libwand = ctypes.util.find_library('CORE_RL_wand_' + suffix)
        else:
            libwand = ctypes.util.find_library('MagickWand' + suffix)
    if system == 'Windows':
        # On Windows, the API is split between two libs. On other platforms,
        # it's all contained in one.
        libmagick_filename = 'CORE_RL_magick_' + suffix
        if magick_home:
            libmagick = os.path.join(magick_home, libmagick_filename + '.dll')
        else:
            libmagick = ctypes.util.find_library(libmagick_filename)
        return libwand, libmagick
    return libwand, libwand


def load_library():
    """Loads the MagickWand library.

    :returns: the MagickWand library and the ImageMagick library
    :rtype: :class:`ctypes.CDLL`

    """
    tried_paths = []
    for suffix in '', '-Q16', '-Q8', '-6.Q16':
        libwand_path, libmagick_path = find_library(suffix)
        if libwand_path is None or libmagick_path is None:
            continue
        tried_paths.append(libwand_path)
        try:
            libwand = ctypes.CDLL(libwand_path)
            if libwand_path == libmagick_path:
                libmagick = libwand
            else:
                tried_paths.append(libmagick_path)
                libmagick = ctypes.CDLL(libmagick_path)
        except (IOError, OSError):
            continue
        return libwand, libmagick
    raise IOError('cannot find library; tried paths: ' + repr(tried_paths))


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


# Preserve the module itself even if it fails to import
sys.modules['wand._api'] = sys.modules['wand.api']

try:
    libraries = load_library()
except (OSError, IOError):
    msg = 'http://docs.wand-py.org/en/latest/guide/install.html'
    if sys.platform.startswith('freebsd'):
        msg = 'pkg_add -r'
    elif sys.platform == 'win32':
        msg += '#install-imagemagick-on-windows'
    elif sys.platform == 'darwin':
        for pkgmgr in 'brew', 'port':
            with os.popen('which ' + pkgmgr) as f:
                if f.read().strip():
                    msg = pkgmgr + ' install imagemagick'
                    break
        else:
            msg += '#install-imagemagick-on-mac'
    else:
        distname, _, __ = platform.linux_distribution()
        distname = (distname or '').lower()
        if distname in ('debian', 'ubuntu'):
            msg = 'apt-get install libmagickwand-dev'
        elif distname in ('fedora', 'centos', 'redhat'):
            msg = 'yum install ImageMagick-devel'
    raise ImportError('MagickWand shared library not found.\n'
                      'You probably had not installed ImageMagick library.\n'
                      'Try to install:\n  ' + msg)

#: (:class:`ctypes.CDLL`) The MagickWand library.
library = libraries[0]

#: (:class:`ctypes.CDLL`) The ImageMagick library.  It is the same with
#: :data:`library` on platforms other than Windows.
#:
#: .. versionadded:: 0.1.10
libmagick = libraries[1]

try:
    library.MagickWandGenesis.argtypes = []
    library.MagickWandTerminus.argtypes = []

    library.NewMagickWand.argtypes = []
    library.NewMagickWand.restype = ctypes.c_void_p

    library.MagickNewImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                       ctypes.c_int, ctypes.c_void_p]

    library.ClearMagickWand.argtypes = [ctypes.c_void_p]

    library.DestroyMagickWand.argtypes = [ctypes.c_void_p]
    library.DestroyMagickWand.restype = ctypes.c_void_p

    library.CloneMagickWand.argtypes = [ctypes.c_void_p]
    library.CloneMagickWand.restype = ctypes.c_void_p

    library.IsMagickWand.argtypes = [ctypes.c_void_p]

    library.MagickGetException.argtypes = [ctypes.c_void_p,
                                           ctypes.POINTER(ctypes.c_int)]
    library.MagickGetException.restype = c_magick_char_p

    library.MagickClearException.argtypes = [ctypes.c_void_p]

    library.MagickSetFilename.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickReadImageBlob.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                            ctypes.c_size_t]

    library.MagickReadImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickReadImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageFormat.argtypes = [ctypes.c_void_p]
    library.MagickGetImageFormat.restype = c_magick_char_p

    library.MagickSetImageFormat.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    libmagick.MagickToMime.argtypes = [ctypes.c_char_p]
    libmagick.MagickToMime.restype = c_magick_char_p

    library.MagickGetImageSignature.argtypes = [ctypes.c_void_p]
    library.MagickGetImageSignature.restype = c_magick_char_p

    library.MagickGetImageProperty.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    library.MagickGetImageProperty.restype = c_magick_char_p

    library.MagickGetImageProperties.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_size_t)
    ]
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

    library.MagickGetImagesBlob.argtypes = [ctypes.c_void_p,
                                            ctypes.POINTER(ctypes.c_size_t)]
    library.MagickGetImagesBlob.restype = ctypes.POINTER(ctypes.c_ubyte)

    library.MagickWriteImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickWriteImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickWriteImages.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                          ctypes.c_int]

    library.MagickWriteImagesFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageResolution.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)
    ]

    library.MagickSetImageResolution.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_double,
                                                 ctypes.c_double]

    library.MagickSetResolution.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                            ctypes.c_double]

    library.MagickGetImageWidth.argtypes = [ctypes.c_void_p]
    library.MagickGetImageWidth.restype = ctypes.c_size_t

    library.MagickGetImageHeight.argtypes = [ctypes.c_void_p]
    library.MagickGetImageHeight.restype = ctypes.c_size_t

    library.MagickGetImageOrientation.argtypes = [ctypes.c_void_p]
    library.MagickGetImageOrientation.restype = ctypes.c_int

    library.MagickSetImageOrientation.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickGetImageUnits.argtypes = [ctypes.c_void_p]

    library.MagickSetImageUnits.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickGetImageColorspace.argtypes = [ctypes.c_void_p]
    library.MagickGetImageColorspace.restype = ctypes.c_int

    library.MagickSetImageColorspace.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickGetImageDepth.argtypes = [ctypes.c_void_p]
    library.MagickGetImageDepth.restype = ctypes.c_size_t

    library.MagickSetImageDepth.argtypes = [ctypes.c_void_p]

    library.MagickGetImageChannelDepth.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int]
    library.MagickGetImageChannelDepth.restype = ctypes.c_size_t

    library.MagickSeparateImageChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int]

    library.MagickCropImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                        ctypes.c_size_t, ctypes.c_ssize_t,
                                        ctypes.c_ssize_t]

    library.MagickFlipImage.argtypes = [ctypes.c_void_p]

    library.MagickFlopImage.argtypes = [ctypes.c_void_p]

    library.MagickResetImagePage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickResizeImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t, ctypes.c_int,
                                          ctypes.c_double]

    library.MagickTransformImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                             ctypes.c_char_p]
    library.MagickTransformImage.restype = ctypes.c_void_p

    library.MagickTransparentPaintImage.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double, ctypes.c_double,
        ctypes.c_int
    ]

    library.MagickLiquidRescaleImage.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_double, ctypes.c_double
    ]

    library.MagickRotateImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                          ctypes.c_double]

    library.MagickBorderImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                          ctypes.c_size_t, ctypes.c_size_t]

    library.MagickResetIterator.argtypes = [ctypes.c_void_p]

    library.MagickSetLastIterator.argtypes = [ctypes.c_void_p]

    library.MagickGetIteratorIndex.argtypes = [ctypes.c_void_p]
    library.MagickGetIteratorIndex.restype = ctypes.c_ssize_t

    library.MagickCoalesceImages.argtypes = [ctypes.c_void_p]
    library.MagickCoalesceImages.restype = ctypes.c_void_p

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
    library.PixelGetIteratorException.restype = c_magick_char_p

    library.PixelClearIteratorException.argtypes = [ctypes.c_void_p]

    library.PixelSetFirstIteratorRow.argtypes = [ctypes.c_void_p]

    library.PixelSetIteratorRow.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t]

    library.PixelGetNextIteratorRow.argtypes = [ctypes.c_void_p,
                                                ctypes.POINTER(ctypes.c_size_t)]
    library.PixelGetNextIteratorRow.restype = ctypes.POINTER(ctypes.c_void_p)

    library.NewPixelWand.argtypes = []
    library.NewPixelWand.restype = ctypes.c_void_p

    library.DestroyPixelWand.argtypes = [ctypes.c_void_p]
    library.DestroyPixelWand.restype = ctypes.c_void_p

    library.IsPixelWand.argtypes = [ctypes.c_void_p]

    library.PixelGetException.argtypes = [ctypes.c_void_p,
                                          ctypes.POINTER(ctypes.c_int)]
    library.PixelGetException.restype = c_magick_char_p

    library.PixelClearException.argtypes = [ctypes.c_void_p]

    library.IsPixelWandSimilar.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                           ctypes.c_double]

    library.PixelGetMagickColor.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.PixelSetMagickColor.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.PixelSetColor.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.PixelGetColorAsString.argtypes = [ctypes.c_void_p]
    library.PixelGetColorAsString.restype = c_magick_char_p

    library.PixelGetColorAsNormalizedString.argtypes = [ctypes.c_void_p]
    library.PixelGetColorAsNormalizedString.restype = c_magick_char_p

    library.PixelGetRed.argtypes = [ctypes.c_void_p]
    library.PixelGetRed.restype = ctypes.c_double

    library.PixelGetGreen.argtypes = [ctypes.c_void_p]
    library.PixelGetGreen.restype = ctypes.c_double

    library.PixelGetBlue.argtypes = [ctypes.c_void_p]
    library.PixelGetBlue.restype = ctypes.c_double

    library.PixelGetAlpha.argtypes = [ctypes.c_void_p]
    library.PixelGetAlpha.restype = ctypes.c_double

    library.PixelGetRedQuantum.argtypes = [ctypes.c_void_p]
    library.PixelGetRedQuantum.restype = ctypes.c_size_t

    library.PixelGetGreenQuantum.argtypes = [ctypes.c_void_p]
    library.PixelGetGreenQuantum.restype = ctypes.c_size_t

    library.PixelGetBlueQuantum.argtypes = [ctypes.c_void_p]
    library.PixelGetBlueQuantum.restype = ctypes.c_size_t

    library.PixelGetAlphaQuantum.argtypes = [ctypes.c_void_p]
    library.PixelGetAlphaQuantum.restype = ctypes.c_size_t

    library.PixelGetColorCount.argtypes = [ctypes.c_void_p]
    library.PixelGetColorCount.restype = ctypes.c_size_t

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

    library.MagickCompositeImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
        ctypes.c_int, ctypes.c_ssize_t, ctypes.c_ssize_t
    ]

    library.MagickGetImageCompressionQuality.argtypes = [ctypes.c_void_p]
    library.MagickGetImageCompressionQuality.restype = ctypes.c_ssize_t

    library.MagickSetImageCompressionQuality.argtypes = [ctypes.c_void_p,
                                                         ctypes.c_ssize_t]

    library.MagickStripImage.argtypes = [ctypes.c_void_p]

    library.MagickTrimImage.argtypes = [ctypes.c_void_p,
                                        ctypes.c_double]

    library.MagickGaussianBlurImage.argtypes = [ctypes.c_void_p,
                                                ctypes.c_double,
                                                ctypes.c_double]

    library.MagickUnsharpMaskImage.argtypes = [ctypes.c_void_p,
                                               ctypes.c_double,
                                               ctypes.c_double,
                                               ctypes.c_double,
                                               ctypes.c_double]

    library.MagickGetNumberImages.argtypes = [ctypes.c_void_p]
    library.MagickGetNumberImages.restype = ctypes.c_size_t

    library.MagickGetIteratorIndex.argtypes = [ctypes.c_void_p]
    library.MagickGetIteratorIndex.restype = ctypes.c_size_t

    library.MagickSetIteratorIndex.argtypes = [ctypes.c_void_p,
                                               ctypes.c_ssize_t]

    library.MagickSetFirstIterator.argtypes = [ctypes.c_void_p]

    library.MagickSetLastIterator.argtypes = [ctypes.c_void_p]

    library.MagickAddImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickRemoveImage.argtypes = [ctypes.c_void_p]

    libmagick.GetNextImageInList.argtypes = [ctypes.c_void_p]
    libmagick.GetNextImageInList.restype = ctypes.c_void_p

    library.MagickGetImageDelay.argtypes = [ctypes.c_void_p]
    library.MagickGetImageDelay.restype = ctypes.c_ssize_t

    library.MagickSetImageDelay.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t]

    library.NewMagickWandFromImage.argtypes = [ctypes.c_void_p]
    library.NewMagickWandFromImage.restype = ctypes.c_void_p

    library.GetImageFromMagickWand.argtypes = [ctypes.c_void_p]
    library.GetImageFromMagickWand.restype = ctypes.c_void_p

    libmagick.CloneImages.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                      ctypes.c_void_p]
    libmagick.CloneImages.restype = ctypes.c_void_p

    libmagick.AcquireExceptionInfo.argtypes = []
    libmagick.AcquireExceptionInfo.restype = ctypes.c_void_p

    libmagick.DestroyExceptionInfo.argtypes = [ctypes.c_void_p]
    libmagick.DestroyExceptionInfo.restype = ctypes.c_void_p

    library.MagickGetSize.argtypes = [ctypes.c_void_p,
                                      ctypes.POINTER(ctypes.c_uint),
                                      ctypes.POINTER(ctypes.c_uint)]
    library.MagickGetSize.restype = ctypes.c_int

    library.MagickSetSize.argtypes = [ctypes.c_void_p,
                                      ctypes.c_uint,
                                      ctypes.c_uint]
    library.MagickSetSize.restype = ctypes.c_int

    library.MagickGetFont.argtypes = [ctypes.c_void_p]
    library.MagickGetFont.restype = ctypes.c_char_p

    library.MagickSetFont.argtypes = [ctypes.c_void_p,
                                      ctypes.c_char_p]
    library.MagickSetFont.restype = ctypes.c_int

    library.MagickGetPointsize.argtypes = [ctypes.c_void_p]
    library.MagickGetPointsize.restype = ctypes.c_double

    library.MagickSetPointsize.argtypes = [ctypes.c_void_p,
                                           ctypes.c_double]
    library.MagickSetPointsize.restype = ctypes.c_int

    library.MagickGetGravity.argtypes = [ctypes.c_void_p]
    library.MagickGetGravity.restype = ctypes.c_int

    library.MagickSetGravity.argtypes = [ctypes.c_void_p,
                                         ctypes.c_int]
    library.MagickSetGravity.restype = ctypes.c_int

    library.MagickSetLastIterator.argtypes = [ctypes.c_void_p]

    library.MagickGetBackgroundColor.argtypes = [ctypes.c_void_p]
    library.MagickGetBackgroundColor.restype = ctypes.c_void_p

    library.MagickSetBackgroundColor.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_void_p]
    library.MagickSetBackgroundColor.restype = ctypes.c_int

    library.MagickGetOption.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p]
    library.MagickGetOption.restype = ctypes.c_char_p

    library.MagickSetOption.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p]
    library.MagickSetOption.restype = ctypes.c_int

    library.MagickGetAntialias.argtypes = [ctypes.c_void_p]
    library.MagickGetAntialias.restype = ctypes.c_int

    library.MagickSetAntialias.argtypes = [ctypes.c_void_p,
                                           ctypes.c_int]
    library.MagickSetAntialias.restype = ctypes.c_int

    library.MagickGetImageHistogram.argtypes = [ctypes.c_void_p,
                                                ctypes.POINTER(ctypes.c_size_t)]
    library.MagickGetImageHistogram.restype = ctypes.POINTER(ctypes.c_void_p)

    # These functions are const so it's okay for them to be c_char_p
    libmagick.GetMagickVersion.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
    libmagick.GetMagickVersion.restype = ctypes.c_char_p

    libmagick.GetMagickReleaseDate.argtypes = []
    libmagick.GetMagickReleaseDate.restype = ctypes.c_char_p

    libmagick.GetMagickQuantumDepth.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
    libmagick.GetMagickQuantumDepth.restype = ctypes.c_char_p

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

    library.DrawSetFontSize.argtypes = [ctypes.c_void_p,
                                        ctypes.c_double]

    library.DrawSetFillColor.argtypes = [ctypes.c_void_p,
                                         ctypes.c_void_p]

    library.DrawSetStrokeColor.argtypes = [ctypes.c_void_p, 
                                           ctypes.c_void_p]

    library.DrawSetStrokeWidth.argtypes = [ctypes.c_void_p, 
                                           ctypes.c_double]

    library.DrawSetTextAlignment.argtypes = [ctypes.c_void_p,
                                             ctypes.c_int]

    library.DrawSetTextAntialias.argtypes = [ctypes.c_void_p,
                                             ctypes.c_int]

    library.DrawSetTextDecoration.argtypes = [ctypes.c_void_p,
                                              ctypes.c_int]

    library.DrawSetTextEncoding.argtypes = [ctypes.c_void_p,
                                            ctypes.c_char_p]

    try:
        library.DrawSetTextInterlineSpacing.argtypes = [ctypes.c_void_p,
                                                        ctypes.c_double]
    except AttributeError:
        library.DrawSetTextInterlineSpacing = None

    library.DrawSetTextInterwordSpacing.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_double]

    library.DrawSetTextKerning.argtypes = [ctypes.c_void_p,
                                           ctypes.c_double]

    library.DrawSetTextUnderColor.argtypes = [ctypes.c_void_p,
                                              ctypes.c_void_p]

    library.DrawGetFillColor.argtypes = [ctypes.c_void_p,
                                         ctypes.c_void_p]

    library.DrawGetStrokeColor.argtypes = [ctypes.c_void_p, 
                                           ctypes.c_void_p]

    library.DrawGetStrokeWidth.argtypes = [ctypes.c_void_p]
    library.DrawGetStrokeWidth.restype = ctypes.c_double

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

    try:
        library.DrawGetTextInterlineSpacing.argtypes = [ctypes.c_void_p]
        library.DrawGetTextInterlineSpacing.restype = ctypes.c_double
    except AttributeError:
        library.DrawGetTextInterlineSpacing = None

    library.DrawGetTextInterwordSpacing.argtypes = [ctypes.c_void_p]
    library.DrawGetTextInterwordSpacing.restype = ctypes.c_double

    library.DrawGetTextKerning.argtypes = [ctypes.c_void_p]
    library.DrawGetTextKerning.restype = ctypes.c_double

    library.DrawGetTextUnderColor.argtypes = [ctypes.c_void_p,
                                              ctypes.c_void_p]

    library.DrawSetGravity.argtypes = [ctypes.c_void_p,
                                       ctypes.c_int]

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

    library.MagickDrawImage.argtypes = [ctypes.c_void_p,
                                        ctypes.c_void_p]
    library.MagickDrawImage.restype = ctypes.c_int

    library.DrawLine.argtypes = [ctypes.c_void_p,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double,
                                 ctypes.c_double]

    library.DrawAnnotation.argtypes = [ctypes.c_void_p,
                                       ctypes.c_double,
                                       ctypes.c_double,
                                       ctypes.POINTER(ctypes.c_ubyte)]

    library.MagickNormalizeImage.argtypes = [ctypes.c_void_p]

    library.MagickNormalizeImageChannel.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int]

    library.MagickQueryFontMetrics.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p,
                                               ctypes.c_char_p]
    library.MagickQueryFontMetrics.restype = ctypes.POINTER(ctypes.c_double)

    library.MagickQueryMultilineFontMetrics.argtypes = [ctypes.c_void_p,
                                                        ctypes.c_void_p,
                                                        ctypes.c_char_p]
    library.MagickQueryMultilineFontMetrics.restype = ctypes.POINTER(
        ctypes.c_double
    )
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

