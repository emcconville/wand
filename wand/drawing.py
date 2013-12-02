""":mod:`wand.drawing` --- Drawings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The module provides some vector drawing functions.

.. versionadded:: 0.3.0

"""
import collections
import ctypes
import numbers

from .api import library, MagickPixelPacket
from .color import Color
from .compat import binary, string_type, text, text_type, xrange
from .image import Image
from .resource import Resource
from .exceptions import WandLibraryVersionError

__all__ = ('FONT_METRICS_ATTRIBUTES', 'TEXT_ALIGN_TYPES',
           'TEXT_DECORATION_TYPES', 'GRAVITY_TYPES', 'Drawing', 'FontMetrics')


#: (:class:`collections.Sequence`) The list of text align types.
#:
#: - ``'undefined'``
#: - ``'left'``
#: - ``'center'``
#: - ``'right'``
TEXT_ALIGN_TYPES = 'undefined', 'left', 'center', 'right'

#: (:class:`collections.Sequence`) The list of text decoration types.
#:
#: - ``'undefined'``
#: - ``'no'``
#: - ``'underline'``
#: - ``'overline'``
#: - ``'line_through'``
TEXT_DECORATION_TYPES = ('undefined', 'no', 'underline', 'overline',
                         'line_through')

#: (:class:`collections.Sequence`) The list of text gravity types.
#:
#: - ``'forget'``
#: - ``'north_west'``
#: - ``'north'``
#: - ``'north_east'``
#: - ``'west'``
#: - ``'center'``
#: - ``'east'``
#: - ``'south_west'``
#: - ``'south'``
#: - ``'south_east'``
#: - ``'static'``
GRAVITY_TYPES = ('forget', 'north_west', 'north', 'north_east', 'west',
                 'center', 'east', 'south_west', 'south', 'south_east',
                 'static')

#: (:class:`collections.Sequence`) The attribute names of font metrics.
FONT_METRICS_ATTRIBUTES = ('character_width', 'character_height', 'ascender',
                           'descender', 'text_width', 'text_height',
                           'maximum_horizontal_advance', 'x1', 'y1', 'x2',
                           'y2', 'x', 'y')

#: The tuple subtype which consists of font metrics data.
FontMetrics = collections.namedtuple('FontMetrics', FONT_METRICS_ATTRIBUTES)


