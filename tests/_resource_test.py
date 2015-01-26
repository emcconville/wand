# Why the name of this file does start with underscore?
#
# This tests Wand's internal reference counter, so we can't assume
# the initial state after any function of Wand are used.
# That means this tests have to be first, and py.test automatically
# discovers tests just using filenames.  Fortuneately, it seems to run
# tests in lexicographical order, so we simply adds underscore to
# the beginning of the filename.
from pytest import mark, raises

from wand import exceptions, resource


def test_refcount():
    """Refcount maintains the global instance."""
    genesis = resource.genesis
    terminus = resource.terminus
    called = {'genesis': False, 'terminus': False}

    def decorated_genesis():
        genesis()
        called['genesis'] = True

    def decorated_terminus():
        terminus()
        called['terminus'] = True

    resource.genesis = decorated_genesis
    resource.terminus = decorated_terminus
    assert not called['genesis']
    assert not called['terminus']
    assert resource.reference_count == 0
    resource.increment_refcount()
    assert called['genesis']
    assert not called['terminus']
    assert resource.reference_count == 1
    resource.increment_refcount()
    assert not called['terminus']
    assert resource.reference_count == 2
    resource.decrement_refcount()
    assert not called['terminus']
    assert resource.reference_count == 1
    resource.decrement_refcount()
    assert called['terminus']
    assert resource.reference_count == 0


def test_negative_refcount():
    """reference_count cannot be negative"""
    with raises(RuntimeError):
        resource.decrement_refcount()


class DummyResource(resource.Resource):

    def set_exception_type(self, idx):
        self.exception_index = idx

    def get_exception(self):
        exc_cls = exceptions.TYPE_MAP[self.exception_index]
        return exc_cls("Dummy exception")


@mark.parametrize('code', exceptions.TYPE_MAP.keys())
def test_raises_exceptions(recwarn, code):
    """Exceptions raise, and warnings warn"""
    res = DummyResource()
    res.set_exception_type(code)
    try:
        res.raise_exception()
    except exceptions.WandException as e:
        assert not e.__class__.__name__.endswith('Warning')
        assert str(e) == 'Dummy exception'
    else:
        w = recwarn.pop()
        assert w.category.__name__.endswith('Warning')
        assert "Dummy exception" in str(w.message)
        assert recwarn.list == []
