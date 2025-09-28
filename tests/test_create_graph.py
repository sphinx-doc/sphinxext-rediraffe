from __future__ import annotations

import pytest
from sphinx.errors import ExtensionError

from sphinxext.rediraffe import create_graph


def test_create_graph(tmp_path):
    path = tmp_path / 'rediraffe.txt'
    path.write_text(
        """
        a b
        c d
        d e
        """,
        encoding='utf-8',
    )
    graph = create_graph(path)
    assert graph == {
        'a': 'b',
        'c': 'd',
        'd': 'e',
    }


def test_create_graph_spacing(tmp_path):
    path = tmp_path / 'rediraffe.txt'
    path.write_text(
        """
        a  b
        c d
        d            e
        """,
        encoding='utf-8',
    )
    graph = create_graph(path)
    assert graph == {
        'a': 'b',
        'c': 'd',
        'd': 'e',
    }


def test_create_graph_link_redirected_twice(tmp_path):
    path = tmp_path / 'rediraffe.txt'
    path.write_text(
        """
        a b
        a c
        """,
        encoding='utf-8',
    )
    with pytest.raises(ExtensionError):
        create_graph(path)


def test_create_graph_link_redirected_lots(tmp_path):
    path = tmp_path / 'rediraffe.txt'
    path.write_text(
        """
        a b
        c d
        a c
        d e
        a q
        """,
        encoding='utf-8',
    )
    with pytest.raises(ExtensionError):
        create_graph(path)


class TestCreateGraphQuotes:
    def test_no_quotes(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            a b
            c d
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_single_quotes(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            'a' b
            c 'd'
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_both_single_quotes(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            'a' 'b'
            'c' 'd'
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_commented(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            # a comment
            a b
            c d
            # another comment
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_double_quotes(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            "a" b
            c "d"
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_both_double_quotes(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            "a" "b"
            "c" "d"
            d e
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'a': 'b',
            'c': 'd',
            'd': 'e',
        }

    def test_quote_in_path(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            "a b
            c d'
            d "e
            "e' f'"
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            '"a': 'b',
            'c': "d'",
            'd': '"e',
            '"e\'': 'f\'"',
        }

    def test_complex(self, tmp_path):
        path = tmp_path / 'rediraffe.txt'
        path.write_text(
            """
            "Double Quoted Path" 'Single Quoted Path'
            "Website's Contents" "other"
            'Store's Contents' other
            "quoteskept' "other"
            ""I'm ready! I'm ready!" - Spongebob Squarepants.rst" "just why?.rst"
            """,
            encoding='utf-8',
        )
        graph = create_graph(path)
        assert graph == {
            'Double Quoted Path': 'Single Quoted Path',
            "Website's Contents": 'other',
            "Store's Contents": 'other',
            '"quoteskept\'': 'other',
            '"I\'m ready! I\'m ready!" - Spongebob Squarepants.rst': 'just why?.rst',
        }
