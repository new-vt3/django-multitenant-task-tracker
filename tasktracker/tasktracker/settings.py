import os
from pathlib import Path
import dj_database_url
import django_heroku

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")

# Debug mode: set to False in production
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Hosts
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# Tailwind
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"  # Optional: remove on Render
INTERNAL_IPS = ['127.0.0.1']

# Tenants
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"

# Shared/Tenant Apps
SHARED_APPS = (
    "django_tenants",
    "customers",
    "tailwind",
    "theme",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
)

TENANT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "tracker",
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Middleware
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLS & WSGI
ROOT_URLCONF = "tasktracker.urls"
WSGI_APPLICATION = "tasktracker.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ✅ Database config
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgresql://vt3db_user:98c1jtteY9EXufsVLRhe6ZqcwdPApJRl@dpg-d26g75ali9vc7393iveg-a/vt3db"
        ),
        conn_max_age=600,
        engine='django_tenants.postgresql_backend'  # ✅ This line is required
    )
}
# ✅ Set the correct DB engine for django-tenants
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

# ✅ Use django-tenants DB router
DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']

# Auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / TAILWIND_APP_NAME / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Others
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ✅ Apply Render-friendly settings
django_heroku.settings(locals())
