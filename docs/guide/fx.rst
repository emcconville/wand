Special Effects (FX)
====================

..
  This document covers methods defined in MagickCore's fx.c file.
  https://imagemagick.org/api/MagickCore/fx_8c.html


.. _noise:

Add Noise
---------

.. versionadded:: 0.5.3

You can add random noise to an image. This operation can be useful when applied
before a blur operation to defuse an image. The types of noise can be any
of the following.

 - ``'gaussian'``
 - ``'impulse'``
 - ``'laplacian'``
 - ``'multiplicative_gaussian'``
 - ``'poisson'``
 - ``'random'``
 - ``'uniform'``

The amount of noise can be adjusted by passing an `attenuate` kwarg where the
value can be between `0.0` and `1.0`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.noise("laplacian", attenuate=1.0)
        img.save(filename="fx-noise.jpg")

+-------------------------------------+------------------------------------+
| Original                            | Noise                              |
+-------------------------------------+------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-noise.jpg |
|    :alt: Original                   |    :alt: Noise                     |
+-------------------------------------+------------------------------------+


.. _blue_shift:

Blue Shift
----------

.. versionadded:: 0.5.3

Gently mutes colors by shifting blue values by a factor. This produces a
nighttime scene with a moonlight effect.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.blue_shift(factor=1.25)
        img.save(filename="fx-blue-shift.jpg")

+-----------------------------+---------------------------------+
| Original                    | Blue Shift                      |
+-----------------------------+---------------------------------+
| .. image::                  | .. image::                      |
|    ../_images/inca_tern.jpg |    ../_images/fx-blue-shift.jpg |
|    :alt: Original           |    :alt: Blue Shift             |
+-----------------------------+---------------------------------+


.. _charcoal:

Charcoal
--------

.. versionadded:: 0.5.3

One of the artistic simulations, :meth:`~wand.image.BaseImage.charcoal()`
can emulate a drawing on paper.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.charcoal(radius=1.5, sigma=0.5)
        img.save(filename="fx-charcoal.jpg")

+-------------------------------------+---------------------------------------+
| Original                            | Charcoal                              |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-charcoal.jpg |
|    :alt: Original                   |    :alt: Charcoal                     |
+-------------------------------------+---------------------------------------+


.. _color_matrix:

Color Matrix
------------

.. versionadded:: 0.5.3

This method allows you to recalculate color values by applying a matrix
transform. A matrix can be up to a 6x6 grid where each column maps to
a color channel to reference, and each row represents a color channel
to effect. Usually ``red``, ``green``, ``blue``, ``n/a``, ``alpha``,
and a constant (a.k.a offset) for RGB images, or ``cyan``, ``yellow``,
``magenta``, ``black``, ``alpha``, and a constant for CMYK images.

For example: To swap Red & Blue channels.


.. math::

    \begin{aligned}
    red'   &= 0.0 * red + 0.0 * green + 1.0 * blue\\
    green' &= 0.0 * red + 1.0 * green + 0.0 * blue\\
    blue'  &= 1.0 * red + 0.0 * green + 0.0 * blue\\
    \end{aligned}


.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        matrix = [[0, 0, 1],
                  [0, 1, 0],
                  [1, 0, 0]]
        img.color_matrix(matrix)
        img.save(filename="fx-color-matrix.jpg")

+-----------------------------+-----------------------------------+
| Original                    | Color Matrix                      |
+-----------------------------+-----------------------------------+
| .. image::                  | .. image::                        |
|    ../_images/inca_tern.jpg |    ../_images/fx-color-matrix.jpg |
|    :alt: Original           |    :alt: Color Matrix             |
+-----------------------------+-----------------------------------+


.. _colorize:

Colorize
--------

.. versionadded:: 0.5.3

Blends an image with a constant color. With
:meth:`Image.colorize() <wand.image.BaseImage.colorize>`, the ``color``
parameter is the constant color to blend, and the ``alpha`` is a mask-color
to control the blend rate per color channel.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.colorize(color="yellow", alpha="rgb(10%, 0%, 20%)")
        img.save(filename="fx-colorize.jpg")

+-------------------------------------+---------------------------------------+
| Original                            | Colorize                              |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-colorize.jpg |
|    :alt: Original                   |    :alt: Colorize                     |
+-------------------------------------+---------------------------------------+


