""":mod:`wand.assertions` --- Input assertion helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module checks user input before calling MagickWands C-API methods.


.. versionadded:: 0.5.4
"""

import numbers

from .compat import string_type


def assert_integer(subject, label=None):
    if not isinstance(subject, numbers.Integral):
        if label:
            fmt = "{0} must be an integer, not {1}"
            msg = fmt.format(label, repr(subject))
        else:
            fmt = "expecting an integer, not {0}"
            msg = fmt.format(repr(subject))
        raise TypeError(msg)


def assert_real(subject, label=None):
    if not isinstance(subject, numbers.Real):
        if label:
            fmt = "{0} must be a real number, not {1}"
            msg = fmt.format(label, repr(subject))
        else:
            fmt = "expecting a real number, not {0}"
            msg = fmt.format(repr(subject))
        raise TypeError(msg)


def assert_unsigned_integer(subject, label=None):
    assert_integer(subject, label)
    if subject < 0:
        if label:
            fmt = "{0}={1} must be a postive integer"
            msg = fmt.format(label, subject)
        else:
            fmt = "expecting a postive integer, not {0}"
            msg = fmt.format(subject)
        raise ValueError(msg)


def assert_counting_number(subject, label):
    assert_integer(subject, label)
    if subject < 1:
        fmt = "{0}={1} must be an natural number greater than 0"
        msg = fmt.format(label, subject)
        raise ValueError(msg)


def assert_bool(subject, label=None):
    if not isinstance(subject, bool):
        if label:
            fmt = "{0} must be a bool, not {1}"
            msg = fmt.format(label, repr(subject))
        else:
            fmt = "expecting a bool type, not {0}"
            msg = fmt.format(repr(subject))
        raise TypeError(msg)


def assert_string(subject, label=None):
    if not isinstance(subject, string_type):
        if label:
            fmt = "{0} must be a string, not {1}"
            msg = fmt.format(label, repr(subject))
        else:
            fmt = "expecting a string type, not {0}"
            msg = fmt.format(repr(subject))
        raise TypeError(msg)


def assert_color(subject, label=None):
    if not isinstance(subject, Color):
        if label:
            fmt = "Expecting an instance of wand.color.Color for {0}, not {1}"
            msg = fmt.format(label, repr(subject))
        else:
            fmt = "Expecting an instance of wand.color.Color, not {0}"
            msg = fmt.format(repr(subject))
        raise TypeError(msg)


def counting_numbers(**kwargs):
    for label, subject in kwargs.items():
        assert_counting_number(subject, label)


def in_list(options, label, **kwargs):
    for subject_label, subject in kwargs.items():
        if subject not in options:
            fmt = "{0} must be defined in {1}, not {2}"
            msg = fmt.format(subject_label, label, repr(subject))
            raise ValueError(msg)


def string_in_list(options, label, **kwargs):
    for subject_label, subject in kwargs.items():
        assert_string(subject, subject_label)
    in_list(options, label, **kwargs)


# Lazy load recursive import
from .color import Color  # noqa: E402
