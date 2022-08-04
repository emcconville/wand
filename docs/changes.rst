Wand Changelog
==============

.. _changelog-0.6:

0.6 series
~~~~~~~~~~


.. _changelog-0.6.9:

Version 0.6.9
-------------

Released on August 3rd, 2022.

 - Updated :meth:`Image.fx() <wand.image.BaseImage.fx>` method to raise :class:`~wand.exceptions.WandRuntimeError` if ImageMagick is unable to generate an image. [:issue:`582`]
 - Fixed :meth:`Image.from_array() <wand.image.Image.from_array>` classmethod to handle Numpy's strided arrays. [:issue:`582`]
 - Fixed segmentation fault introduced with ImageMagick 7.1.0-45. [:issue:`586`]


.. _changelog-0.6.8:

Version 0.6.8
-------------

Released on July 16th, 2022.

 - Added :meth:`Image.label() <wand.image.BaseImage.label>` method.
 - Added :meth:`Image.region() <wand.image.BaseImage.region>` method.
 - Updated :meth:`Image.chop() <wand.image.BaseImage.chop>` method to support ``gravity`` keyword.
 - Updated :meth:`Image.extent() <wand.image.BaseImage.extent>` method to support ``gravity`` keyword. [:issue:`554`]
 - Added `.so.9` shared library suffix to :meth:`wand.api.library_paths()` generator when searching :const:`MAGICK_HOME` path.
 - Added :const:`QUANTUM_SCALE <wand.version.QUANTUM_SCALE>` constant.
 - Added :meth:`Image.montage() <wand.image.Image.montage>` method. [:issue:`575`]
 - Added :meth:`Image.roll() <wand.image.BaseImage.roll>` method.
 - Fixed returned values for :meth:`Image.connected_components() <wand.image.BaseImage.connected_components>` method for ImageMagick 7.1.1. [:issue:`574`]
 - Fixed :c:func:`MagickSetImageDepth()` C-API method signature. [:issue:`577` by Pavel Borzenkov]
 - Fixed :meth:`Image.encipher() <wand.image.BaseImage.encipher>` method to call the correct API. [:issue:`578` by Pavel Borzenkov]
 - [DOC] Improved :class:`~wand.drawing.FontMetrics` documentation. [:issue:`566`]
 - [TEST] Migrated CI from `travis-ci.org <https://travis-ci.org/github/emcconville/wand>`_ to `travis-ci.com <https://app.travis-ci.com/emcconville/wand>`_.
 - [TEST] Removed unneeded SVG dependency from regression test.
 - [TEST] Suppressed :class:`~wand.exceptions.OptionWarning` when testing user errors.
 - [TEST] Added Python 3.9 regression test for `travis-ci.com <https://app.travis-ci.com/emcconville/wand>`_.
 - [TEST] Removed Python 3.7 & 3.8 regression test for `travis-ci.com <https://app.travis-ci.com/emcconville/wand>`_.
 - [TEST] Added Python 3.10 regression tests for `github actions <https://github.com/emcconville/wand/actions>`_.


.. _changelog-0.6.7:

Version 0.6.7
-------------

Released on August 16th, 2021.

 - Added :meth:`Image.image_add() <wand.image.Image.image_add>` method.
 - Added :meth:`Image.image_get() <wand.image.Image.image_get>` method.
 - Added :meth:`Image.image_remove() <wand.image.Image.image_remove>` method.
 - Added :meth:`Image.image_set() <wand.image.Image.image_set>` method.
 - Added :meth:`Image.image_swap() <wand.image.Image.image_swap>` method.
 - Fixed sub-image extraction on read. [:issue:`532`]
 - Fixed :attr:`~wand.image.BaseImage.background_color` attribute when image was not read.
 - [DOC] Completed :doc:`Distortion <./guide/distortion>` guide. [:issue:`534`]
 - [DOC] Added :doc:`Morphology <./guide/morphology>` guide.


.. _changelog-0.6.6:

Version 0.6.6
-------------

Released on February 28th, 2021.

 - Added :meth:`Image.get_image_distortion() <wand.image.BaseImage.get_image_distortion>` method.
 - Fixed `QuantumType` allocation for 32-bit architectures using HDRI. [:issue:`518`]
 - Fixed `MagickSizeType` allocation for :meth:`ResourceLimits.set_resource_limit() <wand.resource.ResourceLimits.set_resource_limit>` and segfault with ``armv7l`` architecture. [:issue:`520`]
 - Fixed :class:`~wand.color.Color` deallocation error on 32-bit architectures.
 - Deprecated :meth:`wand.color.scale_quantum_to_int8()`
 - [TEST] Deprecated PDF format from test assets.
 - [TEST] Deprecated :class:`~wand.drawing.Drawing` test `fx_wand` fixture to improve parallel CI testing.
 - [TEST] Marked all ImageMagick-7 features skipped when running test suite with ImageMagick-6. [:issue:`522`]


.. _changelog-0.6.5:

Version 0.6.5
-------------

Released on November 29th, 2020.

 - Fixed memory allocation & deallocation bugs with PyPy3, and various memory leaks identified during regression testing. [:issue:`510`]
 - [TEST] Added Python 3.9 into Github regression tests. [:issue:`513` by Thijs Triemstra]


.. _changelog-0.6.4:

Version 0.6.4
-------------

Released on November 21st, 2020.

 - Fixed `MagickFloatType` mapping for **s390x** architecture. [:issue:`504` & :issue:`505`]
 - Fixed image order when calling :meth:`wand.sequence.Sequence.__setitem__()` method. [:issue:`506`]
 - Fixed :meth:`Image.gaussian_blur() <wand.image.BaseImage.gaussian_blur>` method with ``channel`` parameter. [:issue:`507`]
 - Added :meth:`Image.color_threshold() <wand.image.BaseImage.color_threshold>` method.
 - Added :meth:`Image.convex_hull() <wand.image.BaseImage.convex_hull>` method. Requires ImageMagick-7.0.10 or above.
 - Added :meth:`Image.kmeans() <wand.image.BaseImage.kmeans>` method. Only available with ImageMagick-7.0.10-37 or later.
 - Added :meth:`Image.minimum_bounding_box() <wand.image.BaseImage.minimum_bounding_box>` method. Requires ImageMagick-7.0.10 or above;
 - Added :meth:`Image.white_balance() <wand.image.BaseImage.white_balance>` method. Only available with ImageMagick-7.0.10-37 or later.
 - Added ``percent_background`` & ``background_color`` parameters to :meth:`Image.trim() <wand.image.BaseImage.trim>` method.
 - Added the following arguments to :meth:`Image.connected_components() <wand.image.BaseImage.connected_components>`:

   - ``angle_threshold``
   - ``background_id``
   - ``circularity_threshold``
   - ``diameter_threshold``
   - ``eccentricity_threshold``
   - ``keep_colors``
   - ``keep_top``
   - ``major_axis_threshold``
   - ``minor_axis_threshold``
   - ``perimeter_threshold``
   - ``remove_colors``

 - Added ``'inverse_log'`` operator to :meth:`Image.evaluate() <wand.image.BaseImage.evaluate>` method.
 - Added ``'rigidaffine'`` operator to :meth:`Image.distort() <wand.image.BaseImage.distort>` method. Requires ImageMagick-7.0.10 or above.
 - Added :class:`PAPERSIZE_MAP <wand.image.PAPERSIZE_MAP>` dict as a convenience lookup table.
 - Added support for setting :attr:`Image.page <wand.image.BaseImage.page>` attribute with papersizes defined in :class:`~wand.image.PAPERSIZE_MAP`.
 - [DOC] Created :doc:`Threshold <./guide/threshold>` guide.
 - [DOC] Created :doc:`Quantize <./guide/quantize>` guide.


.. _changelog-0.6.3:

Version 0.6.3
-------------

Released on September 14th, 2020.

 - Fixed buffer overflow bug in :meth:`Image.connected_components() <wand.image.BaseImage.connected_components>` method. [:issue:`496`]
 - Added :meth:`Image.data_url() <wand.image.Image.data_url>` method. [:issue:`489`]
 - Added :attr:`Image.sampling_factors <wand.image.BaseImage.sampling_factors>` property. [:issue:`491`]
 - Added :meth:`Image.encipher() <wand.image.BaseImage.encipher>` & :meth:`Image.decipher() <wand.image.BaseImage.decipher>` methods.
 - Argument ``fuzz`` for :meth:`Image.transparent_color() <wand.image.BaseImage.transparent_color>` now accepts :class:`numbers.Real` numbers.
 - Uniformed additional pre-read parameters between :meth:`Image.__init__()` & :meth:`Image.read()`.


