# -*- coding: utf-8 -*-
import pathlib
import shutil
from typing import Dict, Optional
import pytest

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


def package_maker(pkg_name: str, pkg_content: Optional[Dict] = None):
    if not pkg_content:
        with open(TEST_DOCS.joinpath("dirty_code.txt")) as f_in:
            code_content = f_in.read()
        pkg_content = {"__main__.py": code_content}

    pkg_dir = pathlib.Path(TEST_ROOT).joinpath(pkg_name)
    pkg_dir.mkdir(exist_ok=True)
    init_path = pkg_dir.joinpath("__init__.py")
    with init_path.open(mode="w") as f_out:
        f_out.write(f"# {pkg_name}/__init__ file")

    for name, content in pkg_content.items():
        module_path = pkg_dir.joinpath(name)
        with module_path.open(mode="w") as f_out:
            f_out.write(content)
    return pkg_dir


@pytest.fixture(scope="module")
def dirty_package():
    temp_pkg_path = package_maker("pkg_a")
    print("Yielded...")
    yield temp_pkg_path
    print("CLEANING UP DIRTY PACKAGE")
    shutil.rmtree(temp_pkg_path)


if __name__ == "__main__":
    print(TEST_ROOT)
    print(TEST_DOCS)
    print(package_maker("pkg_a"))
