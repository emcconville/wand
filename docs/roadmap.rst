Roadmap
=======

Version 0.5
-----------

CFFI
   Wand 0.5 will move to CFFI from ctypes.

Image layers (:issue:`22`)
   Wand 0.5 will be able to deal with layers of an image.

   Its branch name will be :branch:`layer`.


Very future versions
--------------------

PIL compatibility layer
   PIL has very long history and the most of Python projects still
   depend on it.  We will work on PIL compatibility layer using Wand.
   It will provide two ways to emulate PIL:

   - Module-level compatibility which can be used by changing
     :keyword:`import`::

         try:
             from wand.pilcompat import Image
         except ImportError:
             from PIL import Image

   - Global monkeypatcher which changes :attr:`sys.modules`::

         from wand.pilcompat.monkey import patch; patch()
         import PIL.Image  # it imports wand.pilcompat.Image module

CLI (:program:`covert` command) to Wand compiler (:issue:`100`)
   Primary interface of ImageMagick is :program:`convert` command.
   It provides a small *parameter language*, and many answers on the Web
   contain code using this.  The problem is that you can't simply
   copy-and-paste these code to utilize Wand.

   This feature is to make these CLI codes possible to be used with Wand.

Supporting :meth:`__array_interface__` for NumPy (:issue:`65`)
   It makes :func:`numpy.asarray()` able to take :class:`~wand.image.Image`
   object to deal with its pixels as matrix.

   Its branch name will be :branch:`numpy`.
