# -*- coding: utf-8 -*-
"""
utils
~~~~~
lint-roller utility methods
"""
import pathlib
import re
from pprint import pprint as pp

# from pprint import pprint as pp
from typing import Dict, Optional, Union, List, Tuple
from py._path.local import LocalPath
from pylint import epylint

PKG_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
ROOT = PKG_ROOT.joinpath("..").resolve()
DEPOT = ROOT.joinpath("pkg_depot")
DATA = ROOT.joinpath("data")


def package_maker(
    pkg_name: str,
    pkg_content: Optional[Dict[str, str]] = None,
    new_pkg_path: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """Create the directory structure and source code for a Python package.

    Parameters
    ----------
    pkg_name
        Name of the package. Will be used as package directory name.
    pkg_content
        Dictionary of package module names and string of module source code as value
        (the default is None, which will use some boilerplate code in need of linting)
    new_pkg_path
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

    if not new_pkg_path:
        DEPOT.mkdir(exist_ok=True)
        new_pkg_path = pathlib.Path(DEPOT).joinpath(pkg_name)
    elif isinstance(new_pkg_path, (pathlib.Path, str, LocalPath)):
        new_pkg_path = pathlib.Path(new_pkg_path).resolve()
    else:
        raise TypeError("new_pkg_path should be Path object or path string")

    new_pkg_path.mkdir(exist_ok=True)
    init_path = new_pkg_path.joinpath("__init__.py")
    with init_path.open(mode="w") as f_out:
        f_out.write(f"# {pkg_name}/__init__ file")

    for name, content in pkg_content.items():
        module_path = new_pkg_path.joinpath(name)
        with module_path.open(mode="w") as f_out:
            f_out.write(content)
    return new_pkg_path


def write_file(
    filecontent: Union[str, List, Tuple],
    filename: Union[pathlib.Path, str],
    mode: Optional = "w",
) -> pathlib.Path:
    """Write to a file.

    Write a str or list of strings to a file.

    Parameters
    ----------
    filecontent : Union[str, List, Tuple]
        The content to be written. If a list or tuple, writelines() will be used,
        instead of write().
    filename : Union[pathlib.Path, str]
        The filename or path.
    mode : Optional, optional
        Write mode to use. (the default is "w")

    Returns
    -------
    pathlib.Path
        A path object of the newly written file.
    """
    filepath = pathlib.Path(filename)
    with open(filepath, mode=mode) as f_out:
        if isinstance(filecontent, (list, tuple)):
            f_out.writelines(filecontent)
        if isinstance(filecontent, str):
            f_out.write(filecontent)
    return filepath


def parse_pylint(pylint_output):
    if isinstance(pylint_output, (list, tuple)):
        pylint_output = "\n".join(pylint_output)
    print(type(pylint_output))
    path_match = r"(?P<path>.+\.py)"
    line_match = r"(?P<line>\d+)"
    full_match = r"(?P<path>.+\.py):(?P<line>\d+): (?P<type>\w+) \((?P<msg_id>[IRCWEF]\d+), (?P<symbol>[a-z-]+)"
    msgs = re.findall(full_match, pylint_output)
    pp(msgs)
    # result = re.search(r"\*{13} Module", pylint_output)
    # print(result)


def run_pylint(module_name: str):
    """Run pylint and collect lint errors messages.

    Parameters
    ----------
    module_name
        Module or package to run against.

    Returns
    -------
    str
        A string of the pylint results
    """
    (pylint_stdout, pylint_stderr) = epylint.py_run(module_name, True)
    # show pylint errors
    for i in pylint_stderr:
        print(i)

    return pylint_stdout.getvalue()


if __name__ == "__main__":
    package_maker("package_a")
    pylint_res = run_pylint("pkg_depot/package_a")
    parse_pylint(pylint_res)
    # write_file(pylint_res, "sample_pylint.txt")
