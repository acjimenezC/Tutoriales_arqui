"""
Configuración de la app pages.
Define metadatos de la aplicación.
"""
from django.apps import AppConfig
from django.utils.module_loading import import_string
from django.conf import settings


class PagesConfig(AppConfig):
    """
    Configuración para la app 'pages'.
    
    - default_auto_field: Campo primario automático para modelos
    - name: Nombre de la aplicación
    - verbose_name: Nombre legible en admin
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Páginas'

    def ready(self):
        """Initialize the app and load the image storage provider."""
        ImageStorageClass = import_string(settings.IMAGE_STORAGE_CLASS)
