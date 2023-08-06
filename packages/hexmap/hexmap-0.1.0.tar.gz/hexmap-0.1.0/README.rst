========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/hexmap/badge/?style=flat
    :target: https://readthedocs.org/projects/hexmap
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tmacro/hexmap.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tmacro/hexmap

.. |coveralls| image:: https://coveralls.io/repos/tmacro/hexmap/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/tmacro/hexmap

.. |version| image:: https://img.shields.io/pypi/v/hexmap.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/hexmap

.. |downloads| image:: https://img.shields.io/pypi/dm/hexmap.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/hexmap

.. |wheel| image:: https://img.shields.io/pypi/wheel/hexmap.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/hexmap

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/hexmap.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/hexmap

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/hexmap.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/hexmap


.. end-badges

A library for hexagonal grid storage and manipulation.

* Free software: BSD license

Installation
============

::

    pip install hexmap

Documentation
=============

https://hexmap.readthedocs.io/

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
