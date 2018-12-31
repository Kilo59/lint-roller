# -*- coding: utf-8 -*-
from pprint import pprint as pp
from pathlib import Path
import pytest
import lint_roller as lr
from lint_roller.utils import Auditor, silence


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


def test_basic_run_pylint_and_parse(tmpdir):
    """place holder test for running pylint"""
    pkg_path = lr.utils.package_maker("lint_target_pkg", new_pkg_path=tmpdir)
    pylint_result = Auditor.run_pylint(str(pkg_path))
    pp(pylint_result)
    assert Auditor.parse_pylint(pylint_result) is not None


def test_silencing_decorator(capsys):
    """Test the use of the lint_roller.utils @silence decorator"""
    output = "SHOW ME WHAT YOU GOT!"

    @silence
    def show_me_what_you_got():
        print(output)

    print("check12")
    capture_control = capsys.readouterr()
    assert capture_control.out == "check12\n"

    show_me_what_you_got()
    captured = capsys.readouterr()
    assert captured.out != f"{output}\n"

    print(capture_control.out)
    print(captured.out)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
