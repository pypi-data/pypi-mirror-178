from unittest.mock import Mock

from tenant_admin.config import conf


def test_strategy(db):
    from demoapp.factories import OfficeFactory
    from demoapp.models import Office

    from tenant_admin.strategy import DefaultStrategy

    o = OfficeFactory()
    s = DefaultStrategy(conf)
    assert s.model == Office
    assert s.get_allowed_tenants(Mock()).first() == o
