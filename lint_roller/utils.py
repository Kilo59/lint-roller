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
DATA = ROOT.joinpath("data")


def package_maker(
    pkg_name: str,
    pkg_content: Optional[Dict] = None,
    new_pkg_dir_path: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """Create the directory structure and source code for a Python package.

    Parameters
    ----------
    pkg_name : str
        [description]
    pkg_content : Optional[Dict], optional
        [description] (the default is None, which [default_description])
    new_pkg_dir_path : Optional[pathlib.Path, str], optional
        [description] (the default is None, which [default_description])

    Returns
    -------
    pathlib.Path
        Path object of created python package
    """
    if not pkg_content:
        with open(DATA.joinpath("dirty_code.txt")) as f_in:
            code_content = f_in.read()
        pkg_content = {"__main__.py": code_content}

    if not new_pkg_dir_path:
        new_pkg_dir_path = pathlib.Path(ROOT).joinpath(pkg_name)
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
