===================
sphinxext-rediraffe
===================

.. role:: code-py(code)
   :language: Python

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

Just add ``sphinxext.rediraffe`` to the extensions list in :file:`conf.py`,

.. code-block:: python

   extensions = [
      'sphinxext.rediraffe',
   ]

and set :confval:`rediraffe_redirects` to a dict or file of redirects.

Diff Checker
------------

The diff checker ensures that deleted or renamed files in your git repo
are in your redirects.

To run the diff checker:

1. Set :confval:`rediraffe_branch` and :confval:`rediraffe_redirects`
   in :file:`conf.py`.
2. Run the ``rediraffecheckdiff`` builder.

Auto Redirect builder
---------------------

The auto redirect builder can be used to automatically add renamed files
to your redirects file.
Simply run the ``rediraffewritediff`` builder.

To run the auto redirecter:

1. Set :confval:`rediraffe_branch` and :confval:`rediraffe_redirects`
   in :file:`conf.py`.
2. Run the ``rediraffewritediff`` builder.

Note: The auto redirect builder only works with a configuration file.

Note: Deleted files cannot be added to your redirects file automatically.


Options
=======

These values are placed in the :file:`conf.py` of your Sphinx project.

.. confval:: rediraffe_branch
   :type: :code-py:`str`
   :default: :code-py:`''`

   **Required** for the ``rediraffecheckdiff`` & ``rediraffewritediff`` builders.
   The branch or commit to diff against.

.. confval:: rediraffe_redirects
   :type: :code-py:`str | dict[str, str]`

   A filename or dict containing redirects.

.. confval:: rediraffe_template
   :type: :code-py:`str`
   :default: :code-py:`None`

   A jinja template to use to render the inserted redirecting files.
   If not specified, a default template will be used.
   This template will only be accessed after the html/htmldir builder is finished,
   meaning that this file may be generated as part of your build.

   Variables available to :confval:`!rediraffe_template`:

   ``from_file``
     the file being redirected as written in :confval:`rediraffe_redirects`.
   ``to_file``
     the destination file that from_file is redirected to as written in
     :confval:`rediraffe_redirects`.
   ``from_url``
     the path to ``from_url``'s html file (built by rediraffe) relative to the
     :confval:`!outdir`.
   ``to_url``
     the path to ``to_url``'s built html file relative to the :confval:`!outdir`.
   ``rel_url``
     the relative path from ``from_url`` to ``to_url``.

.. confval:: rediraffe_auto_redirect_perc
   :type: :code-py:`int`
   :default: :code-py:`100`

   Only used by the ``rediraffewritediff`` builder.
   The percentage as an integer representing the accuracy required before
   auto redirecting with the ``rediraffewritediff`` builder.

Example Config
==============

redirects only (file)
---------------------

:file:`conf.py`:

.. code-block:: python

   rediraffe_redirects = 'redirects.txt'

:file:`redirects.txt`:

.. code-block:: text

   # comments start with '#'
   'another file.rst' index.rst
   another2.rst "another file.rst"

Note: Filepaths can be wrapped in quotes (single or double).
This is especially useful for filepaths containing spaces.

redirects only (dict)
---------------------

:file:`conf.py`:

.. code-block:: python

   rediraffe_redirects = {
       'another.rst': 'index.rst',
       'another2.rst': 'another.rst',
   }

redirects + diff checker
------------------------

:file:`conf.py`:

.. code-block:: python

   rediraffe_redirects = 'redirects.txt'
   rediraffe_branch = 'main~1'

redirects with jinja template
-----------------------------

:file:`conf.py`:

.. code-block:: python

   rediraffe_redirects = 'redirects.txt'
   rediraffe_template = 'template.html'

:file:`template.html`:

.. code-block:: html

   <html>
     <body>
       <p>Your destination is {{to_url}}</p>
     </body>
   </html>

A complex example can be found at :file:`tests/roots/ext/`.

Testing
=======

Rediraffe uses pytest for testing.
To run tests:

1. Install this package
2. Install test dependencies

   .. code-block:: sh

      python -m pip install --group test

3. Navigate to the tests directory and run

   .. code-block:: sh

      python -m pytest --headless

The ``--headless`` flag ensures that a browser window does not open
during browser backed selenium testing.
