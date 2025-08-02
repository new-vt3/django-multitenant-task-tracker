import os
from pathlib import Path
import dj_database_url
import django_heroku
import pprint  # ✅ for pretty-printing debug output

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# === Tailwind (Optional) ===
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
INTERNAL_IPS = ['127.0.0.1']

# === Tenant Setup ===
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"

# === Installed Apps ===
SHARED_APPS = (
    "django_tenants",
    "customers",
    "tailwind",  # Optional
    "theme",     # Optional
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

# === Middleware ===
MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",  # ✅ Must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# === URL & WSGI ===
ROOT_URLCONF = "tasktracker.urls"
WSGI_APPLICATION = "tasktracker.wsgi.application"

# === Templates ===
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

# === Database Setup ===
print("🔍 Setting up database...")

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# ✅ Override the engine after dj_database_url config
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

# ✅ DEBUG print database config
print("✅ DATABASE CONFIGURATION:")
pprint.pprint(DATABASES)
print("📦 ENGINE in use:", DATABASES['default']['ENGINE'])

# === DB Router ===
DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']

# === Auth ===
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# === Email Settings ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# === Static Files ===
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / TAILWIND_APP_NAME / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# === Localization ===
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Render-friendly settings ===
print("🚀 Finalizing Django-Heroku settings...")
django_heroku.settings(locals())
print("✅ settings.py loaded successfully.")

