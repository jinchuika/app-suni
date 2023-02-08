from django.apps import AppConfig


class BeqtConfig(AppConfig):
    name = 'apps.beqt'

    def ready(self):
        from . import signals
