from __future__ import annotations

import os
import shutil
import stat
import subprocess
from contextlib import suppress
from pathlib import Path

import pytest
import sphinx
from seleniumbase import config as sb_config

if sphinx.version_info[:2] >= (7, 2):
    TESTS_ROOT = Path(__file__).resolve().parent
else:
    from sphinx.testing.path import path

    TESTS_ROOT = path(__file__).abspath().parent


pytest_plugins = ['sphinx.testing.fixtures']


def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


def delete(path: str | Path):
    path = Path(path).resolve()
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path, onerror=del_rw)
        else:
            try:
                path.unlink()
            except Exception:
                del_rw(None, path, None)


# @pytest.fixture(scope="session")
# def rootdir():
#     return TESTS_ROOT / "roots"


@pytest.fixture
def content(app):
    app.build()
    return app


@pytest.fixture
def outdir(app):
    return app.outdir


@pytest.fixture
def app_init_repo(make_app, app_params):
    """
    Initializes a git repo before returning the app.

    The files in the specified test root are converted into a git repo.
    For example, in a test root with folders: HEAD, HEAD~1, HEAD~2,
    the files in each folder are treated as a snapshot of a git repo at
    their respective revs.
    A git repo is created and in order:
    1. HEAD~2's files are moved to the parent and are commited
    2. HEAD~1's files are moved to the parent and are commited
    3. HEAD's files are moved to the parent and are commited


    Returns:
    app: Sphinx app; same as the `app` fixture
    """

    args, kwargs = app_params

    srcdir = None
    if 'srcdir' in kwargs:
        srcdir = kwargs['srcdir']
    elif 'buildername' in kwargs:
        srcdir = args[1]
    else:
        srcdir = args[0]

    print(srcdir)
    src_path = Path(srcdir)

    def git(*cmd: str):
        with suppress(subprocess.CalledProcessError):
            subprocess.check_output(
                (
                    'git',
                    '-c',
                    'user.name="sphinxext-linkcheckdiff test runner"',
                    '-c',
                    'user.email="NONE"',
                    *cmd,
                ),
                cwd=src_path,
            )

    git('init')

    src_item_paths = list(src_path.glob('*'))

    commits = []

    for item_path in src_item_paths:
        if not item_path.name.startswith('HEAD'):
            continue

        commit_num = None

        sq_idx = item_path.name.find('~')
        if sq_idx != -1:
            commit_num = int(item_path.name[sq_idx + 1 :])
        else:
            commit_num = 0

        commits.append((item_path, commit_num))

    commits.sort(key=lambda tup: tup[1], reverse=True)

    for commit in commits:
        files = list(src_path.glob('*'))

        for file in files:
            if file not in src_item_paths:
                delete(file)

        for file in (src_path / commit[0]).glob('*'):
            new_path = file.parent.parent / file.name
            file.rename(new_path)

        git('add', '.')
        for path in src_item_paths:
            git('rm', '--cached', '-r', path)

        git('commit', '-m', f'Apply {commit[0]}')

        delete(src_path / commit[0])

    return make_app(*args, **kwargs)


def pytest_configure(config):
    config.addinivalue_line('markers', 'sphinx')


def rel2url(outdir, path):
    return 'file://' + str((Path(outdir) / path).resolve())


@pytest.fixture(scope='session')
def sb_(request):
    """Same as the sb fixture but with a session scope"""
    from seleniumbase import BaseCase

    class BaseClass(BaseCase):
        def setUp(self):
            super().setUp()

        def tearDown(self):
            self.save_teardown_screenshot()
            super().tearDown()

        def base_method(self):
            pass

    sb = BaseClass('base_method')
    sb.setUp()
    sb._needs_tearDown = True
    sb_config._sb_node[request.node.nodeid] = sb
    yield sb
    if sb._needs_tearDown:
        sb.tearDown()
        sb._needs_tearDown = False


@pytest.fixture
def ensure_redirect(outdir, sb_):
    # outdir = app.outdir
    def _ensure_redirect(before: str, expected_after: str):
        before_url = rel2url(outdir, before)
        sb_.open(before_url)
        expected_after_path = Path(rel2url(outdir, expected_after))
        actual_after_path = Path(sb_.get_current_url())
        assert actual_after_path == expected_after_path

    return _ensure_redirect
