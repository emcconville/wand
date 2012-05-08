""":mod:`wand.pycompat` --- Python 2/3 compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Abstracts away differences between Python 2 and 3, mostly related to str/bytes.

"""


def b(seq):
    """Normalizes a sequence to bytes."""
    if not isinstance(seq, bytes):
        return seq.encode('iso-8859-1')
    return seq


def u(seq):
    """Normalizes a sequence to unicode."""
    if not isinstance(seq, str):
        return seq.decode('iso-8859-1')
    return seq
