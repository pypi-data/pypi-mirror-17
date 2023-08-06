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


