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


.. _draw-arc:

Arc
---

.. versionadded:: 0.4.0

Arcs can be drawn by using :meth:`~wand.drawing.Drawing.arc()` method. You'll
need two pairs of (x, y) coordinates to map out the minimum bounding rectangle,
and the starting & ending degree.

An example::

    with Drawing() as draw:
        draw.arc((25, 25), # Stating point
                 (75, 75), # Ending point
                 (45,-45)) # From bottom left around to top left

.. image:: ../_images/draw-arc.gif
   :alt: draw-arc.gif

.. _draw-bezier:

Bezier
------

.. versionadded:: 0.4.0

You can draw bezier curves using :meth:`~wand.drawing.Drawing.bezier()` method.
This method requires at lest four points to determine a bezier curve. Given
as a list of (x, y) coordinates. The first & last pair of coordinates are
treated as start & end, and the second & third pair of coordinates act as
controls.

For example::

    with Drawing() as draw:
        points = [(10,50), # Start point
                  (50,10), # First control
                  (50,90), # Second control
                  (90,50)] # End point
        draw.bezier(points)
        with Image(width=100, height=100, background=Color("#fff")) as image:
            draw(image)

.. image:: ../_images/draw-bezier.gif
   :alt: draw-bezier.gif

Control width & color of curve with the drawing properties:

- :attr:`~wand.drawing.Drawing.stroke_color`
- :attr:`~wand.drawing.Drawing.stroke_width`


.. _draw-circle:

Circle
------

.. versionadded:: 0.4.0

You can draw circles using :meth:`~wand.drawing.Drawing.circle()` method.
It simply takes two (x, y) coordinates for center ``origin`` and outer
``perimeter``. For example, the following code draws a circle in the middle of
the ``image``::

    center = (image.width / 2, image.height / 2)
    perimeter = (image.width / 4, image.height / 4)
    draw.circle(center, perimeter)

.. image:: ../_images/draw-circle.gif
   :alt: draw-circle.gif


.. _draw-ellipse:

Ellipse
-------

.. versionadded:: 0.4.0

Ellipse can be drawn by using the :meth:`~wand.drawing.Drawing.ellipse()` method.
Like drawing circles, the ellipse requires a ``origin`` point, however, a pair
of (x, y) ``radius`` are used in relationship to the ``origin`` coordinate. By
default a complete "closed" ellipse is drawn. To draw a partial ellipse, provide
a pair of starting & ending degrees as the third parameter.

An example of a full ellipse::

    draw.ellipse((50, 50), # Origin (center) point
                 (40, 20)) # 80px wide, and 40px tall

.. image:: ../_images/draw-ellipse-full.gif
   :alt: draw-ellipse-full.gif

An example of a half-partial ellipse::

    draw.ellipse((50, 50), # Origin (center) point
                 (40, 20), # 80px wide, and 40px tall
                 (90,-90)) # Draw half of ellipse fro bottom to top

.. image:: ../_images/draw-ellipse-part.gif
   :alt: draw-ellipse-part.gif


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


.. _draw-point:

Point
-----

.. versionadded:: 0.4.0

You can draw points by using :meth:`~wand.drawing.Drawing.point()` method.
It simply takes two ``x``, ``y`` arguments for the point coordinate.

The following example will use this method draw a math function across a given
``image``::

    for x in xrange(0,image.width):
        y = math.tan(x) * 4 + (image.height / 2)
        draw.point(x, y)
    draw(image)

.. image:: ../_images/draw-point-path.gif
   :alt: draw-point-math.gif

Color of the point can be defined by setting the following property

- :attr:`~wand.drawing.Drawing.fill_color`


.. _draw-polygon:

Polygon
-------

.. versionadded:: 0.4.0

Complex shapes can be created with the :meth:`~wand.drawing.Drawing.polygon()`
method. You can draw a polygon by given this method a list of points. Stroke
line will automatically close between first & last point.

For example, the following code will draw a triangle into the ``image``::

    points = [(25, 25), (75, 50), (25, 75)]
    draw.polygon(points)
    draw(image)

.. image:: ../_images/draw-polygon.gif
   :alt: draw-polygon.gif

Control the fill & stroke with the following properties:

- :attr:`~wand.drawing.Drawing.stroke_color`
- :attr:`~wand.drawing.Drawing.stroke_width`
- :attr:`~wand.drawing.Drawing.fill_color`


.. _draw-polyline:

Polyline
-------

.. versionadded:: 0.4.0

Identical to :meth:`~wand.drawing.Drawing.polygon()`, except
:meth:`~wand.drawing.Drawing.polyline()` will not close the stroke line
between the first & last point.

For example, the following code will draw a two line path on the ``image``::

    points = [(25, 25), (75, 50), (25, 75)]
    draw.polyline(points)
    draw(image)

.. image:: ../_images/draw-polyline.gif
   :alt: draw-polyline.gif

Control the fill & stroke with the following properties:

- :attr:`~wand.drawing.Drawing.stroke_color`
- :attr:`~wand.drawing.Drawing.stroke_width`
- :attr:`~wand.drawing.Drawing.fill_color`


.. _draw-rectangles:

Rectangles
----------

.. versionadded:: 0.3.6

If you want to draw rectangles use :meth:`~wand.drawing.Drawing.rectangle()`
method.  It takes ``left``/``top`` coordinate, and ``right``/``bottom``
coordinate, or ``width`` and ``height``.  For example, the following code
draws a square on the ``image``::

    draw.rectangle(left=10, top=10, right=40, bottom=40)
    draw(image)

Or using ``width`` and ``height`` instead of ``right`` and ``bottom``::

    draw.rectangle(left=10, top=10, width=30, height=30)
    draw(image)

Note that the stoke and the fill are determined by the following properties:

- :attr:`~wand.drawing.Drawing.stroke_color`
- :attr:`~wand.drawing.Drawing.stroke_width`
- :attr:`~wand.drawing.Drawing.fill_color`


.. _draw-texts:

Texts
-----

:class:`~wand.drawing.Drawing` object can write texts as well using its
:meth:`~wand.drawing.Drawing.text()` method.  It takes ``x`` and ``y``
coordinates to be drawn and a string to write::

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
