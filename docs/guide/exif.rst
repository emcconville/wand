Reading EXIF
============

.. versionadded:: 0.3.0

:attr:`Image.metadata <wand.image.Image.metadata>` contains metadata
of the image including EXIF.  These are prefixed by ``'exif:'``
e.g. ``'exif:ExifVersion'``, ``'exif:Flash'``.

Here's a straightforward example to access EXIF of an image::

    exif = {}
    with Image(filename='wandtests/assets/beach.jpg') as image:
        exif.update((k[5:], v) for k, v in image.metadata.items()
                               if k.startswith('exif:'))

.. note::

   You can't write into :attr:`Image.metadata <wand.image.Image.metadata>`.
