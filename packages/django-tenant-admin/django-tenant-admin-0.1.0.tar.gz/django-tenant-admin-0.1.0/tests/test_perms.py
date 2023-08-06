def test_perms(user):
    from tenant_admin.backends import BaseTenantBackend

    b = BaseTenantBackend()
    assert b.get_all_permissions(user) == set()
