from django.core import management
from django.conf import settings


def backup_cron():
    if settings.DBBACKUP_STORAGE is not '':
        management.call_command('dbbackup')
