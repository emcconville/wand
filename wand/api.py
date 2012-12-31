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


try:
    libraries = load_library()
except (OSError, IOError):
    msg = 'http://dahlia.github.com/wand/guide/install.html'
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

    library.MagickWriteImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickWriteImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageResolution.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)
    ]

    library.MagickSetImageResolution.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_double,
                                                 ctypes.c_double]

    library.MagickSetResolution.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                            ctypes.c_double]
    library.MagickSetResolution.restype = ctypes.c_bool

    library.MagickGetImageWidth.argtypes = [ctypes.c_void_p]
    library.MagickGetImageWidth.restype = ctypes.c_size_t

    library.MagickGetImageHeight.argtypes = [ctypes.c_void_p]
    library.MagickGetImageHeight.restype = ctypes.c_size_t

    library.MagickGetImageUnits.argtypes = [ctypes.c_void_p]

    library.MagickSetImageUnits.argtypes = [ctypes.c_void_p, ctypes.c_int]

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

    library.MagickResetImagePage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickResizeImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t, ctypes.c_int,
                                          ctypes.c_double]

    library.MagickTransformImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                             ctypes.c_char_p]
    library.MagickTransformImage.restype = ctypes.c_void_p

    library.MagickLiquidRescaleImage.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_double, ctypes.c_double
    ]

    library.MagickRotateImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                          ctypes.c_double]

    library.MagickBorderImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                          ctypes.c_size_t, ctypes.c_size_t]

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

    library.MagickCompositeImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
        ctypes.c_int, ctypes.c_ssize_t, ctypes.c_ssize_t
    ]

    library.MagickGetImageCompressionQuality.argtypes = [ctypes.c_void_p]
    library.MagickGetImageCompressionQuality.restype = ctypes.c_ssize_t

    library.MagickSetImageCompressionQuality.argtypes = [ctypes.c_void_p,
                                                         ctypes.c_ssize_t]

    library.MagickStripImage.argtypes = [ctypes.c_void_p]

    library.MagickTrimImage.argtypes = [ctypes.c_void_p]

    # These functions are const so it's okay for them to be c_char_p
    libmagick.GetMagickVersion.argtypes = [ctypes.POINTER(ctypes.c_size_t)]
    libmagick.GetMagickVersion.restype = ctypes.c_char_p

    libmagick.GetMagickReleaseDate.argtypes = []
    libmagick.GetMagickReleaseDate.restype = ctypes.c_char_p

    # mechanically generated from magick-image.h of MagickWand
    library.MagickSetImageScene.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    library.MagickSetImageScene.restype = ctypes.c_void_p

    library.MagickSigmoidalContrastImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]
    library.MagickSigmoidalContrastImage.restype = ctypes.c_void_p

    library.MagickGetImagePixelColor.argtypes = [
        ctypes.c_void_p, ctypes.c_ssize_t,
        ctypes.c_ssize_t, ctypes.c_void_p]

    library.MagickFunctionImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_size_t, ctypes.POINTER(ctypes.c_double)]

    library.MagickEmbossImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                          ctypes.c_double]

    library.MagickContrastStretchImage.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_double,
                                                   ctypes.c_double]

    library.MagickBrightnessContrastImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]

    library.MagickDeskewImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickSteganoImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                           ctypes.c_ssize_t]
    library.MagickSteganoImage.restype = ctypes.c_void_p

    library.MagickWriteImages.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                          ctypes.c_int]

    library.MagickBrightnessContrastImage.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_double,
                                                      ctypes.c_double]

    library.MagickGetImageChannelFeatures.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_size_t]
    library.MagickGetImageChannelFeatures.restype = ctypes.c_void_p

    library.MagickPingImageFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.MagickPingImageFile.restype = ctypes.c_void_p

    library.MagickSetImageColor.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.MagickSetImageColor.restype = ctypes.c_void_p

    library.MagickEnhanceImage.argtypes = [ctypes.c_void_p]

    library.MagickHasNextImage.argtypes = [ctypes.c_void_p]

    library.MagickClutImageChannel.argtypes = [ctypes.c_void_p,
                                               ctypes.c_int, ctypes.c_void_p]

    library.MagickExtentImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t, ctypes.c_ssize_t,
                                          ctypes.c_ssize_t]

    library.MagickSetImageOpacity.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSetImageOpacity.restype = ctypes.c_void_p

    library.MagickHasPreviousImage.argtypes = [ctypes.c_void_p]

    library.MagickDespeckleImage.argtypes = [ctypes.c_void_p]

    library.MagickForwardFourierTransformImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int]

    library.MagickBlurImageChannel.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                               ctypes.c_double, ctypes.c_double]

    library.MagickThumbnailImage.argtypes = [ctypes.c_void_p,
                                             ctypes.c_size_t, ctypes.c_size_t]

    library.MagickPingImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    library.MagickPingImage.restype = ctypes.c_void_p

    library.MagickClampImageChannel.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickHaldClutImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickSpliceImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t, ctypes.c_ssize_t,
                                          ctypes.c_ssize_t]

    library.MagickRadialBlurImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickRadialBlurImage.restype = ctypes.c_void_p

    library.MagickBlurImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                        ctypes.c_double]

    library.MagickSetImageFuzz.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSetImageFuzz.restype = ctypes.c_void_p

    library.MagickAdaptiveSharpenImage.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_double,
                                                   ctypes.c_double]

    library.MagickCompareImageChannels.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,
        ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
    library.MagickCompareImageChannels.restype = ctypes.c_void_p

    library.MagickReduceNoiseImage.argtypes = [ctypes.c_void_p,
                                               ctypes.c_double]
    library.MagickReduceNoiseImage.restype = ctypes.c_void_p

    library.MagickShearImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                         ctypes.c_double, ctypes.c_double]
    library.MagickShearImage.restype = ctypes.c_void_p

    library.MagickSetImageBorderColor.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_void_p]
    library.MagickSetImageBorderColor.restype = ctypes.c_void_p

    library.MagickSetImageChannelDepth.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int,
                                                   ctypes.c_size_t]
    library.MagickSetImageChannelDepth.restype = ctypes.c_void_p

    library.MagickAddNoiseImageChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int,
                                                   ctypes.c_int]

    library.MagickGetImageMatteColor.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_void_p]

    library.MagickGetImageChannelDistortions.argtypes = [ctypes.c_void_p,
                                                         ctypes.c_void_p,
                                                         ctypes.c_int]
    library.MagickGetImageChannelDistortions.restype = \
        ctypes.POINTER(ctypes.c_double)

    library.MagickSetImageCompression.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_int]
    library.MagickSetImageCompression.restype = ctypes.c_void_p

    library.MagickGetImageFuzz.argtypes = [ctypes.c_void_p]
    library.MagickGetImageFuzz.restype = ctypes.c_double

    library.MagickSetImageExtent.argtypes = [ctypes.c_void_p,
                                             ctypes.c_size_t, ctypes.c_size_t]
    library.MagickSetImageExtent.restype = ctypes.c_void_p

    library.MagickAffineTransformImage.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_void_p]

    library.MagickGaussianBlurImage.argtypes = [ctypes.c_void_p,
                                                ctypes.c_double,
                                                ctypes.c_double]

    library.MagickSetImageDelay.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    library.MagickSetImageDelay.restype = ctypes.c_void_p

    library.MagickGetImageBluePrimary.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickModeImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickGetImageChannelKurtosis.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickEvaluateImage.argtypes = [ctypes.c_void_p,
                                            ctypes.c_int, ctypes.c_double]

    library.MagickShaveImage.argtypes = [ctypes.c_void_p,
                                         ctypes.c_size_t, ctypes.c_size_t]
    library.MagickShaveImage.restype = ctypes.c_void_p

    library.MagickAutoLevelImageChannel.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int]

    library.MagickColorizeImage.argtypes = [ctypes.c_void_p,
                                            ctypes.c_void_p, ctypes.c_void_p]

    library.MagickTintImage.argtypes = [ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.c_void_p]

    library.MagickClipImagePath.argtypes = [ctypes.c_void_p,
                                            ctypes.c_char_p, ctypes.c_int]

    library.MagickChopImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                        ctypes.c_size_t, ctypes.c_ssize_t,
                                        ctypes.c_ssize_t]

    library.MagickSetImageInterpolateMethod.argtypes = [ctypes.c_void_p,
                                                        ctypes.c_int]
    library.MagickSetImageInterpolateMethod.restype = ctypes.c_void_p

    library.MagickGaussianBlurImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]

    library.MagickGetImageChannelStatistics.argtypes = [ctypes.c_void_p]
    library.MagickGetImageChannelStatistics.restype = ctypes.c_void_p

    library.MagickSetImageRenderingIntent.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_int]
    library.MagickSetImageRenderingIntent.restype = ctypes.c_void_p

    library.MagickUnsharpMaskImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_double,
        ctypes.c_double, ctypes.c_double, ctypes.c_double]

    library.MagickStatisticImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                             ctypes.c_int, ctypes.c_size_t,
                                             ctypes.c_size_t]

    library.MagickQuantizeImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                            ctypes.c_int, ctypes.c_size_t,
                                            ctypes.c_int, ctypes.c_int]
    library.MagickQuantizeImage.restype = ctypes.c_void_p

    library.MagickMorphologyImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
        ctypes.c_ssize_t, ctypes.c_void_p]

    library.MagickAdaptiveSharpenImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]

    library.MagickGetImageGamma.argtypes = [ctypes.c_void_p]
    library.MagickGetImageGamma.restype = ctypes.c_double

    library.MagickGetImageCompression.argtypes = [ctypes.c_void_p]

    library.MagickThresholdImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickScaleImage.argtypes = [ctypes.c_void_p,
                                         ctypes.c_size_t, ctypes.c_size_t]
    library.MagickScaleImage.restype = ctypes.c_void_p

    library.MagickFlipImage.argtypes = [ctypes.c_void_p]

    library.MagickGetImageRange.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickWriteImagesFile.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickSetImageBias.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSetImageBias.restype = ctypes.c_void_p

    library.MagickMinifyImage.argtypes = [ctypes.c_void_p]

    library.MagickShadowImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                          ctypes.c_double, ctypes.c_ssize_t,
                                          ctypes.c_ssize_t]
    library.MagickShadowImage.restype = ctypes.c_void_p

    library.MagickDisplayImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickSetImageMatteColor.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_void_p]
    library.MagickSetImageMatteColor.restype = ctypes.c_void_p

    library.MagickAnnotateImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                            ctypes.c_double, ctypes.c_double,
                                            ctypes.c_double, ctypes.c_char_p]

    library.MagickDistortImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double), ctypes.c_int]

    library.MagickEqualizeImage.argtypes = [ctypes.c_void_p]

    library.MagickUniqueImageColors.argtypes = [ctypes.c_void_p]

    library.MagickGetImageGreenPrimary.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickPosterizeImage.argtypes = [ctypes.c_void_p,
                                             ctypes.c_size_t, ctypes.c_int]
    library.MagickPosterizeImage.restype = ctypes.c_void_p

    library.MagickGetImageRegion.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_ssize_t, ctypes.c_ssize_t]
    library.MagickGetImageRegion.restype = ctypes.c_void_p

    library.MagickGetImageInterpolateMethod.argtypes = [ctypes.c_void_p]

    library.MagickFloodfillPaintImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
        ctypes.c_double, ctypes.c_void_p, ctypes.c_ssize_t,
        ctypes.c_ssize_t, ctypes.c_int]

    library.MagickColorMatrixImage.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p]

    library.MagickSelectiveBlurImage.argtypes = [
            ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    library.MagickSelectiveBlurImage.restype = ctypes.c_void_p

    library.MagickSetImageColormapColor.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_size_t,
                                                    ctypes.c_void_p]
    library.MagickSetImageColormapColor.restype = ctypes.c_void_p

    library.MagickInverseFourierTransformImage.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]

    library.MagickFxImageChannel.argtypes = [ctypes.c_void_p,
                                             ctypes.c_int, ctypes.c_char_p]
    library.MagickFxImageChannel.restype = ctypes.c_void_p

    library.MagickOptimizeImageLayers.argtypes = [ctypes.c_void_p]
    library.MagickOptimizeImageLayers.restype = ctypes.c_void_p

    library.MagickAdaptiveResizeImage.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_size_t,
                                                  ctypes.c_size_t]

    library.MagickPreviousImage.argtypes = [ctypes.c_void_p]
    library.MagickPreviousImage.restype = ctypes.c_void_p

    library.MagickGetImageColormapColor.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_size_t,
                                                    ctypes.c_void_p]

    library.MagickStereoImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.MagickStereoImage.restype = ctypes.c_void_p

    library.MagickCompareImages.argtypes = [ctypes.c_void_p,
                                            ctypes.c_void_p, ctypes.c_int,
                                            ctypes.POINTER(ctypes.c_double)]
    library.MagickCompareImages.restype = ctypes.c_void_p

    library.MagickCompositeLayers.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                              ctypes.c_int, ctypes.c_ssize_t,
                                              ctypes.c_ssize_t]

    library.MagickFunctionImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
        ctypes.c_size_t, ctypes.POINTER(ctypes.c_double)]

    library.MagickRollImage.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t,
                                        ctypes.c_ssize_t]
    library.MagickRollImage.restype = ctypes.c_void_p

    library.MagickContrastStretchImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]

    library.MagickClutImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickSetImageIterations.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_size_t]
    library.MagickSetImageIterations.restype = ctypes.c_void_p

    library.MagickFxImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    library.MagickFxImage.restype = ctypes.c_void_p

    library.MagickSketchImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                          ctypes.c_double, ctypes.c_double]
    library.MagickSketchImage.restype = ctypes.c_void_p

    library.MagickEncipherImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickDeconstructImages.argtypes = [ctypes.c_void_p]
    library.MagickDeconstructImages.restype = ctypes.c_void_p

    library.MagickRemoveImage.argtypes = [ctypes.c_void_p]
    library.MagickRemoveImage.restype = ctypes.c_void_p

    library.MagickPingImageBlob.argtypes = [ctypes.c_void_p,
                                            ctypes.c_void_p, ctypes.c_size_t]
    library.MagickPingImageBlob.restype = ctypes.c_void_p

    library.MagickMotionBlurImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_double,
        ctypes.c_double, ctypes.c_double]

    library.MagickAppendImages.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickAppendImages.restype = ctypes.c_void_p

    library.MagickGetImageFilename.argtypes = [ctypes.c_void_p]
    library.MagickGetImageFilename.restype = ctypes.c_char_p

    library.MagickGetImageRedPrimary.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickClipImage.argtypes = [ctypes.c_void_p]

    library.MagickMergeImageLayers.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickMergeImageLayers.restype = ctypes.c_void_p

    library.MagickTransformImageColorspace.argtypes = [ctypes.c_void_p,
                                                       ctypes.c_int]

    library.MagickLinearStretchImage.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_double,
                                                 ctypes.c_double]

    library.MagickGetImageChannelDistortion.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,
        ctypes.c_int, ctypes.POINTER(ctypes.c_double)]

    library.MagickGetImageBorderColor.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_void_p]

    library.MagickRemapImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                         ctypes.c_int]
    library.MagickRemapImage.restype = ctypes.c_void_p

    library.MagickUnsharpMaskImage.argtypes = [
        ctypes.c_void_p, ctypes.c_double, ctypes.c_double,
        ctypes.c_double, ctypes.c_double]

    library.MagickLevelImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_double,
        ctypes.c_double, ctypes.c_double]

    library.MagickSharpenImage.argtypes = [ctypes.c_void_p,
                                           ctypes.c_double, ctypes.c_double]
    library.MagickSharpenImage.restype = ctypes.c_void_p

    library.MagickAnimateImages.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickAdaptiveThresholdImage.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t,
        ctypes.c_size_t, ctypes.c_ssize_t]

    library.GetImageFromMagickWand.argtypes = [ctypes.c_void_p]
    library.GetImageFromMagickWand.restype = ctypes.c_void_p

    library.MagickFilterImageChannel.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_int,
                                                 ctypes.c_void_p]

    library.MagickAddImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickAutoGammaImage.argtypes = [ctypes.c_void_p]

    library.MagickCompareImageLayers.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickCompareImageLayers.restype = ctypes.c_void_p

    library.MagickRaiseImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                         ctypes.c_size_t, ctypes.c_ssize_t,
                                         ctypes.c_ssize_t, ctypes.c_int]
    library.MagickRaiseImage.restype = ctypes.c_void_p

    library.MagickFilterImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickGetImageClipMask.argtypes = [ctypes.c_void_p]
    library.MagickGetImageClipMask.restype = ctypes.c_void_p

    library.MagickHaldClutImageChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int,
                                                   ctypes.c_void_p]

    library.MagickMorphImages.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    library.MagickMorphImages.restype = ctypes.c_void_p

    library.MagickMagnifyImage.argtypes = [ctypes.c_void_p]

    library.MagickSampleImage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_size_t]
    library.MagickSampleImage.restype = ctypes.c_void_p

    library.MagickExportImagePixels.argtypes = [
        ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_ssize_t,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_char_p,
        ctypes.c_int, ctypes.c_void_p]

    library.MagickCycleColormapImage.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_ssize_t]

    library.MagickAddNoiseImage.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickMedianFilterImage.argtypes = [ctypes.c_void_p,
                                                ctypes.c_double]

    library.MagickTextureImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.MagickTextureImage.restype = ctypes.c_void_p

    library.MagickRandomThresholdImage.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_double,
                                                   ctypes.c_double]
    library.MagickRandomThresholdImage.restype = ctypes.c_void_p

    library.MagickSetImageClipMask.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p]
    library.MagickSetImageClipMask.restype = ctypes.c_void_p

    library.MagickMotionBlurImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                              ctypes.c_double, ctypes.c_double]

    library.MagickOpaquePaintImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_double, ctypes.c_int]

    library.MagickEvaluateImages.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickEvaluateImages.restype = ctypes.c_void_p

    library.MagickGammaImageChannel.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                                ctypes.c_double]

    library.MagickConvolveImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double)]

    library.MagickDisplayImages.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickGetImageDistortion.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_int, ctypes.POINTER(ctypes.c_double)]

    library.MagickCoalesceImages.argtypes = [ctypes.c_void_p]
    library.MagickCoalesceImages.restype = ctypes.c_void_p

    library.MagickSetImagePage.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                           ctypes.c_size_t, ctypes.c_ssize_t,
                                           ctypes.c_ssize_t]
    library.MagickSetImagePage.restype = ctypes.c_void_p

    library.MagickOilPaintImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickLevelImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                         ctypes.c_double, ctypes.c_double]

    library.MagickNegateImage.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickSparseColorImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                               ctypes.c_int, ctypes.c_size_t,
                                               ctypes.POINTER(ctypes.c_double)]

    library.MagickAdaptiveBlurImage.argtypes = [
        ctypes.c_void_p, ctypes.c_double, ctypes.c_double]

    library.MagickContrastImage.argtypes = [ctypes.c_void_p, ctypes.c_int]

    library.MagickDestroyImage.argtypes = [ctypes.c_void_p]
    library.MagickDestroyImage.restype = ctypes.c_void_p

    library.MagickBlackThresholdImage.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_void_p]

    library.MagickTransverseImage.argtypes = [ctypes.c_void_p]

    library.MagickGetImageEndian.argtypes = [ctypes.c_void_p]

    library.MagickPolaroidImage.argtypes = [ctypes.c_void_p,
                                            ctypes.c_void_p, ctypes.c_double]
    library.MagickPolaroidImage.restype = ctypes.c_void_p

    library.MagickClampImage.argtypes = [ctypes.c_void_p]

    library.MagickRandomThresholdImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]
    library.MagickRandomThresholdImageChannel.restype = ctypes.c_void_p

    library.MagickNormalizeImage.argtypes = [ctypes.c_void_p]

    library.MagickNextImage.argtypes = [ctypes.c_void_p]

    library.MagickSetImageBluePrimary.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_double,
                                                  ctypes.c_double]
    library.MagickSetImageBluePrimary.restype = ctypes.c_void_p

    library.MagickCommentImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickWhiteThresholdImage.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_void_p]

    library.MagickGetImageWhitePoint.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double)]

    library.MagickEqualizeImageChannel.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_int]

    library.MagickSwirlImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickNormalizeImageChannel.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int]

    library.MagickSetImageOrientation.argtypes = [ctypes.c_void_p,
                                                  ctypes.c_int]
    library.MagickSetImageOrientation.restype = ctypes.c_void_p

    library.MagickSetImageFilename.argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p]
    library.MagickSetImageFilename.restype = ctypes.c_void_p

    library.MagickGetImageDispose.argtypes = [ctypes.c_void_p]

    library.MagickGetImagePage.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t),
        ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_ssize_t),
        ctypes.POINTER(ctypes.c_ssize_t)]

    library.MagickImplodeImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickMorphologyImage.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_ssize_t, ctypes.c_void_p]

    library.MagickSelectiveBlurImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_double,
        ctypes.c_double, ctypes.c_double]
    library.MagickSelectiveBlurImageChannel.restype = ctypes.c_void_p

    library.MagickDrawImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickSetImageInterlaceScheme.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_int]
    library.MagickSetImageInterlaceScheme.restype = ctypes.c_void_p

    library.MagickGetImage.argtypes = [ctypes.c_void_p]
    library.MagickGetImage.restype = ctypes.c_void_p

    library.MagickOrderedPosterizeImageChannel.argtypes = [ctypes.c_void_p,
                                                           ctypes.c_int,
                                                           ctypes.c_char_p]

    library.MagickGetImageInterlaceScheme.argtypes = [ctypes.c_void_p]

    library.MagickAutoGammaImageChannel.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int]

    library.MagickSetImageGamma.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSetImageGamma.restype = ctypes.c_void_p

    library.MagickSetImageProgressMonitor.argtypes = [ctypes.c_void_p,
                                                      ctypes.c_int,
                                                      ctypes.c_void_p]

    library.MagickSolarizeImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSolarizeImage.restype = ctypes.c_void_p

    library.MagickNegateImageChannel.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_int, ctypes.c_int]

    library.MagickSetImageDispose.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageDispose.restype = ctypes.c_void_p

    library.MagickMontageImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
    library.MagickMontageImage.restype = ctypes.c_void_p

    library.MagickSigmoidalContrastImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]
    library.MagickSigmoidalContrastImageChannel.restype = ctypes.c_void_p

    library.MagickSimilarityImage.argtypes = [ctypes.c_void_p,
        ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
    library.MagickSimilarityImage.restype = ctypes.c_void_p

    library.MagickResampleImage.argtypes = [ctypes.c_void_p,
        ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_double]
    library.MagickResampleImage.restype = ctypes.c_void_p

    library.MagickSetImageCompose.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageCompose.restype = ctypes.c_void_p

    library.MagickGetImageChannelRange.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

    library.MagickOrderedPosterizeImage.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_char_p]

    library.MagickLabelImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickBlueShiftImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickSetImageMatte.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageMatte.restype = ctypes.c_void_p

    library.MagickThresholdImageChannel.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int,
                                                    ctypes.c_double]

    library.MagickTransposeImage.argtypes = [ctypes.c_void_p]

    library.MagickSetImageColorspace.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageColorspace.restype = ctypes.c_void_p

    library.MagickDecipherImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    library.MagickWaveImage.argtypes = [ctypes.c_void_p,
        ctypes.c_double, ctypes.c_double]

    library.MagickCharcoalImage.argtypes = [ctypes.c_void_p,
        ctypes.c_double, ctypes.c_double]

    library.MagickSetImageTicksPerSecond.argtypes = [ctypes.c_void_p,
        ctypes.c_ssize_t]
    library.MagickSetImageTicksPerSecond.restype = ctypes.c_void_p

    library.MagickGetImageTotalInkDensity.argtypes = [ctypes.c_void_p]
    library.MagickGetImageTotalInkDensity.restype = ctypes.c_double

    library.MagickConstituteImage.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p]

    library.MagickColorDecisionListImage.argtypes = [ctypes.c_void_p,
                                                     ctypes.c_char_p]

    library.MagickQuantizeImages.argtypes = [
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
        ctypes.c_size_t, ctypes.c_int, ctypes.c_int]
    library.MagickQuantizeImages.restype = ctypes.c_void_p

    library.MagickSetImageGravity.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageGravity.restype = ctypes.c_void_p

    library.MagickGetImageGravity.argtypes = [ctypes.c_void_p]

    library.MagickCombineImages.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickCombineImages.restype = ctypes.c_void_p

    library.MagickAutoLevelImage.argtypes = [ctypes.c_void_p]

    library.MagickConvolveImage.argtypes = [ctypes.c_void_p,
                                            ctypes.c_size_t,
                                            ctypes.POINTER(ctypes.c_double)]

    library.MagickSetImageGreenPrimary.argtypes = [ctypes.c_void_p,
                                                   ctypes.c_double,
                                                   ctypes.c_double]
    library.MagickSetImageGreenPrimary.restype = ctypes.c_void_p

    library.MagickModulateImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                            ctypes.c_double, ctypes.c_double]

    library.MagickRadialBlurImageChannel.argtypes = [ctypes.c_void_p,
        ctypes.c_int, ctypes.c_double]
    library.MagickRadialBlurImageChannel.restype = ctypes.c_void_p

    library.MagickSetImageEndian.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickSetImageEndian.restype = ctypes.c_void_p

    library.MagickFrameImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                         ctypes.c_size_t, ctypes.c_size_t,
                                         ctypes.c_ssize_t, ctypes.c_ssize_t]

    library.MagickShadeImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                         ctypes.c_double, ctypes.c_double]
    library.MagickShadeImage.restype = ctypes.c_void_p

    library.MagickSpreadImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickEdgeImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickSharpenImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]
    library.MagickSharpenImageChannel.restype = ctypes.c_void_p

    library.MagickOpaquePaintImage.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_double, ctypes.c_int]

    library.MagickSetImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    library.MagickSetImage.restype = ctypes.c_void_p

    library.MagickSetImageWhitePoint.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_double,
                                                 ctypes.c_double]
    library.MagickSetImageWhitePoint.restype = ctypes.c_void_p

    library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSepiaToneImage.restype = ctypes.c_void_p

    library.MagickTransparentPaintImage.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double,
        ctypes.c_double, ctypes.c_int]
    library.MagickTransparentPaintImage.restype = ctypes.c_void_p

    library.MagickGetImageColorspace.argtypes = [ctypes.c_void_p]

    library.MagickFlopImage.argtypes = [ctypes.c_void_p]

    library.MagickSmushImages.argtypes = [ctypes.c_void_p,
        ctypes.c_int, ctypes.c_ssize_t]
    library.MagickSmushImages.restype = ctypes.c_void_p

    library.MagickGetImageChannelMean.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

    library.MagickSetImageRedPrimary.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_double,
                                                 ctypes.c_double]
    library.MagickSetImageRedPrimary.restype = ctypes.c_void_p

    library.MagickGetImageCompose.argtypes = [ctypes.c_void_p]

    library.MagickAdaptiveBlurImageChannel.argtypes = [
        ctypes.c_void_p, ctypes.c_int,
        ctypes.c_double, ctypes.c_double]

    library.MagickVignetteImage.argtypes = [ctypes.c_void_p, ctypes.c_double,
                                            ctypes.c_double, ctypes.c_ssize_t,
                                            ctypes.c_ssize_t]

    library.MagickGetImageLength.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    library.MagickSegmentImage.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                           ctypes.c_int, ctypes.c_double,
                                           ctypes.c_double]
    library.MagickSegmentImage.restype = ctypes.c_void_p

    library.MagickPreviewImages.argtypes = [ctypes.c_void_p, ctypes.c_int]
    library.MagickPreviewImages.restype = ctypes.c_void_p

    library.MagickGammaImage.argtypes = [ctypes.c_void_p, ctypes.c_double]

    library.MagickImportImagePixels.argtypes = [
        ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_ssize_t,
        ctypes.c_size_t, ctypes.c_size_t, ctypes.c_char_p,
        ctypes.c_int, ctypes.c_void_p]
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

