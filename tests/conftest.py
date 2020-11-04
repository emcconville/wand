import base64
import inspect
import json
import os
try:
    from urllib import parse as urllib, request as urllib2
except ImportError:
    import urllib
    import urllib2

from py.path import local
from pytest import fixture, hookimpl, mark

from wand.display import display as display_fn
from wand.image import Image
from wand.version import MAGICK_VERSION, VERSION


def pytest_addoption(parser):
    parser.addoption('--skip-slow', action='store_true',
                     help='Skip slow tests')
    parser.addoption('--imgur-client-id',
                     help='Imgur.com api client id.  Use imgur.com for '
                          'display() fixture if present.  Useful for '
                          'debugging on CI',
                     default=os.environ.get('IMGUR_CLIENT_ID'))
    parser.addoption('--skip-pdf', action='store_true',
                     help='Skip any test with PDF documents.')
    parser.addoption('--skip-fft', action='store_true',
                     help='Skip any test with Forward Fourier Transform.')
    parser.addoption('--no-pdf', action='store_true',
                     help='Alias to --skip-pdf.')


def pytest_collection_modifyitems(config, items):
    skip_slow = False
    skip_pdf = False
    skip_fft = False
    if config.getoption('--skip-slow'):
        skip_slow = mark.skip('skipped; --skip-slow option was used')
    if config.getoption('--skip-pdf'):
        skip_pdf = mark.skip('skipped; --skip-pdf option was used')
    if config.getoption('--skip-fft'):
        skip_fft = mark.skip('skipped; --skip-fft option was used')
    if config.getoption('--no-pdf'):
        skip_pdf = mark.skip('skipped; --skip-pdf option was used')
    for item in items:
        if skip_slow and 'slow' in item.keywords:
            item.add_marker(skip_slow)
        if skip_pdf and 'pdf' in item.keywords:
            item.add_marker(skip_pdf)
        if skip_fft and 'fft' in item.keywords:
            item.add_marker(skip_fft)


def pytest_configure(config):
    config.addinivalue_line(
        'markers', 'slow: marks test as slow-running'
    )
    config.addinivalue_line(
        'markers', 'pdf: marks test as PDF/Ghostscript dependent'
    )
    config.addinivalue_line(
        'markers', 'fft: marks test as Forward Fourier Transform dependent'
    )


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Copied from http://pytest.org/dev/example/simple.html#making-test-result-information-available-in-fixtures

    """  # noqa
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


def pytest_report_header(config):
    versions = (VERSION, os.linesep, MAGICK_VERSION)
    return "Wand Version: {0}{1}ImageMagick Version: {2}".format(*versions)


@fixture
def fx_asset():
    """The fixture that provides :class:`py.path.local` instance that
    points the :file:`assets` directory.  You can use this in test
    functions::

        def test_something(fx_asset):
            monalisa = str(fx_asset.join('mona-lisa.jpg'))
            with open(monalisa) as f:
                assert f.tell() == 0

    """
    return local(__file__).dirpath('assets')


@fixture
def display(request):
    """Display an given image when a test fails.  It's a function that
    takes one required argument of :class:`~wand.image.Image` and one
    optional argument of its human readable label.

    For example::

        def test_something(display):
            with Image(filename='...') as image:
                display(image)
                image.resize(100, 100)
                display(image)
                assert image.size == (100, 101)

    if the above test fails, it will display two images.

    If you give ``--imgur-client-id`` option to pytest, it uploads
    these images instead of displaying:

    .. code-block::

       test_something.py:3 (image 1) http://i.imgur.com/iJPHO68.png
       test_something.py:5 (image 2) http://i.imgur.com/iJPHO69.png

    This option would be useful for remote debugging on CI.

    """
    images = []

    @request.addfinalizer
    def finalize():
        if request.node.rep_call.passed:
            return
        imgur_client_id = request.config.getoption('--imgur-client-id')
        if imgur_client_id:
            longrepr = request.node.rep_call.longrepr
            prints = []
            for line, label, format, blob in images:
                req = urllib2.Request(
                    'https://api.imgur.com/3/image',
                    headers={'Authorization': 'Client-ID ' + imgur_client_id},
                    data=urllib.urlencode({
                        'image': base64.b64encode(blob),
                        'title': '[{0}] {1}'.format(line, label)
                    }).encode('ascii')
                )
                response = urllib2.urlopen(req)
                result = json.loads(response.read().decode('utf-8'))
                prints.append((line, label, result['data']['link']))
                response.close()
            longrepr.addsection(
                'display',
                '\n'.join(map('{0[0]} ({0[1]}) {0[2]}'.format, prints))
            )
        else:
            for _, __, format, blob in images:
                with Image(blob=blob, format=format) as i:
                    display_fn(i)

    def log(image, label=None):
        back = inspect.currentframe().f_back
        line = '{0}:{1}'.format(back.f_code.co_filename, back.f_lineno)
        label = label or 'image {0}'.format(len(images))
        format = image.format or 'png'
        images.append((
            line, label, format,
            image.make_blob(format)
        ))
    return log
