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

@tests.test
def raises_exceptions():
    """Exceptions raise, and warnings warn"""
    from wand import resource
    exceptions = resource.exceptions
    class DummyResource(resource.Resource):

        def set_exception_type(self, idx):
            self.exception_index = idx

        def get_exception(self):
            exc_cls = exceptions.TYPE_MAP[self.exception_index]
            return exc_cls("Dummy exception")

    for code in exceptions.TYPE_MAP.keys():
        resource = DummyResource()
        resource.set_exception_type(code)
        import warnings
        with warnings.catch_warnings(record=True) as w:
            try:
                resource.raise_exception()
                assert len(w) == 1
                assert w[-1].category.__name__.endswith('Warning')
                assert "Dummy exception" in str(w[-1].message)
            except exceptions.WandException as e:
                assert not e.__class__.__name__.endswith('Warning')
                assert e.message == 'Dummy exception'
