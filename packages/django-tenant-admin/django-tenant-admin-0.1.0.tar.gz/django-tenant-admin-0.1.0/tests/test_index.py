import pytest
from django.urls import reverse


@pytest.fixture
def tenant_user():
    from demoapp.factories import OfficeFactory, UserRoleFactory

    o1 = OfficeFactory(country__name="Afghanistan")
    o2 = OfficeFactory(country__name="Ukraine")
    role = UserRoleFactory(
        office=o1,
        group__name="admins",
        user__username="admin-afg",
        user__is_staff=False,
        user__is_active=True,
    )
    UserRoleFactory(
        office=o2,
        group__name="admins",
        user=role.user,
    )
    return role.user


@pytest.mark.django_db
def test_admin_index(app, admin_user):
    url = reverse("admin:index")
    res = app.get(url, user=admin_user.username)
    assert res.pyquery('a:contains("Django administration")')


@pytest.mark.django_db
def test_tenant_index_no_tenants(app, admin_user):
    url = reverse("tenant_admin:index")
    res = app.get(url, user=admin_user.username)
    assert res.status_code == 302


@pytest.mark.django_db
def test_tenant_index(app, tenant_user):
    url = reverse("tenant_admin:index")
    res = app.get(url, user=tenant_user.username)
    assert res.status_code == 302
    assert res.headers["Location"] == "/select/"


@pytest.mark.django_db
def test_tenant_select(app, tenant_user):
    url = reverse("tenant_admin:select_tenant")
    res = app.get(url, user=tenant_user.username)
    res.form["tenant"] = tenant_user.roles.first().office.pk
    res = res.form.submit().follow()
    assert res.pyquery('a:contains("Control Panel")')


@pytest.mark.django_db
def test_tenant_switch(app, tenant_user):
    url = reverse("tenant_admin:select_tenant")
    res = app.get(url, user=tenant_user.username)
    res.form["tenant"] = tenant_user.roles.get(
        office__country__name="Afghanistan"
    ).office.pk
    res = res.form.submit().follow()
    assert res.pyquery('a:contains("Afghanistan Office Control Panel")')
    res.form["tenant"] = tenant_user.roles.get(
        office__country__name="Ukraine"
    ).office.pk
    res = res.form.submit().follow()
    assert res.pyquery('a:contains("Ukraine Office Control Panel")')
    res = res.click("Offices")
    assert res.pyquery('a:contains("Ukraine Office Control Panel")')
