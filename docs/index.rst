Wand
====

Wand is a :mod:`ctypes`-based simple `MagickWand API`_ binding for Python. ::

    from wand.image import Image

    with Image(filename='mona-lisa.png') as img:
        print img.size
        for r in 1, 2, 3:
            with img.clone() as i:
                i.rotate_right()
                if r % 2:
                    i.sepia_tone()
                i.save('mona-lisa-{0}.png'.format(i))

You can install it from PyPI (and it requires MagickWand library):

.. sourcecode:: bash

   $ apt-get install libmagickwand-dev
   $ easy_install Wand

.. _MagickWand API: http://www.imagemagick.org/script/magick-wand.php


Why just another binding?
-------------------------

There are already many MagickWand API bindings for Python, however they
are lacking something we need:

- Pythonic and modern interfaces
- Good documentation
- Binding through :mod:`ctypes` (not C API) --- we are ready to go PyPy!
- Installation using :program:`pip` or :program:`easy_install`


References
----------

.. toctree::
   :maxdepth: 2

   wand


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

