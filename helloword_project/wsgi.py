"""
WSGI config for helloword_project project.

WSGI es el interfaz de puerta de enlace del servidor web.
Se usa para servidores de producción como Gunicorn o uWSGI.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword_project.settings')

application = get_wsgi_application()