.. _changelog-0.6.2:

Version 0.6.2
-------------

Released on July 6th, 2020.

 - Added aspect cropping support for :meth:`Image.transform() <wand.image.BaseImage.transform>` method.
 - Added iterator methods to directly navigate the internal image-stack.

   - :meth:`Image.iterator_first() <wand.image.BaseImage.iterator_first>`
   - :meth:`Image.iterator_get() <wand.image.BaseImage.iterator_get>`
   - :meth:`Image.iterator_last() <wand.image.BaseImage.iterator_last>`
   - :meth:`Image.iterator_length() <wand.image.BaseImage.iterator_length>`
   - :meth:`Image.iterator_next() <wand.image.BaseImage.iterator_next>`
   - :meth:`Image.iterator_previous() <wand.image.BaseImage.iterator_previous>`
   - :meth:`Image.iterator_reset() <wand.image.BaseImage.iterator_reset>`
   - :meth:`Image.iterator_set() <wand.image.BaseImage.iterator_set>`

 - Added ``gray`` & ``cmyk`` support for Numpy's array interface.
 - Fixed :func:`~wand.display.display` on Windows & MacOS when previewing MIFF & XC formats.
 - Fixed memory leak in :meth:`Image.transform() <wand.image.BaseImage.transform>` for ImageMagick-6.
 - Fixed animation preservation with :meth:`Image.transform() <wand.image.BaseImage.transform>` method. [:issue:`251`]
 - Fixed :attr:`Image.interlace_scheme <wand.image.BaseImage.interlace_scheme>` property. [:issue:`488`]
 - [DOC] Make the documentation reproducible. [:issue:`484` by Chris Lamb]


.. _changelog-0.6.1:

Version 0.6.1
-------------

Released on May 15th, 2020.

 - Fixed RuntimeError on deallocation when ``allocation_map`` changes. [:issue:`482` by Louis Sautier]


.. _changelog-0.6.0:

Version 0.6.0
-------------

Released on May 14th, 2020.

 - Updated :mod:`numpy` array interface methods to accept / generate
   :attr:`shape` data values as ``rows``, ``columns``, and ``channels``.
   This change should match other python-image numpy integrations. [:issue:`447`]
 - Added ``adjoin=`` argument to :meth:`Image.save() <wand.image.Image.save>` method.
 - Added ``reset_coords=`` argument to :meth:`Image.trim() <wand.image.BaseImage.trim>` method. [:issue:`472` ]
 - Added support for :mod:`atexit`'s shutdown routine. [:issue:`248` & :issue:`361`]
 - Added Python 2 classifiers to :file:`MANIFEST.in`. [:issue:`462` by Thijs Triemstra]
 - Added both test-cases and documentation to source distribution packages. [:issue:`7`, :issue:`479`, :issue:`480`]
 - Removed :file:`README.rst` from :file:`setup.py`. [:issue:`460`]
 - Rewrote memory allocation manager. [:issue:`300` & :issue:`312`]
 - Fixed segfault on macOS when invoking resource limits without calling
   :c:func:`MagickWandGenesis()`.
 - Fixed ``grayscalealpha`` spelling. [:issue:`463`]
 - Fixed :meth:`Image.deskew() <wand.image.BaseImage.deskew>` threshold argument. [:issue:`467`]
 - Fixed :attr:`Image.alpha_channel <wand.image.BaseImage.alpha_channel>` property to apply changes to all images in the stack. [:issue:`468`]
 - Fixed :meth:`Image.trim() <wand.image.BaseImage.trim>` paging offsets affected by 1x1 border. [:issue:`475`]
 - [TEST] Updated Travis CI environment to Ubuntu 18.04.04 LTS (Bionic)
 - [TEST] Deprecated display fixtures.


.. _changelog-0.5:

0.5 series
~~~~~~~~~~


.. _changelog-0.5.9:

Version 0.5.9
-------------

Released on February 10th, 2020.

 - Fixed ``dither`` parameter in :meth:`Image.quantize() <wand.image.BaseImage.quantize>` method for ImageMagick-7.
 - Added :meth:`Image.combine() <wand.image.Image.combine>` method. [Thanks Fred!]
 - Check ``__fspath__`` attribute for ``filename`` parameter when calling :meth:`Image.save() <wand.image.Image.save>`. [:issue:`452`]
 - Fixed typo in :class:`ProfileDict <wand.image.ProfileDict>` documentation. [:issue:`450` by Thijs Triemstra]
 - Fixed typo in :attr:`Resource.c_is_resource <wand.resource.Resource.c_is_resource>` documentation. [:issue:`448`]
 - Updated broken sentence in :meth:`Image.thumbnail() <wand.image.BaseImage.thumbnail>` method. [:issue:`446`]
 - Check for :meth:`linux_distribution() <platform.linux_distribution>` as method was removed in Python 3.8. [:issue:`456`]
 - Added :attr:`Image.delay <wand.image.BaseImage.delay>` property. Previously only available with :class:`~wand.sequence.SingleImage` class.


.. _changelog-0.5.8:

Version 0.5.8
-------------

Released on December 5th, 2019.

 - Check :envvar:`WAND_MAGICK_LIBRARY_SUFFIX` for additional library suffixes. [:issue:`436`]
 - Fixed :c:func:`MagickCompareImagesLayers` loading for ImageMagick-6 [:issue:`439`]
 - Fixed incorrect color values for first 5 pixels when exporting to :class:`numpy.array` [:issue:`442`]
 - Updated example in :meth:`Image.annotate() <wand.image.BaseImage.annotate>` docstring. [:issue:`441` by alexgv]
 - Fixed :attr:`Image.resolution <wand.image.BaseImage.resolution>` property to return a tuple of float values. [:issue:`444`]
 - Improved pycache performance by explicitly defining all ImageMagick warnings & errors in :mod:`wand.exceptions`.
   Previously all ImageMagick exceptions were generated dynamically during run-time.


.. _changelog-0.5.7:

Version 0.5.7
-------------

Released on September 3rd, 2019.

 - Added :meth:`Image.color_decision_list() <wand.image.BaseImage.color_decision_list>` method.
 - Added :meth:`Image.contrast() <wand.image.BaseImage.contrast>` method.
 - Added :meth:`Image.local_contrast() <wand.image.BaseImage.local_contrast>` method.
 - Added :meth:`Image.ordered_dither() <wand.image.BaseImage.ordered_dither>` method.
 - Added :meth:`Image.random_threshold() <wand.image.BaseImage.random_threshold>` method.
 - Added :meth:`Image.read_mask() <wand.image.BaseImage.read_mask>` method. [:issue:`433`]
 - Added :meth:`Image.scale() <wand.image.BaseImage.scale>` method.
 - Added :meth:`Image.sepia_tone() <wand.image.BaseImage.sepia_tone>` method.
 - Added :meth:`Image.swirl() <wand.image.BaseImage.swirl>` method.
 - Added :meth:`Image.write_mask() <wand.image.BaseImage.write_mask>` method. [:issue:`433`]
 - Converted positional to key-word arguments to allow default values & allow more consistent
   behavior with CLI operations for the following methods:

   - :meth:`Image.blur() <wand.image.BaseImage.blur>`
   - :meth:`Image.gaussian_blur() <wand.image.BaseImage.gaussian_blur>`
   - :meth:`Image.selective_blur() <wand.image.BaseImage.selective_blur>`
   - :meth:`Image.spread() <wand.image.BaseImage.spread>`
   - :meth:`Image.unsharp_mask() <wand.image.BaseImage.unsharp_mask>`

 - Restored :issue:`320` fix. [Reported by :issue:`435`]
 - Added ``colorspace`` & ``units`` argument to :class:`~wand.image.Image` init. This is useful
   for defining sRGB ahead of reading CMYKA PDF documents.



.. _changelog-0.5.6:

Version 0.5.6
-------------

