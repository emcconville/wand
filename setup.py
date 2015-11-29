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


try:
    from setuptools.command.test import test
except ImportError:
    cmdclass = {}
else:
    class pytest(test):

        def finalize_options(self):
            test.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            from pytest import main
            errno = main(self.test_args)
            raise SystemExit(errno)
    cmdclass = {'test': pytest}


setup(
    name='Wand',
    packages=['wand'],
    data_files=[('', ['README.rst'])],
    version=VERSION,
    description='Ctypes-based simple MagickWand API binding for Python',
    long_description=readme(),
    license='MIT License',
    author='Hong Minhee',
    author_email='hongminhee' '@' 'member.fsf.org',
    maintainer='Hong Minhee',
    maintainer_email='hongminhee' '@' 'member.fsf.org',
    url='http://wand-py.org/',
    tests_require=[
        'pytest >= 2.3.0',
        'pytest-xdist >= 1.8',
        'memory_profiler >= 0.27',
        'psutil >= 1.0.1'
    ],
    extras_require={'doc': ['Sphinx >=1.0']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Multimedia :: Graphics'
    ],
    cmdclass=cmdclass
)
