# -*- coding: utf-8 -*-
import subprocess
import pathlib
import pytest

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


def test_cli_lint_task_simple():
    cmplt_process = subprocess.run(["lint-roller", "lint"])
    print(cmplt_process.stdout)
    assert cmplt_process.stderr is None


if __name__ == "__main__":
    pytest.main(["-v", __file__])
