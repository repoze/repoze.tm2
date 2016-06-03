repoze.tm2 (Transaction Manager)
================================

.. image:: https://travis-ci.org/repoze/repoze.tm2.png?branch=master
        :target: https://travis-ci.org/repoze/repoze.tm2

.. image:: https://readthedocs.org/projects/repozetm2/badge/?version=latest
        :target: http://repozetm2.readthedocs.org/en/latest/ 
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/repoze.tm2.svg
        :target: https://pypi.python.org/pypi/repoze.tm2

.. image:: https://img.shields.io/pypi/pyversions/repoze.tm2.svg
        :target: https://pypi.python.org/pypi/repoze.tm2

Middleware which uses the ZODB transaction manager to wrap a call to
its pipeline children inside a transaction.  This is a fork of the
``repoze.tm`` package which depends only on the ``transaction``
package rather than the entirety of ZODB (for users who don't rely on ZODB).
