from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from conftest import TESTS_ROOT, rel2url
from sphinx.errors import ExtensionError

TYPE_CHECKING = False
if TYPE_CHECKING:
    from seleniumbase import BaseCase
    from sphinx.application import Sphinx


@pytest.fixture(scope='module')
def rootdir():
    return TESTS_ROOT / 'roots' / 'ext'


class TestExtHtml:
    @pytest.mark.sphinx('html', testroot='no_redirects')
    def test_no_redirects(self, app: Sphinx):
        app.build()
        assert app.statuscode == 0

    @pytest.mark.sphinx('html', testroot='simple')
    def test_simple(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('another.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='simple')
    def test_simple_rebuild(self, app_params, make_app, ensure_redirect):
        args, kwargs = app_params
        app = make_app(*args, **kwargs)
        if Path(app.outdir).exists():
            shutil.rmtree(Path(app.outdir))
        app.build()
        assert app.statuscode == 0
        app2 = make_app(*args, **kwargs)
        app2.build()
        assert app2.statuscode == 0
        ensure_redirect('another.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='no_cycle')
    def test_no_cycle(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('a.html', 'index.html')
        ensure_redirect('b.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='cycle')
    def test_cycle(self, app: Sphinx):
        with pytest.raises(ExtensionError):
            app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('html', testroot='nested')
    def test_nested(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof2.html', 'docs/folder2/f2.html')
        ensure_redirect('docs/folder2/toindex.html', 'index.html')
        ensure_redirect('totoindex.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='backslashes')
    def test_backslashes(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof2.html', 'docs/folder2/f2.html')
        ensure_redirect('docs/folder2/toindex.html', 'index.html')
        ensure_redirect('totoindex.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='dot_in_filename')
    def test_dot_in_filename(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('docs/x.y.z.html', 'docs/a.b.c.html')

    @pytest.mark.sphinx('html', testroot='mixed_slashes')
    def test_mixed_slashes(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof1.html', 'docs/folder1/f1.html')
        ensure_redirect('docs/folder1/tof2.html', 'docs/folder2/f2.html')
        ensure_redirect('docs/folder2/toindex.html', 'index.html')
        ensure_redirect('totoindex.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='link_redirected_twice')
    def test_link_redirected_twice(self, app: Sphinx):
        with pytest.raises(ExtensionError):
            app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('html', testroot='link_redirected_to_nonexistant_file')
    def test_link_redirected_to_nonexistant_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('html', testroot='existing_link_redirected')
    def test_existing_link_redirected(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('html', testroot='bad_rediraffe_file')
    def test_bad_rediraffe_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('html', testroot='no_rediraffe_file')
    def test_no_rediraffe_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 0
        assert 'rediraffe was not given redirects to process' in app._warning.getvalue()

    @pytest.mark.sphinx('html', testroot='redirect_from_deleted_folder')
    def test_redirect_from_deleted_folder(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('deletedfolder/another.html', 'index.html')
        ensure_redirect('deletedfolder/deletedfolder2/another.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='complex')
    def test_complex(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('a.html', 'e.html')
        ensure_redirect('b.html', 'e.html')
        ensure_redirect('c.html', 'e.html')
        ensure_redirect('d.html', 'e.html')
        ensure_redirect('f.html', 'e.html')
        ensure_redirect('g.html', 'e.html')
        ensure_redirect('h.html', 'e.html')

        ensure_redirect('i.html', 'j.html')

        ensure_redirect('k.html', 'l.html')

        ensure_redirect('m.html', 'o.html')
        ensure_redirect('n.html', 'o.html')

        ensure_redirect('q.html', 'z.html')
        ensure_redirect('r.html', 'z.html')
        ensure_redirect('s.html', 'z.html')
        ensure_redirect('t.html', 'z.html')
        ensure_redirect('u.html', 'z.html')
        ensure_redirect('v.html', 'z.html')
        ensure_redirect('w.html', 'z.html')
        ensure_redirect('x.html', 'z.html')
        ensure_redirect('y.html', 'z.html')
        ensure_redirect('F1/1.html', 'z.html')
        ensure_redirect('F1/2.html', 'z.html')
        ensure_redirect('F2/1.html', 'z.html')

        ensure_redirect('F5/F4/F3/F2/F1/1.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='complex_dict')
    def test_complex_dict(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('a.html', 'e.html')
        ensure_redirect('b.html', 'e.html')
        ensure_redirect('c.html', 'e.html')
        ensure_redirect('d.html', 'e.html')
        ensure_redirect('f.html', 'e.html')
        ensure_redirect('g.html', 'e.html')
        ensure_redirect('h.html', 'e.html')

        ensure_redirect('i.html', 'j.html')

        ensure_redirect('k.html', 'l.html')

        ensure_redirect('m.html', 'o.html')
        ensure_redirect('n.html', 'o.html')

        ensure_redirect('q.html', 'z.html')
        ensure_redirect('r.html', 'z.html')
        ensure_redirect('s.html', 'z.html')
        ensure_redirect('t.html', 'z.html')
        ensure_redirect('u.html', 'z.html')
        ensure_redirect('v.html', 'z.html')
        ensure_redirect('w.html', 'z.html')
        ensure_redirect('x.html', 'z.html')
        ensure_redirect('y.html', 'z.html')
        ensure_redirect('F1/1.html', 'z.html')
        ensure_redirect('F1/2.html', 'z.html')
        ensure_redirect('F2/1.html', 'z.html')

        ensure_redirect('F5/F4/F3/F2/F1/1.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='jinja')
    def test_jinja(self, app: Sphinx, sb_: BaseCase):
        app.build()
        assert app.statuscode == 0

        sb_.open(rel2url(app.outdir, 'another.html'))
        text = sb_.get_text(selector='html')
        text = text.replace('\\', '/')
        text = text.replace('//', '/')

        assert 'rel_url: index.html' in text
        assert 'from_file: another.rst' in text
        assert 'to_file: index.rst' in text
        assert 'from_url: another.html' in text
        assert 'to_url: index.html' in text

    @pytest.mark.sphinx('html', testroot='jinja_bad_path')
    def test_jinja_bad_path(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('another.html', 'index.html')

    @pytest.mark.sphinx('html', testroot='pass_url_fragments_queries')
    def test_pass_url_fragments(self, app: Sphinx, sb_: BaseCase, ensure_redirect):
        app.build()

        ensure_redirect('another.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another.html') + '#haha')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return  window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check hash
        assert '#haha' == sb_.execute_script('return window.location.hash')

    @pytest.mark.sphinx('html', testroot='pass_url_fragments_queries')
    def test_pass_url_queries(self, app: Sphinx, sb_: BaseCase, ensure_redirect):
        app.build()

        ensure_redirect('another.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another.html') + '?phrase=haha')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check query
        assert '?phrase=haha' == sb_.execute_script('return window.location.search')

    @pytest.mark.sphinx('html', testroot='pass_url_fragments_queries')
    def test_pass_url_fragment_and_query(
        self, app: Sphinx, sb_: BaseCase, ensure_redirect
    ):
        app.build()

        ensure_redirect('another.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another.html') + '?phrase=haha#giraffe')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check query
        assert '?phrase=haha' == sb_.execute_script('return window.location.search')
        # check hash
        assert '#giraffe' == sb_.execute_script('return window.location.hash')


class TestExtDirHtml:
    @pytest.mark.sphinx('dirhtml', testroot='no_redirects')
    def test_no_redirects(self, app: Sphinx):
        app.build()
        assert app.statuscode == 0

    @pytest.mark.sphinx('dirhtml', testroot='simple')
    def test_simple(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('another/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='dirhtml_user_index_files')
    def test_index_file_foldering(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('another/index.html', 'mydir/index.html')

    @pytest.mark.sphinx('dirhtml', testroot='simple', freshenv=False)
    def test_simple_rebuild(self, app_params, make_app, ensure_redirect):
        args, kwargs = app_params
        app = make_app(*args, **kwargs)
        if Path(app.outdir).exists():
            shutil.rmtree(Path(app.outdir))
        app.build()
        assert app.statuscode == 0
        app2 = make_app(*args, **kwargs)
        app2.build()
        assert app2.statuscode == 0
        ensure_redirect('another/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='no_cycle')
    def test_no_cycle(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('a/index.html', 'index.html')
        ensure_redirect('b/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='cycle')
    def test_cycle(self, app: Sphinx):
        with pytest.raises(ExtensionError):
            app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('dirhtml', testroot='nested')
    def test_nested(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof2/index.html', 'docs/folder2/f2/index.html')
        ensure_redirect('docs/folder2/toindex/index.html', 'index.html')
        ensure_redirect('totoindex/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='backslashes')
    def test_backslashes(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof2/index.html', 'docs/folder2/f2/index.html')
        ensure_redirect('docs/folder2/toindex/index.html', 'index.html')
        ensure_redirect('totoindex/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='dot_in_filename')
    def test_dot_in_filename(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('docs/x.y.z/index.html', 'docs/a.b.c/index.html')

    @pytest.mark.sphinx('dirhtml', testroot='mixed_slashes')
    def test_mixed_slashes(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0
        ensure_redirect('tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof1/index.html', 'docs/folder1/f1/index.html')
        ensure_redirect('docs/folder1/tof2/index.html', 'docs/folder2/f2/index.html')
        ensure_redirect('docs/folder2/toindex/index.html', 'index.html')
        ensure_redirect('totoindex/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='link_redirected_twice')
    def test_link_redirected_twice(self, app: Sphinx):
        with pytest.raises(ExtensionError):
            app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('dirhtml', testroot='link_redirected_to_nonexistant_file')
    def test_link_redirected_to_nonexistant_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('dirhtml', testroot='existing_link_redirected')
    def test_existing_link_redirected(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('dirhtml', testroot='bad_rediraffe_file')
    def test_bad_rediraffe_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 1

    @pytest.mark.sphinx('dirhtml', testroot='no_rediraffe_file')
    def test_no_rediraffe_file(self, app: Sphinx):
        app.build()
        assert app.statuscode == 0
        assert 'rediraffe was not given redirects to process' in app._warning.getvalue()

    @pytest.mark.sphinx('dirhtml', testroot='redirect_from_deleted_folder')
    def test_redirect_from_deleted_folder(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('deletedfolder/another/index.html', 'index.html')
        ensure_redirect('deletedfolder/deletedfolder2/another/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='complex')
    def test_complex(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('a/index.html', 'e/index.html')
        ensure_redirect('b/index.html', 'e/index.html')
        ensure_redirect('c/index.html', 'e/index.html')
        ensure_redirect('d/index.html', 'e/index.html')
        ensure_redirect('f/index.html', 'e/index.html')
        ensure_redirect('g/index.html', 'e/index.html')
        ensure_redirect('h/index.html', 'e/index.html')

        ensure_redirect('i/index.html', 'j/index.html')

        ensure_redirect('k/index.html', 'l/index.html')

        ensure_redirect('m/index.html', 'o/index.html')
        ensure_redirect('n/index.html', 'o/index.html')

        ensure_redirect('q/index.html', 'z/index.html')
        ensure_redirect('r/index.html', 'z/index.html')
        ensure_redirect('s/index.html', 'z/index.html')
        ensure_redirect('t/index.html', 'z/index.html')
        ensure_redirect('u/index.html', 'z/index.html')
        ensure_redirect('v/index.html', 'z/index.html')
        ensure_redirect('w/index.html', 'z/index.html')
        ensure_redirect('x/index.html', 'z/index.html')
        ensure_redirect('y/index.html', 'z/index.html')
        ensure_redirect('F1/1/index.html', 'z/index.html')
        ensure_redirect('F1/2/index.html', 'z/index.html')
        ensure_redirect('F2/1/index.html', 'z/index.html')

        ensure_redirect('F5/F4/F3/F2/F1/1/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='complex_dict')
    def test_complex_dict(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('a/index.html', 'e/index.html')
        ensure_redirect('b/index.html', 'e/index.html')
        ensure_redirect('c/index.html', 'e/index.html')
        ensure_redirect('d/index.html', 'e/index.html')
        ensure_redirect('f/index.html', 'e/index.html')
        ensure_redirect('g/index.html', 'e/index.html')
        ensure_redirect('h/index.html', 'e/index.html')

        ensure_redirect('i/index.html', 'j/index.html')

        ensure_redirect('k/index.html', 'l/index.html')

        ensure_redirect('m/index.html', 'o/index.html')
        ensure_redirect('n/index.html', 'o/index.html')

        ensure_redirect('q/index.html', 'z/index.html')
        ensure_redirect('r/index.html', 'z/index.html')
        ensure_redirect('s/index.html', 'z/index.html')
        ensure_redirect('t/index.html', 'z/index.html')
        ensure_redirect('u/index.html', 'z/index.html')
        ensure_redirect('v/index.html', 'z/index.html')
        ensure_redirect('w/index.html', 'z/index.html')
        ensure_redirect('x/index.html', 'z/index.html')
        ensure_redirect('y/index.html', 'z/index.html')
        ensure_redirect('F1/1/index.html', 'z/index.html')
        ensure_redirect('F1/2/index.html', 'z/index.html')
        ensure_redirect('F2/1/index.html', 'z/index.html')

        ensure_redirect('F5/F4/F3/F2/F1/1/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='jinja')
    def test_jinja(self, app: Sphinx, sb_: BaseCase):
        app.build()
        assert app.statuscode == 0

        sb_.open(rel2url(app.outdir, 'another/index.html'))
        text = sb_.get_text(selector='html')
        text = text.replace('\\', '/')
        text = text.replace('//', '/')

        assert 'rel_url: ../index.html' in text
        assert 'from_file: another.rst' in text
        assert 'to_file: index.rst' in text
        assert 'from_url: another/index.html' in text
        assert 'to_url: index.html' in text

    @pytest.mark.sphinx('dirhtml', testroot='jinja_bad_path')
    def test_jinja_bad_path(self, app: Sphinx, ensure_redirect):
        app.build()
        assert app.statuscode == 0

        ensure_redirect('another/index.html', 'index.html')

    @pytest.mark.sphinx('dirhtml', testroot='pass_url_fragments_queries')
    def test_pass_url_fragments(self, app: Sphinx, sb_: BaseCase, ensure_redirect):
        app.build()

        ensure_redirect('another/index.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another/index.html') + '#haha')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return  window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check hash
        assert '#haha' == sb_.execute_script('return window.location.hash')

    @pytest.mark.sphinx('dirhtml', testroot='pass_url_fragments_queries')
    def test_pass_url_queries(self, app: Sphinx, sb_: BaseCase, ensure_redirect):
        app.build()

        ensure_redirect('another/index.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another/index.html') + '?phrase=haha')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check query
        assert '?phrase=haha' == sb_.execute_script('return window.location.search')

    @pytest.mark.sphinx('dirhtml', testroot='pass_url_fragments_queries')
    def test_pass_url_fragment_and_query(
        self, app: Sphinx, sb_: BaseCase, ensure_redirect
    ):
        app.build()

        ensure_redirect('another/index.html', 'index.html')
        sb_.open(rel2url(app.outdir, 'another/index.html') + '?phrase=haha#giraffe')
        # check url
        assert Path(rel2url(app.outdir, 'index.html')) == Path(
            sb_.execute_script(
                'return window.location.protocol + "//" + window.location.host + "/" + window.location.pathname'
            )
        )
        # check query
        assert '?phrase=haha' == sb_.execute_script('return window.location.search')
        # check hash
        assert '#giraffe' == sb_.execute_script('return window.location.hash')
