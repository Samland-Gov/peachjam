from liiweb.settings import *  # noqa

INSTALLED_APPS = ["sierralii.apps.SierraLIIConfig"] + INSTALLED_APPS  # noqa

ROOT_URLCONF = "sierralii.urls"


JAZZMIN_SETTINGS["site_title"] = "SierraLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "SierraLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "sierralii.org"  # noqa
