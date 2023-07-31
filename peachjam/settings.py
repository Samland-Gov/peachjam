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

import dj_database_url
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
    "rest_framework.authtoken",
    "django_filters",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "jazzmin",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "sass_processor",
    "import_export",
    "treebeard",
    "background_task",
    "ckeditor",
    "polymorphic",
]

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "peachjam.middleware.RedirectWWWMiddleware",
    "peachjam.middleware.RedirectNewMiddleware",
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
    "CITATOR_API": os.environ.get(
        "CITATOR_API", "https://services.lawsafrica.com/citator/v1/extract-citations"
    ),
    "CITATOR_API_KEY": os.environ.get("CITATOR_API_KEY"),
    "EXTRA_SEARCH_INDEXES": [],
    "SEARCH_JURISDICTION_FILTER": False,
}

PEACHJAM["ES_INDEX"] = os.environ.get("ES_INDEX", slugify(PEACHJAM["APP_NAME"]))

WSGI_APPLICATION = "peachjam.wsgi.application"
EMAIL_SUBJECT_PREFIX = f"[{PEACHJAM['APP_NAME']}] "
SERVER_EMAIL = DEFAULT_FROM_EMAIL = PEACHJAM["SUPPORT_EMAIL"]

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
LOGIN_REDIRECT_URL = "home_page"

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
default_db_url = "postgres://peachjam:peachjam@localhost:5432/peachjam"
gazette_db_url = "postgres://indigo:indigo@localhost:5432/indigo"
default_db_config = dj_database_url.config(default=default_db_url)
gazette_db_config = dj_database_url.config(
    default=gazette_db_url, env="GAZETTES_DATABASE_URL"
)
default_db_config["ATOMIC_REQUESTS"] = True

DATABASES = {
    "default": default_db_config,
    "gazettes_africa": gazette_db_config,
}


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
    ("pt", _("Portuguese")),
    ("sw", _("Swahili")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = False
DATE_FORMAT = "j F Y"

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

# effectively, max pages we'll index from documents
ELASTICSEARCH_DSL_INDEX_SETTINGS = {"index.mapping.nested_objects.limit": "50000"}
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": os.environ.get("ELASTICSEARCH_HOST", "localhost:9200"),
        "timeout": 30,
    },
}

ELASTICSEARCH_MAX_ANALYZED_OFFSET = os.environ.get(
    "ELASTICSEARCH_MAX_ANALYZED_OFFSET", 2000000
)

ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = (
    "peachjam_search.tasks.BackgroundTaskSearchProcessor"
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissions"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

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
        # sample x% of requests for performance metrics
        traces_sample_rate=float(os.environ.get("SENTRY_SAMPLE_RATE", "0.25")),
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
    os.environ.get("NODE_PATH") or os.path.join(BASE_DIR, "node_modules"),
]

# Configure dynamic file storage for fields which use it. This is a type of storage which can dynamically
# determine whether an individual file is in S3 or a local file.
#
# In DEBUG mode, we default to the default locale file storage. In production, we use S3.
DYNAMIC_STORAGE = {
    # use file storage by default
    "DEFAULTS": {"": "file:"},
    "PREFIXES": {
        # storage backends for the different prefixes
        "file": {"storage": "peachjam.storage.DynamicFileSystemStorage"},
        "s3": {"storage": "peachjam.storage.DynamicS3Boto3Storage"},
    },
}

if not DEBUG:
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as env variables
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_QUERYSTRING_AUTH = True

    # In production, use S3 and the default S3 bucket
    DYNAMIC_STORAGE["DEFAULTS"][""] = f"s3:{AWS_STORAGE_BUCKET_NAME}:"

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


JAZZMIN_SETTINGS = {
    "site_title": PEACHJAM["APP_NAME"],
    "site_header": PEACHJAM["APP_NAME"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "account.EmailAddress": "fa fa-envelope",
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "peachjam.Judgment": "fa fa-balance-scale",
        "background_task.CompletedTask": "fa fa-calendar-check",
        "background_task.Task": "fa fa-tasks",
        "countries_plus.Country": "fa fa-globe",
        "languages_plus.CultureCode": "fa fa-align-justify",
        "languages_plus.Language": "fa fa-language",
        "peachjam.Judge": "fa fa-gavel",
        "peachjam.JudgmentMediaSummaryFile": "fa fa-folder-open",
        "peachjam.Author": "fa fa-pencil-alt",
        "peachjam.Legislation": "fa fa-book",
        "peachjam.CitationLink": "fa fa-link",
        "liiweb.CourtClass": "fa fa-building",
        "liiweb.CourtDetail": "fa fa-list-alt",
        "peachjam.GenericDocument": "fa fa-copy",
        "peachjam.LegalInstrument": "fa fa-briefcase",
        "peachjam.Locality": "fa fa-map",
        "peachjam.Ingestor": "fa fa-download",
        "peachjam.Image": "fa fa-file-image",
        "peachjam.MatterType": "fa fa-list",
        "peachjam.PeachjamSettings": "fa fa-wrench",
        "peachjam.DocumentNature": "fa fa-list",
        "peachjam.SourceFile": "fa fa-file-archive",
        "peachjam.Taxonomy": "fa fa-tags",
        "peachjam.Predicate": "fa fa-exchange-alt",
        "django.Site": "fa fa-server",
        "socialaccount.SocialAccount": "fa fa-users",
        "socialaccount.SocialToken": "fa fa-key",
        "socialaccount.SocialApp": "fa fa-puzzle-piece",
    },
    "related_modal_active": True,
    "show_ui_builder": False,
    "topmenu_links": [
        {"app": "peachjam"},
        {"app": "liiweb"},
    ],
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "peachjam",
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_compact_style": True,
    "sidebar_nav_flat_style": True,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "ERROR"},
        "django": {"level": "INFO"},
        "peachjam": {"level": "DEBUG" if DEBUG else "INFO"},
        "peachjam_search": {"level": "DEBUG" if DEBUG else "INFO"},
        "peachjam_api": {"level": "DEBUG" if DEBUG else "INFO"},
        "background_task": {"level": "INFO"},
        "import_export": {"level": "DEBUG"},
    },
}


if DEBUG:
    ELASTICSEARCH_DSL_AUTOSYNC = False


CKEDITOR_CONFIGS = {
    # The rest of this config is defined in ckeditor.configs.DEFAULT_CONFIG
    "default": {
        "removePlugins": ["image"],
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar", "LaAkn"],
            ["Source"],
        ],
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_SECURE = True

# Caches
if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/var/tmp/django_cache",
        },
    }

# Override X-Frame-Options header value
X_FRAME_OPTIONS = "SAMEORIGIN"

# Setup request id logging
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
REQUEST_ID_RESPONSE_HEADER = "X-Request-Id"
LOGGING["filters"] = {"request_id": {"()": "log_request_id.filters.RequestIDFilter"}}
LOGGING["formatters"]["simple"][
    "format"
] = "%(asctime)s %(levelname)s %(module)s %(request_id)s %(process)d %(thread)d %(message)s"
LOGGING["handlers"]["console"]["filters"] = ["request_id"]


# E-mail configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", 25))
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "false") == "true"
EMAIL_USE_SSL = os.environ.get("DJANGO_EMAIL_USE_SSL", "false") == "true"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
