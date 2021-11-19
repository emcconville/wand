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

test_requires = [
    'pytest >= 5.3.5',
]

doc_requires = [
    'Sphinx >= 2.4.1',
]

setup(
    name='Wand',
    packages=['wand', 'wand.cdefs'],
    version=VERSION,
    description='Ctypes-based simple MagickWand API binding for Python',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    license='MIT License',
    author='Hong Minhee',
    author_email='hongminhee' '@' 'member.fsf.org',
    maintainer='E. McConville',
    maintainer_email='emcconville' '@' 'emcconville.com',
    url='http://wand-py.org/',
    tests_require=test_requires,
    extras_require={'doc': doc_requires, 'test': test_requires},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Multimedia :: Graphics'
    ],
    keywords='ImageMagick ctypes',
    cmdclass=cmdclass,
    project_urls={
        'Documentation': 'https://docs.wand-py.org',
        'Source': 'https://github.com/emcconville/wand',
        'Tracker': 'https://github.com/emcconville/wand/issues',
    }
)
