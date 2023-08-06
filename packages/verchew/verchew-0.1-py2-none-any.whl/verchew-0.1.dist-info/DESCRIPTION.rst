Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|
|PyPI Downloads|

Overview
========

Verchew is an embeddable Python script to check the versions of your
project's system dependencies. Its only external dependency is a Python
interpreter, available on macOS and most linux-based operating systems.

Setup
=====

Requirements
------------

-  Python 2.7+ or Python 3.3+

Installation
------------

Install verchew with pip:

.. code:: sh

    $ pip install verchew

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/verchew.git
    $ cd verchew
    $ python setup.py install

Usage
=====

Create a configuration file (``.verchew``) with your project's system
dependencies:

.. code:: ini

    [Python]

    cli = python
    version = Python 3.5.

    [R]

    cli = R
    version = R version 3.

    [Redis]

    cli = redis-server
    version = Redis server v=3.2.

Run ``verchew`` to see if you have the right versions installed:

.. code:: sh

    $ verchew

    Checking for Python...

    $ python --version
    Python 3.5.0
    ✔ MATCHED: Python 3.5.

    Checking for R...

    $ R --version
    R version 3.3.1 (2016-06-21)
    ✔ MATCHED: R version 3.

    Checking for Redis...

    $ redis-server --version
    Redis server v=3.2.1 sha=00000000:0 malloc=libc bits=64 build=62a67eec83b28403
    ✔ MATCHED: Redis server v=3.2.

    Results: ✔ ✔ ✔

.. |Unix Build Status| image:: https://img.shields.io/travis/jacebrowning/verchew/develop.svg
   :target: https://travis-ci.org/jacebrowning/verchew
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/jacebrowning/verchew/develop.svg
   :target: https://ci.appveyor.com/project/jacebrowning/verchew
.. |Coverage Status| image:: https://img.shields.io/coveralls/jacebrowning/verchew/develop.svg
   :target: https://coveralls.io/r/jacebrowning/verchew
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/jacebrowning/verchew.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/verchew/?branch=develop
.. |PyPI Version| image:: https://img.shields.io/pypi/v/verchew.svg
   :target: https://pypi.python.org/pypi/verchew
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/verchew.svg
   :target: https://pypi.python.org/pypi/verchew

Revision History
================

0.1 (2016/10/17)
----------------

-  Initial release.


