from settings_base import *

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
MEDIA_ROOT = 'etc/media/'