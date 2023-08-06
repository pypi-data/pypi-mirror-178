from typing import Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from .exceptions import TenantAdminError


class TenantAdminMiddleware:
    def __init__(self, get_response: Optional[Callable[[HttpRequest], HttpResponse]]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        try:
            response = self.get_response(request)  # type: ignore
        except TenantAdminError:
            from tenant_admin.site import site

            response = redirect(f"{site.name}:select_tenant")
        return response
