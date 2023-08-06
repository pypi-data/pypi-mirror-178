from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Country, Employee, Office, UserRole


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    pass


@admin.register(Office)
class OfficeAdmin(ModelAdmin):
    list_display = ("name", "country")


@admin.register(UserRole)
class UserRoleAdmin(ModelAdmin):
    list_display = ("user", "group", "office")


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = (
        "office",
        "name",
    )
