from __future__ import annotations

import time
from pathlib import Path

import pytest
from conftest import TESTS_ROOT, rel2url

TYPE_CHECKING = False
if TYPE_CHECKING:
    from sphinx.application import Sphinx


@pytest.fixture(scope='module')
def rootdir():
    return TESTS_ROOT / 'roots' / 'ext'


def wait_for_url(sb, expected: str, timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if Path(sb.get_current_url()) == Path(expected):
            return
        time.sleep(0.1)
    assert Path(sb.get_current_url()) == Path(expected)


class TestAnchorMap:
    @pytest.mark.sphinx('html', testroot='anchormap')
    def test_page_output(self, app: Sphinx):
        app.build()
        assert app.statuscode == 0

        outdir = Path(app.outdir)
        old_page = (outdir / 'old.html').read_text(encoding='utf-8')
        assert (
            '<script id="rediraffe-anchormap" type="application/json">'
            '{"removed-anchor": "index.html#new-home",'
            ' "some-content": "index.html#new-home"}</script>'
        ) in old_page
        assert 'src="_static/rediraffe_anchormap.js"' in old_page
        assert (outdir / '_static' / 'rediraffe_anchormap.js').is_file()

        # The directive itself produces no visible output.
        assert 'plain text without a link' not in old_page

        # Pages without an anchormap should not get the scripts.
        index_page = (outdir / 'index.html').read_text(encoding='utf-8')
        assert 'rediraffe-anchormap' not in index_page
        assert 'rediraffe_anchormap' not in index_page

    @pytest.mark.sphinx('html', testroot='anchormap')
    def test_anchor_is_redirected(self, app: Sphinx, sb_):
        app.build()
        assert app.statuscode == 0

        sb_.open(rel2url(app.outdir, 'old.html') + '#removed-anchor')
        wait_for_url(sb_, rel2url(app.outdir, 'index.html') + '#new-home')

    @pytest.mark.sphinx('html', testroot='anchormap')
    def test_existing_anchor_is_not_redirected(self, app: Sphinx, sb_):
        app.build()
        assert app.statuscode == 0

        # 'some-content' is in the anchormap but its anchor still exists,
        # so the existing anchor must win.
        before = rel2url(app.outdir, 'old.html') + '#some-content'
        sb_.open(before)
        time.sleep(0.5)
        assert Path(sb_.get_current_url()) == Path(before)
