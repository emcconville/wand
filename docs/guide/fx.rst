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


.. _charcoal:

Charcoal
--------

.. versionadded:: 0.5.3

One of the artistic simulations, :meth:`~wand.image.BaseImage.charcoal()`
can emulate a drawing on paper.

.. code-block:: python

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


.. _colorize:

Colorize
--------

.. versionadded:: 0.5.3


.. _fx:

FX
--

.. versionadded:: 0.4.1


.. _implode:

Implode
-------

.. versionadded:: 0.5.2


.. _polaroid:

Polaroid
--------

.. versionadded:: 0.5.4


.. _shadow:

Shadow
------

.. versionadded:: 0.5.0


.. _sketch:

Sketch
------

.. versionadded:: 0.5.3


.. _solarize:

Solarize
--------

.. versionadded:: 0.5.3


.. _stegano:

Stegano
-------

.. versionadded:: 0.5.4


.. _stereogram:

Stereogram
----------

.. versionadded:: 0.5.4


.. _tint:

Tint
----

.. versionadded:: 0.5.3


.. _vignette:

Vignette
--------

.. versionadded:: 0.5.2


.. _wave:

Wave
----

.. versionadded:: 0.5.2


.. _wavelet_denoise:

Wavelet Denoise
---------------

.. versionadded:: 0.5.5
