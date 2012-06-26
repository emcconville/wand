import datetime
import numbers
import re

from attest import Tests

from wand.version import (MAGICK_VERSION, MAGICK_VERSION_INFO,
                          MAGICK_VERSION_NUMBER, MAGICK_RELEASE_DATE,
                          MAGICK_RELEASE_DATE_STRING)
from . import color, image, resource


tests = Tests()
tests.register(resource.tests)  # it must be the first
tests.register(color.tests)
tests.register(image.tests)


@tests.test
def version():
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

