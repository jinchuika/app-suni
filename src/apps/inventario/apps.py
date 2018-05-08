from django.apps import AppConfig


class InventarioConfig(AppConfig):
    name = 'apps.inventario'

    def ready(self):
        from . import signals
