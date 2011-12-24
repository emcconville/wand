""":mod:`wand.version` --- Version data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = 'VERSION', 'VERSION_INFO'

#: (:class:`tuple`) The version tuple e.g. ``(0, 1, 2)``.
VERSION_INFO = (0, 1, 10)

#: (:class:`basestring`) The version string e.g. ``'0.1.2'``.
VERSION = '{0}.{1}.{2}'.format(*VERSION_INFO)
