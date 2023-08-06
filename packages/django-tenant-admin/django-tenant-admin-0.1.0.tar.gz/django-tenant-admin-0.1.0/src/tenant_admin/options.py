from functools import update_wrapper
from inspect import isclass
from typing import List, Union

from adminactions.helpers import AdminActionPermMixin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.options import csrf_protect_m
from django.core.checks import Error
from django.db.models import Model
from django.forms.widgets import MediaDefiningClass
from django.shortcuts import redirect
from django.views.generic import RedirectView
from smart_admin.mixins import LinkedObjectsMixin
from smart_admin.modeladmin import SmartModelAdmin

from .config import conf
from .exceptions import InvalidTenantError, TenantAdminError
from .skeleton import Skeleton

model_admin_registry = []


class AutoRegisterMetaClass(MediaDefiningClass):
    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        if new_class.model:
            model_admin_registry.append(new_class)
        return new_class


class TenantTabularInline(TabularInline):
    tenant_filter_field = None

    def get_tenant_filter(self, request):
        if not self.target_field:
            raise ValueError(
                f"Set 'target_field' on {self} or override `get_queryset()` to enable queryset filtering"
            )
        return {self.tenant_filter_field: conf.strategy.get_selected_tenant(request).pk}


class TenantModelAdmin(
    SmartModelAdmin,
    AdminActionPermMixin,
    LinkedObjectsMixin,
    metaclass=AutoRegisterMetaClass,
):
    model: Model = None
    skeleton: Union[ModelAdmin, Skeleton] = None
    tenant_filter_field: str = ""

    change_list_template = "tenant_admin/change_list.html"
    change_form_template = "tenant_admin/change_form.html"
    linked_objects_template = "tenant_admin/linked_objects.html"
    writeable_fields: List[str] = []
    exclude: List[str] = []
    linked_objects_hide_empty = True

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        if self.skeleton:
            if not (
                (isclass(self.skeleton) and issubclass(self.skeleton, Skeleton))
                or isinstance(self.skeleton, Skeleton)
            ):
                self.skeleton = Skeleton(self.skeleton)
            self.skeleton.initialise(self)

    def get_inlines(self, request, obj=None):
        flt = list(
            filter(lambda x: not issubclass(x, TenantTabularInline), self.inlines)
        )
        if flt:
            raise ValueError(
                f"{self}.inlines contains one or more invalid class(es). "
                f" {flt} "
                f"Only use `TenantTabularInline`"
            )
        return self.inlines

    @classmethod
    def create(self, source: ModelAdmin):
        return TenantModelAdmin

    def get_writeable_fields(self, request, obj=None):
        return list(self.writeable_fields) + list(self.exclude)

    def get_readonly_fields(self, request, obj=None):
        all_fields = list(
            set(
                [field.name for field in self.opts.local_fields]
                + [field.name for field in self.opts.local_many_to_many]
            )
        )
        return [
            f for f in all_fields if f not in self.get_writeable_fields(request, obj)
        ]

    def get_tenant_filter(self, request):
        if not self.tenant_filter_field:
            raise ValueError(
                f"Set 'tenant_filter_field' on {self} or override `get_queryset()` to enable queryset filtering"
            )
        active_tenant = conf.strategy.get_selected_tenant(request)
        if not active_tenant:
            raise InvalidTenantError
        return {self.tenant_filter_field: active_tenant.pk}

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.filter(**self.get_tenant_filter(request)).distinct()

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                try:
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                except TenantAdminError:
                    return redirect(f"{self.admin_site.name}:select_tenant")

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        base_urls = [
            path("", wrap(self.changelist_view), name="%s_%s_changelist" % info),
            # path('add/', wrap(self.add_view), name='%s_%s_add' % info),
            # path('<path:object_id>/history/', wrap(self.history_view), name='%s_%s_history' % info),
            # path('<path:object_id>/delete/', wrap(self.delete_view), name='%s_%s_delete' % info),
            path(
                "<path:object_id>/change/",
                wrap(self.change_view),
                name="%s_%s_change" % info,
            ),
            # For backwards compatibility (was the change url before 1.9)
            path(
                "<path:object_id>/",
                wrap(
                    RedirectView.as_view(
                        pattern_name="%s:%s_%s_change"
                        % ((self.admin_site.name,) + info)
                    )
                ),
            ),
        ]
        return self.get_extra_urls() + base_urls

    def get_changeform_buttons(self, context):
        return super().get_changeform_buttons(context)

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class MainTenantModelAdmin(TenantModelAdmin):
    model: Model = None

    # change_list_template = "tenant_admin/change_form.html"
    # change_form_template = "tenant_admin/change_form.html"
    # linked_objects_template = "tenant_admin/linked_objects.html"

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        if cls.model != conf.tenant_model:
            errors.append(
                Error(
                    f'"{cls.__name__}.model must be {conf.tenant_model}" ',
                    id="admin_tenant.E100",
                )
            )

        return errors

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        active_tenant = conf.strategy.get_selected_tenant(request)
        if not active_tenant:
            raise InvalidTenantError
        return qs.filter(pk=active_tenant.pk)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        object_id = str(conf.strategy.get_selected_tenant(request).pk)
        return super().change_view(request, object_id)

    def has_add_permission(self, request):
        return False
