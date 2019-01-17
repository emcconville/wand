""":mod:`wand.cdefs.structures` --- MagickWand C typedefs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 0.5.0
"""
import ctypes
import os
import platform
import sys

__all__ = ('c_magick_char_p', 'c_magick_real_t', 'c_magick_size_t',
           'c_ssize_t')


class c_magick_char_p(ctypes.c_char_p):
    """This subclass prevents the automatic conversion behavior of
    :class:`ctypes.c_char_p`, allowing memory to be properly freed in the
    destructor.  It must only be used for non-const character pointers
    returned by ImageMagick functions.

    """

    def __del__(self):
        """Relinquishes memory allocated by ImageMagick.
        We don't need to worry about checking for ``NULL`` because
        :c:func:`MagickRelinquishMemory` does that for us.
        Note alslo that :class:`ctypes.c_char_p` has no
        :meth:`~object.__del__` method, so we don't need to
        (and indeed can't) call the superclass destructor.

        """
        try:
            from wand.api import library  # Lazy load global library
            library.MagickRelinquishMemory(self)
        except ImportError:
            # Python my be shutting down; and such, ``sys.meta_path``
            # may not be available.
            pass


if not hasattr(ctypes, 'c_ssize_t'):
    if ctypes.sizeof(ctypes.c_uint) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_int
    elif ctypes.sizeof(ctypes.c_ulong) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_long
    elif ctypes.sizeof(ctypes.c_ulonglong) == ctypes.sizeof(ctypes.c_void_p):
        ctypes.c_ssize_t = ctypes.c_longlong
c_ssize_t = ctypes.c_ssize_t


env_real = os.getenv('WAND_REAL_TYPE', 'auto')
if env_real in ('double', 'c_double'):
    c_magick_real_t = ctypes.c_double
elif env_real in ('longdouble', 'c_longdouble'):
    c_magick_real_t = ctypes.c_longdouble
else:
    # Attempt to guess MagickRealType size
    if sys.maxsize > 2**32:
        c_magick_real_t = ctypes.c_double
    else:
        c_magick_real_t = ctypes.c_longdouble
del env_real


# FIXME: Might need to rewrite to check against c_void_p size;
# like `c_ssize_t` above, and not against window platform.
if sys.maxsize > 2**32:
    c_magick_size_t = ctypes.c_size_t
elif platform.system() == "Windows":
    c_magick_size_t = ctypes.c_ulonglong
else:
    c_magick_size_t = ctypes.c_size_t