.. _fx:

FX
--

.. versionadded:: 0.4.1

`FX special effects`__ are a powerful "micro" language to work with.
Simple functions & operators offer a unique way to access & manipulate image
data. The :meth:`~wand.image.BaseImage.fx()` method applies a FX expression,
and generates a new :class:`~wand.image.Image` instance.

     __ http://www.imagemagick.org/script/fx.php

We can create a custom DIY filter that will turn the image black & white,
except colors with a hue above 324°, or below 36°.

.. code-block:: python

    from wand.image import Image

    fx_filter="(hue > 0.9 || hue < 0.1) ? u : lightness"

    with Image(filename="inca_tern.jpg") as img:
        with img.fx(fx_filter) as filtered_img:
           filtered_img.save(filename="fx-fx.jpg")

+-------------------------------------+---------------------------------+
| Original                            | FX                              |
+-------------------------------------+---------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-fx.jpg |
|    :alt: Original                   |    :alt: FX                     |
+-------------------------------------+---------------------------------+


.. _implode:

Implode
-------

.. versionadded:: 0.5.2

This special effect "pulls" pixels into the middle of the image. The ``amount``
argument controls the range of pixels to pull towards the center. With
ImageMagick 7, you can define the pixel interpolate methods. See
:const:`~wand.image.PIXEL_INTERPOLATE_METHODS`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.implode(amount=0.35)
        img.save(filename="fx-implode.jpg")

+-------------------------------------+--------------------------------------+
| Original                            | Implode                              |
+-------------------------------------+--------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-implode.jpg |
|    :alt: Original                   |    :alt: Implode                     |
+-------------------------------------+--------------------------------------+


.. _polaroid:

Polaroid
--------

.. versionadded:: 0.5.4

Wraps am image in a white board, and a slight shadow to create the special
effect of a Polaroid print.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.polaroid()
        img.save(filename="fx-polaroid.jpg")

+-------------------------------------+---------------------------------------+
| Original                            | Polaroid                              |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-polaroid.jpg |
|    :alt: Original                   |    :alt: Polaroid                     |
+-------------------------------------+---------------------------------------+


.. _sepia_tone:

Sepia Tone
----------

.. versionadded:: 0.5.7

We can simulate old-style silver based chemical photography printing by
applying sepia toning to images.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.sepia_tone(threshold=0.8)
        img.save(filename="fx-sepia-tone.jpg")

+-----------------------------+---------------------------------+
| Original                    | Sepia Tone                      |
+-----------------------------+---------------------------------+
| .. image::                  | .. image::                      |
|    ../_images/inca_tern.jpg |    ../_images/fx-sepia-tone.jpg |
|    :alt: Original           |    :alt: Sepia Tone             |
+-----------------------------+---------------------------------+


.. _sketch:

Sketch
------

.. versionadded:: 0.5.3

Simulates an artist sketch drawing. Also see :ref:`charcoal`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.transform_colorspace("gray")
        img.sketch(0.5, 0.0, 98.0)
        img.save(filename="fx-sketch.jpg")

+-------------------------------------+-------------------------------------+
| Original                            | Sketch                              |
+-------------------------------------+-------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-sketch.jpg |
|    :alt: Original                   |    :alt: Sketch                     |
+-------------------------------------+-------------------------------------+


.. _solarize:

Solarize
--------

.. versionadded:: 0.5.3

Creates a "burned" effect on the image by replacing pixel values above a
defined threshold with a negated value.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.solarize(threshold=0.5 * img.quantum_range)
        img.save(filename="fx-solarize.jpg")

+-------------------------------------+---------------------------------------+
| Original                            | Solarize                              |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-solarize.jpg |
|    :alt: Original                   |    :alt: Solarize                     |
+-------------------------------------+---------------------------------------+


.. _stereogram:

Stereogram
----------

.. versionadded:: 0.5.4

Also known as "`anaglyph`_", this class method takes two
:class:`~wand.image.Image` instances (one for each eye), and creates a 3d
image by separating the Red & Cyan.

.. _anaglyph: https://en.wikipedia.org/wiki/Anaglyph_3D

