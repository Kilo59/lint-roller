# -*- coding: utf-8 -*-
import pathlib
import shutil
import pytest

import lint_roller as lr

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


def test_end_to_end():
    package_name = "package_abc"
    audit_file = lr.Auditor.DATA.joinpath(f"audit__{package_name}.csv")
    package_path = pathlib.Path(package_name)

    print(lr.Auditor.check_depot())
    lr.Auditor.datestamp()
    # print(Auditor.empty_depot())
    # print(Auditor.check_depot())
    lr.utils.package_maker(package_name, new_pkg_path=package_path)
    lr.Auditor.parse_pylint(lr.Auditor.run_pylint(str(package_path)))
    test_auditor = lr.Auditor(package_path)
    test_auditor.remediation()
    test_auditor.export()

    shutil.rmtree(package_path)
    audit_file.unlink()


@pytest.mark.xfail()
def test_simple_audit():
    """Placeholder test for future behavior that should produce a useable result"""
    pkg_a_auditor = lr.Auditor("package_a")
    pkg_a_auditor.audit()


@pytest.mark.skip(msg="relying on data for other tests")
def test_deleting_data():
    lr.Auditor._complete_purge(response="Y")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
