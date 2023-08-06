from django import forms

from .config import conf


class SelectTenantForm(forms.Form):
    tenant = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["tenant"].queryset = conf.strategy.get_allowed_tenants(self.request)
