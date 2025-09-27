from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["homeventory.id", "www.homeventory.id"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("PROD_DB_NAME"),
        "USER": env("PROD_DB_USER"),
        "PASSWORD": env("PROD_DB_PASSWORD"),
        "HOST": env("PROD_DB_HOST"),
        "PORT": env("PROD_DB_PORT"),
    }
}
