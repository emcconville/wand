Roadmap
=======

Version 0.3
-----------

Python 3 compatibility
   Wand 0.3 will be the first version that supports Python 3.

   The branch name for it will be :branch:`python3`.

Jython compatibility (:issue:`9`)
   Wand 0.3 will support Jython 2.7+.  Jython 2.7 is (June 2012) currently
   under alpha release, and Wand has been tested on it and fixed incompatible
   things.

   It has been developed in the branch :branch:`jython`.

EXIF (:issue:`25`)
   ImageMagick itself can read/write EXIF through :c:func:`GetMagickInfo`
   function.  Wand 0.3 will make a binding for it.

   Its branch name will be :branch:`exif`.

Image layers (:issue:`22`)
   Wand 0.3 will be able to deal with layers of an image.

   Its branch name will be :branch:`layer`.


Very future versions
--------------------

Animations (:issue:`1`)
   Wand will finally support animations like GIF and SWF in the future.

   Its branch name will be :branch:`animation`.

