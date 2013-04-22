How to contribute
=================

Branching
---------

- Pull requests that fix bugs of a released version should go to
  ``x.y-maintenance`` (e.g. ``0.2-maintenance``) branch.


Coding style
------------

- Follows `PEP 8`_.
- Alphabetically order imports.
- Prefer relative imports.
- All functions, classes, methods, attributes, and modules should have
  the docstring.
- Functions and methods should contain ``:param:``, ``:type:``
  (``:returns:``, ``:rtype`` if it returns something),
  (``:raises:`` if it may raise an error) in their docstring.


Tests
-----

- All code patches should contain one or more unit tests or regression tests.
- There's `docs about how to test`__.
- All commits will be tested by `Travis CI`__.

__ http://docs.wand-py.org/en/latest/test.html
__ http://travis-ci.org/dahlia/wand


Docs
----

- All packages and modules should have ``.rst`` file for them inside ``docs/``
  directory.  For example, if there's ``wand/module.py`` there also should be
  ``docs/wand/module.rst``, and it has to be listed in ``.. toc::`` of
  ``docs/wand.rst``.
- All new classes/functions/methods/attributes/properties have to contain
  ``.. versionadded::`` in their docstring.
- All interface changes have to contain ``.. versionchanged::``
  in theirdocstring.

.. _PEP 8: www.python.org/dev/peps/pep-0008