class Drawing(Resource):
    """Drawing object.  It maintains several vector drawing instructions
    and can get drawn into zero or more :class:`~wand.image.Image` objects
    by calling it.

    For example, the following code draws a diagonal line to the ``image``::

        with Drawing() as draw:
            draw.line((0, 0), image.size)
            draw(image)

    :param drawing: an optional drawing object to clone.
                    use :meth:`clone()` method rathan than this parameter
    :type drawing: :class:`Drawing`

    .. versionadded:: 0.3.0

    """

    c_is_resource = library.IsDrawingWand
    c_destroy_resource = library.DestroyDrawingWand
    c_get_exception = library.DrawGetException
    c_clear_exception = library.DrawClearException

    def __init__(self, drawing=None):
        with self.allocate():
            if not drawing:
                wand = library.NewDrawingWand()
            elif not isinstance(drawing, type(self)):
                raise TypeError('drawing must be a wand.drawing.Drawing '
                                'instance, not ' + repr(drawing))
            else:
                wand = library.CloneDrawingWand(drawing.resource)
            self.resource = wand

    def clone(self):
        """Copies a drawing object.

        :returns: a duplication
        :rtype: :class:`Drawing`

        """
        return type(self)(drawing=self)

    @property
    def font(self):
        """(:class:`basestring`) The current font name.  It also can be set."""
        return text(library.DrawGetFont(self.resource))

    @font.setter
    def font(self, font):
        if not isinstance(font, string_type):
            raise TypeError('expected a string, not ' + repr(font))
        library.DrawSetFont(self.resource, binary(font))

    @property
    def font_size(self):
        """(:class:`numbers.Real`) The font size.  It also can be set."""
        return library.DrawGetFontSize(self.resource)

    @font_size.setter
    def font_size(self, size):
        if not isinstance(size, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(size))
        elif size < 0.0:
            raise ValueError('cannot be less then 0.0, but got ' + repr(size))
        library.DrawSetFontSize(self.resource, size)

    @property
    def fill_color(self):
        """(:class:`~wand.color.Color`) The current color to fill.
        It also can be set.

        """
        pixel = library.NewPixelWand()
        library.DrawGetFillColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @fill_color.setter
    def fill_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetFillColor(self.resource, color.resource)

    @property
    def stroke_color(self):
        """(:class:`~wand.color.Color`) The current color of stroke.
        It also can be set.

        .. versionadded:: 0.3.3
        
        """
        pixel = library.NewPixelWand()
        library.DrawGetStrokeColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @stroke_color.setter
    def stroke_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' + 
                            repr(color))
        with color:
            library.DrawSetStrokeColor(self.resource, color.resource)

    @property
    def stroke_width(self):
        """(:class:`numbers.Real`) The stroke width.  It also can be set.

        .. versionadded:: 0.3.3

        """
        return library.DrawGetStrokeWidth(self.resource)

    @stroke_width.setter
    def stroke_width(self, width):
        if not isinstance(width, numbers.Real):
           raise TypeError('expected a numbers.Real, but got ' + repr(width)) 
        elif width < 0.0:
           raise ValueError('cannot be less then 0.0, but got ' + repr(width))
        library.DrawSetStrokeWidth(self.resource, width)

    @property
    def text_alignment(self):
        """(:class:`basestring`) The current text alignment setting.
        It's a string value from :const:`TEXT_ALIGN_TYPES` list.
        It also can be set.

        """
        text_alignment_index = library.DrawGetTextAlignment(self.resource)
        if not text_alignment_index:
            self.raise_exception()
        return text(TEXT_ALIGN_TYPES[text_alignment_index])

    @text_alignment.setter
    def text_alignment(self, align):
        if not isinstance(align, string_type):
            raise TypeError('expected a string, not ' + repr(align))
        elif align not in TEXT_ALIGN_TYPES:
            raise ValueError('expected a string from TEXT_ALIGN_TYPES, not ' +
                             repr(align))
        library.DrawSetTextAlignment(self.resource,
                                     TEXT_ALIGN_TYPES.index(align))

    @property
    def text_antialias(self):
        """(:class:`bool`) The boolean value which represents whether
        antialiasing is used for text rendering.  It also can be set to
        ``True`` or ``False`` to switch the setting.

        """
        result = library.DrawGetTextAntialias(self.resource)
        return bool(result)

    @text_antialias.setter
    def text_antialias(self, value):
        library.DrawSetTextAntialias(self.resource, bool(value))

    @property
    def text_decoration(self):
        """(:class:`basestring`) The text decoration setting, a string
        from :const:`TEXT_DECORATION_TYPES` list.  It also can be set.

        """
        text_decoration_index = library.DrawGetTextDecoration(self.resource)
        if not text_decoration_index:
            self.raise_exception()
        return text(TEXT_DECORATION_TYPES[text_decoration_index])

    @text_decoration.setter
    def text_decoration(self, decoration):
        if not isinstance(decoration, string_type):
            raise TypeError('expected a string, not ' + repr(decoration))
        elif decoration not in TEXT_DECORATION_TYPES:
            raise ValueError('expected a string from TEXT_DECORATION_TYPES, '
                             'not ' + repr(decoration))
        library.DrawSetTextDecoration(self.resource,
                                      TEXT_DECORATION_TYPES.index(decoration))

    @property
    def text_encoding(self):
        """(:class:`basestring`) The internally used text encoding setting.
        Although it also can be set, but it's not encorouged.

        """
        return text(library.DrawGetTextEncoding(self.resource))

    @text_encoding.setter
    def text_encoding(self, encoding):
        if encoding is not None and not isinstance(encoding, string_type):
            raise TypeError('expected a string, not ' + repr(encoding))
        elif encoding is None:
            # encoding specify an empty string to set text encoding
            # to system's default.
            encoding = b''
        else:
            encoding = binary(encoding)
        library.DrawSetTextEncoding(self.resource, encoding)

    @property
    def text_interline_spacing(self):
        """(:class:`numbers.Real`) The setting of the text line spacing.
        It also can be set.

        """
        if library.DrawGetTextInterlineSpacing is None:
            raise WandLibraryVersionError('The installed version of ImageMagick does not support this feature')
        return library.DrawGetTextInterlineSpacing(self.resource)

    @text_interline_spacing.setter
    def text_interline_spacing(self, spacing):
        if library.DrawSetTextInterlineSpacing is None:
            raise WandLibraryVersionError('The installed version of ImageMagick does not support this feature')
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterlineSpacing(self.resource, spacing)

    @property
    def text_interword_spacing(self):
        """(:class:`numbers.Real`) The setting of the word spacing.
        It also can be set.

        """
        return library.DrawGetTextInterwordSpacing(self.resource)

    @text_interword_spacing.setter
    def text_interword_spacing(self, spacing):
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterwordSpacing(self.resource, spacing)

    @property
    def text_kerning(self):
        """(:class:`numbers.Real`) The setting of the text kerning.
        It also can be set.

        """
        return library.DrawGetTextKerning(self.resource)

    @text_kerning.setter
    def text_kerning(self, kerning):
        if not isinstance(kerning, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(kerning))
        library.DrawSetTextKerning(self.resource, kerning)

    @property
    def text_under_color(self):
        """(:class:`~wand.color.Color`) The color of a background rectangle
        to place under text annotations.  It also can be set.

        """
        pixel = library.NewPixelWand()
        library.DrawGetTextUnderColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @text_under_color.setter
    def text_under_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('expected a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetTextUnderColor(self.resource, color.resource)

    @property
    def gravity(self):
        """(:class:`basestring`) The text placement gravity used when
        annotating with text.  It's a string from :const:`GRAVITY_TYPES`
        list.  It also can be set.

        """
        gravity_index = library.DrawGetGravity(self.resource)
        if not gravity_index:
            self.raise_exception()
        return text(GRAVITY_TYPES[gravity_index])

    @gravity.setter
    def gravity(self, value):
        if not isinstance(value, string_type):
            raise TypeError('expected a string, not ' + repr(value))
        elif value not in GRAVITY_TYPES:
            raise ValueError('expected a string from GRAVITY_TYPES, not '
                             + repr(value))
        library.DrawSetGravity(self.resource, GRAVITY_TYPES.index(value))

    def clear(self):
        library.ClearDrawingWand(self.resource)

    def draw(self, image):
        """Renders the current drawing into the ``image``.  You can simply
        call :class:`Drawing` instance rather than calling this method.
        That means the following code which calls :class:`Drawing` object
        itself::

            drawing(image)

        is equivalent to the following code which calls :meth:`draw()` method::

            drawing.draw(image)

        :param image: the image to be drawn
        :type image: :class:`~wand.image.Image`

        """
        if not isinstance(image, Image):
            raise TypeError('image must be a wand.image.Image instance, not '
                            + repr(image))
        res = library.MagickDrawImage(image.wand, self.resource)
        if not res:
            self.raise_exception()

    def line(self, start, end):
        """Draws a line ``start`` to ``end``.

        :param start: (:class:`~numbers.Integral`, :class:`numbers.Integral`)
                      pair which represents starting x and y of the line
        :type start: :class:`numbers.Sequence`
        :param end: (:class:`~numbers.Integral`, :class:`numbers.Integral`)
                    pair which represents ending x and y of the line
        :type end: :class:`numbers.Sequence`

        """
        start_x, start_y = start
        end_x, end_y = end
        library.DrawLine(self.resource,
                         int(start_x), int(start_y),
                         int(end_x), int(end_y))

    def rectangle(self, left=None, top=None, right=None, bottom=None,
                  width=None, height=None):
        """Draws a rectangle using the current :attr:`stoke_color`,
        :attr:`stroke_width`, and :attr:`fill_color`.

        .. sourcecode:: text

           +--------------------------------------------------+
           |              ^                         ^         |
           |              |                         |         |
           |             top                        |         |
           |              |                         |         |
           |              v                         |         |
           | <-- left --> +-------------------+  bottom       |
           |              |             ^     |     |         |
           |              | <-- width --|---> |     |         |
           |              |           height  |     |         |
           |              |             |     |     |         |
           |              |             v     |     |         |
           |              +-------------------+     v         |
           | <--------------- right ---------->               |
           +--------------------------------------------------+

        :param left: x-offset of the rectangle to draw
        :type left: :class:`numbers.Real`
        :param top: y-offset of the rectangle to draw
        :type top: :class:`numbers.Real`
        :param right: second x-offset of the rectangle to draw.
                      this parameter and ``width`` parameter are exclusive
                      each other
        :type right: :class:`numbers.Real`
        :param bottom: second y-offset of the rectangle to draw.
                       this parameter and ``height`` parameter are exclusive
                       each other
        :type bottom: :class:`numbers.Real`
        :param width: the :attr:`width` of the rectangle to draw.
                      this parameter and ``right`` parameter are exclusive
                      each other
        :type width: :class:`numbers.Real`
        :param height: the :attr:`height` of the rectangle to draw.
                       this parameter and ``bottom`` parameter are exclusive
                       each other
        :type height: :class:`numbers.Real`

        .. versionadded:: 0.3.6

        """
        if left is None:
            raise TypeError('left is missing')
        elif top is None:
            raise TypeError('top is missing')
        elif right is None and width is None:
            raise TypeError('right/width is missing')
        elif bottom is None and height is None:
            raise TypeError('bottom/height is missing')
        elif not (right is None or width is None):
            raise TypeError('parameters right and width are exclusive each '
                            'other; use one at a time')
        elif not (bottom is None or height is None):
            raise TypeError('parameters bottom and height are exclusive each '
                            'other; use one at a time')
        elif not isinstance(left, numbers.Real):
            raise TypeError('left must be numbers.Real, not ' + repr(left))
        elif not isinstance(top, numbers.Real):
            raise TypeError('top must be numbers.Real, not ' + repr(top))
        elif not (right is None or isinstance(right, numbers.Real)):
            raise TypeError('right must be numbers.Real, not ' + repr(right))
        elif not (bottom is None or isinstance(bottom , numbers.Real)):
            raise TypeError('bottom must be numbers.Real, not ' + repr(bottom))
        elif not (width is None or isinstance(width, numbers.Real)):
            raise TypeError('width must be numbers.Real, not ' + repr(width))
        elif not (height is None or isinstance(height, numbers.Real)):
            raise TypeError('height must be numbers.Real, not ' + repr(height))
        if right is None:
            if width < 0:
                raise ValueError('width must be positive, not ' + repr(width))
            right = left + width
        elif right < left:
            raise ValueError('right must be more than left ({0!r}), '
                             'not {1!r})'.format(left, right))
        if bottom is None:
            if height < 0:
                raise ValueError('height must be positive, not ' + repr(height))
            bottom = top + height
        elif bottom < top:
            raise ValueError('bottom must be more than top ({0!r}), '
                             'not {1!r})'.format(top, bottom))
        library.DrawRectangle(self.resource, left, top, right, bottom)
        self.raise_exception()

    def text(self, x, y, body):
        """Writes a text ``body`` into (``x``, ``y``).

        :param x: the left offset where to start writing a text
        :type x: :class:`numbers.Integral`
        :param y: the top offset where to start writing a text
        :type y: :class:`numbers.Integral`
        :param body: the body string to write
        :type body: :class:`basestring`

        """
        if not isinstance(x, numbers.Integral) or x < 0:
            exc = ValueError if x < 0 else TypeError
            raise exc('x must be a natural number, not ' + repr(x))
        elif not isinstance(y, numbers.Integral) or y < 0:
            exc = ValueError if y < 0 else TypeError
            raise exc('y must be a natural number, not ' + repr(y))
        elif not isinstance(body, string_type):
            raise TypeError('body must be a string, not ' + repr(body))
        elif not body:
            raise ValueError('body string cannot be empty')
        if isinstance(body, text_type):
            # According to ImageMagick C API docs, we can use only UTF-8
            # at this time, so we do hardcoding here.
            # http://imagemagick.org/api/drawing-wand.php#DrawSetTextEncoding
            if not self.text_encoding:
                self.text_encoding = 'UTF-8'
            body = body.encode(self.text_encoding)
        body_p = ctypes.create_string_buffer(body)
        library.DrawAnnotation(
            self.resource, x, y,
            ctypes.cast(body_p,ctypes.POINTER(ctypes.c_ubyte))
        )

    def get_font_metrics(self, image, text, multiline=False):
        """Queries font metrics from the given ``text``.

        :param image: the image to be drawn
        :type image: :class:`~wand.image.Image`
        :param text: the text string for get font metrics.
        :type text: :class:`basestring`
        :param multiline: text is multiline or not
        :type multiline: `boolean`

        """
        if not isinstance(image, Image):
            raise TypeError('image must be a wand.image.Image instance, not '
                            + repr(image))
        if not isinstance(text, string_type):
            raise TypeError('text must be a string, not ' + repr(text))
        if multiline:
            font_metrics_f = library.MagickQueryMultilineFontMetrics
        else:
            font_metrics_f = library.MagickQueryFontMetrics
        if isinstance(text, text_type):
            if self.text_encoding:
                text = text.encode(self.text_encoding)
            else:
                text = binary(text)
        result = font_metrics_f(image.wand, self.resource, text)
        args = (result[i] for i in xrange(13))
        return FontMetrics(*args)

    def __call__(self, image):
        return self.draw(image)
