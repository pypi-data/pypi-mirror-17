========
Overview
========



CloudWatch-based monitoring for your servers.

* Free software: BSD license

Installation
============

::

    pip install cwmon

Documentation
=============

https://cwmon.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

Changelog
=========

0.2.0 (2016-10-13)
------------------

New
~~~

- Import initial functionality from internal project. [Hank Gay]

Changes
~~~~~~~

- Make some docstrings a little less personal. [Hank Gay]

- Fix classifiers and keywords. [Hank Gay]

- Add some docstings to make flake8 happy. [Hank Gay]

- Point everything to RescueTime instead of my personal info. [Hank Gay]

Fix
~~~

- Fix actually posting to CloudWatch (had 'Timestamp' in wrong place in
  payload before). [Hank Gay]

- Tweak badges some more. [Hank Gay]

- Fix coveralls badge. [Hank Gay]

Other
~~~~~

- Bump version: 0.1.6 → 0.2.0. [Hank Gay]

- Add helpers for echoing styled text (and use them). [Hank Gay]

- Add dependency on colorama. [Hank Gay]

- Doc: Add requires.io badge. [Hank Gay]

- Doc: List 'tox' as a dev dependency. [Hank Gay]

- Add dev dependency on twine. [Hank Gay]

- Initial project skeleton. [Hank Gay]


