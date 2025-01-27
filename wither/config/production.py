import os
import django_heroku
from .common import Common


class Production(Common):
    DEBUG = os.getenv("DEBUG", False)

    INSTALLED_APPS = Common.INSTALLED_APPS
    MIDDLEWARE = Common.MIDDLEWARE
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn",)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATIC_URL = "/static/"

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Logging Overrides
    LOGGING = Common.LOGGING
    LOGGING["handlers"]["django.server"]["level"] = "DEBUG" if DEBUG else "INFO"

    # Activate Django-Heroku.
    django_heroku.settings(locals())
