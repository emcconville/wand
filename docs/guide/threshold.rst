Threshold
=========

..
  This document covers methods defined in MagickCore's threshold.c file.
  https://imagemagick.org/api/MagickCore/threshold_8c.html


.. _adaptive_threshold:

Adaptive Threshold
------------------

.. versionadded:: 0.5.3

Also known as Local Adaptive Threshold, each pixel value is adjusted
by the surrounding pixels. If the current pixel has greater value than the
average of the surrounding pixels, then the pixel becomes white, else black.

The size of the surrounding pixels is defined by passing ``width`` & ``height``
arguments. Use ``offset`` argument to apply a +/- value to the current pixel.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        img.adaptive_threshold(width=16, height=16,
                               offset=-0.08 * img.quantum_range)
        img.save(filename='threshold_adaptive.jpg')

+-------------------------------------+----------------------------------------------+
| Original                            | Adaptive Threshold                           |
+-------------------------------------+----------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_adaptive.jpg |
|    :alt: Original                   |    :alt: Adaptive Threshold                  |
+-------------------------------------+----------------------------------------------+

.. note:: Requires ImageMagick-7.


.. _auto_threshold:

Auto Threshold
--------------

.. versionadded:: 0.5.5

This method applies threshold automatically. You can define which method to
use from :class:`~wand.image.AUTO_THRESHOLD_METHODS`. Defaults to ``'kapur'``.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        with img.clone() as kapur:
            kapur.auto_threshold(method='kapur')
            kapur.save(filename='threshold_auto_kapur.jpg')
        with img.clone() as otsu:
            otsu.auto_threshold(method='otsu')
            otsu.save(filename='threshold_auto_otsu.jpg')
        with img.clone() as triangle:
            triangle.auto_threshold(method='triangle')
            triangle.save(filename='threshold_auto_triangle.jpg')

+-----------------------------------------------+---------------------------------------------------+
| Original                                      | Auto Threshold (``'kapur'``)                      |
+-----------------------------------------------+---------------------------------------------------+
| .. image:: ../_images/inca_tern.jpg           | .. image:: ../_images/threshold_auto_kapur.jpg    |
|    :alt: Original                             |    :alt: Auto Threshold (``'kapur'``)             |
+-----------------------------------------------+---------------------------------------------------+
| Auto Threshold (``'otsu'``)                   | Auto Threshold (``'triangle'``)                   |
+-----------------------------------------------+---------------------------------------------------+
| .. image:: ../_images/threshold_auto_otsu.jpg | .. image:: ../_images/threshold_auto_triangle.jpg |
|    :alt: Auto Threshold (``'otsu'``)          |    :alt: Auto Threshold (``'triangle'``)          |
+-----------------------------------------------+---------------------------------------------------+

.. note:: Requires ImageMagick-7.0.8-41


.. _black_threshold:

Black Threshold
---------------

.. versionadded:: 0.5.3

Force all pixels below a given pixel value to black.
This works on a color channel-by-channel basis, and can be used to reduce
unwanted colors.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.black_threshold(threshold='#930')
        img.save(filename='threshold_black.jpg')

+-------------------------------------+-------------------------------------------+
| Original                            | Black Threshold                           |
+-------------------------------------+-------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_black.jpg |
|    :alt: Original                   |    :alt: Black Threshold                  |
+-------------------------------------+-------------------------------------------+


.. _color_threshold:

Color Threshold
---------------

.. versionadded:: 0.6.4

Creates a binary image where all pixels between ``start`` & ``stop`` are forced
to white, else black.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.color_threshold(start='#333', stop='#cdc')
        img.save(filename='threshold_color.jpg')

+-------------------------------------+-------------------------------------------+
| Original                            | Color Threshold                           |
+-------------------------------------+-------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_color.jpg |
|    :alt: Original                   |    :alt: Color Threshold                  |
+-------------------------------------+-------------------------------------------+

.. note:: Requires ImageMagick-7.0.10


.. _ordered_dither:

Ordered Dither
--------------

Applies a pre-defined threshold map to create dithering to an image.

The pre-defined thresholds are the following:

