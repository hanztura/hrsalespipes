from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

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
        'HOST': os.environ.setdefault('HRSALESPIPES_DATABASE_HOST', 'localhost'),
        'PORT': os.environ.setdefault('HRSALESPIPES_DATABASE_PORT', ''),
    }
}
