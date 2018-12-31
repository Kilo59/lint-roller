# -*- coding: utf-8 -*-
"""
utils
~~~~~
lint-roller utility methods
"""
import pathlib
import shutil
import re
import csv
import collections
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime
from pprint import pprint as pp

# from pprint import pprint as pp
from typing import Dict, Optional, Union, List, Tuple
from py._path.local import LocalPath
from pylint import epylint
import black

PKG_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
ROOT = PKG_ROOT.joinpath("..").resolve()


def silence(fn):
    def silent_function(*args, **kwargs):
        with redirect_stdout(StringIO()):
            result = fn(*args, **kwargs)
        return result

    return silent_function


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
        with open(Auditor.DATA.joinpath("dirty_code.txt")) as f_in:
            code_content = f_in.read()
        pkg_content = {"__main__.py": code_content}
    elif not isinstance(pkg_content, dict):
        raise TypeError("pkg_content should be a dictionary")

    if not new_pkg_path:
        Auditor.DEPOT.mkdir(exist_ok=True)
        new_pkg_path = pathlib.Path(Auditor.DEPOT).joinpath(pkg_name)
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


def file_tree(directory, glob_pattern="*", verbose=True):
    if verbose:
        print(f"+ {directory}")
    matched_paths = []
    for path in sorted(directory.rglob(glob_pattern)):
        matched_paths.append(path)
        depth = len(path.relative_to(directory).parts)
        spacer = "    " * depth
        if verbose:
            print(f"{spacer}+ {path.name}")
    return matched_paths


class Auditor:
    """Methods for assessing and tracking pylint messages over time."""

    DATA = ROOT.joinpath("data")
    DEPOT = ROOT.joinpath("pkg_depot")

    def __init__(self, target):
        self._target = target
        self._ledger = {}
        self.line_length = 79
        self.check_records()

    @classmethod
    def check_depot(cls, full_path=False):
        pkgs_paths = [pkg for pkg in sorted(cls.DEPOT.glob("*"))]
        if pkgs_paths is None:
            print("Depot empty...")
            return None
        if not full_path:
            return [pkg.stem for pkg in pkgs_paths]
        return pkgs_paths

    @classmethod
    def empty_depot(cls, response=""):
        print("Package Depot\n=============")
        depot_pkgs = cls.check_depot(full_path=True)
        for pkg_path in depot_pkgs:
            print(f"  {pkg_path.stem}")

        if not response:
            response = input("Are you sure you want to empty the package depot?\n(Y/N)")
        if response.upper() == "Y":
            packages_deleted = len([shutil.rmtree(pkg_path) for pkg_path in depot_pkgs])
            print(f"{packages_deleted}: Depot emptied...\n")
            return packages_deleted
        print("Operation cancelled...\n")
        return 0

    @classmethod
    def delete_audit_recods(cls, response=""):
        print("Audit Records\n=============")
        audit_records = file_tree(cls.DATA, glob_pattern=f"audit__*.csv", verbose=False)
        for pkg_path in audit_records:
            print(f"  {pkg_path.stem}")

        if not response:
            response = input("Are you sure you want to clear all audit records?\n(Y/N)")
        if response.upper() == "Y":
            records_purged = len([record.unlink() for record in audit_records])
            print(f"{records_purged}: Records purged...\n")
            return records_purged
        print("Operation cancelled...\n")
        return 0

    @classmethod
    def _complete_purge(cls, response=""):
        msg = "Purge All Records and stored Packages"
        print(f"{msg}\n{'=' * len(msg)}")

        empty_depot_silent = silence(Auditor.empty_depot)
        delete_audit_recods_silent = silence(Auditor.delete_audit_recods)

        if not response:
            response = input("Purge all audit records and stored packages?\n(Y/N)")
        if response.upper() == "Y":
            pkgs = empty_depot_silent(response="Y")
            records = delete_audit_recods_silent(response="Y")
            print(f"Packages:\t{pkgs}\nAudit Records:\t{records}")
            print("  PURGED!\n")

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
            self._ledger.update(ledger_dict)
            print(f"  Updating {self.target.stem} ledger!")
            print(ledger_dict, end="\n\n")
        else:
            raise TypeError("ledger must be a dictionary.")

    def check_records(self):
        # access class attribute
        audit_file = type(self).DATA.joinpath(f"audit__{self.target.stem}.csv")
        if audit_file.exists():
            print("  Audit records found!")
            with open(audit_file, newline="") as csv_in:
                reader = csv.DictReader(csv_in)
                all_dates = [row["date"] for row in reader]
            self.ledger = dict(collections.Counter(all_dates))
        else:
            print("  No Audit records found!")

    @staticmethod
    def datestamp(compact=True):
        # YYYY-MM-DDTHH:MM
        stamp = datetime.today().isoformat().split(".")[0][:-3]
        if compact:
            # YY-MM-DD
            return stamp[2:-6]
        return stamp

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

        full_match = r"(?P<path>[A-z/\\]+\.py):(?P<line>\d+): (?P<type>\w+) \((?P<msg_id>[IRCWEF]\d+), (?P<symbol>[a-z-]+)"
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
        pylint_stdout, pylint_stderr = epylint.py_run(module_name, True)
        # show pylint errors
        for i in pylint_stderr:
            print(i)

        return pylint_stdout.getvalue()

    def export(self):
        # TODO: breakup audit(commit=False), export()?
        # `if not commit` do you want to commit the audit?
        # export to csv/json based on .ext
        # csv by default
        print(self.target)
        lint_res = Auditor.parse_pylint(Auditor.run_pylint(str(self.target)))
        # pp(lint_res[:5], width=100)
        date = Auditor.datestamp(compact=False)
        lint_msgs = len(lint_res)
        # print(DATESTAMP, LINT_MSGS)
        self.ledger = {date: lint_msgs}
        result_table = []
        for lint_tuple in lint_res:
            result_table.append(
                {
                    "path": lint_tuple[0],
                    "line": lint_tuple[1],
                    "type": lint_tuple[2],
                    "msg_id": lint_tuple[3],
                    "symbol": lint_tuple[4],
                    "date": date,
                }
            )
        # TODO: remove
        # pp(result_table[:5])
        audit_filepath = pathlib.Path(f"data/audit__{self.target.stem}.csv")
        audit_file_exits = audit_filepath.exists()
        with open(audit_filepath, "a", newline="") as csv_out:
            fieldnames = ("path", "line", "type", "msg_id", "symbol", "date")
            writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            if not audit_file_exits:
                writer.writeheader()
            writer.writerows(result_table)

    def remediation(self):
        "  Formatting files..."
        for src_file in file_tree(self.target, "*.py"):
            black.format_file_in_place(
                src_file, self.line_length, False, write_back=black.WriteBack.YES
            )


if __name__ == "__main__":
    print(Auditor.check_depot())
    Auditor.datestamp()
    # print(Auditor.empty_depot())
    # print(Auditor.check_depot())
    package_maker("package_a")
    Auditor.parse_pylint(Auditor.run_pylint("pkg_depot/package_a"))
    test_auditor = Auditor("pkg_depot/package_a")
    test_auditor.remediation()
    test_auditor.export()
    # print(test_auditor.ledger)
