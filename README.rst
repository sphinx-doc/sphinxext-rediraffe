===================
sphinxext-rediraffe
===================

.. image:: https://img.shields.io/pypi/v/sphinxext-rediraffe.svg
   :target: https://pypi.org/project/sphinxext-rediraffe/
   :alt: Package on PyPI

.. image:: https://github.com/sphinx-doc/sphinxext-rediraffe/actions/workflows/test.yml/badge.svg
   :target: https://github.com/sphinx-doc/sphinxext-rediraffe/actions
   :alt: Build Status

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

Sphinx extension to redirect files

.. image:: ./assets/rediraffe_logo.svg
   :align: center

This Sphinx extension redirects non-existent pages to working pages.
Rediraffe can also check that deleted or renamed files in your git repo
are redirected.

Rediraffe creates a graph of all specified redirects and traverses it
to point all internal urls to leaf urls.
This means that chained redirects will be resolved.
For example, if a config has 6 chained redirects, all 6 links will redirect
directly to the final link.
The end user will never experience more than 1 redirection.

Note: Rediraffe supports the html and dirhtml builders.

Installation
============

.. code-block:: sh

   python -m pip install sphinxext-rediraffe

Usage
=====

See the `documentation`_.

.. _documentation: https://sphinxext-rediraffe.readthedocs.io/en/latest/
