Installation
============

Wand itself can be installed from PyPI_ using :program:`easy_install` or
:program:`pip`:

.. sourcecode:: console

   $ easy_install Wand  # or
   $ pip install Wand

Wand is a Python binding of ImageMagick_, so you have to install it as well:

- :ref:`Debian/Ubuntu <install-imagemagick-debian>`
- :ref:`Fedora/CentOS <install-imagemagick-redhat>`
- :ref:`Mac <install-imagemagick-mac>`
- :ref:`Windows <install-imagemagick-windows>`
- :ref:`FreeBSD <install-wand-freebsd>`

.. _PyPI: http://pypi.python.org/pypi/Wand
.. _ImageMagick: http://www.imagemagick.org/


.. _install-imagemagick-debian:

Install ImageMagick on Debian/Ubuntu
------------------------------------

If you're using Linux distributions based on Debian like Ubuntu, it can be
easily installed using APT:

.. sourcecode:: console

   $ sudo apt-get install libmagickwand-dev


.. _install-imagemagick-redhat:

Install ImageMagick on Fedora/CentOS
------------------------------------

If you're using Linux distributions based on Redhat like Fedora or CentOS,
it can be installed using Yum:

.. sourcecode:: console

   $ yum update
   $ yum install ImageMagick-devel


.. _install-imagemagick-mac:

Install ImageMagick on Mac
--------------------------

You need one of Homebrew_ or MacPorts_ to install ImageMagick.

Homebrew
   .. sourcecode:: console

      $ brew install imagemagick

MacPorts
   .. sourcecode:: console

      $ sudo port install imagemagick

.. _Homebrew: http://mxcl.github.com/homebrew/
.. _MacPorts: http://www.macports.org/


.. _install-imagemagick-windows:

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


.. _install-wand-freebsd:

Install Wand on FreeBSD
-----------------------

Wand itself is already packaged in FreeBSD ports collection: py-wand_.
You can install using :program:`pkg_add` command:

.. sourcecode:: console

   $ pkg_add -r py-wand

.. _py-wand: http://www.freebsd.org/cgi/cvsweb.cgi/ports/graphics/py-wand/
