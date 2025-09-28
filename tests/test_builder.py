from __future__ import annotations

import pytest
from conftest import TESTS_ROOT


@pytest.fixture(scope='module')
def rootdir():
    return TESTS_ROOT / 'roots' / 'builder'


@pytest.mark.sphinx('rediraffecheckdiff', testroot='file_changed')
def test_file_changed(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='deleted_file_redirected')
def test_builder_deleted_file_redirected(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='deleted_file_not_redirected')
def test_builder_deleted_file_not_redirected(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 1


@pytest.mark.sphinx('rediraffecheckdiff', testroot='renamed_file_redirected')
def test_builder_renamed_file_redirected(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='renamed_file_not_redirected')
def test_builder_renamed_file_not_redirected(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 1


@pytest.mark.sphinx('rediraffecheckdiff', testroot='link_redirected_to_chain')
def test_builder_link_redirected_to_chain(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='link_redirected_twice')
def test_builder_link_redirected_twice(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 1


@pytest.mark.sphinx('rediraffecheckdiff', testroot='bad_rediraffe_file')
def test_builder_bad_rediraffe_file(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 1


@pytest.mark.sphinx('rediraffecheckdiff', testroot='nested')
def test_builder_nested(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='backslashes')
def test_builder_backslashes(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='mixed_slashes')
def test_builder_mixed_slashes(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='deleted_file_redirected_commit')
def test_builder_deleted_file_redirected_commit(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0


@pytest.mark.sphinx('rediraffecheckdiff', testroot='deleted_file_not_redirected_commit')
def test_builder_deleted_file_not_redirected_commit(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 1


@pytest.mark.sphinx('rediraffecheckdiff', testroot='deleted_file_redirected_dict')
def test_builder_deleted_file_redirected_dict(app_init_repo):
    app_init_repo.build()
    assert app_init_repo.statuscode == 0
