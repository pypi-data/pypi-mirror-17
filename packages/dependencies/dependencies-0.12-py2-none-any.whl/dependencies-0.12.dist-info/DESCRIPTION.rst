.. |travis| image:: https://img.shields.io/travis/proofit404/dependencies.svg?style=flat-square
    :target: https://travis-ci.org/proofit404/dependencies
    :alt: Build Status

.. |coveralls| image:: https://img.shields.io/coveralls/proofit404/dependencies.svg?style=flat-square
    :target: https://coveralls.io/r/proofit404/dependencies
    :alt: Coverage Status

.. |requires| image:: https://img.shields.io/requires/github/proofit404/dependencies.svg?style=flat-square
    :target: https://requires.io/github/proofit404/dependencies/requirements
    :alt: Requirements Status

.. |codacy| image:: https://img.shields.io/codacy/907efcab21d14e9ea1d110411d5791cd.svg?style=flat-square
    :target: https://www.codacy.com/app/proofit404/dependencies
    :alt: Code Quality Status

.. |pypi| image:: https://img.shields.io/pypi/v/dependencies.svg?style=flat-square
    :target: https://pypi.python.org/pypi/dependencies/
    :alt: Python Package Version

============
Dependencies
============

|travis| |coveralls| |requires| |codacy| |pypi|

Dependency Injection for Humans.

- `Source Code`_
- `Issue Tracker`_
- Documentation_

Installation
------------

All released versions are hosted on the Python Package Index.  You can
install this package with following command.

.. code:: bash

    pip install dependencies

Usage
-----

Dependency injection without ``dependencies``

.. code:: python

    robot = Robot(
        servo=Servo(amplifier=Amplifier()),
        controller=Controller(),
        settings=Settings(environment="production"))

Dependency injection with ``dependencies``

.. code:: python

    class Container(Injector):
        robot = Robot
        servo = Servo
        amplifier = Amplifier
        controller = Controller
        settings = Settings
        environment = "production"

    robot = Container.robot

License
-------

Dependencies library is offered under LGPL license.

.. _source code: https://github.com/proofit404/dependencies
.. _issue tracker: https://github.com/proofit404/dependencies/issues
.. _documentation: http://dependencies.readthedocs.io/en/latest/

.. :changelog:

Changelog
---------

0.12 (2016-09-29)
+++++++++++++++++

- Allow multiple inheritance for Injector subclasses.
- Evaluate dependencies once.
- Add ``use`` decorator.
- Allow nested injectors.

0.11 (2016-08-22)
+++++++++++++++++

- Twelve times speed up.
- Protect from incorrect operations with attribute assignment.
- Deny `*args` and `**kwargs` in the injectable classes.
- Classes can be used as default argument values only if argument name
  ends with ``_cls``.
- Remove ``six`` library from install requires.

0.10 (2016-06-09)
+++++++++++++++++

- Turn into module.

0.9 (2016-06-08)
++++++++++++++++

- Dependency assignment and cancellation for ``Injector`` subclasses.

0.8 (2016-06-05)
++++++++++++++++

- Correct syntax error for Python 2.6

0.7 (2016-06-04)
++++++++++++++++

- Raise ``DependencyError`` for mutual recursion in constructor
  arguments and specified dependencies.
- Show injected dependencies in the ``dir`` result.
- Deny to instantiate ``Injector`` and its subclasses.

0.6 (2016-03-09)
++++++++++++++++

- Deprecate ``c`` alias.  Use real classes.
- Allow to use ``let`` directly on ``Injector``.
- Do not instantiate dependencies named with ``cls`` at the end.

0.5 (2016-03-03)
++++++++++++++++

- Avoid attribute search recursion.  This occurs with inheritance
  chain length started at 3 and missing dependency on first level.
- Add ``c`` alias for ``Injector`` subclass access.
- Add ``let`` factory to temporarily overwrite specified
  dependencies.

0.4 (2016-03-03)
++++++++++++++++

- Detect ``object.__init__`` and skip it in the argument injection.

0.3 (2016-03-02)
++++++++++++++++

- Deprecate injectable mechanism.  Injector may inject any arguments
  to any classes.  Injector now support multiple DI targets.  All
  possible targets now specified in the Injector attributes.  Only
  single base inheritance allowed for Injector subclasses.

0.2 (2016-02-13)
++++++++++++++++

- Allows to override dependencies specified with Injector by
  inheritance from this Injector subclass.

0.1 (2016-01-31)
++++++++++++++++

- Initial release.


