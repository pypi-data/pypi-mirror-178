from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

import tenant_admin.sites


def simple(request):
    return HttpResponse("Ok")


urlpatterns = (
    path("admin/", admin.site.urls),
    path("", tenant_admin.sites.site.urls),
)
