""":mod:`wand.version` --- Version data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find the current version in the command line interface:

.. sourcecode:: console

   $ python -m wand.version
   0.1.2

.. versionadded:: 0.2.0
   The command line interface.

"""

__all__ = 'VERSION', 'VERSION_INFO'

#: (:class:`tuple`) The version tuple e.g. ``(0, 1, 2)``.
#:
#: .. versionchanged:: 0.1.9
#:    Becomes :class:`tuple`.  (It was string before.)
VERSION_INFO = (0, 2, 0)

#: (:class:`basestring`) The version string e.g. ``'0.1.2'``.
#:
#: .. versionchanged:: 0.1.9
#:    Becomes string.  (It was :class:`tuple` before.)
VERSION = '{0}.{1}.{2}'.format(*VERSION_INFO)

__doc__ = __doc__.replace('0.1.2', VERSION)


if __name__ == '__main__':
    print VERSION

