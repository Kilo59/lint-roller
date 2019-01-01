# -*- coding: utf-8 -*-
import pathlib
import shutil
from typing import Dict, Optional
import pytest

from lint_roller import utils as lr_utils

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


@pytest.fixture(scope="module")
def dirty_package():
    temp_pkg_path = lr_utils.package_maker("my_package")
    print(f"Package create at: {temp_pkg_path}")
    yield temp_pkg_path
    print("CLEANING UP DIRTY PACKAGE")
    shutil.rmtree(temp_pkg_path)


if __name__ == "__main__":
    print(TEST_ROOT)
    print(TEST_DOCS)
    print(lr_utils.package_maker("my_package"))
