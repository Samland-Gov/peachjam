"""
Django settings for peachjam project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import base64
import logging
import os
from pathlib import Path

import sentry_sdk
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "true") == "true"

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = "django-insecure-1q!zjpjmde2=yf0$doia!@74h-(f85(&&8)l05a+tt(b8g^rrt"
else:
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "peachjam.apps.PeachJamConfig",
    "peachjam_search.apps.PeachjamSearchConfig",
    "peachjam_api.apps.PeachjamApiConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "countries_plus",
    "languages_plus",
    "rest_framework",
    "django_filters",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "sass_processor",
    "import_export",
    "treebeard",
    "background_task",
    "ckeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "peachjam.urls"

TEMPLATES = [
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
                "peachjam.context_processors.general",
            ],
        },
    },
]

PEACHJAM = {
    "APP_NAME": os.environ.get("APP_NAME", "Peachjam"),
    "SUPPORT_EMAIL": os.environ.get("SUPPORT_EMAIL"),
    "SENTRY_DSN_KEY": os.environ.get("SENTRY_DSN_KEY"),
    "SENTRY_ENVIRONMENT": os.environ.get("SENTRY_ENVIRONMENT", "staging"),
}

PEACHJAM["ES_INDEX"] = os.environ.get("ES_INDEX", slugify(PEACHJAM["APP_NAME"]))

WSGI_APPLICATION = "peachjam.wsgi.application"
EMAIL_SUBJECT_PREFIX = f"[{PEACHJAM['APP_NAME']}] "

# Django all-auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# admins must create accounts
ACCOUNT_SIGNUP_ENABLED = False
# sign in with email addresses
ACCOUNT_AUTHENTICATION_METHOD = "email"
# email addresses are required for new accounts
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
LOGIN_URL = "account_login"

# social logins
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    },
}

SOCIALACCOUNT_ADAPTER = "peachjam.auth.SocialAccountAdapter"

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    INSTALLED_APPS.append("django_extensions")
    INSTALLED_APPS.append("elastic_panel")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
import dj_database_url  # noqa

default_db_url = "postgres://peachjam:peachjam@localhost:5432/peachjam"
db_config = dj_database_url.config(
    default=os.environ.get("DATABASE_URL", default_db_url)
)
db_config["ATOMIC_REQUESTS"] = True

DATABASES = {"default": db_config}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    ("sw", _("Swahili")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.getcwd(), "staticfiles")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": os.environ.get("ELASTICSEARCH_HOST", "localhost:9200"),
        "timeout": 5,
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissions"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

# Elastic APM
APM_SERVER_URL = os.environ.get("APM_SERVER_URL", "")
ELK_PROJECT = "peachjam-staging"
ELASTIC_APM = {
    "SERVICE_NAME": ELK_PROJECT,
    "SERVER_URL": APM_SERVER_URL,
}
if not DEBUG and APM_SERVER_URL:
    INSTALLED_APPS = INSTALLED_APPS + ["elasticapm.contrib.django"]
    MIDDLEWARE = [
        "elasticapm.contrib.django.middleware.TracingMiddleware",
        "elasticapm.contrib.django.middleware.Catch404Middleware",
    ] + MIDDLEWARE


# Sentry
if not DEBUG:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=None,  # Don't send errors based on log messages
    )
    sentry_sdk.init(
        dsn=PEACHJAM["SENTRY_DSN_KEY"],
        environment=PEACHJAM["SENTRY_ENVIRONMENT"],
        integrations=[DjangoIntegration(), sentry_logging],
        send_default_pii=True,
    )

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

DEBUG_TOOLBAR_PANELS = (
    # Defaults
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    # Additional
    "elastic_panel.panel.ElasticDebugPanel",
)

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, "node_modules"),
]

if not DEBUG:
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as env variables
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "")
    AWS_SIGNATURE_VERSION = "s3v4"
    AWS_QUERYSTRING_AUTH = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = {
    "type": "service_account",
    "project_id": os.environ.get("GOOGLE_PROJECT_ID", ""),
    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID", ""),
    #  private key is expected to be base64 encoded string
    "private_key": base64.b64decode(
        os.environ.get("GOOGLE_PRIVATE_KEY", "").encode("utf-8")
    ).decode("utf-8"),
    "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL", ""),
    "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
    "auth_uri": os.environ.get("GOOGLE_AUTH_URI", ""),
    "token_uri": os.environ.get("GOOGLE_TOKEN_URI", ""),
    "auth_provider_x509_cert_url": os.environ.get(
        "GOOGLE_AUTH_PROVIDER_X509_CERT_URL", ""
    ),
    "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL", ""),
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "africanlii": {"handlers": ["console"], "level": "DEBUG"},
        "peachjam": {"handlers": ["console"], "level": "DEBUG"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
}


if DEBUG:
    ELASTICSEARCH_DSL_AUTOSYNC = False

GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID")

CKEDITOR_CONFIGS = {"default": {"removePlugins": ["image"]}}
