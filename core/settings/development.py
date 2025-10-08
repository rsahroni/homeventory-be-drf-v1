from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DEV_DB_NAME"),
        "USER": env("DEV_DB_USER"),
        "PASSWORD": env("DEV_DB_PASSWORD"),  # Pastikan ini ada di .env
        "HOST": env("DEV_DB_HOST"),  # Nama service database di docker-compose.yml
        "PORT": env("DEV_DB_PORT"),
    }
}
