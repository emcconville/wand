Threshold
=========

..
  This document covers methods defined in MagickCore's fx.c file.
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


.. _random_threshold:

Random Threshold
----------------

.. versionadded:: 0.5.7

Applies a random threshold between ``low`` & ``heigh`` values.

.. code-block:: python

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

    with Image(filename='inca_tern.jpg') as img:
        img.threshold_threshold(threshold='#ace')
        img.save(filename='threshold_white.jpg')

+-------------------------------------+-------------------------------------------+
| Original                            | White Threshold                           |
+-------------------------------------+-------------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/threshold_white.jpg |
|    :alt: Original                   |    :alt: White Threshold                  |
+-------------------------------------+-------------------------------------------+

