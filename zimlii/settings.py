from liiweb.settings import *  # noqa

INSTALLED_APPS = ["zimlii.apps.ZimLIIConfig"] + INSTALLED_APPS  # noqa

ROOT_URLCONF = "zimlii.urls"


JAZZMIN_SETTINGS["site_title"] = "ZimLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "ZimLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "zimlii.org"  # noqa