Released on August 2nd, 2019.

 - Fixed invalid escape sequence warnings [:issue:`428`]
 - Fixed error on Drawing exception handling. [:issue:`427`]
 - Fixed undefined behavior when working with image frames in ImageMagick-7. [:issue:`431`]
 - Added :meth:`Image.annotate() <wand.image.BaseImage.annotate>` method. [:issue:`418`]
 - Added :meth:`Image.level_colors() <wand.image.BaseImage.level_colors>` method.
 - Added :meth:`Image.levelize_colors() <wand.image.BaseImage.levelize_colors>` method.
 - Added :meth:`Image.parse_meta_geometry() <wand.image.BaseImage.parse_meta_geometry>` method.
 - Added :meth:`Image.percent_escape() <wand.image.BaseImage.percent_escape>` helper method. [:issue:`421`]
 - Added :meth:`Image.ping() <wand.image.Image.ping>` class method. [:issue:`425`]
 - Added ``mean_color``, ``keep``, & ``remove`` parameters in :meth:`Image.connected_components() <wand.image.BaseImage.connected_components>` method.


.. _changelog-0.5.5:

Version 0.5.5
-------------

Released on July 8th, 2019.

 - Rewrote :meth:`Image.contrast_stretch() <wand.image.BaseImage.contrast_stretch>`
   method to follow modern CLI behavior.
 - Added :meth:`Image.chop() <wand.image.BaseImage.chop>` method.
 - Added :meth:`Image.clahe() <wand.image.BaseImage.clahe>` method.
 - Added :meth:`Image.features() <wand.image.BaseImage.features>` method.
 - Added :meth:`Image.forward_fourier_transform() <wand.image.BaseImage.forward_fourier_transform>` method.
 - Added :meth:`Image.inverse_fourier_transform() <wand.image.BaseImage.inverse_fourier_transform>` method.
 - Added :meth:`Image.magnify() <wand.image.BaseImage.magnify>` method.
 - Added ``channel`` parameter support for the following methods.

   - :meth:`Image.adaptive_blur() <wand.image.BaseImage.adaptive_blur>`
   - :meth:`Image.adaptive_sharpen() <wand.image.BaseImage.adaptive_sharpen>`
   - :meth:`Image.blur() <wand.image.BaseImage.blur>`
   - :meth:`Image.brightness_contrast() <wand.image.BaseImage.brightness_contrast>`
   - :meth:`Image.clamp() <wand.image.BaseImage.clamp>`
   - :meth:`Image.clut() <wand.image.BaseImage.clut>`
   - :meth:`Image.equalize() <wand.image.BaseImage.equalize>`
   - :meth:`Image.gaussian_blur() <wand.image.BaseImage.gaussian_blur>`
   - :meth:`Image.hald_clut() <wand.image.BaseImage.hald_clut>`
   - :meth:`Image.noise() <wand.image.BaseImage.noise>`
   - :meth:`Image.morphology() <wand.image.BaseImage.morphology>`
   - :meth:`Image.opaque_paint() <wand.image.BaseImage.opaque_paint>`
   - :meth:`Image.selective_blur() <wand.image.BaseImage.selective_blur>`
   - :meth:`Image.sharpen() <wand.image.BaseImage.sharpen>`
   - :meth:`Image.sigmoidal_contrast() <wand.image.BaseImage.sigmoidal_contrast>`
   - :meth:`Image.solarize() <wand.image.BaseImage.solarize>`
   - :meth:`Image.statistic() <wand.image.BaseImage.statistic>`
   - :meth:`Image.unsharp_mask() <wand.image.BaseImage.unsharp_mask>`

 - Added support for new methods introduced with ImageMagick 7.0.8-41. Upgrade to
   the latest ImageMagick version to take advantage of the following features.

   - :meth:`Image.auto_threshold() <wand.image.BaseImage.auto_threshold>`
   - :meth:`Image.canny() <wand.image.BaseImage.canny>`
   - :meth:`Image.complex() <wand.image.BaseImage.complex>`
   - :meth:`Image.connected_components() <wand.image.BaseImage.connected_components>`
   - :meth:`Image.hough_lines() <wand.image.BaseImage.hough_lines>`
   - :meth:`Image.kuwahara() <wand.image.BaseImage.kuwahara>`
   - :meth:`Image.levelize() <wand.image.BaseImage.levelize>`
   - :meth:`Image.mean_shift() <wand.image.BaseImage.mean_shift>`
   - :meth:`Image.polynomial() <wand.image.BaseImage.polynomial>`
   - :meth:`Image.range_threshold() <wand.image.BaseImage.range_threshold>`
   - :attr:`Image.seed <wand.image.BaseImage.seed>`
   - :meth:`Image.wavelet_denoise() <wand.image.BaseImage.wavelet_denoise>`


.. _changelog-0.5.4:

Version 0.5.4
-------------

Released on May 25th, 2019.

 - Rewrote :attr:`~wand.api.libc` library loader. [:issue:`409`]
 - Respect ``background`` parameter in :meth:`Image.__init__() <wand.image.Image.__init__>` constructor. [:issue:`410`]
 - Fixed :meth:`Drawing.get_font_metrics() <wand.drawing.Drawing.get_font_metrics>` not raising internal ImageMagick exception on rendering error. [:issue:`411`]
 - Fixed deleting image artifact value.
 - Fixed offset memory calculation in :meth:`Image.export_pixels() <wand.image.BaseImage.export_pixels>`
   & :meth:`Image.import_pixels() <wand.image.BaseImage.import_pixels>` methods. [:issue:`413`]
 - Added :meth:`Image.auto_gamma() <wand.image.BaseImage.auto_gamma>` method.
 - Added :meth:`Image.auto_level() <wand.image.BaseImage.auto_level>` method.
 - Added :attr:`Image.border_color <wand.image.BaseImage.border_color>` property.
 - Added :meth:`Image.brightness_contrast() <wand.image.BaseImage.brightness_contrast>` method.
 - Added :meth:`Image.mode() <wand.image.BaseImage.mode>` method.
 - Added :meth:`Image.motion_blur() <wand.image.BaseImage.motion_blur>` method.
 - Added :meth:`Image.oil_paint() <wand.image.BaseImage.oil_paint>` method.
 - Added :meth:`Image.opaque_paint() <wand.image.BaseImage.opaque_paint>` method.
 - Added :meth:`Image.polaroid() <wand.image.BaseImage.polaroid>` method.
 - Added :attr:`Image.rendering_intent <wand.image.BaseImage.rendering_intent>` property.
 - Added :meth:`Image.rotational_blur() <wand.image.BaseImage.rotational_blur>` method.
 - Added :attr:`Image.scene <wand.image.BaseImage.scene>` property.
 - Added :meth:`Image.shear() <wand.image.BaseImage.shear>` method.
 - Added :meth:`Image.sigmoidal_contrast() <wand.image.BaseImage.sigmoidal_contrast>` method.
 - Added :meth:`Image.similarity() <wand.image.BaseImage.similarity>` method.
 - Added :meth:`Image.stegano() <wand.image.BaseImage.stegano>` method.
 - Added :meth:`Image.stereogram() <wand.image.Image.stereogram>` class method.
 - Added :meth:`Image.texture() <wand.image.BaseImage.texture>` method.
 - Added :meth:`Image.thumbnail() <wand.image.BaseImage.thumbnail>` method. [:issue:`357` by yoch]
 - Added :attr:`Image.ticks_per_second <wand.image.BaseImage.ticks_per_second>` property.


.. _changelog-0.5.3:

Version 0.5.3
-------------

