from django.core import management


def backup_cron():
    management.call_command('dbbackup')
