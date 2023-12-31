from django.utils.translation import gettext_lazy as _

from liiweb.settings import *  # noqa

INSTALLED_APPS = ["malawilii.apps.MalawiLIIConfig"] + INSTALLED_APPS  # noqa


JAZZMIN_SETTINGS["site_title"] = "MalawiLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "MalawiLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "malawilii.org"  # noqa

COURT_CODE_MAPPINGS = {
    "supreme-court-of-appeal": "MWSC",
    "magistrate-court-blantyre": "MWMCB",
    "high-court-criminal-division": "MWHCCrim",
    "high-court-family-and-probate-division": "MWHCFam",
    "high-court-revenue-division": "MWHCRev",
    "high-court-civil-division": "MWHCCiv",
    "high-court-general-division": "MWHC",
    "high-court-commercial-division": "MWCommC",
    "industrial-relations-court": "MWIRC",
    "magistrate-court-lilongwe": "MWMCL",
    "magistrate-court-mangochi": "MWMCM",
    "magistrate-court-zomba": "MWMCZ",
}

LANGUAGES = [
    ("en", _("English")),
]
