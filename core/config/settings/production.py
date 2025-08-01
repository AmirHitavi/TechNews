from .base import *  # noqa
from .base import BASE_DIR, config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "PRODUCTION_SECRET_KEY",
    cast=str,
    default="django-insecure-%p(05l3adavf&^6#hi@d@gl0@h1%u9a##ebt34!$bn0977v6x8",
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "prod.sqlite3",
    }
}
