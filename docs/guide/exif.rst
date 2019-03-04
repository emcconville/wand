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


Image Profiles
--------------

Although wand provides a way to quickly access profile attributes through
:attr:`Image.metadata <wand.image.Image.metadata>`, ImageMagick is not a
tag editor. Users are expected to export the profile payload, modify as needed,
and import the payload back into the source image. Payload are byte-arrays, and
should be treated as binary blobs.

Image profiles can be imported, extracted, and deleted with
:attr:`Image.profiles <wand.image.Image.profiles>` dictionary::

    with Image(filename='wandtests/assets/beach.jpg') as image:
        # Extract EXIF payload
        if 'EXIF' in image.profiles:
            exif_binary = image.profiles['EXIF']
        # Import/replace ICC payload
        with open('color_profile.icc', 'rb') as icc:
            image.profiles['ICC'] = icc.read()
        # Remove XMP payload
        del image.profiles['XMP']

.. note::

    Each write operation on any profile type requires the raster image-data
    to be re-encoded. On lossy formats, such encoding operations can be
    considered a generation loss.

