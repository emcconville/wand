import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from wand.version import VERSION_INFO


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


setup(name='Wand',
      packages=['wand'],
      version=VERSION_INFO,
      description='Ctypes-based simple MagickWand API binding for Python',
      long_description=readme(),
      license='MIT License',
      author='Hong Minhee',
      author_email='dahlia' '@' 'stylesha.re',
      maintainer='StyleShare',
      maintainer_email='dev' '@' 'stylesha.re',
      url='https://styleshare.github.com/wand/',
      tests_require=['Attest'],
      test_loader='attest:auto_reporter.test_loader',
      test_suite='wandtests.tests',
      extras_require={'doc': ['Sphinx >=1.0']},
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Graphics'
      ])

