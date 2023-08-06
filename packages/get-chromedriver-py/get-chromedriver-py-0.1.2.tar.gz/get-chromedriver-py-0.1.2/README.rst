===================
get-chromedriver-py
===================
Get `chromedriver-py <https://pypi.org/project/chromedriver-py/>`__
version most suitable for your system.

For instance, you could use it with GitHub Actions to match
installed ``Chromium`` browser version with most suitable version
of ``chromedriver-py``.

See the documentation for more information on what is provided.

.. image:: https://img.shields.io/pypi/v/get-chromedriver-py.svg
   :target: https://pypi.python.org/pypi/get-chromedriver-py
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/get-chromedriver-py.svg
    :target: https://pypi.python.org/pypi/get-chromedriver-py/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/get-chromedriver-py/workflows/test/badge.svg
   :target: https://github.com/barseghyanartur/get-chromedriver-py/actions?query=workflow%3Atest
   :alt: Build Status

.. image:: https://readthedocs.org/projects/get-chromedriver-py/badge/?version=latest
    :target: http://get-chromedriver-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/get-chromedriver-py/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/get-chromedriver-py/badge.svg?branch=main
    :target: https://coveralls.io/github/barseghyanartur/get-chromedriver-py?branch=main
    :alt: Coverage

Documentation
=============
Documentation is available on `Read the Docs
<http://get-chromedriver-py.readthedocs.io/>`_.

Prerequisites
=============
- Python 3.7, 3.8, 3.9, 3.10 and 3.11.

Installation
============
Install latest stable version from PyPI:

.. code-block:: sh

    pip install get-chromedriver-py

Or latest stable version from GitHub:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/get-chromedriver-py/archive/main.tar.gz

Usage
=====
.. code-block:: sh

    get-chromedriver

Or run it in a very verbose mode:

.. code-block:: sh

    get-chromedriver -vvvv

Testing
=======
Project is covered with tests.

To test with all supported Python versions type:

.. code-block:: sh

    tox

To test against specific environment, type:

.. code-block:: sh

    tox -e py39

To test just your working environment type:

.. code-block:: sh

    pytest

To run a single test in your working environment type:

.. code-block:: sh

    pytest test_get_chromedriver.py

To run a single test class in a given test module in your working environment
type:

.. code-block:: sh

    pytest test_get_chromedriver.py::GetChromedriverTestCase

It's assumed that you have `chromium` browser installed. If not, install it
first.

Writing documentation
=====================
Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
MIT

Support
=======
For any security issues contact me at the e-mail given in the `Author`_ section.
For overall issues, go to `GitHub <https://github.com/get-chromedriver-py/anysearch/issues>`_.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
