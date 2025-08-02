import os
from pathlib import Path
import pprint
import django_heroku
from dotenv import load_dotenv

load_dotenv()

print("✅ Starting settings.py...")

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"📁 BASE_DIR = {BASE_DIR}")

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
print(f"🔐 SECRET_KEY = {SECRET_KEY}")
print(f"🐞 DEBUG = {DEBUG}")
print(f"🌐 ALLOWED_HOSTS = {ALLOWED_HOSTS}")

TAILWIND_APP_NAME = 'theme'
# Adjust NPM_BIN_PATH to your OS and setup, example:
NPM_BIN_PATH = os.environ.get("NPM_BIN_PATH", "C:/Program Files/nodejs/npm.cmd" if os.name == 'nt' else "/usr/bin/npm")
INTERNAL_IPS = ['127.0.0.1']

TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"
print(f"🏢 TENANT_MODEL = {TENANT_MODEL}, TENANT_DOMAIN_MODEL = {TENANT_DOMAIN_MODEL}")

SHARED_APPS = (
    "django_tenants",       # must be first for django-tenants
    "customers",            # tenant app holding Client and Domain models
    "tailwind",             # optional: only if using django-tailwind
    "theme",                # optional tailwind theme app
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
)

TENANT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "tracker",              # your main app for business logic
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
print(f"📦 INSTALLED_APPS = {INSTALLED_APPS}")

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
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
print("🧾 TEMPLATES configured.")

# === Database ===
print("🔍 Setting up database...")
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # must use tenant-ready backend
        'NAME': 'vt3db',
        'USER': 'vt3db_user',
        'PASSWORD': '98c1jtteY9EXufsVLRhe6ZqcwdPApJRl',
        'HOST': 'dpg-d26g75ali9vc7393iveg-a.oregon-postgres.render.com',
        'PORT': '5432',  # default Postgres port
    }
}
print("✅ DATABASE CONFIGURATION:")
pprint.pprint(DATABASES)

DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']
print(f"🚦 DATABASE_ROUTERS = {DATABASE_ROUTERS}")

# === Authentication ===
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

# === Static files ===
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

print("🚀 Finalizing Django-Heroku settings...")
django_heroku.settings(locals())
print("✅ settings.py loaded successfully.")
