Image Effects
=============

..
  This document covers methods defined in MagickCore's effect.c file.
  https://imagemagick.org/api/MagickCore/effect_8c.html

.. _blur:

Blur
----

.. versionadded:: 0.4.5

Basic blur operation. The ``radius`` argument defines the size of the area to
sample, and the ``sigma`` defines the standard deviation. For all blur based
methods, the best results are given when the ``radius`` is larger than
``sigma``. However, if ``radius`` is omitted, or zero valued, the value
will be selected based off the given ``sigma`` property.

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.blur(radius=0, sigma=3)
        img.save(filename="effect-blur.jpg")

+---------------------------------------+---------------------------------------+
| Original                              | Blur                                  |
+---------------------------------------+---------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-blur.jpg |
|    :alt: Original                     |    :alt: Blur                         |
+---------------------------------------+---------------------------------------+


.. _adaptive_blur:

Adaptive Blur
'''''''''''''

.. versionadded:: 0.5.3

This method blurs less intensely around areas of an image with detectable edges,
and blurs more intensely for areas without edges. The ``radius`` should
always be larger than the ``sigma`` (standard deviation).

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.adaptive_blur(radius=8, sigma=4)
        img.save(filename="effect-adaptive-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Adaptive Blur                                  |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-adaptive-blur.jpg |
|    :alt: Original                     |    :alt: Adaptive Blur                         |
+---------------------------------------+------------------------------------------------+


.. _gaussian_blur:

Gaussian Blur
'''''''''''''

.. versionadded:: 0.3.3

Smooths images by performing a Gaussian function. The ``sigma`` argument is
used to define the standard deviation.


.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.gaussian_blur(sigma=3)
        img.save(filename="effect-gaussian-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Gaussian Blur                                  |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-gaussian-blur.jpg |
|    :alt: Original                     |    :alt: Gaussian Blur                         |
+---------------------------------------+------------------------------------------------+


.. _motion_blur:

Motion Blur
'''''''''''

.. versionadded:: 0.5.4

Performs a Gaussian blur operation along a linear direction to simulate a
motion effect. The ``radius`` argument should always be larger than the
``sigma`` argument, but if the ``radius`` is not given (or ``0`` value) the
radius value is selected for you.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.motion_blur(radius=16, sigma=8, angle=-45)
        img.save(filename="effect-motion-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Motion Blur                                    |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-motion-blur.jpg   |
|    :alt: Original                     |    :alt: Motion Blur                           |
+---------------------------------------+------------------------------------------------+


.. _rotational_blur:

Rotational Blur
'''''''''''''''

.. versionadded:: 0.5.4

This method simulates a motion blur by rotating at the center of the image.
The larger the angle, the more extreme the blur will be.
Unlike the other blur methods, there is no ``radius`` or ``sigma`` arguments.
The ``angle`` parameter can be between ``0°`` and ``360°`` degrees
with ``0°`` having no effect.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.rotational_blur(angle=5)
        img.save(filename="effect-rotational-blur.jpg")

+---------------------------------------+----------------------------------------------------+
| Original                              | Rotational Blur                                    |
+---------------------------------------+----------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-rotational-blur.jpg   |
|    :alt: Original                     |    :alt: Rotational Blur                           |
+---------------------------------------+----------------------------------------------------+


.. _selective_blur:

Selective Blur
''''''''''''''

.. versionadded:: 0.5.3

Similar to :meth:`Image.blur() <wand.image.BaseImage.blur>` method, this
method will only effect parts of the image that have a contrast below a given
quantum threshold.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.selective_blur(radius=8,
                           sigma=3,
                           threshold=0.25 * img.quantum_range)
        img.save(filename="effect-selective-blur.jpg")

+---------------------------------------+---------------------------------------------------+
| Original                              | Selective Blur                                    |
+---------------------------------------+---------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-selective-blur.jpg   |
|    :alt: Original                     |    :alt: Selective Blur                           |
+---------------------------------------+---------------------------------------------------+


.. _despeckle:

Despeckle
---------

.. versionadded:: 0.5.0

Despeckling is one of the many techniques you can use to reduce noise on a
given image. Also see :ref:`enhance`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.despeckle()
        img.save(filename="effect-despeckle.jpg")

+---------------------------------------+--------------------------------------------+
| Original                              | Despeckle                                  |
+---------------------------------------+--------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-despeckle.jpg |
|    :alt: Original                     |    :alt: Despeckle                         |
+---------------------------------------+--------------------------------------------+


.. _edge:

Edge
----

.. versionadded:: 0.5.0

Detects edges on black and white images with a simple convolution filter. If
used with a color image, the transformation will be applied to each
color-channel.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.transform_colorspace('gray')
        img.edge(radius=1)
        img.save(filename="effect-edge.jpg")

+---------------------------------------+---------------------------------------+
| Original                              | Edge                                  |
+---------------------------------------+---------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-edge.jpg |
|    :alt: Original                     |    :alt: Edge                         |
+---------------------------------------+---------------------------------------+


.. _emboss:

Emboss
-------

.. versionadded:: 0.5.0

Generates a 3D effect that can be described as print reliefs. Like :ref:`edge`,
best results can be generated with grayscale image. Also see :ref:`shade`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.transform_colorspace('gray')
        img.emboss(radius=3.0, sigma=1.75)
        img.save(filename="effect-emboss.jpg")

+---------------------------------------+-----------------------------------------+
| Original                              | Emboss                                  |
+---------------------------------------+-----------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-emboss.jpg |
|    :alt: Original                     |    :alt: Emboss                         |
+---------------------------------------+-----------------------------------------+


.. _kuwahara:

Kuwahara
--------

.. versionadded:: 0.5.5

.. warning::

    Class method only available with ImageMagick 7.0.8-41 or greater.

The :meth:`~wand.image.BaseImage.kuwahara` method applies a smoothing filter
to reduce noise in an image, but also preserves edges.

.. code-block:: python

    from image.wand import Image

    with Image(filename="hummingbird.jpg") as img:
        img.kuwahara(radius=2, sigma=1.5)
        img.save(filename="effect-kuwahara.jpg")

+---------------------------------------+-------------------------------------------+
| Original                              | Kuwahara                                  |
+---------------------------------------+-------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-kuwahara.jpg |
|    :alt: Original                     |    :alt: Kuwahara                         |
+---------------------------------------+-------------------------------------------+


.. _shade:

Shade
-----

.. versionadded:: 0.5.0

Creates a 3D effect by simulating light from source where ``aziumth`` controls
the X/Y angle, and ``elevation`` controls the Z angle. You can also determine
of the resulting image should be transformed to grayscale by passing ``gray``
boolean.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.shade(gray=True,
                  azimuth=286.0,
                  elevation=45.0)
        img.save(filename="effect-shade.jpg")

+---------------------------------------+----------------------------------------+
| Original                              | Shade                                  |
+---------------------------------------+----------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-shade.jpg |
|    :alt: Original                     |    :alt: Shade                         |
+---------------------------------------+----------------------------------------+


.. _sharpen:

Sharpen
-------

.. versionadded:: 0.5.0

Convolves an image with a Gaussian operator to enhance blurry edges into a more
distinct "sharp" edge. The ``radius`` should always be larger than ``sigma``
value.  The radius value will be calculated automatically if only ``sigma`` is
given.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.sharpen(radius=8, sigma=4)
        img.save(filename="effect-sharpen.jpg")

+---------------------------------------+------------------------------------------+
| Original                              | Sharpen                                  |
+---------------------------------------+------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-sharpen.jpg |
|    :alt: Original                     |    :alt: Sharpen                         |
+---------------------------------------+------------------------------------------+


.. _adaptive_sharpen:

Adaptive Sharpen
''''''''''''''''

.. versionadded:: 0.5.3

Just like :meth:`Image.sharpen() <wand.image.BaseImage.sharpen>`, adaptive
sharpen uses a convolve & Gaussian operations to sharpen blurred images.
However, the effects of
:meth:`Image.adaptive_sharpen() <wand.image.BaseImage.adaptive_sharpen>`
are more intense around pixels with detectable edges, and less farther away
from edges. In the example below, notice the visible changes around the edge of
the feathers, and limited  changes in the out-of-focus background.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.adaptive_sharpen(radius=8, sigma=4)
        img.save(filename="effect-adaptive-sharpen.jpg")

+---------------------------------------+---------------------------------------------------+
| Original                              | Adaptive Sharpen                                  |
+---------------------------------------+---------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-adaptive-sharpen.jpg |
|    :alt: Original                     |    :alt: Adaptive Sharpen                         |
+---------------------------------------+---------------------------------------------------+


.. _unsharp_mask:

Unsharp Mask
''''''''''''

.. versionadded:: 0.3.4

Identical to :meth:`Image.sharpen <wand.image.BaseImage.sharpen>` method,
but gives users the control to blend between filter & original (``amount``
parameter), and the ``threshold``. When the ``amount`` value is greater than
``1.0`` more if the sharpen filter is applied, and less if the value is under
``1.0``. Values for ``threshold`` over ``0.0`` reduce the sharpens.

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.unsharp_mask(radius=10,
                         sigma=4,
                         amount=1,
                         threshold=0)
        img.save(filename="effect-unsharp-mask.jpg")

+---------------------------------------+-----------------------------------------------+
| Original                              | Unsharp Mask                                  |
+---------------------------------------+-----------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-unsharp-mask.jpg |
|    :alt: Original                     |    :alt: Unsharp Mask                         |
+---------------------------------------+-----------------------------------------------+


.. _spread:

Spread
------

.. versionadded:: 0.5.3

Spread replaces each pixel with the a random pixel value found near by. The
size of the area to search for a new pixel can be controlled by defining a
radius.

.. code-block:: python

    from wand.image import Image

    with Image(filename="hummingbird.jpg") as img:
        img.spread(radius=8.0)
        img.save(filename="effect-spread.jpg")

+---------------------------------------+-----------------------------------------+
| Original                              | Spread                                  |
+---------------------------------------+-----------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-spread.jpg |
|    :alt: Original                     |    :alt: Spread                         |
+---------------------------------------+-----------------------------------------+
