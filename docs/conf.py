from __future__ import annotations

import sphinxext.rediraffe

copyright = (
    '2020, FIRST',
    '2025-%Y, the Sphinx developers',
)

version = release = sphinxext.rediraffe.__version__

master_doc = 'index'
project = 'sphinxext-rediraffe'

exclude_patterns = ['_build']

nitpicky = True

html_theme = 'furo'
html_logo = '../assets/rediraffe_logo_128.png'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinxext.rediraffe',
]

intersphinx_mapping = {
    'sphinx': ('https://www.sphinx-doc.org/', None),
}

rediraffe_redirects = {
    'other.rst': 'index.rst',
    'other2.rst': 'other.rst',
}
