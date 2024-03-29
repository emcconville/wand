Roadmap
=======

Very future versions
--------------------


CFFI
   Wand will move to CFFI from ctypes.

PIL compatibility layer
   PIL has a very long history and most Python projects still
   depend on it.  We will work on a PIL compatibility layer using Wand.
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

CLI (:program:`convert` command) to Wand compiler (:issue:`100`)
   The primary interface of ImageMagick is the :program:`convert` command.
   It provides a small *parameter language*, and many answers on the Web
   contain code using this.  The problem is that you can't simply
   copy-and-paste these snippets of code to utilize Wand.

   This feature is to make these CLI codes possible to be used with Wand.
