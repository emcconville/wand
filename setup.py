import os
import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from wand.version import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


setup(
    name='Wand',
    packages=['wand'],
    data_files=[('', ['README.rst'])],
    version=VERSION,
    description='Ctypes-based simple MagickWand API binding for Python',
    long_description=readme(),
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee@dahlia.kr',
    maintainer='Hong Minhee',
    maintainer_email='minhee@dahlia.kr',
    url='http://wand-py.org/',
    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='wandtests.tests',
    extras_require={'doc': ['Sphinx >=1.0']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Multimedia :: Graphics'
      ],
)
