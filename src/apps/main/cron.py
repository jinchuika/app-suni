from django.core import management
from django.conf import settings
from apps.main.models import ArchivoGenerado


def backup_cron():
    if settings.DBBACKUP_STORAGE is not '':
        management.call_command('dbbackup')


def generar_archivos_fijos():
    for archivo in ArchivoGenerado.objects.filter(activo=True):
        archivo.generar()
