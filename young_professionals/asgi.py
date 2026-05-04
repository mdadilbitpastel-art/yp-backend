"""ASGI config for young_professionals."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "young_professionals.settings")

application = get_asgi_application()
