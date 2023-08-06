from demoapp.models import Office

from tenant_admin.strategy import BaseTenantStrategy


class DemoStrategy(BaseTenantStrategy):
    def get_allowed_tenants(self, request):
        if request.user.is_authenticated:
            return Office.objects.filter(userrole__user=request.user)
        else:
            return Office.objects.none()
