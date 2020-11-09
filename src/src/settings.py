"""
Django settings for SUNI project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$+1+y$)19w80c$a_%$15ic6w#&82$31+lza90a56=4o(g&e)o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ['*']


# Application definition
DJANGO_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters')

THIRD_PARTY_APPS = (
    'braces',
    'easy_thumbnails',
    'dynamic_preferences',
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'widget_tweaks',
    'menu',
    'mixer',
    'dbbackup',
    'django_crontab',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',)

LOCAL_APPS = (
    'apps.main',
    'apps.users',
    'apps.escuela',
    'apps.kardex',
    'apps.fr',
    'apps.cyd',
    'apps.mye',
    'apps.tpe',
    'apps.dh',
    'apps.naat',
    'apps.kalite',
    'apps.ie',
    'apps.crm',
    'apps.inventario',
    'apps.conta',
    'apps.legacy',
    'apps.certificado',
    'apps.coursera',
    'apps.Bienestar',
    'apps.informe',
    'apps.controlNotas'
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
                'apps.main.context_processors.google_analytics',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'src.wsgi.application'


# Database

DATABASE_ROUTERS = ['apps.legacy.dbrouters.LegacyRouter', ]


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'suni_dev',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'legacy.sqlite3'),
    },
}"""
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-GT'

TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_ROOT = 'etc/media/'
MEDIA_ROOT_EXCEL = 'etc/media/excel/'
MEDIA_ROOT_EXCEL_BIENESTAR = 'etc/media/bienestar/excel/'
MEDIA_ROOT_EXCEL_COURSERA = 'etc/media/coursera/excel/'
MEDIA_ROOT_EXCEL_IMPACTO = 'etc/media/impacto/excel/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/'

THUMBNAIL_ALIASES = {
    '': {
        'background': {'size': (1350, 650), 'crop': True},
        'avatar-lg': {'size': (500, 375), 'crop': True},
        'avatar': {'size': (180, 180), 'crop': True},
        'avatar-sm': {'size': (90, 90), 'crop': True},
        'icon': {'size': (40, 40), 'crop': True},
        'icon-xs': {'size': (15, 15), 'crop': True},
    },
}

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/users/profile/'

# account settings
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
ACCOUNT_SIGNUP_FORM_CLASS = 'apps.users.forms.CustomSignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False


DYNAMIC_PREFERENCES = {

    # a python attribute that will be added to model instances with preferences
    'MANAGER_ATTRIBUTE': 'preferences',

    # The python module in which registered preferences will be searched within each app
    'REGISTRY_MODULE': 'dynamic_preferences_registry',

    # Allow quick editing of preferences directly in admin list view
    'ADMIN_ENABLE_CHANGELIST_FORM': False,

    # Should we enable the admin module for user preferences ?
    'ENABLE_USER_PREFERENCES': True,

    # Customize how you can access preferences from managers. The default is to
    # separate sections and keys with two underscores. This is probably not a settings you'll
    # want to change, but it's here just in case
    'SECTION_KEY_SEPARATOR': '__',

    # Use this to disable caching of preference. This can be useful to debug things
    'ENABLE_CACHE': True,

    # Use this to disable checking preferences names. This can be useful to debug things
    'VALIDATE_NAMES': True,
}


DBBACKUP_STORAGE = ''
DBBACKUP_STORAGE_OPTIONS = {}

CRONTAB_DJANGO_PROJECT_NAME = 'src'

CRONJOBS = [
    ('*/59 * * * *', 'apps.main.cron.backup_cron', '>> ~/cronjob.log')
]

# Para conectar a SUNI1
LEGACY_URL = {
    'cyd_informe': 'http://funsepa.net/suni/app/src/libs/informe_ca_escuela.php',
    'certificado':'http://funsepa.net/suni/app/cap/par/certificado_cursos.php',
}
LEGACY_CONNECTION = True
LEGACY_TESTING = False

GOOGLE_ANALYTICS_PROPERTY_ID = ''
GOOGLE_ANALYTICS_DOMAIN = ''
# Back End Correos

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'solicitudes_tpe@funsepa.org'
EMAIL_HOST_PASSWORD = 'Funsepa2019'
