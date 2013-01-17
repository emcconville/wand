from wand import resource

import unittest
import tempfile
import os
import io


class ResourceTests(unittest.TestCase):
    def test_refcount(self):
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
        self.assertEqual(resource.reference_count, 0)
        resource.increment_refcount()
        assert called['genesis']
        assert not called['terminus']
        self.assertEqual(resource.reference_count, 1)
        resource.increment_refcount()
        assert not called['terminus']
        self.assertEqual(resource.reference_count, 2)
        resource.decrement_refcount()
        assert not called['terminus']
        self.assertEqual(resource.reference_count, 1)
        resource.decrement_refcount()
        assert called['terminus']
        self.assertEqual(resource.reference_count, 0)

    def test_negative_refcount(self):
        """reference_count cannot be negative"""
        with self.assertRaises(RuntimeError):
            resource.decrement_refcount()

    def test_raises_exceptions(self):
        """Exceptions raise, and warnings warn"""
        from wand import exceptions, resource
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
                    self.assertEqual(len(w), 1)
                    assert w[-1].category.__name__.endswith('Warning')
                    assert "Dummy exception" in str(w[-1].message)
                except exceptions.WandException as e:
                    assert not e.__class__.__name__.endswith('Warning')
                    self.assertEqual(e.message, 'Dummy exception')
