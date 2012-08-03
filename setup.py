try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import distutils.cmd
import os
import os.path
import platform
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

    def download_extract(self):
        log = distutils.log
        log.info('Downloading ImageMagick source tarball...')
        log.info(self.url)
        response = urllib2.urlopen(self.url)
        tmp = tempfile.TemporaryFile()
        shutil.copyfileobj(response, tmp)
        response.close()
        tmp.seek(0)
        log.info('Extracting ImageMagick source tarball...')
        tar = tarfile.open(fileobj=tmp)
        dirname = tar.getnames()[0]
        tar.extractall()
        return dirname

    def get_library_dir(self, source_dir):
        return os.path.join(source_dir, 'lib')

    def build_library(self, source_dir):
        log = distutils.log
        log.info('Getting configured ImageMagick...')
        subprocess.call([
            './configure', '--prefix=' + os.path.abspath(source_dir),
            '--disable-installed', '--without-magick-plus-plus'
        ], cwd=source_dir)
        log.info('Building ImageMagick...')
        subprocess.call(['make', 'install'], cwd=source_dir)

    def get_bundle_dir(self):
        return os.path.join('wand', 'lib')

    def is_library_filename(self, filename):
        return filename.endswith(('.so', '.dylib'))

    def get_package_data_name(self, filename):
        return os.path.join('lib', filename)

    def main(self):
        log = distutils.log
        for name in os.listdir('.'):
            if name.startswith('ImageMagick-') and os.path.isdir(name):
                dirname = name
                log.info('ImageMagick source seems to already exist')
                break
        else:
            dirname = self.download_extract()
        libdir = self.get_library_dir(dirname)
        if os.path.isdir(libdir):
            log.info('ImageMagick seems already built')
        else:
            self.build_library(dirname)
        dstdir = self.get_bundle_dir()
        if not os.path.isdir(dstdir):
            os.mkdir(dstdir)
        package_data = self.distribution.package_data
        data = []
        for libname in os.listdir(libdir):
            if not self.is_library_filename(libname):
                continue
            shutil.copy(os.path.join(libdir, libname),
                        os.path.join(dstdir, libname))
            data.append(self.get_package_data_name(libname))
        package_data.setdefault('wand', []).extend(data)
        shutil.copytree(os.path.join(libdir, 'modules'),
                        os.path.join(dstdir, 'modules'))
        modulesdir = self.get_package_data_name('modules')
        package_data['wand'].extend([
            modulesdir + '/*.*',
            modulesdir + '/*/*.*'
        ])
        self.distribution.has_ext_modules = lambda: True
        self.distribution.zip_safe = False

    def run(self):
        try:
            self.main()
        except:
            traceback.print_exc()
            raise


class bundle_imagemagick_win32(bundle_imagemagick):
    """Bundle ImageMagick library into the distribution. (Windows)"""

    if platform.architecture()[0] == '64bit':
        url = 'https://github.com/downloads/dahlia/wand/' \
              'ImageMagick-6.7.8-7-Q16-windows-x64-dll.exe'
    else:
        url = 'https://github.com/downloads/dahlia/wand/' \
              'ImageMagick-6.7.8-7-Q16-windows-dll.exe'
    description = __doc__
    user_options = [
        ('url=', 'u', 'ImageMagick binary zip url [default: ' + url + ']')
    ]

    def download_extract(self):
        log = distutils.log
        log.info('Downloading ImageMagick installer...')
        response = urllib2.urlopen(self.url)
        tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfileobj(response, tmp)
        response.close()
        tmp.close()
        log.info('Installing ImageMagick...')
        installdir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'ImageMagick-win')
        subprocess.call([
            tmp.name, '/VERYSILENT', '/NORESTART', '/NOICONS',
            '/DIR=' + installdir
        ])
        return installdir

    def get_library_dir(self, source_dir):
        return source_dir

    def build_library(self, source_dir):
        pass

    def get_bundle_dir(self):
        return 'wand'

    def is_library_filename(self, filename):
        return filename.endswith('.dll')

    def get_package_data_name(self, filename):
        return filename

    def main(self):
        bundle_imagemagick.main(self)
        return
        subprocess.call([
            os.path.join('ImageMagick-win', 'unins000'),
            '/VERYSILENT', '/NORESTART'
        ])


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
        'bundle_imagemagick': (bundle_imagemagick_win32
                               if platform.system() == 'Windows'
                               else bundle_imagemagick),
        'upload_doc': upload_doc
    }
)
