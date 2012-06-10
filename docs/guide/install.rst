Installation
============

Wand itself can be installed from PyPI_ using :program:`easy_install` or
:program:`pip`:

.. sourcecode:: bash

   $ easy_install Wand  # or
   $ pip install Wand

Wand is a Python binding of ImageMagick_, so you have to install it as well.

.. _PyPI: http://pypi.python.org/pypi/Wand
.. _ImageMagick: http://www.imagemagick.org/


Install ImageMagick on Windows
------------------------------

You could build ImageMagick by yourself, but it requires a build tool chain
like Visual Studio to compile it.  The easiest way is simply downloading
a prebuilt binary of ImageMagick for your architecture (``win32`` or
``win64``).

You can download it from the following link:

http://www.imagemagick.org/download/binaries/

Choose a binary for your architecture:

Windows 32-bit
   ImageMagick-6.7.7-6-Q16-windows-dll.exe__

Windows 64-bit
   ImageMagick-6.7.7-6-Q16-windows-x64-dll.exe__

.. image:: ../_static/windows-setup.png

Note that you have to check :guilabel:`Install development headers and
libraries for C and C++` to make Wand able to link to it.

.. image:: ../_static/windows-envvar.png
   :width: 465
   :height: 315

Lastly you have to set :envvar:`MAGICK_HOME` environment variable to the path
of ImageMagick (e.g. :file:`C:\\Program Files\\ImageMagick-6.7.7-Q16`).
You can set it in :menuselection:`Computer --> Properties -->
Advanced system settings --> Advanced --> Enviro&nment Variables...`.

__ http://www.imagemagick.org/download/binaries/ImageMagick-6.7.7-6-Q16-windows-dll.exe
__ http://www.imagemagick.org/download/binaries/ImageMagick-6.7.7-6-Q16-windows-x64-dll.exe


