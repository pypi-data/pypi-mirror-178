from unittest.mock import Mock


def test_check_tenant_model():
    from tenant_admin.checks import check_tenant_model

    assert check_tenant_model(Mock()) == []


def test_check_main_tenant_admin():
    from tenant_admin.checks import check_main_tenant_admin

    assert check_main_tenant_admin(Mock()) == []
