from unittest.mock import Mock

from django.contrib.admin import ModelAdmin
from django.db.models import Model


def test_init():
    from tenant_admin.options import TenantModelAdmin

    assert TenantModelAdmin(Mock(spec=Model, _meta=Mock()), Mock(spec=ModelAdmin))
