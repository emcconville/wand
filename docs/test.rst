.. _running-tests:

Running tests
=============

Wand has unit tests and regression tests.  It can be run using
:file:`setup.py` script:

.. sourcecode:: console

   $ python setup.py test

It uses pytest_ as its testing library.  The above command will automatically
install pytest as well if it's not installed yet.

Or you can manually install pytest and then use :program:`pytest` command.
It provides more options:

.. sourcecode:: console

   $ pip install pytest
   $ pytest

.. _pytest: http://pytest.org/


Skipping tests
--------------

There are some time-consuming tests.  You can skip these tests using
``--skip-slow`` option:

.. sourcecode:: console

   $ pytest --skip-slow

Be default, tests include regression testing for the PDF format. Test cases
will fail if the system does not include `Ghostscript`_ binaries. You can skip
PDF dependent tests with ``--skip-pdf`` option:

.. sourcecode:: console

    $ pytest --skip-pdf

.. _Ghostscript: https://www.ghostscript.com

The same behavior is true for `Fourier Transform`_ library. Use ``--skip-fft``
to skip over any discrete Fourier transformation test cases.

.. sourcecode:: console

    $ pytest --skip-fft

.. _Fourier Transform: http://www.fftw.org/

You can run only tests you want using ``-k`` option.

.. sourcecode:: console

   $ pytest -k image

The source code repository for Wand doesn't ship any `pytest.ini` configuration
files. However nightly regression test are usually run in parallel with coverage
reports. An example `pytest.ini` file might look like::

    [pytest]
    addopts=-n8 -rsfEw --cov wand --cov-report html




Using tox_
----------

Wand should be compatible with various Python implementations including
CPython 2.7, 3.3, PyPy.  tox_ is a testing software that helps Python
packages to test on various Python implementations at a time.

It can be installed using :program:`pip`:

.. sourcecode:: console

   $ pip install tox

If you type just :program:`tox` at Wand directory it will be tested
on multiple Python interpreters:

.. sourcecode:: console

   $ tox
   GLOB sdist-make: /Users/emcconville/Desktop/wand/setup.py
   py26 create: /Users/emcconville/Desktop/wand/.tox/py26
   py26 installdeps: pytest
   py26 sdist-inst: /Users/emcconville/Desktop/wand/.tox/dist/Wand-0.2.2.zip
   py26 runtests: commands[0]
   ...

You can use a double ``--`` to pass options to pytest:

.. sourcecode:: console

   $ tox -- -k sequence

.. _tox: http://tox.testrun.org/


Continuous Integration
----------------------

.. image:: https://secure.travis-ci.org/emcconville/wand.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/emcconville/wand

`Travis CI`_ automatically builds and tests every commit and pull request.
The above banner image shows the current status of Wand build.
You can see the detail of the current status from the following URL:

https://travis-ci.org/emcconville/wand

.. _Travis CI: http://travis-ci.org/


Code Coverage
-------------

.. image:: https://img.shields.io/coveralls/emcconville/wand.svg?style=flat
   :alt: Coverage Status
   :target: https://coveralls.io/r/emcconville/wand

Coveralls_ support tracking Wand's test coverage.  The above banner image
shows the current status of Wand coverage.  You can see the details of the
current status from the following URL:

https://coveralls.io/r/emcconville/wand

.. _Coveralls: https://coveralls.io/