Released on April 20, 2019.

 - Fixed alpha channel set to "on" & "off" values for ImageMagick-7. [:issue:`404`]
 - Updated :meth:`Image.composite <wand.image.BaseImage.composite>` &
   :meth:`Image.composite_channel <wand.image.BaseImage.composite_channel>` to
   include optional arguments for composite methods that require extra controls.
 - Updated :meth:`Image.composite <wand.image.BaseImage.composite>` &
   :meth:`Image.composite_channel <wand.image.BaseImage.composite_channel>` to
   include optional gravity argument.
 - Support for numpy arrays. [:issue:`65`]
     - Added :meth:`Image.from_array <wand.image.Image.from_array>` class method.
 - Support color map / palette manipulation. [:issue:`403`]
     - Added :attr:`Image.colors <wand.image.BaseImage.colors>` property.
     - Added :meth:`Image.color_map() <wand.image.BaseImage.color_map>` method.
     - Added :meth:`Image.cycle_color_map() <wand.image.BaseImage.cycle_color_map>` method.
 - Support for ``highlight`` & ``lowlight`` has been added to
   :meth:`Image.compare() <wand.image.BaseImage.compare>` method.
 - Support for PEP-519 for objects implementing :attr:`__fspath__`, in :meth:`~wand.compat.encode_filename`.
 - Added :meth:`Image.adaptive_blur() <wand.image.BaseImage.adaptive_blur>` method.
 - Added :meth:`Image.adaptive_resize() <wand.image.BaseImage.adaptive_resize>` method.
 - Added :meth:`Image.adaptive_sharpen() <wand.image.BaseImage.adaptive_sharpen>` method.
 - Added :meth:`Image.adaptive_threshold() <wand.image.BaseImage.adaptive_threshold>` method.
 - Added :meth:`Image.black_threshold() <wand.image.BaseImage.black_threshold>` method.
 - Added :meth:`Image.blue_shift() <wand.image.BaseImage.blue_shift>` method.
 - Added :meth:`Image.charcoal() <wand.image.BaseImage.charcoal>` method.
 - Added :meth:`Image.color_matrix() <wand.image.BaseImage.color_matrix>` method.
 - Added :meth:`Image.colorize() <wand.image.BaseImage.colorize>` method.
 - Added :attr:`Image.fuzz <wand.image.BaseImage.fuzz>` property.
 - Added :attr:`Image.kurtosis <wand.image.BaseImage.kurtosis>` property.
 - Added :meth:`Image.kurtosis_channel() <wand.image.BaseImage.kurtosis_channel>` method
 - Added :attr:`Image.maxima <wand.image.BaseImage.maxima>` property.
 - Added :attr:`Image.mean <wand.image.BaseImage.mean>` property.
 - Added :meth:`Image.mean_channel() <wand.image.BaseImage.mean_channel>` method
 - Added :attr:`Image.minima <wand.image.BaseImage.minima>` property.
 - Added :meth:`Image.noise() <wand.image.BaseImage.noise>` method.
 - Added :meth:`Image.range_channel() <wand.image.BaseImage.range_channel>` method
 - Added :meth:`Image.remap() <wand.image.BaseImage.remap>` method.
 - Added :meth:`Image.selective_blur() <wand.image.BaseImage.selective_blur>` method.
 - Added :attr:`Image.skewness <wand.image.BaseImage.skewness>` property.
 - Added :meth:`Image.sketch() <wand.image.BaseImage.sketch>` method.
 - Added :meth:`Image.smush() <wand.image.BaseImage.smush>` method.
 - Added :meth:`Image.sparse_color() <wand.image.BaseImage.sparse_color>` method.
 - Added :meth:`Image.splice() <wand.image.BaseImage.splice>` method.
 - Added :meth:`Image.spread() <wand.image.BaseImage.spread>` method.
 - Added :attr:`Image.standard_deviation <wand.image.BaseImage.standard_deviation>` property.
 - Added :meth:`Image.statistic() <wand.image.BaseImage.statistic>` method.
 - Added :meth:`Image.tint() <wand.image.BaseImage.tint>` method.


*Special thanks to Fred Weinhaus for helping test this release.*


.. _changelog-0.5.2:

Version 0.5.2
-------------

Released on March 24, 2019.

 - Import :mod:`collections.abc` explicitly. [:issue:`398` by Stefan Naumann]
 - Fixed memory leak in :class:`~wand.image.HistogramDict`. [:issue:`397`]
 - Fixed compression & compression quality bug. [:issue:`202` & :issue:`278`]
 - :meth:`Image.read() <wand.image.Image.read>` will raise :class:`~wand.exceptions.WandRuntimeError` if
   :c:func:`MagickReadImage` returns :c:type:`MagickFalse`, but does not emit exception. [:issue:`319`]
 - Added :meth:`Image.implode() <wand.image.BaseImage.implode>` method.
 - Added :meth:`Image.vignette() <wand.image.BaseImage.vignette>` method.
 - Added :meth:`Image.wave() <wand.image.BaseImage.wave>` method.
 - Added :meth:`Image.white_threshold() <wand.image.BaseImage.white_threshold>` method.
 - Added :attr:`Image.blue_primary <wand.image.BaseImage.blue_primary>` property.
 - Added :attr:`Image.green_primary <wand.image.BaseImage.green_primary>` property.
 - Added :attr:`Image.interlace_scheme <wand.image.BaseImage.interlace_scheme>` property.
 - Added :attr:`Image.interpolate_method <wand.image.BaseImage.interpolate_method>` property.
 - Added :attr:`Image.red_primary <wand.image.BaseImage.red_primary>` property.
 - Added :attr:`Image.white_point <wand.image.BaseImage.white_point>` property.


.. _changelog-0.5.1:

Version 0.5.1
-------------

Released on February 15, 2019.

- Added set pixel color via `Image[x, y] = Color('...')`. [:issue:`105`]
- Added :class:`limits <wand.resource.ResourceLimits>` helper dictionary to
  allows getting / setting ImageMagick's resource-limit policies. [:issue:`97`]
- Fixed segmentation violation for win32 & ImageMagick-7. [:issue:`389`]
- Fixed `AssertError` by moving :attr:`~wand.sequence.SingleImage` sync
  behavior from ``destroy`` to context ``__exit__``. [:issue:`388`]
- Fixed memory leak in :attr:`~wand.drawing.Drawing.get_font_metrics`. [:issue:`390`]
- Added property setters for :class:`~wand.color.Color` attributes.
- Added :attr:`~wand.color.Color.cyan`, :attr:`~wand.color.Color.magenta`,
  :attr:`~wand.color.Color.yellow`, & :attr:`~wand.color.Color.black`
  properties for CMYK :class:`~wand.color.Color` instances.
- :class:`~wand.color.Color` instance can be created from HSL values with
  :meth:`~wand.color.Color.from_hsl()` class method.
- Added :attr:`Image.compose <wand.image.BaseImage.compose>` property for
  identifying layer visibility.
- Added :attr:`Image.profiles <wand.image.ProfileDict>` dictionary attribute. [:issue:`249`]
- Moved :mod:`collections.abc` to :attr:`wand.compat.abc` for Python-3.8. [:issue:`394` by Tero Vuotila]
- Update :mod:`wand.display` to use Python3 compatible :func:`print()` function. [:issue:`395` by Tero Vuotila]


.. _changelog-0.5.0:

Version 0.5.0
-------------

Released on January 1, 2019.

- Support for ImageMagick-7.
- Improved support for 32-bit systems.
- Improved support for non-Q16 libraries.
- Removed `README.rst` from setup.py's `data_files`. [:issue:`336`]
- Improved `EXIF:ORIENTATION` handling. [:issue:`364` by M. Skrzypek]
- Tolerate failures while accessing wand.api. [:issue:`220` by Utkarsh Upadhyay]
- Added support for Image Artifacts through :attr:`Image.artifacts <wand.image.Image.artifacts>`. [:issue:`369`]
- Added optional stroke color/width parameters for :class:`Font <wand.font.Font>`.
- Image layers support (:issue:`22`)

    - Added :meth:`Image.coalesce() <wand.image.BaseImage.coalesce>` method.
    - Added :meth:`Image.deconstruct <wand.image.BaseImage.deconstruct>` method.
    - Added :attr:`Image.dispose <wand.image.BaseImage.dispose>` property.
    - Added :meth:`Image.optimize_layers() <wand.image.BaseImage.optimize_layers>` method.
    - Added :meth:`Image.optimize_transparency() <wand.image.BaseImage.optimize_transparency>` method.

- Implemented :meth:`__array_interface__` for NumPy [:issue:`65`]
- Migrated the following methods & attributes from :class:`Image <wand.image.Image>`
  to :class:`BaseImage <wand.image.BaseImage>` for a more uniformed code-base.

    - :attr:`Image.compression <wand.image.BaseImage.compression>`
    - :attr:`Image.format <wand.image.BaseImage.format>`
    - :meth:`Image.auto_orient() <wand.image.BaseImage.auto_orient>`
    - :meth:`Image.border() <wand.image.BaseImage.border>`
    - :meth:`Image.contrast_stretch() <wand.image.BaseImage.contrast_stretch>`
    - :meth:`Image.gamma() <wand.image.BaseImage.gamma>`
    - :meth:`Image.level() <wand.image.BaseImage.level>`
    - :meth:`Image.linear_stretch() <wand.image.BaseImage.linear_stretch>`
    - :meth:`Image.normalize() <wand.image.BaseImage.normalize>`
    - :meth:`Image.strip() <wand.image.BaseImage.strip>`
    - :meth:`Image.transpose() <wand.image.BaseImage.transpose>`
    - :meth:`Image.transverse() <wand.image.BaseImage.transverse>`
    - :meth:`Image.trim() <wand.image.BaseImage.trim>`

