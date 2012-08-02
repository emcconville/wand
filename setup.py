try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import distutils.cmd
import os
import os.path
import shutil
import subprocess
import tarfile
import tempfile
import traceback
import urllib2

from wand.version import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


class bundle_imagemagick(distutils.cmd.Command):
    """Bundle ImageMagick library into the distribution."""

    # url = 'http://www.imagemagick.org/download/ImageMagick-6.7.8-7.tar.bz2'
    url = 'https://github.com/downloads/dahlia/wand/ImageMagick-6.7.8-7.tar.bz2'
    description = __doc__
    user_options = [
        ('url=', 'u', 'ImageMagick source tarball url [default: ' + url + ']')
    ]

    def initialize_options(self):
        self.url = self.__class__.url

    def finalize_options(self):
        pass

    def main(self):
        log = distutils.log
        for name in os.listdir('.'):
            if name.startswith('ImageMagick-') and os.path.isdir(name):
                dirname = name
                log.info('ImageMagick source seems to already exist')
                break
        else:
            log.info('Downloading ImageMagick source tarball...')
            log.info(self.url)
            response = urllib2.urlopen(self.url)
            tmp = tempfile.TemporaryFile()
            self.copy(response, tmp)
            response.close()
            tmp.seek(0)
            log.info('Extracting ImageMagick source tarball...')
            tar = tarfile.open(fileobj=tmp)
            dirname = tar.getnames()[0]
            tar.extractall()
        libdir = os.path.join(dirname, 'lib')
        if os.path.isdir(libdir):
            log.info('ImageMagick seems already built')
        else:
            log.info('Getting configured ImageMagick...')
            subprocess.call([
                './configure', '--prefix=' + os.path.abspath(dirname),
                '--disable-installed', '--without-magick-plus-plus'
            ], cwd=dirname)
            log.info('Building ImageMagick...')
            subprocess.call(['make', 'install'], cwd=dirname)
        dstdir = os.path.join('wand', 'lib')
        if not os.path.isdir(dstdir):
            os.mkdir(dstdir)
        data = []
        for libname in os.listdir(libdir):
            if not libname.endswith(('.so', '.dylib')):
                continue
            with open(os.path.join(libdir, libname), 'rb') as src:
                dstname = os.path.join('lib', libname)
                with open(os.path.join('wand', dstname), 'wb') as dst:
                    self.copy(src, dst)
                data.append(dstname)
        self.distribution.package_data.setdefault('wand', []).extend(data)
        self.distribution.has_ext_modules = lambda: True
        self.distribution.zip_safe = False

    def run(self):
        try:
            self.main()
        except:
            traceback.print_exc()
            raise

    def copy(self, source, destination):
        while 1:
            chunk = source.read(4096)
            if chunk:
                destination.write(chunk)
            else:
                break


class upload_doc(distutils.cmd.Command):
    """Uploads the documentation to GitHub pages."""

    description = __doc__
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path = tempfile.mkdtemp()
        build = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'build', 'sphinx', 'html')
        os.chdir(path)
        os.system('git clone git@github.com:dahlia/wand.git .')
        os.system('git checkout gh-pages')
        os.system('git rm -r .')
        os.system('touch .nojekyll')
        os.system('cp -r ' + build + '/* .')
        os.system('git stage .')
        os.system('git commit -a -m "Documentation updated."')
        os.system('git push origin gh-pages')
        shutil.rmtree(path)


setup(
    name='Wand',
    packages=['wand'],
    version=VERSION,
    description='Ctypes-based simple MagickWand API binding for Python',
    long_description=readme(),
    license='MIT License',
    author='Hong Minhee',
    author_email='minhee@dahlia.kr',
    maintainer='Hong Minhee',
    maintainer_email='minhee@dahlia.kr',
    url='http://dahlia.github.com/wand/',
    data_files=[('', ['README.rst'])],
    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='wandtests.tests',
    extras_require={'doc': ['Sphinx >=1.0']},
    setup_requires=['github-distutils >= 0.1.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Graphics'
    ],
    cmdclass={
        'bundle_imagemagick': bundle_imagemagick,
        'upload_doc': upload_doc
    }
)
