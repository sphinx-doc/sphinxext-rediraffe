from __future__ import annotations

import pytest
from sphinx.errors import ExtensionError

from sphinxext.rediraffe import create_simple_redirects


def test_create_simple_redirects_empty():
    assert create_simple_redirects({}) == {}


def test_create_simple_redirects_no_cycle():
    simple_redirects = redirects = {
        'a': 'b',
    }
    assert create_simple_redirects(redirects) == simple_redirects


def test_create_simple_redirects_simple_cycle():
    redirects = {
        'a': 'b',
        'b': 'a',
    }

    with pytest.raises(ExtensionError):
        create_simple_redirects(redirects)


def test_create_simple_redirects_complex_cycles():
    redirects = {
        'a': 'b',
        'b': 'c',
        'c': 'd',
        'd': 'e',
        'e': 'a',
    }

    with pytest.raises(ExtensionError):
        create_simple_redirects(redirects)


def test_create_simple_redirects_multiple_cycles():
    redirects = {
        'a': 'b',
        'b': 'c',
        'c': 'd',
        'd': 'e',
        'e': 'a',
        'f': 'g',
        'g': 'h',
        'h': 'j',
        'j': 'g',
    }

    with pytest.raises(ExtensionError):
        create_simple_redirects(redirects)


def test_create_simple_redirects_no_chains():
    simple_redirects = redirects = {
        'a': 'b',
        'c': 'd',
        'e': 'f',
    }
    assert create_simple_redirects(redirects) == simple_redirects


def test_create_simple_redirects_chain():
    redirects = {
        'a': 'b',
        'b': 'c',
        'c': 'd',
    }

    simple_redirects = {
        'a': 'd',
        'b': 'd',
        'c': 'd',
    }
    assert create_simple_redirects(redirects) == simple_redirects


def test_create_simple_redirects_mixed_chains():
    redirects = {
        'a': 'b',
        'b': 'c',
        'c': 'd',
        'e': 'f',
        'g': 'h',
        'h': 'i',
    }

    simple_redirects = {
        'a': 'd',
        'b': 'd',
        'c': 'd',
        'e': 'f',
        'g': 'i',
        'h': 'i',
    }
    assert create_simple_redirects(redirects) == simple_redirects