- Added :meth:`Image.clut() <wand.image.BaseImage.clut>` method.
- Added :meth:`Image.concat() <wand.image.BaseImage.concat>` method. [:issue:`177`]
- Added :meth:`Image.deskew() <wand.image.BaseImage.deskew>` method.
- Added :meth:`Image.despeckle() <wand.image.BaseImage.despeckle>` method.
- Added :meth:`Image.edge() <wand.image.BaseImage.edge>` method.
- Added :meth:`Image.emboss() <wand.image.BaseImage.emboss>` method. [:issue:`196`]
- Added :meth:`Image.enhance() <wand.image.BaseImage.enhance>` method. [:issue:`132`]
- Added :meth:`Image.export_pixels() <wand.image.BaseImage.export_pixels>` method.
- Added :meth:`Image.import_pixels() <wand.image.BaseImage.import_pixels>` method.
- Added :meth:`Image.morphology() <wand.image.BaseImage.morphology>` method. [:issue:`132`]
- Added :meth:`Image.posterize() <wand.image.BaseImage.posterize>` method.
- Added :meth:`Image.shade() <wand.image.BaseImage.shade>` method.
- Added :meth:`Image.shadow() <wand.image.BaseImage.shadow>` method.
- Added :meth:`Image.sharpen() <wand.image.BaseImage.sharpen>` method. [:issue:`132`]
- Added :meth:`Image.shave() <wand.image.BaseImage.shave>` method.
- Added :meth:`Image.unique_colors() <wand.image.BaseImage.unique_colors>` method.
- Method :meth:`Drawing.draw() <wand.drawing.Drawing.draw>` now accepts
  :class:`BaseImage <wand.image.BaseImage>` for folks extended classes.
- Added :attr:`Image.loop <wand.image.BaseImage.loop>` property. [:issue:`227`]
- Fixed :attr:`SingleImage.delay <wand.sequence.SingleImage.delay>` property. [:issue:`153`]
- Attribute :attr:`Image.font_antialias <wand.image.BaseImage.font_antialias>` has been
  deprecated in favor of :attr:`Image.antialias <wand.image.BaseImage.antialias>`. [:issue:`218`]
- Fixed ordering of :const:`COMPRESSION_TYPES <wand.image.COMPRESSION_TYPES>`
  based on ImageMagick version. [:issue:`309`]
- Fixed drawing on :class:`SingleImage <wand.sequence.SingleImage>`. [:issue:`289`]
- Fixed wrapping issue for larger offsets when using `gravity` kwarg in
  :meth:`Image.crop() <wand.image.BaseImage.crop>` method. [:issue:`367`]


0.4 series
~~~~~~~~~~

Version 0.4.5
-------------

Released on November 12, 2018.

- Improve library searching when ``MAGICK_HOME`` environment variable is
  set. [:issue:`320` by Chase Anderson]
- Fixed misleading `TypeError: object of type 'NoneType' has no len()` during
  destroy routines.  [:issue:`346` by Carey Metcalfe]
- Added :meth:`Image.blur() <wand.image.BaseImage.blur>` method
  (:c:func:`MagickBlurImage()`).
  [:issue:`311` by Alexander Karpinsky]
- Added :meth:`Image.extent() <wand.image.BaseImage.extent>` method
  (:c:func:`MagickExtentImage()`).
  [:issue:`233` by Jae-Myoung Yu]
- Added :meth:`Image.resample() <wand.image.BaseImage.resample>` method
  (:c:func:`MagickResampleImage()`).
  [:issue:`244` by Zio Tibia]


Version 0.4.4
-------------

Released on October 22, 2016.

- Added :exc:`~wand.exceptions.BaseError`, :exc:`~wand.exceptions.BaseWarning`,
  and :exc:`~wand.exceptions.BaseFatalError`, base classes for domains.
  [:issue:`292`]
- Fixed :exc:`TypeError` during parsing version caused by format change of
  ImageMagick version string (introduced by 6.9.6.2).
  [:issue:`310`, `Debian bug report #841548`__]
- Properly fixed again memory-leak when accessing images constructed in
  :class:`Image.sequence[] <wand.sequence.Sequence>`.  It had still leaked
  memory in the case an image is not closed using ``with`` but manual
  :func:`wand.resource.Resource.destroy()`/:func:`wand.image.Image.close()`
  method call.  [:issue:`237`]

__ https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=841548


Version 0.4.3
-------------

Released on June 1, 2016.

- Fixed :func:`repr()` for empty :class:`~.wand.image.Image` objects.
  [:issue:`265`]
- Added :meth:`Image.compare() <wand.image.BaseImage.compare>` method
  (:c:func:`MagickCompareImages()`).
  [:issue:`238`, :issue:`268` by Gyusun Yeom]
- Added :meth:`Image.page <wand.image.BaseImage.page>` and related properties for virtual canvas handling.
  [:issue:`284` by Dan Harrison]
- Added :meth:`Image.merge_layers() <wand.image.BaseImage.merge_layers>` method
  (:c:func:`MagickMergeImageLayers()`).
  [:issue:`281` by Dan Harrison]
- Fixed :exc:`OSError` during import :file:`libc.dylib` due to El Capitan's
  SIP protection.  [:issue:`275` by Ramesh Dharan]


Version 0.4.2
-------------

Released on November 30, 2015.

- Fixed :exc:`ImportError` on MSYS2.  [:issue:`257` by Eon Jeong]
- Added :meth:`Image.quantize() <wand.image.BaseImage.quantize>` method
  (:c:func:`MagickQuantizeImage()`).
  [:issue:`152` by Kang Hyojun, :issue:`262` by Jeong YunWon]
- Added :meth:`Image.transform_colorspace()
  <wand.image.BaseImage.transform_colorspace>` quantize
  (:c:func:`MagickTransformImageColorspace()`).
  [:issue:`152` by Adrian Jung, :issue:`262` by Jeong YunWon]
- Now ImageMagick DLL can be loaded on Windows even if its location
  is stored in the registry.  [:issue:`261` by Roeland Schoukens]
- Added ``depth`` parameter to :class:`~.wand.image.Image` constructor.
  The ``depth``, ``width`` and ``height`` parameters can be used
  with the ``filename``, ``file`` and ``blob`` parameters to load
  raw pixel data. [:issue:`261` by Roeland Schoukens]


Version 0.4.1
-------------

Released on August 3, 2015.

- Added :meth:`Image.auto_orient() <wand.image.BaseImage.auto_orient>`
  that fixes orientation by checking EXIF tags.
- Added :meth:`Image.transverse() <wand.image.BaseImage.transverse>` method
  (:c:func:`MagickTransverseImage()`).
- Added :meth:`Image.transpose() <wand.image.BaseImage.transpose>` method
  (:c:func:`MagickTransposeImage()`).
- Added :meth:`Image.evaluate() <wand.image.BaseImage.evaluate>` method.
- Added :meth:`Image.frame() <wand.image.BaseImage.frame>` method.
- Added :meth:`Image.function() <wand.image.BaseImage.function>` method.
- Added :meth:`Image.fx() <wand.image.BaseImage.fx>` expression method.
- Added ``gravity`` options in :meth:`Image.crop() <wand.image.BaseImage.crop>`
  method.  [:issue:`222` by Eric McConville]
- Added :attr:`Image.matte_color <wand.image.BaseImage.matte_color>` property.
- Added :attr:`Image.virtual_pixel <wand.image.BaseImage.virtual_pixel>` property.
- Added :meth:`Image.distort() <wand.image.BaseImage.distort>` method.
- Added :meth:`Image.contrast_stretch() <wand.image.BaseImage.contrast_stretch>` method.
- Added :meth:`Image.gamma() <wand.image.BaseImage.gamma>` method.
- Added :meth:`Image.linear_stretch() <wand.image.BaseImage.linear_stretch>` method.
- Additional support for :attr:`Image.alpha_channel <wand.image.BaseImage.alpha_channel>`.
- Additional query functions have been added to :mod:`wand.version` API. [:issue:`120`]

  - Added :func:`configure_options() <wand.version.configure_options>` function.
  - Added :func:`fonts() <wand.version.fonts>` function.
  - Added :func:`formats() <wand.version.formats>` function.

- Additional IPython support. [:issue:`117`]

  - Render RGB :class:`Color <wand.color.Color>` preview.
  - Display each frame in image :class:`Sequence <wand.sequence.Sequence>`.

