

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Activity follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Activity uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.activity.png
  :target: https://travis-ci.org/OneGov/onegov.activity
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.activity/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.activity?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.activity.svg
    :target: https://badge.fury.io/py/onegov.activity
    :alt: Latest PyPI Release

License
-------
onegov.activity is released under GPLv2

Changelog
---------

0.0.4 (2016-10-03)
~~~~~~~~~~~~~~~~~~~

- Overhauls the occasion model.
  [href]

0.0.3 (2016-09-29)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to directly access the user object from the activity.
  [href]

0.0.2 (2016-09-26)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to override the query base on a subclass.
  [href]

- Adds the ability to filter the collection by state.
  [href]

- Adds the ability to get the set of used activity tags.
  [href]

0.0.1 (2016-09-22)
~~~~~~~~~~~~~~~~~~~

- Initial Release


