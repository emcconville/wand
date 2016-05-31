Resizing and cropping
=====================

Creating thumbnails (by resizing images) and cropping are most frequent works 
about images. This guide explains ways to deal with sizes of images.

Above all, to get the current size of the image check
:attr:`~wand.image.BaseImage.width` and :attr:`~wand.image.BaseImage.height`
properties:

.. sourcecode:: pycon

   >>> from urllib2 import urlopen
   >>> from wand.image import Image
   >>> f = urlopen('http://api.twitter.com/1/users/profile_image/hongminhee')
   >>> with Image(file=f) as img:
   ...     width = img.width
   ...     height = img.height
   ... 
   >>> f.close()
   >>> width
   48
   >>> height
   48

If you want the pair of (:attr:`~wand.image.BaseImage.width`,
:attr:`~wand.image.BaseImage.height`), check :attr:`~wand.image.BaseImage.size`
property also.

.. note::

   These three properties are all readonly.


Resize images
-------------

It scales an image into a desired size even if the desired size is larger
than the original size. ImageMagick provides so many algorithms for resizing.
The constant :const:`~wand.image.FILTER_TYPES` contains names of filtering
algorithms.

.. seealso::

   `ImageMagick Resize Filters`__
      Demonstrates the results of resampling three images using the various
      resize filters and blur settings available in ImageMagick,
      and the file size of the resulting thumbnail images.

   __ http://www.dylanbeattie.net/magick/filters/result.html

:meth:`Image.resize() <wand.image.BaseImage.resize>` method takes ``width``
and ``height`` of a desired size, optional ``filter`` (``'undefined'`` by
default which means IM will try to guess best one to use) and optional
``blur`` (default is 1). It returns nothing but resizes itself in-place.

.. sourcecode:: pycon

   >>> img.size
   (500, 600)
   >>> img.resize(50, 60)
   >>> img.size
   (50, 60)


Sample images
-------------

Although :meth:`Image.resize() <wand.image.BaseImage.resize>` provides
many ``filter`` options, it's relatively slow.  If speed is important for
the job, you'd better use :meth:`Image.sample() <wand.image.BaseImage.sample>`
instead.  It works in similar way to :meth:`Image.resize()
<wand.image.BaseImage.resize>` except it doesn't provide ``filter`` and
``blur`` options:

.. sourcecode:: pycon

   >>> img.size
   (500, 600)
   >>> img.sample(50, 60)
   >>> img.size
   (50, 60)


Crop images
-----------

To extract a sub-rectangle from an image, use the
:meth:`~wand.image.BaseImage.crop()` method.  It crops the image in-place.
Its parameters are ``left``, ``top``, ``right``, ``bottom`` in order.

.. sourcecode:: pycon

   >>> img.size
   (200, 300)
   >>> img.crop(10, 20, 50, 100)
   >>> img.size
   (40, 80)

It can also take keyword arguments ``width`` and ``height``. These parameters
replace ``right`` and ``bottom``.

.. sourcecode:: pycon

   >>> img.size
   (200, 300)
   >>> img.crop(10, 20, width=40, height=80)
   >>> img.size
   (40, 80)

There is an another way to crop images: slicing operator. You can crop
an image by ``[left:right, top:bottom]`` with maintaining the original:

.. sourcecode:: pycon

   >>> img.size
   (300, 300)
   >>> with img[10:50, 20:100] as cropped:
   ...     print(cropped.size)
   ...
   (40, 80)
   >>> img.size
   (300, 300)

Specifying ``gravity`` along with ``width`` and ``height`` keyword
arguments allows a simplified cropping alternative.

.. sourcecode:: pycon

    >>> img.size
    (300, 300)
    >>> img.crop(width=40, height=80, gravity='center')
    >>> img.size
    (40, 80)


Transform images
----------------

Use this function to crop and resize and image at the same time,
using ImageMagick geometry strings. Cropping is performed first,
followed by resizing.

For example, if you want to crop your image to 300x300 pixels
and then scale it by 2x for a final size of 600x600 pixels,
you can call::

    img.transform('300x300', '200%')

Other example calls::

    # crop top left corner
    img.transform('50%')

    # scale height to 100px and preserve aspect ratio
    img.transform(resize='x100')

    # if larger than 640x480, fit within box, preserving aspect ratio
    img.transform(resize='640x480>')

    # crop a 320x320 square starting at 160x160 from the top left
    img.transform(crop='320+160+160')

.. seealso::

  `ImageMagick Geometry Specifications`__
     Cropping and resizing geometry for the ``transform`` method are
     specified according to ImageMagick's geometry string format.
     The ImageMagick documentation provides more information about
     geometry strings.

  __ http://www.imagemagick.org/script/command-line-processing.php#geometry


.. _seam-carving:

Seam carving (also known as *content-aware resizing*)
-----------------------------------------------------

.. versionadded:: 0.3.0

`Seam carving`_ is an algorithm for image resizing that functions by
establishing a number of *seams* (paths of least importance) in an image
and automatically removes seams to reduce image size or inserts seams
to extend it.

In short: you can magickally resize images without distortion!
See the following examples:

+-------------------------------------+---------------------------------------+
| Original                            | Resized                               |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/seam.jpg      | .. image:: ../_images/seam-resize.jpg |
|    :alt: seam.jpg                   |    :alt: seam-resize.jpg              |
+-------------------------------------+---------------------------------------+
| Cropped                             | **Seam carving**                      |
+-------------------------------------+---------------------------------------+
| .. image:: ../_images/seam-crop.jpg | .. image:: ../_images/seam-liquid.jpg |
|    :alt: seam-crop.jpg              |    :alt: seam-liquid.jpg              |
+-------------------------------------+---------------------------------------+

You can easily rescale images with seam carving using Wand:
use :meth:`Image.liquid_rescale() <wand.image.BaseImage.liquid_rescale>`
method:

>>> image = Image(filename='seam.jpg')
>>> image.size
(320, 234)
>>> with image.clone() as resize:
...     resize.resize(234, 234)
...     resize.save(filename='seam-resize.jpg')
...     resize.size
...
(234, 234)
>>> with image[:234, :] as crop:
...     crop.save(filename='seam-crop.jpg')
...     crop.size
...
(234, 234)
>>> with image.clone() as liquid:
...     liquid.liquid_rescale(234, 234)
...     liquid.save(filename='seam-liquid.jpg')
...     liquid.size
...
(234, 234)

.. note::

   It may raise :exc:`~wand.exceptions.MissingDelegateError` if your
   ImageMagick is configured ``--without-lqr`` option.  In this case
   you should recompile ImageMagick.

.. seealso::

   `Seam carving`_ --- Wikipedia
      The article which explains what seam carving is on Wikipedia.

.. note::

   The image :file:`seam.jpg` used in the above example is taken by
   `D. Sharon Pruitt`_ and licensed under `CC-BY-2.0`_.
   It can be found the `original photography from Flickr`__.

   .. _D. Sharon Pruitt: http://www.pinksherbet.com/
   .. _CC-BY-2.0: http://creativecommons.org/licenses/by/2.0/
   __ http://www.flickr.com/photos/pinksherbet/2443468531/

.. _Seam carving: http://en.wikipedia.org/wiki/Seam_carving