+-----------+-------+-----------------------------+
| Map       | Alias | Description                 |
+===========+=======+=============================+
| threshold | 1x1   | Threshold 1x1 (non-dither)  |
+-----------+-------+-----------------------------+
| checks    | 2x1   | Checkerboard 2x1 (dither)   |
+-----------+-------+-----------------------------+
| o2x2      | 2x2   | Ordered 2x2 (dispersed)     |
+-----------+-------+-----------------------------+
| o3x3      | 3x3   | Ordered 3x3 (dispersed)     |
+-----------+-------+-----------------------------+
| o4x4      | 4x4   | Ordered 4x4 (dispersed)     |
+-----------+-------+-----------------------------+
| o8x8      | 8x8   | Ordered 8x8 (dispersed)     |
+-----------+-------+-----------------------------+
| h4x4a     | 4x1   | Halftone 4x4 (angled)       |
+-----------+-------+-----------------------------+
| h6x6a     | 6x1   | Halftone 6x6 (angled)       |
+-----------+-------+-----------------------------+
| h8x8a     | 8x1   | Halftone 8x8 (angled)       |
+-----------+-------+-----------------------------+
| h4x4o     |       | Halftone 4x4 (orthogonal)   |
+-----------+-------+-----------------------------+
| h6x6o     |       | Halftone 6x6 (orthogonal)   |
+-----------+-------+-----------------------------+
| h8x8o     |       | Halftone 8x8 (orthogonal)   |
+-----------+-------+-----------------------------+
| h16x16o   |       | Halftone 16x16 (orthogonal) |
+-----------+-------+-----------------------------+
| c5x5b     | c5x5  | Circles 5x5 (black)         |
+-----------+-------+-----------------------------+
| c5x5w     |       | Circles 5x5 (white)         |
+-----------+-------+-----------------------------+
| c6x6b     | c6x6  | Circles 6x6 (black)         |
+-----------+-------+-----------------------------+
| c6x6w     |       | Circles 6x6 (white)         |
+-----------+-------+-----------------------------+
| c7x7b     | c7x7  | Circles 7x7 (black)         |
+-----------+-------+-----------------------------+
| c7x7w     |       | Circles 7x7 (white)         |
+-----------+-------+-----------------------------+

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        with img.clone() as dispersed:
            dispersed.ordered_dither('o3x3')
            dispersed.save(filename='threshold_ordered_dither_dispersed.jpg')
        with img.clone() as halftone:
            halftone.ordered_dither('h6x6a')
            halftone.save(filename='threshold_ordered_dither_halftone.jpg')
        with img.clone() as circles:
            circles.ordered_dither('c6x6b')
            circles.save(filename='threshold_ordered_dither_circles.jpg')

+-------------------------------------------------------------+--------------------------------------------------------------+
| Original                                                    | Ordered Dither (Ordered 3x3)                                 |
+-------------------------------------------------------------+--------------------------------------------------------------+
| .. image:: ../_images/inca_tern.jpg                         | .. image:: ../_images/threshold_ordered_dither_dispersed.jpg |
|    :alt: Original                                           |    :alt: Ordered Dither (Ordered 3x3)                        |
+-------------------------------------------------------------+--------------------------------------------------------------+
| Ordered Dither (Halftone 4x4)                               | Ordered Dither (Circles 6x6)                                 |
+-------------------------------------------------------------+--------------------------------------------------------------+
| .. image:: ../_images/threshold_ordered_dither_halftone.jpg | .. image:: ../_images/threshold_ordered_dither_circles.jpg   |
|    :alt: Ordered Dither (Halftone 4x4)                      |    :alt: Ordered Dither (Circles 6x6)                        |
+-------------------------------------------------------------+--------------------------------------------------------------+


.. _random_threshold:

Random Threshold
----------------

.. versionadded:: 0.5.7

Applies a random threshold between ``low`` & ``high`` values.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        img.random_threshold(low=0.3 * img.quantum_range,
                             high=0.6 * img.quantum_range)
        img.save(filename='threshold_random.jpg')

+-------------------------------------+--------------------------------------------+
| Original                            | Random Threshold                           |
+-------------------------------------+--------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_random.jpg |
|    :alt: Original                   |    :alt: Random Threshold                  |
+-------------------------------------+--------------------------------------------+


.. _range_threshold:

Range Threshold
---------------

.. versionadded:: 0.5.5

This can either apply a soft, or hard, threshold between two quantum points.

To use a soft threshold, define the low & high range between each white & black
point.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        white_point = 0.9 * img.quantum_range
        black_point = 0.5 * img.quantum_range
        delta = 0.05 * img.quantum_range
        img.range_threshold(low_black=black_point - delta,
                            low_white=white_point - delta,
                            high_white=white_point + delta,
                            high_black=black_point + delta)
        img.save(filename='threshold_range_soft.jpg')

+-------------------------------------+------------------------------------------------+
| Original                            | Range Threshold (soft)                         |
+-------------------------------------+------------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_range_soft.jpg |
|    :alt: Original                   |    :alt: Range Threshold (soft)                |
+-------------------------------------+------------------------------------------------+

To use a hard threshold, pass the same values as both low & high range.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.transform_colorspace('gray')
        white_point = 0.9 * img.quantum_range
        black_point = 0.5 * img.quantum_range
        img.range_threshold(low_black=black_point,
                            low_white=white_point,
                            high_white=white_point,
                            high_black=black_point)
        img.save(filename='threshold_range_hard.jpg')

+-------------------------------------+------------------------------------------------+
| Original                            | Range Threshold (hard)                         |
+-------------------------------------+------------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_range_hard.jpg |
|    :alt: Original                   |    :alt: Range Threshold (range)               |
+-------------------------------------+------------------------------------------------+

.. note:: Requires ImageMagick-7.0.8-41

.. _white_threshold:

White Threshold
---------------

.. versionadded:: 0.5.2

Force all pixels above a given pixel value to white.
This works on a color channel-by-channel basis, and can be used to reduce
unwanted colors.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.threshold_threshold(threshold='#ace')
        img.save(filename='threshold_white.jpg')

+-------------------------------------+-------------------------------------------+
| Original                            | White Threshold                           |
+-------------------------------------+-------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_white.jpg |
|    :alt: Original                   |    :alt: White Threshold                  |
+-------------------------------------+-------------------------------------------+

