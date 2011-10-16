Wand Changelog
==============

Version 0.1.2
-------------

To be released. Still alpha version.

- Added `wand.color` module.
- Added the abstract base class of all Wand resource objects:
  :class:`wand.resource.Resource`.
- :class:`~wand.image.Image` implements slicing.
- Cropping :class:`~wand.image.Image` using its slicing operator.

Version 0.1.1
-------------

Released on October 4, 2011. Still alpha version.

- Now it handles errors and warnings properly and in natural way of Python.
- Added :meth:`Image.make_blob() <wand.image.Image.make_blob>` method.
- Added ``blob`` parameter into :class:`~wand.image.Image` constructor.
- Added :meth:`Image.resize() <wand.image.Image.resize>` method.
- Added :meth:`Image.save() <wand.image.Image.save>` method.
- Added :meth:`Image.clone() <wand.image.Image.clone>` method.
- Drawed `the pretty logo picture <_static/wand.png>`_
  (thanks to `Hyojin Choi <http://me2day.net/crocodile>`_).


Version 0.1.0
-------------

Released on October 1, 2011. Very alpha version.

