from .base import *  # noqa
from .base import BASE_DIR, env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("LOCAL_SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "local.sqlite3",
    }
}
