import sys

from attest import Tests
from attest.hook import AssertImportHook

# Attest assert hook doesn't work with Jython
if hasattr(sys, 'JYTHON_JAR'):
    AssertImportHook.disable()

from . import color, image, resource


tests = Tests()
tests.register(resource.tests)  # it must be the first
tests.register(color.tests)
tests.register(image.tests)

