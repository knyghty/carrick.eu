"""Django settings for carrick.eu."""

import os
import pathlib

from django.core.management.utils import get_random_secret_key

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent


def as_bool(value):
    if isinstance(value, bool):
        return value
    return value.lower() in {"1", "true"}


# Security

ALLOWED_HOSTS = [".carrick.eu", "carrick-eu-staging.herokuapp.com", "carrick.localhost"]

CSRF_COOKIE_SECURE = True

DEBUG = as_bool(os.getenv("DEBUG", "0"))

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_SECONDS = 60 * 60

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True


# Application definition

AUTH_USER_MODEL = "accounts.User"

APPEND_SLASH = False

INSTALLED_APPS = [
    "accounts.apps.AccountsConfig",
    "carrick.apps.CarrickConfig",
    "debug_toolbar",
    "django_extensions",
    "snakeoil",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "carrick.urls"

SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"environment": "carrick.jinja2.environment"},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "carrick.wsgi.application"


# Database.

DATABASES = {"default": dj_database_url.config(conn_max_age=None)}


# Passwords.

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Internationalization.

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files.

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "/static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Logging.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}


# Django Debug Toolbar.

ENABLE_DEBUG_TOOLBAR = as_bool(os.getenv("ENABLE_DEBUG_TOOLBAR", DEBUG))

INTERNAL_IPS = os.getenv("INTERNAL_IPS", "").split(",")

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": "carrick.utils.show_toolbar"}


# Sentry.

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "unknown"),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
    traces_sample_rate=1.0,
)


# Snakeoil.

SNAKEOIL_DEFAULT_TAGS = {
    "default": [
        {"name": "author", "content": "Tom Carrick"},
        {"property": "og:image", "static": "carrick/img/logo.png"},
        {"property": "og:image:alt", "content": "Tom Carrick"},
        {"property": "og:image:width", "content": "300"},
        {"property": "og:image:height", "content": "300"},
        {"property": "og:locale", "content": "en_GB"},
        {"property": "og:site_name", "content": "Tom Carrick"},
        {"property": "og:title", "content": "Tom Carrick"},
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": "https://carrick.eu/"},
        {"name": "twitter:card", "content": "summary"},
        {"name": "twitter:creator", "content": "@knyghty"},
        {"name": "twitter:site", "content": "@knyghty"},
    ]
}
