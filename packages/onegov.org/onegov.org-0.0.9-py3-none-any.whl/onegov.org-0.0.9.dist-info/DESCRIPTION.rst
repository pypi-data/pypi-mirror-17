

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Org follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Org uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.org.png
  :target: https://travis-ci.org/OneGov/onegov.org
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.org/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.org?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.org.svg
    :target: https://badge.fury.io/py/onegov.org
    :alt: Latest PyPI Release

License
-------
onegov.org is released under GPLv2

Changelog
---------

0.0.9 (2016-09-22)
~~~~~~~~~~~~~~~~~~~

- Fixes being unable to edit builtin forms.
  [href]

- Adds a ConfirmLink element which works like a DeleteLink but for POST.
  [href]

- Fixes title being shown twice on the news site.
  [href]

0.0.8 (2016-09-12)
~~~~~~~~~~~~~~~~~~~

- Fixes morepath directives not working in all cases.
  [href]

0.0.7 (2016-09-12)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to define a custom homepage through widgets.
  [href]

- Use a uuid converter for all uuid-ids to turn bad requests into 404s.
  [href]

- Adds the ability to override the initial content creation function.
  [href]

- Fixes user editing not working when yubikeys are enabled.
  [href]

0.0.6 (2016-08-31)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to manage users in a usermanagement view.
  [href]

0.0.5 (2016-08-26)
~~~~~~~~~~~~~~~~~~~

- Enables the user profile for simple members.
  [href]

- Adds the ability for new users to register themselves.
  [href]

0.0.4 (2016-08-25)
~~~~~~~~~~~~~~~~~~~

- Fixes upgrade not working in all cases.
  [href]

0.0.3 (2016-08-25)
~~~~~~~~~~~~~~~~~~~

- Possibly fixes release not working for PyPI.
  [href]

0.0.2 (2016-08-24)
~~~~~~~~~~~~~~~~~~~

- Removes dependency to itself.
  [href]

0.0.1 (2016-08-24)
~~~~~~~~~~~~~~~~~~~

- Initial Release


