"""
Django settings for assimilation project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import configparser
import json
import logging
import raven

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(BASE_DIR + "/settingsConfigFile.ini")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'so*0-@g9j!m%+&34f9a4iou-1b4$e-%ywtvawm@f!&o2ftx^nk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean("django","DEBUG")

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'api',
    'webview',
    'raven.contrib.django.raven_compat',

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

ROOT_URLCONF = 'assimilation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
      'django': {
         'format':'django:%(asctime)s %(module)s Line:%(lineno)d %(message)s',
       },
    'django-local': {
         'format':'%(module)s Line:%(lineno)d %(message)s',
       },
    },

   'handlers': {
      'logging.handlers.SysLogHandler': {
         'level': 'DEBUG',
         'class': 'logging.handlers.SysLogHandler',
         'facility': 'local7',
         'formatter': 'django',
         'address' : '/dev/log',
       },
        'sentry': {
            'level': 'DEBUG', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'assimilation-django'},
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'django-local',
        },
   },

   'loggers': {
      'loggly_logs':{
         'handlers': ['logging.handlers.SysLogHandler'],
         'propagate': True,
         'format':'django:%(asctime)s %(module)s Line:%(lineno)d %(message)s',
         'level': 'DEBUG',
       },
    'local': {
            'handlers': ['console'],
            'format':'%(module)s Line:%(lineno)d %(message)s',
            'level':"INFO",
        },
    }
}
LOGGER = logging.getLogger(config.get("django","LOGGER"))

WSGI_APPLICATION = 'assimilation.wsgi.application'

RAVEN_CONFIG = {
    'dsn': config.get("django","SENTRY_DSN"),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': config.get("django","ENGINE"),
        'NAME': config.get("django","NAME"),
        'USER': config.get("django","USER"),
        'PASSWORD': config.get("django","PASSWORD"),
        'HOST': config.get("django","HOST"),
        'PORT': config.get("django","PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

SECURE_SSL_REDIRECT = config.getboolean("django","SSL_REDIRECT")
CSRF_COOKIE_SECURE = config.getboolean("django","SSL_REDIRECT")
SESSION_COOKIE_SECURE = config.getboolean("django","SSL_REDIRECT")


ATTENDANCE_TAKER_GROUP_NAME = "attendanceTakers"
SUPER_ADMINS_GROUP_NAME = "superadmins"
GYMKHANA_GSEC_GROUP_NAME = "gymkhanaGsec"
STUDENT_GROUP_NAME = "student"

GROUPS_MAP = {
    "dep_cs": "CS Department",
    "dep_ee": "EE Department",
    "dep_ag": "AG Department",
    "dep_hs": "HS Department",
    "dep_im": "IM Department",
    "dep_me": "ME Department",
    "dep_na": "NA Department",
    "dep_ch": "CH Department",
    "dep_gg": "GG Department",
    "dep_ma": "MA Department",
    "dep_mi": "MI Department",
    "dep_mt": "MT Department",
    "dep_ph": "PH Department",
    "dep_ae": "AE Department",
    "dep_ar": "AR Department",
    "dep_ce": "CE Department",
    "dep_ec": "EC Department",
    "dep_bt": "BT Department",
    "dep_cy": "CY Department",
    "dep_bs": "BS Department",
    "hall_rph": "RPH Hall",
    "hall_lbs": "LBS Hall",
    "hall_mmh": "MMH Hall",
    "hall_sn/ig": "SN/IG Hall",
    "hall_mth": "MTH Hall",
    "hall_azd": "AZD Hall",
    "hall_rkh": "RKH Hall",
    "hall_nhr": "NHR Hall",
    "hall_pat": "PAT Hall",
    SUPER_ADMINS_GROUP_NAME : "All Students",
    GYMKHANA_GSEC_GROUP_NAME : "All Students",
    "student" : "All Students",
}

FCM_SERVER_KEY = config.get("django","FCM_SERVER_KEY")