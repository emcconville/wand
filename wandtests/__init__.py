from attest import Tests
from . import resource, image


tests = Tests()
tests.register(resource.tests)
tests.register(image.tests)

