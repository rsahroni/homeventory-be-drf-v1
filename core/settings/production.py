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

# Static files (CSS, JavaScript, Images) for Production
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# Direktori tempat 'collectstatic' akan mengumpulkan semua file statis.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Security settings for production
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
