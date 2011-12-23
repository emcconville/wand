""":mod:`wand.display` --- Displaying images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`display()` functions shows you the image.  It is useful for
debugging.

If you are in Mac, the image will be opened by your default image application
(:file:`Preview.app` usually).

You can use it from CLI also.  Execute :mod:`wand.display` module through
:option:`python -m` option:

.. sourcecode:: console

   $ python -m wand.display wandtests/assets/mona-lisa.jpg

"""
import os
import sys
import platform
import tempfile
import ctypes
from .image import Image
from .api import library
from .exceptions import BlobError

__all__ = 'display',


def display(image, server_name=':0'):
    """Displays the passed ``image``.

    :param image: an image to display
    :type image: :class:`~wand.image.Image`
    :param server_name: X11 server name to use.  it is ignored and not used
                        for Mac.  default is ``':0'``
    :type server_name: :class:`str`

    """
    if not isinstance(image, Image):
        raise TypeError('image must be a wand.image.Image instance, not ' +
                        repr(image))
    system = platform.system()
    if system == 'Darwin':
        ext = '.' + image.format.lower()
        path = tempfile.mktemp(suffix=ext)
        image.save(filename=path)
        os.system('open ' + path)
    else:
        library.MagickDisplayImage.argtypes = [ctypes.c_void_p,
                                               ctypes.c_char_p]
        library.MagickDisplayImage(image.wand, str(server_name))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print>>sys.stderr, 'usage: python -m wand.display FILE'
        raise SystemExit
    path = sys.argv[1]
    try:
        with Image(filename=path) as image:
            display(image)
    except BlobError:
        print>>sys.stderr, 'cannot read the file', path

