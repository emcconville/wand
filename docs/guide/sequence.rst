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

If we :doc:`open <read>` this image, :class:`~wand.image.Image` object
has :attr:`~wand.image.BaseImage.sequence`.  It's a list-like object
that maintain its all frames.  For example, if you call :func:`len()`
for this, it returns the number of frames:

>>> from wand.image import Image
>>> with Image(filename='sequence-animation.gif') as image:
...     len(image.sequence)
...
60
