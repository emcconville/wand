Wand
====

.. image:: https://badge.fury.io/py/Wand.svg?
   :alt: Latest PyPI version
   :target: https://pypi.python.org/pypi/Wand

.. image:: https://readthedocs.org/projects/wand/badge/
   :alt: Documentation Status
   :target: https://docs.wand-py.org/en/latest/

.. image:: https://app.travis-ci.com/emcconville/wand.svg?branch=master
   :alt: Build Status
   :target: https://app.travis-ci.com/emcconville/wand

.. image:: https://github.com/emcconville/wand/workflows/Wand%20CI/badge.svg
   :alt: Build Status
   :target: https://github.com/emcconville/wand/actions?query=workflow%3A%22Wand+CI%22

.. image:: https://img.shields.io/coveralls/emcconville/wand.svg?style=flat
   :alt: Coverage Status
   :target: https://coveralls.io/r/emcconville/wand

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

- Python 2.7 or higher

  - CPython 2.7 or higher
  - CPython 3.3 or higher
  - PyPy 1.5 or higher

- MagickWand library

  - ``libmagickwand-dev`` for APT on Debian/Ubuntu
  - ``imagemagick`` for MacPorts/Homebrew on Mac
  - ``ImageMagick-devel`` for Yum on CentOS


User's guide
------------

.. toctree::
   :maxdepth: 2

   whatsnew/0.6
   guide/install
   guide/security
   guide/read
   guide/write
   guide/resizecrop
   guide/effect
   guide/fx
   guide/transform
   guide/colorspace
   guide/colorenhancement
   guide/distortion
   guide/draw
   guide/exif
   guide/layers
   guide/montage
   guide/morphology
   guide/sequence
   guide/resource
   guide/quantize
   guide/threshold
   guide/cli
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

Stack Overflow
''''''''''''''

There's a Stack Overflow tag for Wand:

http://stackoverflow.com/questions/tagged/wand

Freely ask questions about Wand including troubleshooting.

Thanks to everyone in the `Stack Overflow community`__ for contributions.

__ https://stackoverflow.com/tags/wand/topusers


Documentation
'''''''''''''

The documentation_ for Wand is hosted by `ReadTheDocs.org`_. The nightly
development docs can be found under the latest_ version, and the most recent
release under stable_.  Previous & maintenance releases are also available.

.. _documentation: https://docs.wand-py.org
.. _ReadTheDocs.org: https://readthedocs.org
.. _latest: https://docs.wand-py.org/en/latest/
.. _stable: https://docs.wand-py.org/en/stable/


Open source
-----------

Wand is an open source software initially written by `Hong Minhee`_ (for
StyleShare_), and is currently maintained by E. McConville.  See also the
complete list of contributors_ as well. The source code is distributed under
`MIT license`_ and you can find it at `GitHub repository`_. Check out now:

.. sourcecode:: bash

   $ git clone git://github.com/emcconville/wand.git

If you find a bug, please notify to `our issue tracker`_. Pull requests
are always welcome!

Check out :doc:`changes` also.

.. _Hong Minhee: http://hongminhee.org/
.. _StyleShare: https://stylesha.re/
.. _contributors: https://github.com/emcconville/wand/graphs/contributors
.. _MIT license: http://minhee.mit-license.org/
.. _GitHub repository: https://github.com/emcconville/wand
.. _our issue tracker: https://github.com/emcconville/wand/issues


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

