import datetime
import numbers
import os
import re

from attest import Tests

from wand.version import (MAGICK_VERSION, MAGICK_VERSION_INFO,
                          MAGICK_VERSION_NUMBER, MAGICK_RELEASE_DATE,
                          MAGICK_RELEASE_DATE_STRING, QUANTUM_DEPTH)
from . import color, image, resource, sequence, drawing


tests = Tests()

skip_tests = frozenset(os.environ.get('WANDTESTS_SKIP', '').split())
only_tests = frozenset(os.environ.get('WANDTESTS_ONLY', '').split())


def register(test_module):
    """Conditionally register the ``test_module`` according to
    environment variables.

    """
    name = test_module.__name__.split('.', 1)[1]
    if name in skip_tests:
        return
    elif only_tests and name not in only_tests:
        return
    tests.register(test_module.tests)


register(resource)  # it must be the first
register(color)
register(image)
register(sequence)
register(drawing)


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


@tests.test
def quantum_depth():
    """QUANTUM_DEPTH must be one of 8, 16, 32, or 64."""
    assert QUANTUM_DEPTH in (8, 16, 32, 64)
