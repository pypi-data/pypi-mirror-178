django-tenant-admin
===================


Quick Start
===========

In the settings.py:
1. Add "tenant_admin.apps.Config" to your INSTALLED_APPS
2. Add TENANT_TENANT_MODEL and TENANT_STRATEGY

#### settings.py
    INSTALLED_APPS = [
        "demoapp.apps.Config",
        ...
        # 'django.contrib.admin',
        ...
        "django.contrib.staticfiles",
        "smart_admin.apps.SmartTemplateConfig",
        "smart_admin.apps.SmartConfig",
        "admin_extra_buttons",
        "tenant_admin.apps.Config",
    ]

    TENANT_TENANT_MODEL = "<app_label>.<model_name>"
    TENANT_STRATEGY = "<app_label>.YourStrategy"


#### urls.py
    import tenant_admin.sites


    urlpatterns = (
        path("manage/", tenant_admin.sites.site.urls),
        ...
    )


Some clarification:

    `Strategy` is about visibility
    `Permission` is about authorization


### Contributing
    
    git checkout https://gitlab.com/os4d/django-tenant-admin.git
    cd django-tenant-admin
    python -m venv .venv
    . .venv/bin/activate
    pip install -e .[dev]
    pre-commit install

### Create sample data

This will create the DB ./django_tenant_admin.sqlite and populate with some example data.

    ./manage.py demo

This will create:
- 4 `Country` records: 'Afghanistan', 'Ukraine', 'Somalia', 'Sudan'
- 4 `Office` records: 'Afghanistan Office', 'Ukraine Office', 'Somalia Office', 'Sudan Office'
- 10 `Employee` records: 'Employee 0' to 'Employee 9'
- An 'admin-ukr' user assigned to 'Ukraine Office'
- An 'admin-afg' user and 8 additional users (_username3_ to _username12_) assigned to 'Afghanistan Office'
- An 'admin' user not assigned to any office


Try it with:

    ./manage.py runserver

Connect to http://localhost:8000

NB:
- No need to create users as for demo purposes there is a backend that will create the user on the fly using any
password