- Fixed memory-leak when accessing images constructed in
  :class:`Image.sequence[] <wand.sequence.Sequence>`. [:issue:`237` by Eric McConville]
- Fixed Windows memory-deallocate errors on :mod:`wand.drawing` API. [:issue:`226` by Eric McConville]
- Fixed :exc:`ImportError` on FreeBSD.  [:issue:`252` by Pellaeon Lin]


.. _changelog-0.4.0:

Version 0.4.0
-------------

Released on February 20, 2015.

.. seealso::

   :doc:`whatsnew/0.4`
      This guide introduces what's new in Wand 0.4.

- Complete :mod:`wand.drawing` API.  The whole work was done by Eric McConville.
  Huge thanks for his effort!  [:issue:`194` by Eric McConville]

  - Added :meth:`Drawing.arc() <wand.drawing.Drawing.arc>` method
    (:ref:`draw-arc`).
  - Added :meth:`Drawing.bezier() <wand.drawing.Drawing.bezier>` method
    (:ref:`draw-bezier`).
  - Added :meth:`Drawing.circle() <wand.drawing.Drawing.circle>` method
    (:ref:`draw-circle`).

  - :ref:`draw-color-and-matte`

    - Added :const:`wand.drawing.PAINT_METHOD_TYPES` constant.
    - Added :meth:`Drawing.color() <wand.drawing.Drawing.color>` method.
    - Added :meth:`Drawing matte() <wand.drawing.Drawing.matte>` method.

  - Added :meth:`Drawing.composite() <wand.drawing.Drawing.composite>` method
    (:ref:`draw-composite`).
  - Added :meth:`Drawing.ellipse() <wand.drawing.Drawing.ellipse>` method
    (:ref:`draw-ellipse`).

  - :ref:`draw-paths`

    - Added :meth:`~wand.drawing.Drawing.path_start()` method.
    - Added :meth:`~wand.drawing.Drawing.path_finish()` method.
    - Added :meth:`~wand.drawing.Drawing.path_close()` method.
    - Added :meth:`~wand.drawing.Drawing.path_curve()` method.
    - Added :meth:`~wand.drawing.Drawing.path_curve_to_quadratic_bezier()`
      method.
    - Added :meth:`~wand.drawing.Drawing.path_elliptic_arc()` method.
    - Added :meth:`~wand.drawing.Drawing.path_horizontal_line()` method.
    - Added :meth:`~wand.drawing.Drawing.path_line()` method.
    - Added :meth:`~wand.drawing.Drawing.path_move()` method.
    - Added :meth:`~wand.drawing.Drawing.path_vertical_line()` method.

  - Added :meth:`Drawing.point() <wand.drawing.Drawing.point>` method
    (:ref:`draw-point`).
  - Added :meth:`Drawing.polygon() <wand.drawing.Drawing.polygon>` method
    (:ref:`draw-polygon`).
  - Added :meth:`Drawing.polyline() <wand.drawing.Drawing.polyline>` method
    (:ref:`draw-polyline`).

  - :ref:`draw-push-pop`

    - Added :meth:`~wand.drawing.Drawing.push()` method.
    - Added :meth:`~wand.drawing.Drawing.push_clip_path()` method.
    - Added :meth:`~wand.drawing.Drawing.push_defs()` method.
    - Added :meth:`~wand.drawing.Drawing.push_pattern()` method.
    - Added :attr:`~wand.drawing.Drawing.clip_path` property.
    - Added :meth:`~wand.drawing.Drawing.set_fill_pattern_url()` method.
    - Added :meth:`~wand.drawing.Drawing.set_stroke_pattern_url()` method.
    - Added :meth:`~wand.drawing.Drawing.pop()` method.

  - Added :meth:`Drawing.rectangle() <wand.drawing.Drawing.rectangle>` method
    (:ref:`draw-rectangles`).
  - Added :attr:`~wand.drawing.Drawing.stroke_dash_array` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_dash_offset` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_line_cap` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_line_join` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_miter_limit` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_opacity` property.
  - Added :attr:`~wand.drawing.Drawing.stroke_width` property.
  - Added :attr:`~wand.drawing.Drawing.fill_opacity` property.
  - Added :attr:`~wand.drawing.Drawing.fill_rule` property.

- Error message of :exc:`~wand.exceptions.MissingDelegateError` raised by
  :meth:`Image.liquid_rescale() <wand.image.BaseImage.liquid_rescale>`
  became nicer.


0.3 series
~~~~~~~~~~


Version 0.3.9
-------------

Released on December 20, 2014.

- Added ``'pdf:use-cropbox'`` option to :attr:`Image.options
  <wand.image.BaseImage.options>` dictionary (and :const:`~wand.image.OPTIONS`
  constant).  [:issue:`185` by Christoph Neuroth]
- Fixed a bug that exception message was :class:`bytes` instead of
  :class:`str` on Python 3.
- The ``size`` parameter of :class:`~wand.font.Font` class becomes optional.
  Its default value is 0, which means *autosized*.
  [:issue:`191` by Cha, Hojeong]
- Fixed a bug that :meth:`Image.read() <wand.image.Image.read>` had tried
  using :c:func:`MagickReadImageFile()` even when the given file object
  has no :attr:`mode` attribute.  [:issue:`205` by Stephen J. Fuhry]


Version 0.3.8
-------------

Released on August 3, 2014.

- Fixed a bug that transparent background becomes filled with white
  when SVG is converted to other bitmap image format like PNG.  [:issue:`184`]
- Added :meth:`Image.negate() <wand.image.BaseImage.negate>` method.
  [:issue:`174` by Park Joon-Kyu]
- Fixed a segmentation fault on :meth:`Image.modulate()
  <wand.image.BaseImage.modulate>` method.
  [:issue:`173` by Ted Fung, :issue:`158`]
- Added suggestion to install freetype also if Homebrew is used.
  [:issue:`141`]
- Now :mimetype:`image/x-gif` also is determined as :attr:`animation`.
  [:issue:`181` by Juan-Pablo Scaletti]


Version 0.3.7
-------------

Released on March 25, 2014.

- A hotfix of debug prints made at 0.3.6.


Version 0.3.6
-------------

Released on March 23, 2014.

- Added :meth:`Drawing.rectangle() <wand.drawing.Drawing.rectangle>` method.
  :ref:`Now you can draw rectangles. <draw-rectangles>` [:issue:`159`]
- Added :attr:`Image.compression <wand.image.BaseImage.compression>` property.
  [:issue:`171`]
- Added :func:`contextlib.nested()` function to :mod:`wand.compat` module.
- Fixed :exc:`UnicodeEncodeError` when :meth:`Drawing.text()
  <wand.drawing.Drawing.text>` method gives Unicode ``text`` argument
  in Python 2.  [:issue:`163`]
- Now it now allows to use Wand when Python is invoked with the ``-OO`` flag.
  [:issue:`169` by Samuel Maudo]


Version 0.3.5
-------------

Released on September 13, 2013.

- Fix segmentation fault on :meth:`Image.save() <wand.image.Image.save>` method.
  [:issue:`150`]


Version 0.3.4
-------------

Released on September 9, 2013.

- Added :meth:`Image.modulate() <wand.image.BaseImage.modulate>` method.
  [:issue:`134` by Dan P. Smith]
- Added :attr:`Image.colorspace <wand.image.BaseImage.colorspace>` property.
  [:issue:`135` by Volodymyr Kuznetsov]
- Added :meth:`Image.unsharp_mask() <wand.image.BaseImage.unsharp_mask>`
  method.  [:issue:`136` by Volodymyr Kuznetsov]
- Added ``'jpeg:sampling-factor'`` option to :attr:`Image.options
  <wand.image.BaseImage.options>` dictionary (and :const:`~wand.image.OPTIONS`
  constant).  [:issue:`137` by Volodymyr Kuznetsov]
- Fixed ImageMagick shared library resolution on Arch Linux.
  [:issue:`139`, :issue:`140` by Sergey Tereschenko]
- Added :meth:`Image.sample() <wand.image.BaseImage.sample>` method.
  [:issue:`142` by Michael Allen]
- Fixed a bug that :meth:`Image.save() <wand.image.Image.save>` preserves
  only one frame of the given animation when file-like object is passed.
  [:issue:`143`, :issue:`145` by Michael Allen]
- Fixed searching of ImageMagick shared library with HDR support enabled.
  [:issue:`148`, :issue:`149` by Lipin Dmitriy]


Version 0.3.3
-------------

Released on August 4, 2013.  It's author's birthday.

- Added :meth:`Image.gaussian_blur() <wand.image.BaseImage.gaussian_blur>`
  method.
- Added :attr:`Drawing.stroke_color <wand.drawing.Drawing.stroke_color>`
  property.  [:issue:`129` by Zeray Rice]
- Added :attr:`Drawing.stroke_width <wand.drawing.Drawing.stroke_width>`
  property.  [:issue:`130` by Zeray Rice]
- Fixed a memory leak of :class:`~wand.color.Color` class.
  [:issue:`127` by Wieland Morgenstern]
- Fixed a bug that :meth:`Image.save() <wand.image.Image.save>` to stream
  truncates data.  [:issue:`128` by Michael Allen]
- Fixed broken :func:`~wand.display.display()` on Python 3.
  [:issue:`126`]


Version 0.3.2
-------------

Released on July 11, 2013.

- Fixed incorrect encoding of filenames.  [:issue:`122`]
- Fixed key type of :attr:`Image.metadata <wand.image.Image.metadata>`
  dictionary to :class:`str` from :class:`bytes` in Python 3.
- Fixed CentOS compatibility [:issue:`116`, :issue:`124` by Pierre Vanliefland]

  - Made :c:func:`DrawSetTextInterlineSpacing()` and
    :c:func:`DrawGetTextInterlineSpacing()` optional.
  - Added exception in drawing API when trying to use
    :c:func:`DrawSetTextInterlineSpacing()` and
    :c:func:`DrawGetTextInterlineSpacing()` functions when they are not
    available.
  - Added :exc:`~wand.exceptions.WandLibraryVersionError` class for
    library versions issues.


Version 0.3.1
-------------

Released on June 23, 2013.

- Fixed :exc:`~exceptions.ImportError` on Windows.


.. _changelog-0.3.0:

Version 0.3.0
-------------

Released on June 17, 2013.

.. seealso::

   :doc:`whatsnew/0.3`
      This guide introduces what's new in Wand 0.3.

- Now also works on Python 2.6, 2.7, and 3.2 or higher.
- Added :mod:`wand.drawing` module.  [:issue:`64` by Adrian Jung]
- Added :meth:`Drawing.get_font_metrics()
  <wand.drawing.Drawing.get_font_metrics>` method.
  [:issue:`69`, :issue:`71` by Cha, Hojeong]
- Added :meth:`Image.caption() <wand.image.BaseImage.caption>` method.
  [:issue:`74` by Cha, Hojeong]
- Added optional ``color`` parameter to :meth:`Image.trim()
  <wand.image.BaseImage.trim>` method.
- Added :meth:`Image.border() <wand.image.BaseImage.border>` method.
  [:commit:`2496d37f75d75e9425f95dde07033217dc8afefc` by Jae-Myoung Yu]
- Added ``resolution`` parameter to :meth:`Image.read() <wand.image.Image.read>`
  method and the constructor of :class:`~wand.image.Image`.
  [:issue:`75` by Andrey Antukh]
- Added :meth:`Image.liquid_rescale() <wand.image.BaseImage.liquid_rescale>`
  method which does `seam carving`__.  See also :ref:`seam-carving`.
- Added :attr:`Image.metadata <wand.image.Image.metadata>` immutable mapping
  attribute and :class:`~wand.image.Metadata` mapping type for it.
  [:issue:`56` by Michael Elovskikh]
- Added :attr:`Image.channel_images <wand.image.Image.channel_images>`
  immutable mapping attribute and :class:`~wand.image.ChannelImageDict`
  mapping for it.
- Added :attr:`Image.channel_depths <wand.image.Image.channel_depths>`
  immutable mapping attribute and :class:`~wand.image.ChannelDepthDict`
  mapping for it.
- Added :meth:`Image.composite_channel()
  <wand.image.BaseImage.composite_channel>` method.
- Added :meth:`Image.read() <wand.image.Image.read>` method.
  [:issue:`58` by Piotr Florczyk]
- Added :attr:`Image.resolution <wand.image.BaseImage.resolution>` property.
  [:issue:`58` by Piotr Florczyk]
- Added :meth:`Image.blank() <wand.image.Image.blank>` method.
  [:issue:`60` by Piotr Florczyk]
- Fixed several memory leaks.  [:issue:`62` by Mitch Lindgren]
- Added :class:`~wand.image.ImageProperty` mixin class to maintain
  a weak reference to the parent image.
- Ranamed :const:`wand.image.COMPOSITE_OPS` to
  :const:`~wand.image.COMPOSITE_OPERATORS`.
- Now it shows helpful error message when ImageMagick library cannot be
  found.
- Added IPython-specialized formatter.
- Added :const:`~wand.version.QUANTUM_DEPTH` constant.

- Added these properties to :class:`~wand.color.Color` class:

  - :attr:`~wand.color.Color.red_quantum`
  - :attr:`~wand.color.Color.green_quantum`
  - :attr:`~wand.color.Color.blue_quantum`
  - :attr:`~wand.color.Color.alpha_quantum`
  - :attr:`~wand.color.Color.red_int8`
  - :attr:`~wand.color.Color.green_int8`
  - :attr:`~wand.color.Color.blue_int8`
  - :attr:`~wand.color.Color.alpha_int8`

- Added :meth:`Image.normalize() <wand.image.BaseImage.normalize>` method.
  [:issue:`95` by Michael Curry]
- Added :meth:`Image.transparent_color()
  <wand.image.BaseImage.transparent_color>` method.
  [:issue:`98` by Lionel Koenig]
- Started supporting resizing and cropping of GIF images.
  [:issue:`88` by Bear Dong, :issue:`112` by Taeho Kim]
- Added :meth:`Image.flip() <wand.image.BaseImage.flip>` method.
- Added :meth:`Image.flop() <wand.image.BaseImage.flop>` method.
- Added :attr:`Image.orientation <wand.image.BaseImage.orientation>` property.
  [:commit:`88574468a38015669dae903185fb328abdd717c0` by Taeho Kim]
- :exc:`wand.resource.DestroyedResourceError` becomes a subtype of
  :exc:`wand.exceptions.WandException`.
- :class:`~wand.color.Color` is now hashable, so can be used as a key of
  dictionaries, or an element of sets.  [:issue:`114` by klutzy]
- :class:`~wand.color.Color` has :attr:`~wand.color.Color.normalized_string`
  property.
- :class:`~wand.image.Image` has :attr:`~wand.image.BaseImage.histogram`
  dictionary.
- Added optional ``fuzz`` parameter to :meth:`Image.trim()
  <wand.image.BaseImage.trim>` method.  [:issue:`113` by Evaldo Junior]

__ http://en.wikipedia.org/wiki/Seam_carving


0.2 series
~~~~~~~~~~

Version 0.2.4
-------------

Released on May 28, 2013.

- Fix :exc:`~exceptions.NameError` in :attr:`Resource.resource
  <wand.resource.Resource.resource>` setter.
  [:issue:`89` forwarded from Debian bug report `#699064`__
  by Jakub Wilk]
