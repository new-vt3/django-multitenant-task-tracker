import os
from pathlib import Path
import pprint
import dj_database_url
import django_heroku


print("✅ Starting settings.py...")

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"📁 BASE_DIR = {BASE_DIR}")

# ✅ Secret key & debug
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
print(f"🔐 SECRET_KEY = {SECRET_KEY}")
print(f"🐞 DEBUG = {DEBUG}")

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
print(f"🌐 ALLOWED_HOSTS = {ALLOWED_HOSTS}")

# Tailwind setup
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
INTERNAL_IPS = ['127.0.0.1']

# Tenant setup
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"
print(f"🏢 TENANT_MODEL = {TENANT_MODEL}, TENANT_DOMAIN_MODEL = {TENANT_DOMAIN_MODEL}")

SHARED_APPS = (
    "django_tenants",
    "customers",  # your app for Client and Domain models
    "tailwind",
    "theme",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
)

TENANT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",  # also required inside tenant apps
    "django.contrib.sessions",
    "django.contrib.messages",
    "tracker",  # your app with tenant-specific models
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
print(f"📦 INSTALLED_APPS = {INSTALLED_APPS}")

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",  # ✅ must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
print(f"🧱 MIDDLEWARE = {MIDDLEWARE}")

ROOT_URLCONF = "tasktracker.urls"
WSGI_APPLICATION = "tasktracker.wsgi.application"

# ✅ TEMPLATES setup
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
print("🧾 TEMPLATES configured.")

# ✅ DATABASE CONFIGURATION
print("🔍 Setting up database...")

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'
print("✅ DATABASE CONFIGURATION:")
pprint.pprint(DATABASES)

DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']
print(f"🚦 DATABASE_ROUTERS = {DATABASE_ROUTERS}")

# === Auth ===
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
print("🔐 Auth settings done.")

# === Email ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
print(f"✉️ EMAIL_HOST_USER = {EMAIL_HOST_USER}")

# === Static Files ===
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / TAILWIND_APP_NAME / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
print("📁 Static files setup complete.")

# === Localization ===
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
print("🌍 Localization settings set.")

# ✅ Finalize settings for Render/Heroku
print("🚀 Finalizing Django-Heroku settings...")
django_heroku.settings(locals())
print("✅ settings.py loaded successfully.")
