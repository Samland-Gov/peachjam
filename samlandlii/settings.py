from django.utils.translation import gettext_lazy as _

from liiweb.settings import *  # noqa

INSTALLED_APPS = ["samlandlii.apps.SamlandLIIConfig"] + INSTALLED_APPS  # noqa

PEACHJAM = {
    "APP_NAME": "SamlandLII",
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

JAZZMIN_SETTINGS["site_title"] = "SamlandLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "SamlandLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "samlandlii.minersonline.uk"  # noqa

COURT_CODE_MAPPINGS = {
    "supreme-court": "ZLSC",
    "court-of-appeal": "ZLCA",
    "high-court": "ZLHC",
}
LANGUAGES = [
    ("en", _("English")),
]
