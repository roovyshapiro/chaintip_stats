"""
Django settings for ChaintipStats project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os, json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The secret key is stored in the "credentials.json" file
credentials_file = 'credentials.json'
credentials_path = os.path.join(os.path.abspath('.'), credentials_file)
with open(credentials_path) as f:
    data = f.read()
credential_dict = json.loads(data)
SECRET_KEY = credential_dict['django_secret_key']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reddit_tips',
    'celery',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ChaintipStats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ChaintipStats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery application definition
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
#CELERY_IMPORTS = ['comm.tasks']
CELERY_BROKER_URL = 'redis://localhost:6379'

from celery.schedules import crontab
# https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
# https://docs.celeryproject.org/en/latest/reference/celery.schedules.html#celery.schedules.crontab

# The crontab hour is inclusive.
# crontab(minute='*/11', hour='13-23') Will occur every 11 minutes between the hours of 13:00 UTC and 23:59 UTC. 
# On 12-30-2020, it will run at these times:
# 2020-12-30 13:00:00
# 2020-12-30 13:11:00
# 2020-12-30 13:22:00
# ...
# ...
# 2020-12-30 23:33:00
# 2020-12-30 23:44:00
# 2020-12-30 23:55:00
#
# crontab(minute='0', hour='0-12') Will run at the beginning of every hour between 0:00 UTC and 12:00 UTC.
# On 12-30-2020, it will run at these times:
# 2020-12-30 00:00:00
# 2020-12-30 01:00:00
# 2020-12-30 02:00:00
# ...
# ...
# 2020-12-30 10:00:00
# 2020-12-30 11:00:00
# 2020-12-30 12:00:00
#
# day_of_week
# A (list of) integers from 0-6, where Sunday = 0 and Saturday = 6, that represent the days of a week that execution should occur.
# hour = '*/' is equivalent to 
# Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.
CELERY_BEAT_SCHEDULE = {
    'get_reddit_tips':{
        'task': 'reddit_tips.tasks.get_tips',
        'schedule': crontab(minute='*/15'),
    },
    'get_BCH_price':{
        'task': 'reddit_tips.tasks.get_price',
        'schedule': crontab(minute='*/30'),     
    }
}