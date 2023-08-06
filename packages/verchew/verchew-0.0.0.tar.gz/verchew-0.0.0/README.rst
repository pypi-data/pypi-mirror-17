Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|
|PyPI Downloads|

Overview
========

This is an embeddable Python script to check the versions of your system
dependencies.

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

After installation, the package can imported:

.. code:: sh

    $ python
    >>> import verchew
    >>> verchew.__version__

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
