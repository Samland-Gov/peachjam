from liiweb.settings import *  # noqa

INSTALLED_APPS = ["namiblii.apps.ZanzibarLIIConfig"] + INSTALLED_APPS  # noqa

ROOT_URLCONF = "namiblii.urls"


JAZZMIN_SETTINGS["site_title"] = "NamibLII"  # noqa
JAZZMIN_SETTINGS["site_header"] = "NamibLII"  # noqa
JAZZMIN_SETTINGS["site_brand"] = "namiblii.org"  # noqa
