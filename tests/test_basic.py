# -*- coding: utf-8 -*-
from pathlib import Path
import pytest
import lint_roller as lr


def test_basic_pkg_gen(tmpdir):
    """Ensure no errors when generating a package using defaults.
    Excluding custom package default
    TODO: parametrize with tmpdir and default dir"""
    assert isinstance(
        lr.utils.package_maker("my_test_pkg", new_pkg_dir_path=tmpdir), Path
    )


@pytest.mark.parametrize(
    "name,content,pkg_dir", [("bad_content_pkg", "not_a_dict", None)]
)
def test_basic_pkg_gen_bad_args(name, content, pkg_dir):
    with pytest.raises(TypeError):
        lr.utils.package_maker(name, content, pkg_dir)
