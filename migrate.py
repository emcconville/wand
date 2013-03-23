import os
import os.path


def tree(path=os.path.curdir):
    """Travrse file/directory tree inside ``path``.  It doesn't include
    directories.

    """
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            for subentry in tree(entry_path):
                yield os.path.join(entry, subentry)
        else:
            yield entry


def html_filenames(path=os.path.curdir):
    """Find all HTML filenames inside ``path``."""
    for path in tree(path):
        if path.startswith('.git' + os.path.sep):
            continue
        if path.endswith('.html'):
            yield path


for html_path in html_filenames():
    url = 'http://docs.wand-py.org/en/0.2-maintenance/' + html_path
    with open(html_path, 'w') as html_file:
        print >> html_file, '''\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={url}">
    <title>Redirecting to {url}&hellip;</title>
    <link rel="canonical" href="{url}">
  </head>
  <body style="color: transparent;">
    <h1>Redirecting to
        <a href="{url}" style="color: transparent;">{url}</a>&hellip;</h1>
    <p>The website was moved&hellip;</p>
  </body>
</html>
        '''.format(url=url)
