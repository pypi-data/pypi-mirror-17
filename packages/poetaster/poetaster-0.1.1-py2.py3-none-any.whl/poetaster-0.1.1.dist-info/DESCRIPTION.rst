========
Overview
========



Poetry tricks and tools for found -- and generated -- poetry.

* Free software: BSD license

Installation
============

::

    pip install poetaster

Documentation
=============

https://python-poetaster.readthedocs.io/

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

0.1.1 (2016-09-21)
------------------

* First release with functional haiku extraction.

0.1.0dev1 (2016-07-27)
----------------------

* First release on PyPI.


