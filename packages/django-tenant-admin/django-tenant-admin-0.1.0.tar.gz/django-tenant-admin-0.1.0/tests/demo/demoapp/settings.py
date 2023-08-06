from pathlib import Path

SECRET_KEY = "funny_key_just_for_testing"
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(__file__).parent.parent.parent.parent
        / "django_tenant_admin.sqlite",
        "TEST": {
            "NAME": ":memory:",
        },
        "TEST_NAME": ":memory:",
        "HOST": "",
        "PORT": "",
        "ATOMIC_REQUESTS": True,
    }
}
DEBUG = True
TEMPLATE_DEBUG = DEBUG
#
# TIME_ZONE = 'Asia/Bangkok'
# LANGUAGE_CODE = 'en-us'
# SITE_ID = 1
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True
# MEDIA_ROOT = os.path.join(here, 'media')
# MEDIA_URL = ''
# STATIC_ROOT = os.path.join(here, 'static')
# STATIC_URL = '/static/'
# SECRET_KEY = 'c73*n!y=)tziu^2)y*@5i2^)$8z$tx#b9*_r3i6o1ohxo%*2^a'
#
MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
INSTALLED_APPS = [
    "demoapp.apps.Config",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "smart_admin.apps.SmartTemplateConfig",
    "smart_admin.apps.SmartConfig",
    "admin_extra_buttons",
    "tenant_admin.apps.Config",
]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "demoapp.backends.AnyUserAuthBackend",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
            ],
        },
    },
]
ROOT_URLCONF = "demoapp.urls"
STATIC_URL = "/static/"

TENANT_TENANT_MODEL = "demoapp.Office"
TENANT_STRATEGY = "demoapp.tenant_strategy.DemoStrategy"
