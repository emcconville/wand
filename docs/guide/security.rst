Security
========

The authors & contributors of the :mod:`Wand` module, ImageMagick library, and
all the third party image delegates make a genuine effort to release stable
code. However there is a trade off between convenience & secure environment,
and everyone makes honest mistakes. Ensure you're using the latest library
versions, and the system is up to date with security patches. If you are using
:mod:`Wand` to process images from the public, then you **must** be more
vigilant.

- Never use :mod:`Wand` directly within a HTTP service, or on any server with
  public access. A simple queue based background worker can be used.
  For example: `Celery`_, `Redis`_, or Amazon's `SQS`_, but there are many
  others.
- Update the ``policy.xml`` on the system, and reduce the resource limits to
  something reasonable to your system.

  .. code:: xml

      <policy domain="resource" name="memory" value="256MiB"/>
      <policy domain="resource" name="map" value="512MiB"/>
      <policy domain="resource" name="width" value="8KP"/>
      <policy domain="resource" name="height" value="8KP"/>
      <policy domain="resource" name="area" value="16KP"/>
      <policy domain="resource" name="disk" value="1GiB"/>
      <policy domain="resource" name="file" value="768"/>
      <policy domain="resource" name="thread" value="1"/>
      <policy domain="resource" name="throttle" value="0"/>
      <policy domain="resource" name="time" value="120"/>
      <policy domain="resource" name="list-length" value="128"/>

- Update the ``policy.xml`` on the system to restrict any formats that are
  unused, or have a history of abuse.

  .. code:: xml

      <policy domain="coder" rights="none" pattern="MVG" />
      <policy domain="coder" rights="none" pattern="EPS" />
      <policy domain="coder" rights="none" pattern="PS" />
      <policy domain="coder" rights="none" pattern="PS2" />
      <policy domain="coder" rights="none" pattern="PS3" />
      <policy domain="coder" rights="none" pattern="PDF" />
      <policy domain="coder" rights="none" pattern="XPS" />
      <policy domain="filter" rights="none" pattern="*" />
      <policy domain="delegate" rights="none" pattern="HTTPS" />
      <policy domain="delegate" rights="none" pattern="SHOW" />
      <policy domain="delegate" rights="none" pattern="WIN" />
      <policy domain="path" rights="none" pattern="@*"/>

- Check the "`magick bytes`_" of all untrusted files before processing. Never
  assume that the file extension suffix, or mimetype is good enough.
  For example::

    def assert_png(filename):
        """Ensure the file at a give path has the PNG magick-number
        header.  Throw an `AssertionError` if it does not match.
        """
        PNG_HEADER = [
            0x89, 0x50, 0x4E, 0x47,
            0x0D, 0x0A, 0x1A, 0x0A
        ]
        with open(filename, 'rb') as fd:
            file_header = list(fd.read(8))
        assert file_header == PNG_HEADER

    try:
        assert_png(user_file)
        with Image(filename='png:'+user_file) as img:
            # ... do work ...
    except AssertionError:
        # ... handle exception ...

- Ensure that any Python code is invoked with a low-privileged system user.
- Ensure filenames are sanitized.
- Ensure filenames are prefixed with coder protocol.

  .. code::

      with Image(filename='png:input.png') as img:
          # ... do work ...

- Ensure error handling is in place. Expect
  :class:`~wand.exceptions.PolicyError`
  exceptions if a file-format was banned, and
  :class:`~wand.exceptions.ResourceLimitError` if the system
  is unable to allocate additional memory/disk resources.
  Both can be configured by the :file:`policy.xml` listed above.

.. _Celery: http://www.celeryproject.org/
.. _Redis: https://redis.io/
.. _SQS: https://aws.amazon.com/sqs/
.. _magick bytes: https://en.wikipedia.org/wiki/Magic_number_(programming)#Format_indicators
