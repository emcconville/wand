""":mod:`wand.version` --- Version data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find the current version in the command line interface:

.. sourcecode:: console

   $ python -m wand.version
   0.0.0
   $ python -m wand.version --verbose
   Wand 0.0.0
   ImageMagick 6.7.7-6 2012-06-03 Q16 http://www.imagemagick.org

.. versionadded:: 0.2.0
   The command line interface.

.. versionadded:: 0.2.2
   The ``--verbose``/``-v`` option which also prints ImageMagick library
   version for CLI.

"""
from __future__ import print_function

import ctypes
import datetime
import re
import sys

try:
    from .api import libmagick
except ImportError:
    libmagick = None
from .compat import text


__all__ = ('VERSION', 'VERSION_INFO', 'MAGICK_VERSION',
           'MAGICK_VERSION_INFO', 'MAGICK_VERSION_NUMBER',
           'MAGICK_RELEASE_DATE', 'MAGICK_RELEASE_DATE_STRING',
           'QUANTUM_DEPTH')

#: (:class:`tuple`) The version tuple e.g. ``(0, 1, 2)``.
#:
#: .. versionchanged:: 0.1.9
#:    Becomes :class:`tuple`.  (It was string before.)
VERSION_INFO = (0, 3, 5)

#: (:class:`basestring`) The version string e.g. ``'0.1.2'``.
#:
#: .. versionchanged:: 0.1.9
#:    Becomes string.  (It was :class:`tuple` before.)
VERSION = '{0}.{1}.{2}'.format(*VERSION_INFO)

if libmagick:
    c_magick_version = ctypes.c_size_t()
    #: (:class:`basestring`) The version string of the linked ImageMagick
    #: library.  The exactly same string to the result of
    #: :c:func:`GetMagickVersion` function.
    #:
    #: Example::
    #:
    #:    'ImageMagick 6.7.7-6 2012-06-03 Q16 http://www.imagemagick.org'
    #:
    #: .. versionadded:: 0.2.1
    MAGICK_VERSION = text(
        libmagick.GetMagickVersion(ctypes.byref(c_magick_version))
    )

    #: (:class:`numbers.Integral`) The version number of the linked
    #: ImageMagick library.
    #:
    #: .. versionadded:: 0.2.1
    MAGICK_VERSION_NUMBER = c_magick_version.value

    _match = re.match(r'^ImageMagick\s+(\d+)\.(\d+)\.(\d+)(?:-(\d+))?',
                      MAGICK_VERSION)
    #: (:class:`tuple`) The version tuple e.g. ``(6, 7, 7, 6)`` of
    #: :const:`MAGICK_VERSION`.
    #:
    #: .. versionadded:: 0.2.1
    MAGICK_VERSION_INFO = tuple(int(v or 0) for v in _match.groups())

    #: (:class:`datetime.date`) The release date of the linked ImageMagick
    #: library.  The same to the result of :c:func:`GetMagickReleaseDate`
    #: function.
    #:
    #: .. versionadded:: 0.2.1
    MAGICK_RELEASE_DATE_STRING = text(libmagick.GetMagickReleaseDate())

    #: (:class:`basestring`) The date string e.g. ``'2012-06-03'`` of
    #: :const:`MAGICK_RELEASE_DATE_STRING`.  This value is the exactly same
    #: string to the result of :c:func:`GetMagickReleaseDate` function.
    #:
    #: .. versionadded:: 0.2.1
    MAGICK_RELEASE_DATE = datetime.date(
        *map(int, MAGICK_RELEASE_DATE_STRING.split('-')))

    c_quantum_depth = ctypes.c_size_t()
    libmagick.GetMagickQuantumDepth(ctypes.byref(c_quantum_depth))
    #: (:class:`numbers.Integral`) The quantum depth configuration of
    #: the linked ImageMagick library.  One of 8, 16, 32, or 64.
    #:
    #: .. versionadded:: 0.3.0
    QUANTUM_DEPTH = c_quantum_depth.value

    del c_magick_version, _match, c_quantum_depth

__doc__ = __doc__.replace('0.0.0', VERSION)
del libmagick


if __name__ == '__main__':
    options = frozenset(sys.argv[1:])
    if '-v' in options or '--verbose' in options:
        print('Wand', VERSION)
        try:
            print(MAGICK_VERSION)
        except NameError:
            pass
    else:
        print(VERSION)

