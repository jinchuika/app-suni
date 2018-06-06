"""
Routers para usar otras bases de datos. Se utiliza principalmente para acceder
a los datos de capacitación desde la versión anterior de SUNI.
"""
from apps.legacy import models as legacy_m
from django.conf import settings


class LegacyRouter:
    def db_for_read(self, model, **kwargs):
        if model._meta.app_label == 'legacy' and settings.LEGACY_TESTING:
            return 'default'
        elif model._meta.app_label == 'legacy':
            return 'legacy'
        return 'default'

    def db_for_write(self, model, **kwargs):
        if model._meta.app_label == 'legacy' and settings.LEGACY_TESTING:
            return 'default'
        elif model._meta.app_label == 'legacy':
            return 'legacy'
        return 'default'

    def allow_relation(self, obj1, obj2, **kwargs):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Para evitar que se puedan hacer migraciones hacia la base de datos principal
        """
        if db == 'default':
            return True
        else:
            return False
