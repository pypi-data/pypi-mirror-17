Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|
|PyPI Downloads|

Overview
========

Merges custom data sets with OpenStreetMap polygons.

Setup
=====

Requirements
------------

-  Python 3.5+

Installation
------------

Install OSMerge with pip:

.. code:: sh

    $ pip install OSMerge

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/citizenlabsgr/osmerge.git
    $ cd osmerge
    $ python setup.py install

Usage
=====

After installation, the package can imported:

.. code:: sh

    $ python
    >>> import osmerge
    >>> osmerge.__version__

.. |Unix Build Status| image:: http://img.shields.io/travis/citizenlabsgr/osmerge/develop.svg
   :target: https://travis-ci.org/citizenlabsgr/osmerge
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/citizenlabsgr/osmerge/develop.svg
   :target: https://ci.appveyor.com/project/citizenlabsgr/osmerge
.. |Coverage Status| image:: http://img.shields.io/coveralls/citizenlabsgr/osmerge/develop.svg
   :target: https://coveralls.io/r/citizenlabsgr/osmerge
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/citizenlabsgr/osmerge.svg
   :target: https://scrutinizer-ci.com/g/citizenlabsgr/osmerge/?branch=develop
.. |PyPI Version| image:: http://img.shields.io/pypi/v/OSMerge.svg
   :target: https://pypi.python.org/pypi/OSMerge
.. |PyPI Downloads| image:: http://img.shields.io/pypi/dm/OSMerge.svg
   :target: https://pypi.python.org/pypi/OSMerge
