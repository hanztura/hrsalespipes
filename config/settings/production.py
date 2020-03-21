from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.setdefault('HRSALESPIPES_ALLOWED_HOST', '')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.setdefault('HRSALESPIPES_DATABASE_NAME', ''),
        'USER': os.environ.setdefault('HRSALESPIPES_DATABASE_USER', ''),
        'PASSWORD': os.environ.setdefault(
            'HRSALESPIPES_DATABASE_PASSWORD',
            ''),
        'HOST': os.environ.setdefault('HRSALESPIPES_DATABASE_HOST', ''),
        'PORT': os.environ.setdefault('HRSALESPIPES_DATABASE_PORT', ''),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
