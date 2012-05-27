from attest import Tests

from . import color, image, resource


tests = Tests()
tests.register(resource.tests)  # it must be the first
tests.register(color.tests)
tests.register(image.tests)

