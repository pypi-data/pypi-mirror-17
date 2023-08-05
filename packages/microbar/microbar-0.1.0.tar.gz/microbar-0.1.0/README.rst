========
Overview
========

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

.. |docs| image:: https://readthedocs.org/projects/microbar/badge/?style=flat
    :target: https://readthedocs.org/projects/microbar
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/bengt/microbar.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/bengt/microbar

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/bengt/microbar?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/bengt/microbar

.. |requires| image:: https://requires.io/github/bengt/microbar/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/bengt/microbar/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/bengt/microbar/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/bengt/microbar

.. |landscape| image:: https://landscape.io/github/bengt/microbar/master/landscape.svg?style=flat
    :target: https://landscape.io/github/bengt/microbar/master
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

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/bengt/microbar/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/bengt/microbar/


.. end-badges

Low-pressure bar graphs for Python.

* Free software: BSD license

Installation
============

::

    pip install microbar

Documentation
=============

https://microbar.readthedocs.io/

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
