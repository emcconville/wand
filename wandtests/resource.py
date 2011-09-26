import os.path
from attest import assert_hook, Tests, raises
from wand import resource


tests = Tests()


@tests.test
def refcount():
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


def negative_refcount():
    """reference_count cannot be negative"""
    with raises(RuntimeError) as error:
        resource.decrement_refcount()

