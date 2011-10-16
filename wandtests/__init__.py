from attest import Tests
from . import resource, image, color


tests = Tests()
tests.register(resource.tests)
tests.register(image.tests)
tests.register(color.tests)

