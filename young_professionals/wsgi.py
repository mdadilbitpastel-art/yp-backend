"""WSGI config for young_professionals."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "young_professionals.settings")

application = get_wsgi_application()
