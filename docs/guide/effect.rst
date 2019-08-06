Image Effects
=============

Blur
----

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


Adaptive Blur
'''''''''''''

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.adaptive_blur(radius=8, sigma=4)
        img.save(filename="effect-adaptive-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Adaptive Blur                                  |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-adaptive-blur.jpg |
|    :alt: Original                     |    :alt: Adaptive Blur                         |
+---------------------------------------+------------------------------------------------+


Gaussian Blur
'''''''''''''

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.gaussian_blur(radius=3, sigma=1)
        img.save(filename="effect-gaussian-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Gaussian Blur                                  |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-gaussian-blur.jpg |
|    :alt: Original                     |    :alt: Gaussian Blur                         |
+---------------------------------------+------------------------------------------------+


Motion  Blur
''''''''''''

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.motion_blur(radius=16, sigma=8, angle=-45)
        img.save(filename="effect-motion-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Motion Blur                                    |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-motion-blur.jpg   |
|    :alt: Original                     |    :alt: Motion Blur                           |
+---------------------------------------+------------------------------------------------+


Rotational Blur
'''''''''''''''

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.rotational_blur(angle=5)
        img.save(filename="effect-rotational-blur.jpg")

+---------------------------------------+----------------------------------------------------+
| Original                              | Rotational Blur                                    |
+---------------------------------------+----------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-rotational-blur.jpg   |
|    :alt: Original                     |    :alt: Rotational Blur                           |
+---------------------------------------+----------------------------------------------------+


Selective Blur
''''''''''''''

.. code-block:: python

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


Sharpen
-------

Convolves an image with a Gaussian operator to enhance blurry edges into a more
distinct "sharp" edge. The ``radius`` should always be larger than ``sigma``
value.  The radius value will be calculated automatically if only ``sigma`` is
given.

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.sharpen(radius=8, sigma=4)
        img.save(filename="effect-sharpen.jpg")

+---------------------------------------+------------------------------------------+
| Original                              | Sharpen                                  |
+---------------------------------------+------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-sharpen.jpg |
|    :alt: Original                     |    :alt: Sharpen                         |
+---------------------------------------+------------------------------------------+


Adaptive Sharpen
''''''''''''''''

Just like :meth:`Image.sharpen() <wand.image.BaseImage.sharpen>`, adaptive
sharpen uses a convolve & Gaussian operations to sharpen blurred images.
However, the effects of
:meth:`Image.adaptive_sharpen() <wand.image.BaseImage.adaptive_sharpen>`
are more intense around pixels with detectable edges, and less farther away
from edges. In the example below, notice the visible changes around the edge of
the feathers, and limited  changes in the out-of-focus background.

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.adaptive_sharpen(radius=8, sigma=4)
        img.save(filename="effect-adaptive-sharpen.jpg")

+---------------------------------------+---------------------------------------------------+
| Original                              | Adaptive Sharpen                                  |
+---------------------------------------+---------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-adaptive-sharpen.jpg |
|    :alt: Original                     |    :alt: Adaptive Sharpen                         |
+---------------------------------------+---------------------------------------------------+

