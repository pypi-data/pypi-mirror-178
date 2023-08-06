import logging
from abc import ABC, abstractmethod

import django.http
from django.apps import apps
from django.core.signing import Signer
from django.db.models import Model, QuerySet
from django.http import HttpResponse
from django.utils.functional import cached_property

from .config import AppSettings

signer = Signer()
logger = logging.getLogger(__name__)


class BaseTenantStrategy(ABC):
    pk = "pk"

    def __init__(self, config: AppSettings):
        self.config = config
        self._selected_tenant = None
        self._selected_tenant_value = ""

    @cached_property
    def model(self) -> Model:
        return apps.get_model(self.config.TENANT_MODEL)

    def set_selected_tenant(self, response: HttpResponse, instance: Model) -> None:
        response.set_cookie(
            self.config.COOKIE_NAME, signer.sign(getattr(instance, self.pk))
        )

    def get_selected_tenant(self, request: "django.http.HttpRequest") -> Model:
        cookie_value = request.COOKIES.get(self.config.COOKIE_NAME)
        if (self._selected_tenant_value != cookie_value) or (
            self._selected_tenant is None
        ):
            try:
                filters = {self.pk: signer.unsign(cookie_value)}
                self._selected_tenant_value = cookie_value
                self._selected_tenant = self.get_allowed_tenants(request).get(**filters)
            except TypeError:
                self._selected_tenant = None
            # except ObjectDoesNotExist:
            #     raise InvalidTenantError()
            except Exception as e:  # pragma: no cover
                logger.exception(e)
                self._selected_tenant = None
        return self._selected_tenant

    @abstractmethod
    def get_allowed_tenants(self, request: "django.http.HttpRequest") -> QuerySet:
        pass


class DefaultStrategy(BaseTenantStrategy):
    def get_allowed_tenants(self, request: "django.http.HttpRequest") -> QuerySet:
        return self.model.objects.all()
