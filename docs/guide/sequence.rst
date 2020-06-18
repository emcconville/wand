Sequence
========

.. note::

   The image :file:`sequence-animation.gif` used in this docs
   has been released into the public domain by its author,
   C6541_ at Wikipedia_ project.  This applies worldwide.  (Source_)

   .. _C6541: http://en.wikipedia.org/wiki/User:C6541
   .. _Wikipedia: http://en.wikipedia.org/wiki/
   .. _Source: http://commons.wikimedia.org/wiki/File:1.3-B.gif

.. versionadded:: 0.3.0

Some images may actually consist of two or more images.  For example,
animated :mimetype:`image/gif` images consist of multiple frames.
Some :mimetype:`image/ico` images have different sizes of icons.

.. image:: ../_images/sequence-animation.gif
   :alt: sequence-animation.gif

For example, the above image :file:`sequence-animation.gif` consists
of the following frames (actually it has 60 frames, but we sample only
few frames to show here):

.. image:: ../_images/sequence-frames.gif
   :alt: frames of sequence-animation.gif


:attr:`~wand.image.BaseImage.sequence` is a :class:`~collections.Sequence`
--------------------------------------------------------------------------

If we :doc:`open <read>` this image, :class:`~wand.image.Image` object
has :attr:`~wand.image.BaseImage.sequence`.  It's a list-like object
that maintain its all frames.

For example, :func:`len()` for this returns the number of frames:

>>> from wand.image import Image
>>> with Image(filename='sequence-animation.gif') as image:
...     len(image.sequence)
...
60

You can get an item by index from :attr:`~wand.image.BaseImage.sequence`:

>>> with Image(filename='sequence-animation.gif') as image:
...     image.sequence[0]
...
<wand.sequence.SingleImage: ed84c1b (256x256)>

Or slice it:

>>> with Image(filename='sequence-animation.gif') as image:
...     image.sequence[5:10]
...
[<wand.sequence.SingleImage: 0f49491 (256x256)>,
 <wand.sequence.SingleImage: 8eba0a5 (256x256)>,
 <wand.sequence.SingleImage: 98c10fa (256x256)>,
 <wand.sequence.SingleImage: b893194 (256x256)>,
 <wand.sequence.SingleImage: 181ce21 (256x256)>]


:attr:`~wand.image.Image` versus :attr:`~wand.sequence.SingleImage`
-------------------------------------------------------------------

Note that each item of :attr:`~wand.image.BaseImage.sequence` is a
:class:`~wand.sequence.SingleImage` instance, not :class:`~wand.image.Image`.

:class:`~wand.image.Image` is a container that directly represents
*image files* like :file:`sequence-animation.gif`, and
:class:`~wand.sequence.SingleImage` is a single image that represents
*frames* in animations or *sizes* in :mimetype:`image/ico` files.

They both inherit :class:`~wand.image.BaseImage`, the common abstract class.
They share the most of available operations and properties like
:meth:`~wand.image.BaseImage.resize()` and :attr:`~wand.image.BaseImage.size`,
but some are not.  For example, :meth:`~wand.image.Image.save()` and
:attr:`~wand.image.Image.mimetype` are only provided by
:class:`~wand.image.Image`.  :attr:`~wand.sequence.SingleImage.delay` and
:attr:`~wand.sequence.SingleImage.index` are only available for
:class:`~wand.sequence.SingleImage`.

In most cases, images don't have multiple images, so it's okay if you think
that :class:`~wand.image.Image` and :class:`~wand.sequence.SingleImage` are
the same, but be careful when you deal with animated :mimetype:`image/gif`
files or :mimetype:`image/ico` files that contain multiple icons.


Manipulating :attr:`~wand.sequence.SingleImage`
-----------------------------------------------
When working with :attr:`~wand.image.BaseImage.sequence`, it's important to
remember that each instance of :class:`~wand.sequence.SingleImage` holds a
*copy* of image data from the stack. Altering the copied data will not
automatically sync back to the original image-stack.

>>> with Image(filename='animation.gif') as image:
...     # Changes on SingleImage are invisible to `image` container.
...     image.sequence[2].negate()
...     image.save(filename='output.gif')  # Changes ignored.

If you intended to alter a :class:`~wand.sequence.SingleImage`, and have
changes synchronized back to the parent image-stack, use an additional
with-statement context manager.

>>> with Image(filename='animation.gif') as image:
...     # Changes on SingleImage are sync-ed after context manager closes.
...     with image.sequence[2] as frame:
...         frame.negate()
...     image.save(filename='output.gif')  # Changes applied.


Working directly with Image-Stack Iterators
-------------------------------------------
A faster way to work with images in a sequence is to use the internal stack
iterator. This does not create copies, or generate :class:`~wand.sequence.Sequence` /
:class:`~wand.sequence.SingleImage` instances.

.. warning::

   Users should **NOT** mix :attr:`Image.sequence <wand.image.BaseImage.sequence>`
   code with direct iterator methods.

When reading a image file, the internal iterator is pointing to the last frame
read. To iterate over all frames, use :meth:`Image.iterator_reset() <wand.image.BaseImage.iterator_reset>`
and :meth:`Image.iterator_next() <wand.image.BaseImage.iterator_next>` methods.

>>> with Image(filename='link_to_the_past.gif') as img:
...     img.iterator_reset()
...     print("First frame", img.size)
...     while img.iterator_next():
...         print("Additional frame", img.size)
First frame (300, 289)
Additional frame (172, 128)
Additional frame (172, 145)
Additional frame (123, 112)
Additional frame (144, 182)
Additional frame (107, 117)
Additional frame (171, 128)
Additional frame (123, 107)

You can also iterate backwards with :meth:`Image.iterator_last() <wand.image.BaseImage.iterator_last>`
and :meth:`Image.iterator_previous() <wand.image.BaseImage.iterator_previous>` methods.

>>> with Image(filename='link_to_the_past.gif') as img:
...     img.iterator_last()
...     print("End frame", img.size)
...     while img.iterator_previous():
...         print("Previous frame", img.size)
End frame (123, 107)
Previous frame (171, 128)
Previous frame (107, 117)
Previous frame (144, 182)
Previous frame (123, 112)
Previous frame (172, 145)
Previous frame (172, 128)
Previous frame (300, 289)

Method :meth:`Image.iterator_first() <wand.image.BaseImage.iterator_first>` is
like :meth:`Image.iterator_reset() <wand.image.BaseImage.iterator_reset>`, but allows
the next image read to be prepended at the start of the stack.

>>> with Image(filename='support/link_net.gif') as img:
...     img.iterator_first()
...     img.pseudo(1, 1, 'xc:gold')
...     img.iterator_set(0)
...     print(img.size)
...     img.iterator_set(1)
...     print(img.size)
(1, 1)
(300, 289)

.. note::

   The "image-stack" is general term for a `linked list`_ of sub-images in a file.
   The nomenclature varies between industries & users. You may find documents
   referencing sub-images as:

    - *Frame* for animated formats (GIF)
    - *Page* for document based formats (PDF)
    - *Layer* for publishing formats (PSD, TIFF)

   .. _linked list: https://en.wikipedia.org/wiki/Linked_list