- Fix the problem of library loading for Mac with Homebrew and Arch Linux.
  [:issue:`102` by Roel Gerrits, :issue:`44`]

__ http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=699064


Version 0.2.3
-------------

Released on January 25, 2013.

- Fixed a bug that :meth:`Image.transparentize()
  <wand.image.BaseImage.transparentize>` method (and :meth:`Image.watermark()
  <wand.image.BaseImage.watermark>` method which internally uses it) didn't
  work.
- Fixed segmentation fault occurred when :attr:`Color.red
  <wand.color.Color.red>`, :attr:`Color.green <wand.color.Color.green>`,
  or :attr:`Color.blue <wand.color.Color.blue>` is accessed.
- Added :attr:`Color.alpha <wand.color.Color.alpha>` property.
- Fixed a bug that format converting using :attr:`Image.format
  <wand.image.BaseImage.format>` property or :meth:`Image.convert()
  <wand.image.Image.convert>` method doesn't correctly work
  to save blob.


Version 0.2.2
-------------

Released on September 24, 2012.

- A compatibility fix for FreeBSD.
  [`Patch`__ by Olivier Duchateau]
- Now :class:`~wand.image.Image` can be instantiated without any opening.
  Instead, it can take ``width``/``height`` and ``background``.
  [:issue:`53` by Michael Elovskikh]
- Added :meth:`Image.transform() <wand.image.BaseImage.transform>` method
  which is a convenience method accepting geometry strings to perform
  cropping and resizing.
  [:issue:`50` by Mitch Lindgren]
