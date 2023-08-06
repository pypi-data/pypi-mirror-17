==========
 DataCite
==========

.. image:: https://travis-ci.org/inveniosoftware/datacite.svg?branch=master
   :target: https://travis-ci.org/inveniosoftware/datacite
.. image:: https://coveralls.io/repos/inveniosoftware/datacite/badge.svg?branch=master
   :target: https://coveralls.io/r/inveniosoftware/datacite?branch=master
.. image:: https://pypip.in/v/datacite/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/datacite/
.. image:: https://pypip.in/d/datacite/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/datacite/


About
=====

Python API wrapper for the DataCite Metadata Store API and DataCite XML
generation.


Installation
============
The datacite package is on PyPI so all you need is: ::

    pip install datacite


Documentation
=============

Documentation is readable at http://pythonhosted.org/datacite/ or can be
built using Sphinx: ::

    pip install datacite[docs]
    python setup.py build_sphinx


Testing
=======
Running the test suite is as simple as: ::

    pip install -e .[all]
    ./run-tests.sh


Changes
=======

Version v0.2.2 (released 2016-09-23):

- Fixes issue with generated order of nameIdentifier and affiliation tags.

Version v0.2.1 (released 2016-03-29):

- Fixes issue with JSON schemas not being included when installing from PyPI.

Version v0.2.0 (released 2016-03-21):

- Adds DataCite XML generation support.

Version 0.1 (released 2015-02-25):

- Initial public release.


