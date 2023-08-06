========
Overview
========



A cwmon_ plugin for system-level monitoring.

.. _cwmon: https://github.com/RescueTime/cwmon

* Free software: BSD license

Installation
============

::

    pip install cwmon-system

Documentation
=============

https://cwmon-system.readthedocs.io/

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

0.5.0 (2016-10-18)
------------------

Changes
~~~~~~~

- Depend on cwmon 0.5 instead of 0.3. [Hank Gay]

Other
~~~~~

- Bump version: 0.1.0 → 0.5.0. [Hank Gay]

- Remove a bunch of extraneous positional arguments. [Hank Gay]

- Use https in the rescuetime link. [Hank Gay]

0.1.0 (2016-10-18)
------------------

- Merge branch 'release/0.1.0' [Hank Gay]

- Further cleanup of cwmon-mysql leftovrs. [Hank Gay]

- Initial project refactoring. [Hank Gay]

- Initial commit. [Hank Gay]




