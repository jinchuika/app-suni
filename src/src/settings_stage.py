from .settings import *

# Motor de DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stage_suni',
        'USER': 'stage_suni',
        'PASSWORD': 'St@geSun1',
        'HOST': '149.56.16.135',
        'PORT': '3306',
    }
}


# DBBACKUP_STORAGE = 'storages.backends.ftp.FTPStorage'
# DBBACKUP_STORAGE_OPTIONS = {
#     'location': 'ftp://ftp-backup:db_Fun53P@!2@200.114.118.174:21/suni',
#     'base_url': '/ftp/files'
# }

# CRONJOBS = [
#     ('0 1 * * *', 'apps.main.cron.backup_cron')
# ]
