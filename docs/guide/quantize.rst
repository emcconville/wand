Quantize
========

..
  This document covers methods defined in MagickCore's quantize.c file.
  https://imagemagick.org/api/MagickCore/quantize_8c.html


.. _kmeans:

Kmeans
------

.. versionadded:: 0.6.4

Reduces the number of colors to a target number. Processing stops if
max number of iterations, or tolerance are reached.

.. code-block:: python

    from wand.image import Image

    with Image(filename='hummingbird.jpg') as img:
        img.kmeans(number_colors=32, max_iterations=100, tolerance=0.01)
        img.save(filename='quantize_kmeans.jpg')

+---------------------------------------+-------------------------------------------+
| Original                              | Quantize Kmeans                           |
+---------------------------------------+-------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/quantize_kmeans.jpg |
|    :alt: Original                     |    :alt: Quantize Kmeans                  |
+---------------------------------------+-------------------------------------------+

We can also seed the initial colors used on the first iteration by
defining a semicolon delimited list of colors.

.. code-block:: python

    from wand.image import Image

    with Image(filename='hummingbird.jpg') as img:
        img.artifacts['kmeans:seed-colors'] = 'teal;#586f5f;#4d545c;#617284'
        img.kmeans(number_colors=32, max_iterations=100, tolerance=0.01)
        img.save(filename='quantize_kmeans_seed.jpg')

+---------------------------------------+------------------------------------------------+
| Original                              | Quantize Kmeans (seed)                         |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/quantize_kmeans_seed.jpg |
|    :alt: Original                     |    :alt: Quantize Kmeans (seed)                |
+---------------------------------------+------------------------------------------------+

.. note:: Requires ImageMagick-7.0.10-37


.. _posterize:

Posterize
---------

.. versionadded:: 0.5.0

Reduces number of colors per channel. Dither can be defined by passing
``'no'``, ``'riemersma'``,  or ``'floyd_steinberg'`` arguments.

.. code-block:: python

    from wand.image import Image

    with Image(filename='hummingbird.jpg') as img:
        img.posterize(levels=16, dither='floyd_steinberg')
        img.save(filename='quantize_posterize.jpg')

+---------------------------------------+----------------------------------------------+
| Original                              | Quantize Posterize                           |
+---------------------------------------+----------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/quantize_posterize.jpg |
|    :alt: Original                     |    :alt: Quantize Posterize                  |
+---------------------------------------+----------------------------------------------+


.. _quantize:

Quantize
--------

.. versionadded:: 0.4.2

Analyzes the colors in an image, and replace pixel values from a fixed number
of color.

.. code-block:: python

    from wand.image import Image

    with Image(filename='hummingbird.jpg') as img:
        img.quantize(number_colors=8, colorspace_type='srgb',
                     treedepth=1, dither=True, measure_error=False)
        img.save(filename='quantize_quantize.jpg')

+---------------------------------------+---------------------------------------------+
| Original                              | Quantize                                    |
+---------------------------------------+---------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/quantize_quantize.jpg |
|    :alt: Original                     |    :alt: Quantize                           |
+---------------------------------------+---------------------------------------------+


.. _remap:

Remap
-----

.. versionadded:: 0.5.3


Remap replaces all pixels with the closest matching pixel found in the
*affinity* reference image.

.. code-block:: python

    from wand.image import Image

    with Image(filename='hummingbird.jpg') as img:
        with Image(width=256, height=1,
                   pseudo='gradient:SaddleBrown-LavenderBlush') as amap:
            img.remap(affinity=amap, method='riemersma')
        img.save(filename='quantize_remap.jpg')


+---------------------------------------+------------------------------------------+
| Original                              | Quantize Remap                           |
+---------------------------------------+------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/quantize_remap.jpg |
|    :alt: Original                     |    :alt: Quantize Remap                  |
+---------------------------------------+------------------------------------------+
