Writing images
==============

You can write an :class:`~wand.image.Image` object into a file or a byte
string buffer (blob) as format what you want.


Convert images to JPEG
----------------------

If you wonder what is image's format, use :attr:`~wand.image.Image.format`
property.

.. sourcecode:: pycon

   >>> image.format
   'JPEG'

The :attr:`~wand.image.Image.format` property is writable, so you can convert
images by setting this property. ::

    from wand.image import Image

    with Image(filename='pikachu.png') as img:
        img.format = 'jpeg'
        # operations to a jpeg image...

If you want to convert an image without any changes of the original,
use :meth:`~wand.image.Image.convert()` method instead::

    from wand.image import Image

    with Image(filename='pikachu.png') as original:
        with original.convert('jpeg') as converted:
            # operations to a jpeg image...
            pass

.. note::

   Support for some of the formats are delegated to libraries or external
   programs. To get a complete listing of which image formats are supported
   on your system, use :program:`identify` command provided by ImageMagick:

   .. sourcecode:: console

      $ identify -list format


Save to file
------------

In order to save an image to a file, use :meth:`~wand.image.Image.save()`
method with the keyword argument ``filename``::

    from wand.image import Image

    with Image(filename='pikachu.png') as img:
        img.format = 'jpeg'
        img.save(filename='pikachu.jpg')


Save to stream
--------------

You can write an image into a output stream (file-like object which implements
:meth:`~file.write()` method) as well. The parameter ``file`` takes a such
object (it also is the first positional parameter of
:meth:`~wand.image.Image.save()` method).

For example, the following code converts :file:`pikachu.png` image into
JPEG, gzips it, and then saves it to :file:`pikachu.jpg.gz`::

    import gzip
    from wand.image import Image

    gz = gzip.open('pikachu.jpg.gz')
    with Image(filename='pikachu.png') as img:
        img.format = 'jpeg'
        img.save(file=gz)
    gz.close()


Get binary string
-----------------

Want just a binary string of the image? Use
:meth:`~wand.image.Image.make_blob()` method so::

    from wand.image import Image

    with image(filename='pikachu.png') as img:
        img.format = 'jpeg'
        jpeg_bin = img.make_blob()

There's the optional ``format`` parameter as well. So the above example code
can be simpler::

    from wand.image import Image

    with Image(filename='pikachu.png') as img:
        jpeg_bin = img.make_blob('jpeg')
