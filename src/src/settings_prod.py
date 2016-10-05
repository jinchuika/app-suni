from settings_base import *

DEBUG = False

# Motor de DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    }
}

# Carpeta para guardar archivos
MEDIA_ROOT = ''