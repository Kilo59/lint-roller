# -*- coding: utf-8 -*-
from pprint import pprint as pp
from pathlib import Path
import pytest
import lint_roller as lr


def test_basic_pkg_gen(tmpdir):
    """Ensure no errors when generating a package using defaults.
    Excluding custom package default
    TODO: parametrize with tmpdir and default dir"""
    print(type(tmpdir))
    assert isinstance(lr.utils.package_maker("my_test_pkg", new_pkg_path=tmpdir), Path)


@pytest.mark.parametrize(
    "name,content,pkg_dir",
    [("bad_content_pkg", "not_a_dict", None), ("bad_path_pkg", None, 123)],
)
def test_basic_pkg_gen_bad_args(name, content, pkg_dir):
    """Test type checking"""
    with pytest.raises(TypeError):
        lr.utils.package_maker(name, content, pkg_dir)


@pytest.mark.parametrize("content", ["ABC", list("ABC")])
def test_writing_file(tmpdir, content):
    """Ensure no errors when writing file"""
    lr.utils.write_file(content, tmpdir.join("abc.txt"))


def test_basic_run_pylint(tmpdir):
    """place holder test for running pylint"""
    pkg_path = lr.utils.package_maker("lint_target_pkg", new_pkg_path=tmpdir)
    pylint_result = lr.utils.run_pylint(str(pkg_path))
    pp(pylint_result)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
