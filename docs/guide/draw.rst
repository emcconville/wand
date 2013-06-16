Drawing
=======

.. versionadded:: 0.3.0

The :mod:`wand.drawing` module provides some basic drawing functions.
:class:`wand.drawing.Drawing` object buffers instructions for drawing
shapes into images, and then it can draw these shapes into zero or more
images.

It's also callable and takes an :class:`~wand.image.Image` object::

    from wand.drawing import Drawing
    from wand.image import Image

    with Drawing() as draw:
        # does something with ``draw`` object,
        # and then...
        with Image(filename='wandtests/assets/beach.jpg') as image:
            draw(image)


.. _draw-lines:

Lines
-----

You can draw lines using :meth:`~wand.drawing.Drawing.line()` method.
It simply takes two (x, y) coordinates for start and end of a line.
For example, the following code draws a diagonal line into the ``image``::

    draw.line((0, 0), image.size)
    draw(image)

Or you can turn this diagonal line upside down::

    draw.line((0, image.height), (image.width, 0))
    draw(image)

The line color is determined by :attr:`~wand.drawing.Drawing.fill_color`
property, and you can change this of course.  The following code draws
a red diagonal line into the ``image``::

    from wand.color import Color

    with Color('red') as color:
        draw.fill_color = color
        draw.line((0, 0), image.size)
        draw(image)


.. _draw-texts:

Texts
-----

:class:`~wand.drawing.Drawing` object can write texts as well using its
:meth:`~wand.drawing.Drawing.text()` method.  It takes ``x`` and ``y``
cordinates to be drawn and a string to write::

    draw.font = 'wandtests/assets/League_Gothic.otf'
    draw.font_size = 40
    draw.text(image.width / 2, image.height / 2, 'Hello, world!')
    draw(image)

As the above code shows you can adjust several settings before writing texts:

- :attr:`~wand.drawing.Drawing.font`
- :attr:`~wand.drawing.Drawing.font_size`
- :attr:`~wand.drawing.Drawing.gravity`
- :attr:`~wand.drawing.Drawing.text_alignment`
- :attr:`~wand.drawing.Drawing.text_antialias`
- :attr:`~wand.drawing.Drawing.text_decoration`
- :attr:`~wand.drawing.Drawing.text_interline_spacing`
- :attr:`~wand.drawing.Drawing.text_interword_spacing`
- :attr:`~wand.drawing.Drawing.text_kerning`
- :attr:`~wand.drawing.Drawing.text_under_color`
