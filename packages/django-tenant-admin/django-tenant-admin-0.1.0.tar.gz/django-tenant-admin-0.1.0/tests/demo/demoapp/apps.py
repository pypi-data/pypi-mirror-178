from django.apps import AppConfig


class Config(AppConfig):
    name = "demoapp"

    def ready(self):
        from tenant_admin.options import model_admin_registry
        from tenant_admin.sites import site

        from . import tenant_admin  # noqa

        for opt in model_admin_registry:
            site.register(opt)
