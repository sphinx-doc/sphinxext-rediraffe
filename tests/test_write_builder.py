from __future__ import annotations

import pytest
from conftest import TESTS_ROOT


@pytest.fixture(scope='module')
def rootdir():
    return TESTS_ROOT / 'roots' / 'builder'


@pytest.mark.sphinx('rediraffewritediff', testroot='renamed_write_file_not_redirected')
def test_builder_renamed_file_write_not_redirected(app_init_repo):
    app_init_repo.build()
    valid_string = '"another.rst" "another2.rst"'
    redirects_text = (app_init_repo.srcdir / 'redirects.txt').read_text(
        encoding='utf-8'
    )
    assert valid_string in redirects_text


@pytest.mark.sphinx('rediraffewritediff', testroot='renamed_write_file_perc_low_fail')
def test_builder_renamed_file_write_perc_low_fail(app_init_repo):
    app_init_repo.build()
    valid_string = '"another.rst" "another2.rst"'
    redirects_text = (app_init_repo.srcdir / 'redirects.txt').read_text(
        encoding='utf-8'
    )
    assert valid_string not in redirects_text


@pytest.mark.sphinx('rediraffewritediff', testroot='renamed_write_file_perc_low_pass')
def test_builder_renamed_file_write_perc_low_pass(app_init_repo):
    app_init_repo.build()
    valid_string = '"another.rst" "another2.rst"'
    redirects_text = (app_init_repo.srcdir / 'redirects.txt').read_text(
        encoding='utf-8'
    )
    assert valid_string in redirects_text
