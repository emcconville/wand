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
CPython & PyPy.  tox_ is a testing software that helps Python packages to test
on various Python implementations at a time.

It can be installed using :program:`pip`:

.. sourcecode:: console

   $ pip install tox

If you type just :program:`tox` at Wand directory it will be tested
on multiple Python interpreters:

.. sourcecode:: console

   $ tox
   pypy3: install_deps> python -I -m pip install pytest pytest-forked
   pypy3: install_package> python -I -m pip install [...] Wand-X.X.X.tar.gz
   pypy3: commands[0]> pytest --forked
   ...

You can use a double ``--`` to pass options to pytest:

.. sourcecode:: console

   $ tox -- -k sequence

.. _tox: http://tox.testrun.org/


Continuous Integration
----------------------

.. image:: https://github.com/emcconville/wand/workflows/Wand%20CI/badge.svg
   :alt: Build Status
   :target: https://github.com/emcconville/wand/actions?query=workflow%3A%22Wand+CI%22

`GitHub Actions`_ automatically builds and tests every commit and pull request.
The above banner image shows the current status of Wand build.
You can see the detail of the current status from the following URL:

https://github.com/emcconville/wand/actions

.. _GitHub Actions: https://docs.github.com/en/actions


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
