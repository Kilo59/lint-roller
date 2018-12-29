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


class Auditor:
    """Methods for assessing and tracking pylint messages over time."""

    def __init__(self, target):
        self._target = target
        self._ledger = None

    @property
    def target(self):
        target_path = pathlib.Path(self._target)
        if target_path.exists():
            return pathlib.Path(self._target)
        raise FileNotFoundError(f"Could not locate {self._target}")

    @property
    def ledger(self):
        return self._ledger

    @ledger.setter
    def ledger(self, ledger_dict):
        if isinstance(ledger_dict, dict):
            self._ledger = ledger_dict
            print(f"Updating {self.target.stem} ledger!")
        else:
            raise TypeError("ledger must be a dictionary.")

    @staticmethod
    def parse_pylint(pylint_output: Union[str, List, Tuple]) -> List:
        """parse the output of pylint and capture details.

        Assumes the default pylint format is being used.

        Note
        ----
        The format of each message tuple:
        (path, line, type, msg_id, symbol)

        Parameters
        ----------
        pylint_output : Union[str, List, Tuple]
            A single string or collection of strings containing pylint default output.

        Returns
        -------
        list
            List of pylint message detail tuples.
        """
        if isinstance(pylint_output, (list, tuple)):
            pylint_output = "\n".join(pylint_output)

        full_match = r"(?P<path>.+\.py):(?P<line>\d+): (?P<type>\w+) \((?P<msg_id>[IRCWEF]\d+), (?P<symbol>[a-z-]+)"
        find_res = re.findall(full_match, pylint_output)
        return find_res

    @staticmethod
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

    def export(self):
        # export to csv/json based on .ext
        # csv by default
        print(self.target)
        lint_res = Auditor.parse_pylint(Auditor.run_pylint(str(self.target)))
        print(len(lint_res))


if __name__ == "__main__":
    package_maker("package_a")
    Auditor.parse_pylint(Auditor.run_pylint("pkg_depot/package_a"))
    test_auditor = Auditor("pkg_depot/package_a")
    test_auditor.export()