.. code-block:: python

    from wand.image import Image

    with Image(filename="left_camera.jpg") as left_eye:
        with Image(filename="right_camera.jpg") as right_eye:
            with Image.stereogram(left=left_eye,
                                  right=right_eye) as img:
                img.save(filename="fx-stereogram.jpg")

+-----------------------------------------+
| Stereogram                              |
+-----------------------------------------+
| .. image:: ../_images/fx-stereogram.jpg |
|    :alt: Stereogram                     |
+-----------------------------------------+


.. _swirl:

Swirl
-----

.. versionadded:: 0.5.7

Creates a visual whirlpool effect by rotating pixels around the center of the
image. The value of ``degree`` controls the amount, and distance, of pixels to
rotate around the center. Negative degrees move pixels clockwise, and positive
values move pixels counter-clockwise.

.. code-block:: python

    from wand.image import Image

    with Image(filename='inca_tern.jpg') as img:
        img.swirl(degree=-90)
        img.save(filename='fx-swirl.jpg')

+-------------------------------------+------------------------------------+
| Original                            | Swirl                              |
+-------------------------------------+------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-swirl.jpg |
|    :alt: Original                   |    :alt: Swirl                     |
+-------------------------------------+------------------------------------+


.. _tint:

Tint
----

.. versionadded:: 0.5.3

Tint colorizes midtones of an image by blending the given ``color``.
The ``alpha`` parameter controls how the blend is effected between color
channels. However, this can be tricky to use, so when in doubt, use a
``alpha="gray(50)"`` argument.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.tint(color="yellow", alpha="rgb(40%, 60%, 80%)")
        img.save(filename="fx-tint.jpg")

+-------------------------------------+-----------------------------------+
| Original                            | Tint                              |
+-------------------------------------+-----------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-tint.jpg |
|    :alt: Original                   |    :alt: Tint                     |
+-------------------------------------+-----------------------------------+


.. _vignette:

Vignette
--------

.. versionadded:: 0.5.2

Creates a soft & blurry ellipse on the image. Use the ``x`` & ``y`` arguments
to control edge of the ellipse inset from the image border, and ``radius``
& ``sigma`` argument to control the blurriness. The ``radius`` can be omitted
if you wish ImageMagick to select a value from the defined ``sigma`` value.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.vignette(sigma=3, x=10, y=10)
        img.save(filename="fx-vignette.jpg")

+-------------------------------------+---------------------------------------+
| Original                            | Vignette                              |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-vignette.jpg |
|    :alt: Original                   |    :alt: Vignette                     |
+-------------------------------------+---------------------------------------+


.. _wave:

Wave
----

.. versionadded:: 0.5.2

Creates a ripple effect within the image. With ImageMagick 7, you can define
the pixel interpolate methods. See
:const:`~wand.image.PIXEL_INTERPOLATE_METHODS`.

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.wave(amplitude=img.height / 32,
                 wave_length=img.width / 4)
        img.save(filename="fx-wave.jpg")

+-------------------------------------+-----------------------------------+
| Original                            | Wave                              |
+-------------------------------------+-----------------------------------+
| .. image:: ../_images/inca_tern.jpg | .. image:: ../_images/fx-wave.jpg |
|    :alt: Original                   |    :alt: Wave                     |
+-------------------------------------+-----------------------------------+


.. _wavelet_denoise:

Wavelet Denoise
---------------

.. versionadded:: 0.5.5

This method removes noise by applying a `wavelet transform`_. The ``threshold``
argument should be a value between ``0.0`` &
:attr:`~wand.image.BaseImage.quantum_range`, and the ``softness`` argument
should be a value between ``0.0`` & ``1.0``.

.. _`wavelet transform`: https://en.wikipedia.org/wiki/Wavelet_transform

.. code-block:: python

    from wand.image import Image

    with Image(filename="inca_tern.jpg") as img:
        img.wavelet_denoise(threshold=0.05 * img.quantum_range,
                            softness=0.0)
        img.save(filename="fx-wavelet-denoise.jpg")

+-----------------------------+--------------------------------------+
| Original                    | Wavelet Denoise                      |
+-----------------------------+--------------------------------------+
| .. image::                  | .. image::                           |
|    ../_images/inca_tern.jpg |    ../_images/fx-wavelet-denoise.jpg |
|    :alt: Original           |    :alt: Wavelet Denoise             |
+-----------------------------+--------------------------------------+


