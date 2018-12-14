# -*- coding: utf-8 -*-
"""
utils
~~~~~
lint-roller utility methods
"""
import pathlib
import shutil
from typing import Dict, Optional
import pytest

PKG_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
ROOT = PKG_ROOT.joinpath("..").resolve()
DEPOT = ROOT.joinpath("pkg_depot")
DATA = ROOT.joinpath("data")


def package_maker(
    pkg_name: str,
    pkg_content: Optional[Dict[str, str]] = None,
    new_pkg_dir_path: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """Create the directory structure and source code for a Python package.

    Parameters
    ----------
    pkg_name
        Name of the package. Will be used as package directory name.
    pkg_content
        Dictionary of package module names and string of module source code as value
        (the default is None, which will use some boilerplate code in need of linting)
    new_pkg_dir_path
        Where to create the new package (the default is None, which will store it in a
        sibling directory called `pkg_depot/`)

    Returns
    -------
    pathlib.Path
        Path object of created python package
    """
    if not pkg_content:
        with open(DATA.joinpath("dirty_code.txt")) as f_in:
            code_content = f_in.read()
        pkg_content = {"__main__.py": code_content}
    elif not isinstance(pkg_content, dict):
        raise TypeError("pkg_content should be a dictionary")

    if not new_pkg_dir_path:
        DEPOT.mkdir(exist_ok=True)
        new_pkg_dir_path = pathlib.Path(DEPOT).joinpath(pkg_name)
    else:
        new_pkg_dir_path = pathlib.Path(new_pkg_dir_path).resolve()

    new_pkg_dir_path.mkdir(exist_ok=True)
    init_path = new_pkg_dir_path.joinpath("__init__.py")
    with init_path.open(mode="w") as f_out:
        f_out.write(f"# {pkg_name}/__init__ file")

    for name, content in pkg_content.items():
        module_path = new_pkg_dir_path.joinpath(name)
        with module_path.open(mode="w") as f_out:
            f_out.write(content)
    return new_pkg_dir_path
