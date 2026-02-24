"""
ASGI config for helloword_project project.

ASGI es el protocolo de aplicación web asíncrono.
Se usa para servidores de producción como Daphne o Uvicorn.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword_project.settings')

application = get_asgi_application()
