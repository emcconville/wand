Resizing and cropping
=====================

Creating thumbnails (by resizing images) and cropping are most frequent works 
about images. This guide explains ways to deal with sizes of images.

Above all, to get the current size of the image check
:attr:`~wand.image.Image.width` and :attr:`~wand.image.Image.height`
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

If you want to the pair of (:attr:`~wand.image.Image.width`,
:attr:`~wand.image.Image.height`), check :attr:`~wand.image.Image.size`
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

:meth:`Image.resize() <wand.image.Image.resize>` method takes ``width`` and
``height`` of a desired size, optional ``filter`` (``'undefined'`` by
default which means IM will try to guess best one to use) and optional
``blur`` (default is 1). It returns nothing but resizes itself in-place.

.. sourcecode:: pycon

   >>> img.size
   (500, 600)
   >>> img.resize(50, 60)
   >>> img.size
   (50, 60)


Crop images
-----------

To extract a sub-rectangle from an image,
use the :meth:`~wand.image.Image.crop()` method. It crops the image in-place.
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
   ...     print cropped.size
   ...
   (40, 80)
   >>> img.size
   (300, 300)

