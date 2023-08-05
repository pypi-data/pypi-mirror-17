========
Overview
========

Low-pressure bar graphs for Python.

Features
========

* Safe: Object is thread-safe and parameters are type-checked.
* Friendly: Raises human-readable errors.
* Tested: Package has good test coverage.
* Customizable: Constructor takes custom bar characters.
* Free software: Published under a OSI-compatible license.
* Compatible: Runs on multiple versions of CPython and PyPy.
* Convenient: Package installable from PyPI via pip.

Status
======

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |landscape| |scrutinizer|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|


.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
      :target: https://readthedocs.org/projects/microbar/
      :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Bengt/microbar.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Bengt/microbar

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/bengt/microbar?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/bengt/microbar

.. |requires| image:: https://requires.io/github/Bengt/microbar/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Bengt/microbar/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/bengt/microbar/branch/master/graph/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/gh/bengt/microbar

.. |landscape| image:: https://landscape.io/github/Bengt/microbar/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Bengt/microbar/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/microbar.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/microbar

.. |downloads| image:: https://img.shields.io/pypi/dm/microbar.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/microbar

.. |wheel| image:: https://img.shields.io/pypi/wheel/microbar.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/microbar

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/microbar.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/microbar

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/microbar.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/microbar

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/Bengt/microbar/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Bengt/microbar/


.. end-badges

Installation
============

::

    pip install microbar

Documentation
=============

https://microbar.readthedocs.io/en/latest/

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

Releasing
=========

::

    bumpversion --new-version 0.2.0 minor
    python setup.py sdist bdist_wheel upload
