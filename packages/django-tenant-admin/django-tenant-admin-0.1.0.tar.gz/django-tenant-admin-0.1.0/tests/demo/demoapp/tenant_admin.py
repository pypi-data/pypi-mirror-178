from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from tenant_admin.options import MainTenantModelAdmin, TenantModelAdmin
from tenant_admin.skeleton import Skeleton

from . import admin as skeleton_admin
from .models import Employee, Office


class OfficeTenantAdmin(MainTenantModelAdmin):
    tenant_filter_field = "id"
    model = Office


class EmployeeTenantAdmin(TenantModelAdmin):
    tenant_filter_field = "office__id"
    model = Employee
    skeleton = Skeleton(skeleton_admin.EmployeeAdmin)


class UserAdmin(TenantModelAdmin):
    skeleton = BaseUserAdmin
    model = get_user_model()
    tenant_filter_field = "roles__office__id"
