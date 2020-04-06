"""
Django settings for hrsalespipes project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
import secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('hrsalespipes')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.setdefault('HRSALESPIPES_SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_admin_env_notice',
    'admin_honeypot',
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_extensions',
    'guardian',
    'rest_framework',
    'django_filters',
    'import_export',
    'simple_history',

    'system',
    'commissions',
    'contacts',
    'jobs',
    'salespipes',
    'dashboard',
    'reports',
    'backups',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [APPS_DIR.path('templates'), 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_admin_env_notice.context_processors.from_settings',

                'system.context_processors.get_icons',
                'system.context_processors.get_system_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
BACKUPS_STORAGE_ROOT = ROOT_DIR.path('db').path('backups')
ENABLE_IMPORT_EXPORT_IN_ADMIN = os.environ.setdefault(
    'HRSALESPIPES_ENABLE_ENABLE_IMPORT_EXPORT_IN_ADMIN', 'no')

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
]

AUTH_USER_MODEL = 'system.User'

# admin url is random if not set with value
RANDOM_ADMIN_URL = '{}/'.format(secrets.token_urlsafe(6))
ADMIN_URL = os.environ.setdefault('HRSALESPIPES_ADMIN_URL', RANDOM_ADMIN_URL)


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.setdefault('HRSALESPIPES_TIME_ZONE', 'UTC')

USE_I18N = False

USE_L10N = False

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59',
    '%Y-%m-%dT%H:%M',        # '2006-10-25T14:30'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

LOGIN_URL = 'system:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'system:home'

INTERNAL_IPS = ('127.0.0.1', 'localhost', '192.168.1.12')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# project instance settings
JOB_REFERENCE_NUMBER_ALIAS = os.environ.setdefault(
    'HRSALESPIPES_JOB_REFERENCE_NUMBER_ALIAS', 'Job Reference Number')
JOB_DATE_ALIAS = os.environ.setdefault(
    'HRSALESPIPES_JOB_DATE_ALIAS', 'Date')
JOB_POTENTIAL_INCOME_ALIAS = os.environ.setdefault(
    'HRSALESPIPES_JOB_POTENTIAL_INCOME_ALIAS', 'Potential Income')
JOB_CANDIDATE_ACTUAL_INCOME_ALIAS = os.environ.setdefault(
    'HRSALESPIPES_JOB_CANDIDATE_ACTUAL_INCOME_ALIAS', 'Actual Income')
PIPELINE_DATE_ALIAS = os.environ.setdefault(
    'HRSALESPIPES_PIPELINE_DATE_ALIAS', 'Date')
COMMISSION_RATE_ROLE_TYPE_ONE_ALIAS = os.environ.setdefault(
    'COMMISSION_RATE_ROLE_TYPE_ONE_ALIAS', 'Level One')
COMMISSION_RATE_ROLE_TYPE_TWO_ALIAS = os.environ.setdefault(
    'COMMISSION_RATE_ROLE_TYPE_TWO_ALIAS', 'Level Two')
COMMISSION_RATE_ROLE_TYPE_THREE_ALIAS = os.environ.setdefault(
    'COMMISSION_RATE_ROLE_TYPE_THREE_ALIAS', 'Level Three')
COMMISSION_RATE_ROLE_TYPE_OTHERS_ALIAS = os.environ.setdefault(
    'COMMISSION_RATE_ROLE_TYPE_OTHERS_ALIAS', 'Others')

# GRAPPELLI
GRAPPELLI_ADMIN_TITLE = os.environ.setdefault(
    'HRSALESPIPES_ADMIN_TITLE', 'HRSalesPipes')

ENVIRONMENT_NAME = "Production server"
ENVIRONMENT_COLOR = "#FF2222"
ENVIRONMENT_FLOAT = True

# system wide icons
ICON_DASHBOARD = 'mdi-view-dashboard-variant'
ICON_CONTACTS = 'mdi-contacts'
ICON_JOBS = 'mdi-briefcase-search'
ICON_PIPELINE = 'mdi-pipe'
ICON_REPORTS = 'mdi-file-document'
ICON_COMMISSIONS = 'mdi-calculator'
ICON_BACKUPS = 'mdi-database'
ICON_ACCOUNT = 'mdi-account-circle'
ICON_CANDIDATES = 'mdi-account-tie'
ICON_CLIENTS = 'mdi-currency-usd'
ICON_SUPPLIERS = 'mdi-truck'

PROJECT_NAME = 'HRSalesPipes'
PROJECT_VERSION = '1.0'
