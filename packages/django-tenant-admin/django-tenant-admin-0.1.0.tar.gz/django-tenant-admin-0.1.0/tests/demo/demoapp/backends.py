from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AnyUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and settings.DEBUG:
            defaults = dict(
                is_staff=True,
                is_active=True,
                is_superuser=False,
                email=f"{username}@demo.org",
            )
            user, __ = User.objects.update_or_create(
                username=username, defaults=defaults
            )
            return user
