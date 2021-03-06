from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']
ADMIN_URL = 'sysadmin/'

INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'local.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.setdefault(
            'HRSALESPIPES_DATABASE_NAME', 'hrsalespipes'),
        'USER': os.environ.setdefault(
            'HRSALESPIPES_DATABASE_USER', 'hrsalespipes'),
        'PASSWORD': os.environ.setdefault(
            'HRSALESPIPES_DATABASE_PASSWORD',
            'hrsalespipes'),
        'HOST': os.environ.setdefault(
            'HRSALESPIPES_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.setdefault('HRSALESPIPES_DATABASE_PORT', ''),
    }
}
ENABLE_IMPORT_EXPORT_IN_ADMIN = 'yes'

ENVIRONMENT_NAME = "Devlopment server"
ENVIRONMENT_COLOR = "#9E9E9E"

COMPRESS_ENABLED = True
