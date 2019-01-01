# -*- coding: utf-8 -*-
import pathlib
import shutil
import pytest

import lint_roller as lr

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


def test_end_to_end():
    package_name = "package_abc"
    audit_file = lr.Auditor.RECORDS.joinpath(f"audit__{package_name}.csv")
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


def test_clean_up(dirty_package):
    package_name = "dustbunny"
    package_path = lr.utils.package_maker(package_name)
    control_pkg_path = dirty_package

    dustbunny_auditor = lr.Auditor(package_path)
    with pytest.raises(NotImplementedError):
        dustbunny_auditor.audit()

    depot_packages = dustbunny_auditor.check_depot()
    assert package_name in depot_packages
    assert control_pkg_path.stem in depot_packages
    dustbunny_auditor.clear_depot()

    post_cleanup_pkgs = dustbunny_auditor.check_depot()
    assert package_name not in post_cleanup_pkgs

    # ensure extra packages were not removed.
    assert len(depot_packages) - 1 == len(post_cleanup_pkgs)
    assert control_pkg_path.stem in post_cleanup_pkgs


@pytest.mark.xfail()
def test_simple_audit(dirty_package):
    """Placeholder test for future behavior that should produce a useable result"""
    my_package_path = dirty_package
    my_pkg_auditor = lr.Auditor(my_package_path)
    my_pkg_auditor.audit()


@pytest.mark.skip(msg="relying on data for other tests")
def test_deleting_data():
    lr.Auditor._complete_purge(response="Y")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
