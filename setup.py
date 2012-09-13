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

    url_base = 'https://github.com/downloads/dahlia/wand/'
    libraries = {
        'ImageMagick': (
            url_base + 'ImageMagick-6.7.9-5.tar.bz2',
            ['--disable-installed', '--without-magick-plus-plus',
             '--enable-delegate-build'] +
            (['--disable-openmp'] if platform.system() == 'Darwin' else []),
            {
                'CFLAGS': '-I@/include',
                'CPPFLAGS': '-I@/include',
                'LDFLAGS': '-L@/lib'
            },
        ),
        'jpeg': (url_base + 'jpegsrc.v8d.tar.gz', [], {}),
        'libpng': (url_base + 'libpng-1.5.12.tar.gz', [], {})
    }
    description = __doc__
    user_options = list(
        (libname.lower() + '-url=', 'u' if libname == 'ImageMagick' else None,
         libname + ' source tarball url [default: ' + url + ']')
        for libname, (url, _, __) in libraries.iteritems()
    )

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.urls = dict(
            (libname, getattr(self, libname.lower() + '_url', None) or url)
            for libname, url in self.__class__.libraries.iteritems()
        )

    def download_extract(self):
        log = distutils.log
        names = os.listdir('.')
        for libname, (url, _, __) in self.urls.iteritems():
            for dirname in names:
                if os.path.isdir(dirname) and dirname.startswith(libname + '-'):
                    log.info(libname + ' source seems to already exist')
                    break
            else:
                log.info('Downloading %s source tarball...', libname)
                log.info('%s', url)
                response = urllib2.urlopen(url)
                tmp = tempfile.TemporaryFile()
                shutil.copyfileobj(response, tmp)
                response.close()
                tmp.seek(0)
                log.info('Extracting %s source tarball...', libname)
                tar = tarfile.open(fileobj=tmp)
                dirname = tar.getnames()[0]
                tar.extractall()
            yield libname, dirname

    def main(self):
        log = distutils.log
        path = os.path
        join = path.join
        states = dict(
            (libname, {'dir': dirname})
            for libname, dirname in self.download_extract()
        )
        magick_dir = path.abspath(states['ImageMagick']['dir'])
        for subdir in 'lib', 'man', join('man', 'man1'), 'bin':
            subdir = join(magick_dir, subdir)
            if not path.isdir(subdir):
                os.mkdir(subdir)
        libnames = states.keys()
        libnames.sort(key=lambda name: name == 'ImageMagick')
        if not (path.isfile(join(magick_dir, 'lib', 'libMagickCore.so')) or
                path.isfile(join(magick_dir, 'lib', 'libMagickCore.dylib'))):
            for libname in libnames:
                log.info('Getting configured %s...', libname)
                env = dict(os.environ)
                env.update(
                    (k, v.replace('@', magick_dir))
                    for k, v in self.__class__.libraries[libname][2].iteritems()
                )
                dirname = path.abspath(states[libname]['dir'])
                subprocess.call(['./configure', '--prefix=' + magick_dir] +
                                self.__class__.libraries[libname][1],
                                cwd=dirname, env=env)
                log.info('Building %s...', libname)
                subprocess.call(['make', 'install'], cwd=dirname, env=env)
        dstdir = join('wand', 'lib')
        if not path.isdir(dstdir):
            os.mkdir(dstdir)
        package_data = self.distribution.package_data
        data = []
        libdir = join(magick_dir, 'lib')
        for soname in os.listdir(libdir):
            if soname.endswith(('.so', '.dylib')):
                shutil.copy(join(libdir, soname), join(dstdir, soname))
                data.append('lib/' + soname)
        package_data.setdefault('wand', []).extend(data)
        # shutil.copytree(os.path.join(libdir, 'modules'),
        #                 os.path.join(dstdir, 'modules'))
        # package_data['wand'].extend([
        #     'lib/modules/*.*',
        #     'lib/modules/*/*.*',
        # ])
        self.distribution.has_ext_modules = lambda: True
        self.distribution.zip_safe = False

    def run(self):
        try:
            self.main()
        except:
            traceback.print_exc()
            raise


class bundle_imagemagick_win32(distutils.cmd.Command):
    """Bundle ImageMagick library into the distribution. (Windows)"""

    urls = {
        'win-amd64': 'https://github.com/downloads/dahlia/wand/'
                     'ImageMagick-6.7.8-7-Q16-windows-x64-dll.exe',
        'win32': 'https://github.com/downloads/dahlia/wand/'
                 'ImageMagick-6.7.8-7-Q16-windows-dll.exe'
    }
    description = __doc__
    user_options = [
        ('url=', 'u', 'ImageMagick binary zip url [default: ' +
                      urls['win-amd64' if platform.architecture()[0] == '64bit'
                                       else 'win32'] +
                      ']')
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        if not self.url:
            self.url = self.__class__.urls[self.plat_name]

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

    def main(self):
        log = distutils.log
        if os.path.isdir('ImageMagick-win'):
            log.info('ImageMagick source seems to already exist')
        else:
            self.download_extract()
        package_data = self.distribution.package_data
        data = []
        for libname in os.listdir('ImageMagick-win'):
            if libname.endswith('.dll'):
                shutil.copy(os.path.join('ImageMagick-win', libname),
                            os.path.join('wand', libname))
                data.append(libname)
        package_data.setdefault('wand', []).extend(data)
        shutil.copytree(os.path.join('ImageMagick-win', 'modules'),
                        os.path.join('wand', 'modules'))
        package_data['wand'].extend([
            'modules/*.*',
            'modules/*/*.*'
        ])
        self.distribution.has_ext_modules = lambda: True
        self.distribution.zip_safe = False
        subprocess.call([
            os.path.join('ImageMagick-win', 'unins000'),
            '/VERYSILENT', '/NORESTART'
        ])

    def run(self):
        try:
            self.main()
        except:
            traceback.print_exc()
            raise


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
