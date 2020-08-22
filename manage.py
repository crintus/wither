#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings
from configurations import importer


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wither.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

    importer.install()

    if settings.DEBUG:
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import ptvsd

            ptvsd.enable_attach(address=("0.0.0.0", 3000))
            print("Attached remote debugger")

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
