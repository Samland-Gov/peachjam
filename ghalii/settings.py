from liiweb.settings import *  # noqa

INSTALLED_APPS = ["ghalii.apps.GhaLIIConfig"] + INSTALLED_APPS  # noqa

COURT_CODE_MAPPINGS = {}

JAZZMIN_SETTINGS["site_title"] = "GhaLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "GhaLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "ghalii.org"  # noqa
