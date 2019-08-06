Image Effects
=============

Blur
----

.. code-block:: python

    with Image(filename="hummingbird.jpg") as img:
        img.blur(0, 3)
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
        img.adaptive_blur(8, 4)
        img.save(filename="effect-adaptive-blur.jpg")

+---------------------------------------+------------------------------------------------+
| Original                              | Adaptive Blur                                  |
+---------------------------------------+------------------------------------------------+
| .. image:: ../_images/hummingbird.jpg | .. image:: ../_images/effect-adaptive-blur.jpg |
|    :alt: Original                     |    :alt: Adaptive Blur                         |
+---------------------------------------+------------------------------------------------+


Sharpen
-------

Adaptive Sharpen
''''''''''''''''

