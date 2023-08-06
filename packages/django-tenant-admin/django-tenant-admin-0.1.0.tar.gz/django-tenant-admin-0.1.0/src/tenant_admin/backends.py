from django.contrib.auth.backends import ModelBackend

from tenant_admin.config import conf


class BaseTenantBackend(ModelBackend):
    def get_all_permissions(self, user_obj, obj=None):
        if obj and isinstance(obj, conf.stratrgy.model):
            return []
        return super().get_all_permissions(user_obj)
