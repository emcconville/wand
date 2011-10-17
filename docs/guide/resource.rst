Resource management
===================

.. seealso::

   :mod:`wand.resource` --- Global resource management
      There is the global resource to manage in MagickWand API.
      This module implements automatic global resource management through
      reference counting.

Objects Wand provides are resources to be managed. It has to be closed
(destroyed) after using like file or database connection. You can deal
with it using :keyword:`with` very easily and explicitly::

    with Image(filename='') as img:
        # deal with img...

Or you can call its :meth:`~wand.resource.Resource.destroy()` (or
:meth:`~wand.image.Image.close()` if it is an :class:`~wand.image.Image`
instance) method manually::

    try:
        img = Image(filename='')
        # deal with img...
    finally:
        img.destroy()

.. note::

   It also implements the destructor that invokes
   :meth:`~wand.resource.Resource.destroy()`, and if your program runs on
   CPython (which does reference counting instead of ordinary garbage
   collection) most of resources are automatically deallocated.

   However it's just depending on CPython's implementation detail of
   memory management, so it's not a good idea. If your program
   runs on PyPy (which implements garbage collector) for example,
   invocation time of destructors is not determined, so the program
   would be broken.

