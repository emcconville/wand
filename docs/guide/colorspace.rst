Colorspace
==========

Image types
-----------

Every :class:`~wand.image.Image` object has  :attr:`~wand.image.BaseImage.type`
property which identifies its colorspace.  The value can be one of
:const:`~wand.image.IMAGE_TYPES` enumeration, and set of its available
values depends on its :attr:`~wand.image.Image.format` as well.  For example,
``'grayscale'`` isn't available on JPEG.

>>> from wand.image import Image
>>> with Image(filename='wandtests/assets/bilevel.gif') as img:
...     img.type
...
'bilevel'
>>> with Image(filename='wandtests/assets/sasha.jpg') as img2:
...    img2.type
...
'truecolor'

You can change this value::

    with Image(filename='wandtests/assets/bilevel.gif') as img:
        img.type = 'truecolor'
        img.save(filename='truecolor.gif')

.. seealso::

   `-type`__ --- ImageMagick: command-line-Options
      Corresponding command-line option of :program:`convert` program.

   __ http://www.imagemagick.org/script/command-line-options.php#type


Enable alpha channel
--------------------

You can find whether an image has alpha channel and change it to have or
not to have the alpha channel using :attr:`~wand.image.BaseImage.alpha_channel`
property, which is preserving a :class:`bool` value.

>>> with Image(filename='wandtests/assets/sasha.jpg') as img:
...    img.alpha_channel
...
False
>>> with Image(filename='wandtests/assets/croptest.png') as img:
...    img.alpha_channel
...
True

It's a writable property::

    with Image(filename='wandtests/assets/sasha.jpg') as img:
        img.alpha_channel = True
