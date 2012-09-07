Running tests
=============

Wand has unit tests and regression tests.  It can be run using
:file:`setup.py` script:

.. sourcecode:: console

   $ python setup.py test

It uses Attest_ as its testing library.  The above command will automatically
install Attest as well if it's not installed yet.

.. _Attest: http://packages.python.org/Attest/


Skipping tests
--------------

There are some time-consuming tests.  If :envvar:`WANDTESTS_SKIP` environment
variable it skips specified modules:

.. sourcecode:: console

   $ WANDTESTS_SKIP="color image" python setup.py test

Or you can test only specified modules using :envvar:`WANDTESTS_ONLY`
environment variable:

.. sourcecode:: console

   $ WANDTESTS_ONLY="color resource" python setup.py test


Using tox_
----------

Wand should be compatible with various Python implementations including
CPython 2.6, 2.7, PyPy.  tox_ is a testing software that helps Python
packages to test on various Python implementations at a time.

It can be installed using :program:`easy_install` or :program:`pip`:

.. sourcecode:: console

   $ easy_install tox

If you type just :program:`tox` at Wand directory it will be tested
on multiple Python interpreters:

.. sourcecode:: console

   $ tox
   GLOB sdist-make: /Users/dahlia/Desktop/wand/setup.py
   py26 create: /Users/dahlia/Desktop/wand/.tox/py26
   py26 installdeps: Attest
   py26 sdist-inst: /Users/dahlia/Desktop/wand/.tox/dist/Wand-0.2.2.zip
   py26 runtests: commands[0]
   ...

.. _tox: http://tox.testrun.org/


Continuous Integration
----------------------

.. image:: https://secure.travis-ci.org/dahlia/wand.png?branch=master
   :alt: Build Status
   :target: http://travis-ci.org/dahlia/wand

`Travis CI`_ automatically builds and tests every commit and pull request.
The above banner image shows the current status of Wand build.
You can see the detail of the current status from the following URL:

http://travis-ci.org/dahlia/wand

.. _Travis CI: http://travis-ci.org/
