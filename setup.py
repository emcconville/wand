import os
import os.path
import sys
from setuptools import setup, find_packages
sys.path.insert(0, '.')
from wand.version import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


wand_includes = [
    "wand",
    "wand.cdefs"
]

wand_excludes = [
    "prof",     # CI Memory profile.
    "reports",  # CI coverage reports.
    "temp",     # CI artifacts.
    "sample",   # Old documents.
    "support",  # Non-public issues.
]

test_requires = [
    'pytest >= 7.2.0',
]

doc_requires = [
    'Sphinx >= 5.3.0',
]

setup(
    name='Wand',
    packages=find_packages(
        include=wand_includes,
        exclude=wand_excludes,
    ),
    version=VERSION,
    description='Ctypes-based simple MagickWand API binding for Python',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    license='MIT',
    license_files = ['LICENSE'],
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
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Multimedia :: Graphics'
    ],
    keywords='ImageMagick ctypes',
    project_urls={
        'Documentation': 'https://docs.wand-py.org',
        'Source': 'https://github.com/emcconville/wand',
        'Tracker': 'https://github.com/emcconville/wand/issues',
    }
)
