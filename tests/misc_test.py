import datetime
import numbers
import re
from py.test import mark

from wand.version import (MAGICK_VERSION, MAGICK_VERSION_INFO,
                          MAGICK_VERSION_NUMBER, MAGICK_RELEASE_DATE,
                          MAGICK_RELEASE_DATE_STRING, QUANTUM_DEPTH,
                          configure_options, fonts, formats)


def test_version():
    """Test version strings."""
    match = re.match('^ImageMagick\s+\d+\.\d+\.\d+(?:-\d+)?', MAGICK_VERSION)
    assert match
    assert isinstance(MAGICK_VERSION_INFO, tuple)
    assert (len(MAGICK_VERSION_INFO) ==
            match.group(0).count('.') + match.group(0).count('-') + 1)
    assert all(isinstance(v, int) for v in MAGICK_VERSION_INFO)
    assert isinstance(MAGICK_VERSION_NUMBER, numbers.Integral)
    assert isinstance(MAGICK_RELEASE_DATE, datetime.date)
    assert (MAGICK_RELEASE_DATE_STRING ==
            MAGICK_RELEASE_DATE.strftime('%Y-%m-%d'))


def test_quantum_depth():
    """QUANTUM_DEPTH must be one of 8, 16, 32, or 64."""
    assert QUANTUM_DEPTH in (8, 16, 32, 64)


def test_configure_options():
    assert 'RELEASE_DATE' in configure_options('RELEASE_DATE')


def test_fonts():
    font_list = fonts()
    mark.skipif(not font_list, reason='Fonts not configured on system')
    first_font = font_list[0]
    first_font_part = first_font[1:-1]
    assert first_font in fonts('*{0}*'.format(first_font_part))


def test_formats():
    xc = 'XC'
    assert formats(xc) == [xc]