- Added :attr:`Image.units <wand.image.BaseImage.units>` property.
  [:issue:`45` by Piotr Florczyk]
- Now :meth:`Image.resize() <wand.image.BaseImage.resize>` method raises
  a proper error when it fails for any reason.
  [:issue:`41` by Piotr Florczyk]
- Added :attr:`Image.type <wand.image.BaseImage.type>` property.
  [:issue:`33` by Yauhen Yakimovich, :issue:`42` by Piotr Florczyk]

__ http://olivier-freebsd-ports.googlecode.com/hg-history/efb852a5572/graphics/py-wand/files/patch-wand_api.py


Version 0.2.1
-------------

Released on August 19, 2012.  Beta version.

- Added :meth:`Image.trim() <wand.image.BaseImage.trim>` method.
  [:issue:`26` by Jökull Sólberg Auðunsson]

- Added :attr:`Image.depth <wand.image.BaseImage.depth>` property.
  [:issue:`31` by Piotr Florczyk]

- Now :class:`~wand.image.Image` can take an optional ``format`` hint.
  [:issue:`32` by Michael Elovskikh]

- Added :attr:`Image.alpha_channel <wand.image.BaseImage.alpha_channel>`
  property.  [:issue:`35` by Piotr Florczyk]

- The default value of :meth:`Image.resize() <wand.image.BaseImage.resize>`'s
  ``filter`` option has changed from ``'triangle'`` to ``'undefined'``.
  [:issue:`37` by Piotr Florczyk]

- Added version data of the linked ImageMagick library into :mod:`wand.version`
  module:

  - :const:`~wand.version.MAGICK_VERSION` (:c:func:`GetMagickVersion`)
  - :const:`~wand.version.MAGICK_VERSION_INFO` (:c:func:`GetMagickVersion`)
  - :const:`~wand.version.MAGICK_VERSION_NUMBER` (:c:func:`GetMagickVersion`)
  - :const:`~wand.version.MAGICK_RELEASE_DATE` (:c:func:`GetMagickReleaseDate`)
  - :const:`~wand.version.MAGICK_RELEASE_DATE_STRING`
    (:c:func:`GetMagickReleaseDate`)


Version 0.2.0
-------------

Released on June 20, 2012.  Alpha version.

- Added :meth:`Image.transparentize() <wand.image.BaseImage.transparentize>` method.
  [:issue:`19` by Jeremy Axmacher]
- Added :meth:`Image.composite() <wand.image.BaseImage.composite>` method.
  [:issue:`19` by Jeremy Axmacher]
- Added :meth:`Image.watermark() <wand.image.BaseImage.watermark>` method.
  [:issue:`19` by Jeremy Axmacher]
- Added :attr:`Image.quantum_range <wand.image.BaseImage.quantum_range>` property.
  [:issue:`19` by Jeremy Axmacher]
- Added :meth:`Image.reset_coords() <wand.image.BaseImage.reset_coords>` method
  and ``reset_coords`` option to :meth:`Image.rotate()
  <wand.image.BaseImage.rotate>` method. [:issue:`20` by Juan Pablo Scaletti]
- Added :meth:`Image.strip() <wand.image.BaseImage.strip>` method.
  [:issue:`23` by Dmitry Vukolov]
- Added :attr:`Image.compression_quality <wand.image.BaseImage.compression_quality>`
  property.  [:issue:`23` by Dmitry Vukolov]
- Now the current version can be found from the command line interface:
  ``python -m wand.version``.


0.1 series
~~~~~~~~~~

Version 0.1.10
--------------

Released on May 8, 2012.  Still alpha version.

- So many Windows compatibility issues are fixed. [:issue:`14` by John Simon]
- Added :data:`wand.api.libmagick`.
- Fixed a bug that raises :exc:`~exceptions.AttributeError` when it's trying
  to warn.  [:issue:`16` by Tim Dettrick]
- Now it throws :exc:`~exceptions.ImportError` instead of
  :exc:`~exceptions.AttributeError` when the shared library fails
  to load.  [:issue:`17` by Kieran Spear]
- Fixed the example usage on index page of the documentation.
  [:issue:`18` by Jeremy Axmacher]


Version 0.1.9
-------------

Released on December 23, 2011. Still alpha version.

- Now :const:`wand.version.VERSION_INFO` becomes :class:`tuple` and
  :const:`wand.version.VERSION` becomes a string.
- Added :attr:`Image.background_color <wand.image.BaseImage.background_color>`
  property.
- Added ``==`` operator for :class:`~wand.image.Image` type.
- Added :func:`hash()` support of :class:`~wand.image.Image` type.
- Added :attr:`Image.signature <wand.image.BaseImage.signature>` property.
- Added :mod:`wand.display` module.
- Changed the theme of Sphinx documentation.
- Changed the start example of the documentation.

Version 0.1.8
-------------

Released on December 2, 2011. Still alpha version.

- Wrote some guide documentations: :doc:`guide/read`, :doc:`guide/write` and
  :doc:`guide/resizecrop`.
- Added :meth:`Image.rotate() <wand.image.BaseImage.rotate>` method for in-place
  rotation.
- Made :meth:`Image.crop() <wand.image.BaseImage.crop>` to raise proper
  :exc:`ValueError` instead of :exc:`IndexError` for invalid width/height
  arguments.
- Changed the type of :meth:`Image.resize() <wand.image.BaseImage.resize()>`
  method's ``blur`` parameter from :class:`numbers.Rational` to
  :class:`numbers.Real`.
- Fixed a bug of raising :exc:`~exceptions.ValueError` when invalid ``filter``
  has passed to :meth:`Image.resize() <wand.image.BaseImage.resize>` method.

Version 0.1.7
-------------

Released on November 10, 2011. Still alpha version.

- Added :attr:`Image.mimetype <wand.image.Image.mimetype>` property.
- Added :meth:`Image.crop() <wand.image.BaseImage.crop>` method for in-place
  crop.

Version 0.1.6
-------------

Released on October 31, 2011. Still alpha version.

- Removed a side effect of :class:`Image.make_blob()
  <wand.image.Image.make_blob>` method that changes the image format silently.
- Added :attr:`Image.format <wand.image.BaseImage.format>` property.
- Added :meth:`Image.convert() <wand.image.Image.convert>` method.
- Fixed a bug about Python 2.6 compatibility.
- Use the internal representation of :c:type:`PixelWand` instead of
  the string representation for :class:`~wand.color.Color` type.

Version 0.1.5
-------------

Released on October 28, 2011. Slightly mature alpha version.

- Now :class:`~wand.image.Image` can read Python file objects by ``file``
  keyword argument.
- Now :class:`Image.save() <wand.image.Image.save>` method can write into
  Python file objects by ``file`` keyword argument.
- :class:`Image.make_blob() <wand.image.Image.make_blob>`'s ``format``
  argument becomes omittable.

Version 0.1.4
-------------

Released on October 27, 2011. Hotfix of the malformed Python package.

Version 0.1.3
-------------

Released on October 27, 2011. Slightly mature alpha version.

- Pixel getter for :class:`~wand.image.Image`.
- Row getter for :class:`~wand.image.Image`.
- Mac compatibility.
- Windows compatibility.
- 64-bit processor compatibility.

Version 0.1.2
-------------

Released on October 16, 2011. Still alpha version.

- :class:`~wand.image.Image` implements iterable interface.
- Added :mod:`wand.color` module.
- Added the abstract base class of all Wand resource objects:
  :class:`wand.resource.Resource`.
- :class:`~wand.image.Image` implements slicing.
- Cropping :class:`~wand.image.Image` using its slicing operator.

Version 0.1.1
-------------

Released on October 4, 2011. Still alpha version.

- Now it handles errors and warnings properly and in natural way of Python.
- Added :meth:`Image.make_blob() <wand.image.Image.make_blob>` method.
- Added ``blob`` parameter into :class:`~wand.image.Image` constructor.
- Added :meth:`Image.resize() <wand.image.BaseImage.resize>` method.
- Added :meth:`Image.save() <wand.image.Image.save>` method.
- Added :meth:`Image.clone() <wand.image.BaseImage.clone>` method.
- Drawed `the pretty logo picture <_static/wand.png>`_
  (thanks to `Hyojin Choi <http://me2day.net/crocodile>`_).


Version 0.1.0
-------------

Released on October 1, 2011. Very alpha version.

