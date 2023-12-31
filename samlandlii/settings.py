from django.utils.translation import gettext_lazy as _

from liiweb.settings import *  # noqa

INSTALLED_APPS = ["samlandlii.apps.SamlandLIIConfig"] + INSTALLED_APPS  # noqa

DEBUG = 0

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
