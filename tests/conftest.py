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
from pytest import fixture, mark, skip

from wand.display import display as display_fn
from wand.image import Image


def pytest_addoption(parser):
    parser.addoption('--skip-slow', action='store_true',
                     help='Skip slow tests')
    parser.addoption('--imgur-client-id',
                     help='Imgur.com api client id.  Use imgur.com for '
                          'display() fixture if present.  Useful for '
                          'debugging on CI',
                     default=os.environ.get('IMGUR_CLIENT_ID'))


def pytest_runtest_setup(item):
    if 'slow' in item.keywords:
        try:
            skip_value = item.config.getoption('--skip-slow')
        except ValueError:
            pass
        else:
            if skip_value:
                skip('skipped; --skip-slow option is used')


@mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    """Copied from http://pytest.org/dev/example/simple.html#making-test-result-information-available-in-fixtures

    """  # noqa
    # execute all other hooks to obtain the report object
    rep = __multicall__.execute()
    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, 'rep_' + rep.when, rep)
    return rep


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
