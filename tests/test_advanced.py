# -*- coding: utf-8 -*-
import pathlib
import pytest

import lint_roller as lr

TEST_ROOT = pathlib.Path(__file__).joinpath("..").resolve()
TEST_DOCS = TEST_ROOT.joinpath("docs")


def test_auditor_instance_pkg_clean_up(dirty_package):
    """Test that Auditor instance objects can purge their associated package source code
    data cleanly."""
    package_name = "dustbunny1"
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
def test_auditor_instance_audit_clean_up(dirty_package):
    """Test that Auditor instance objects can purge their associated audit record data
    cleanly."""
    package_name = "dustbunny2"
    package_path = lr.utils.package_maker(package_name)
    dustbunny_auditor = lr.Auditor(package_path)
    dustbunny_auditor.audit()

    control_pkg_path = dirty_package
    control_auditor = lr.Auditor(control_pkg_path)
    control_auditor.audit()

    # depot_packages = dustbunny_auditor.check_depot()
    # assert package_name in depot_packages
    # assert control_pkg_path.stem in depot_packages
    # dustbunny_auditor.clear_depot()

    # post_cleanup_pkgs = dustbunny_auditor.check_depot()
    # assert package_name not in post_cleanup_pkgs

    # ensure extra audit records were not removed.
    # assert len(depot_packages) - 1 == len(post_cleanup_pkgs)
    # assert control_pkg_path.stem in post_cleanup_pkgs


if __name__ == "__main__":
    pytest.main(["-v", __file__])
