Wand
====

.. image:: https://badge.fury.io/py/Wand.svg?
   :alt: Latest PyPI version
   :target: https://pypi.python.org/pypi/Wand

.. image:: https://readthedocs.org/projects/wand/badge/
   :alt: Documentation Status
   :target: http://docs.wand-py.org/en/latest/

.. image:: https://secure.travis-ci.org/dahlia/wand.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/dahlia/wand

.. image:: https://img.shields.io/coveralls/dahlia/wand.svg?style=flat
   :alt: Coverage Status
   :target: https://coveralls.io/r/dahlia/wand

Wand is a :mod:`ctypes`-based simple ImageMagick_ binding for Python. ::

    from wand.image import Image
    from wand.display import display

    with Image(filename='mona-lisa.png') as img:
        print(img.size)
        for r in 1, 2, 3:
            with img.clone() as i:
                i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
                i.rotate(90 * r)
                i.save(filename='mona-lisa-{0}.png'.format(r))
                display(i)

You can install it from PyPI_ (and it requires MagickWand library):

.. sourcecode:: bash

   $ apt-get install libmagickwand-dev
   $ pip install Wand

.. _ImageMagick: http://www.imagemagick.org/
.. _PyPI: https://pypi.python.org/pypi/Wand


Why just another binding?
-------------------------

There are already many MagickWand API bindings for Python, however they
are lacking something we need:

- Pythonic and modern interfaces
- Good documentation
- Binding through :mod:`ctypes` (not C API) --- we are ready to go PyPy!
- Installation using :program:`pip`


Requirements
------------

- Python 2.6 or higher

  - CPython 2.6 or higher
  - CPython 3.2 or higher
  - PyPy 1.5 or higher

- MagickWand library

  - ``libmagickwand-dev`` for APT on Debian/Ubuntu
  - ``imagemagick`` for MacPorts/Homebrew on Mac
  - ``ImageMagick-devel`` for Yum on CentOS


User's guide
------------

.. toctree::
   :maxdepth: 2

   whatsnew/0.4
   guide/install
   guide/read
   guide/write
   guide/resizecrop
   guide/transform
   guide/draw
   guide/colorspace
   guide/colorenhancement
   guide/exif
   guide/sequence
   guide/resource
   test
   roadmap
   changes
   talks


References
----------

.. toctree::
   :maxdepth: 2

   wand


Troubleshooting
---------------

Mailing list
''''''''''''

Wand has the list for users.  If you want to subscribe the list, just send a
mail to:

    wand@librelist.com

The `list archive`_ provided by Librelist_ is synchronized every hour.

.. _list archive: http://librelist.com/browser/wand/
.. _Librelist: http://librelist.com/


Stack Overflow
''''''''''''''

There's a Stack Overflow tag for Wand:

http://stackoverflow.com/questions/tagged/wand

Freely ask questions about Wand including troubleshooting.  Thanks for
sindikat_'s contribution.

.. _sindikat: http://stackoverflow.com/users/596361/sindikat


Quora
'''''

There's a Quora topic for Wand: `Wand (ImageMagick binding)`__.  Be free
to add questions to the topic, though it's suitable for higher-level questions
rather than troubleshooting.

__ https://www.quora.com/Wand-ImageMagick-binding


Open source
-----------

Wand is an open source software written by `Hong Minhee`_ (initially written
for StyleShare_).  See also the complete list of contributors_ as well.
The source code is distributed under `MIT license`_ and you can find it at
`GitHub repository`_. Check out now:

.. sourcecode:: bash

   $ git clone git://github.com/dahlia/wand.git

If you find a bug, please notify to `our issue tracker`_. Pull requests
are always welcome!

We discuss about Wand's development on IRC.  Come #wand channel on
freenode network.

Check out :doc:`changes` also.

.. _Hong Minhee: http://hongminhee.org/
.. _StyleShare: https://stylesha.re/
.. _contributors: https://github.com/dahlia/wand/graphs/contributors
.. _MIT license: http://minhee.mit-license.org/
.. _GitHub repository: https://github.com/dahlia/wand
.. _our issue tracker: https://github.com/dahlia/wand/issues


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

