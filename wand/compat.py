""":mod:`wand.compat` --- Compatibility layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides several encoding-related utilities.

"""
import sys

__all__ = ('binary', 'encode_filename', 'text')


def binary(string, var=None):
    """Makes ``string`` to :class:`bytes`.

    :param string: a string to cast it to :data:`bytes`
    :type string: :class:`bytes`, :class:`str`, :class:`unicode`
    :param var: an optional variable name to be used for error message
    :type var: :class:`str`

    """
    if isinstance(string, str):
        return string.encode()
    elif isinstance(string, bytes):
        return string
    if var:
        raise TypeError('{0} must be a string, not {1!r}'.format(var, string))
    raise TypeError('expected a string, not ' + repr(string))


def text(string):
    if isinstance(string, bytes):
        return string.decode('utf-8')
    return string


def encode_filename(filename):
    """If ``filename`` is a :data:`text_type`, encode it to
    :data:`bytes` according to filesystem's default encoding.

    .. versionchanged:: 0.5.3
       Added support for PEP-519 https://github.com/emcconville/wand/pull/339
    """
    if hasattr(filename, "__fspath__"):  # PEP 519
        filename = filename.__fspath__()
    if isinstance(filename, str):
        return filename.encode(sys.getfilesystemencoding())
    return filename
