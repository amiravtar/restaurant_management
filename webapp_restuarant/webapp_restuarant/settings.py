"""
Django settings for webapp_restuarant project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&3y(a!xl^5is14==7+c8em+icm7h_!8a(hm5x-1u(m)8y439+1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "jalali_date",
    "deliver",
    "food",
    "order",
    "restaurant",
    "pages",
    "panel",
    "user",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "webapp_restuarant.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webapp_restuarant.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# dir that collect static will put static file in
STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
# url that statics will serve on
STATIC_URL = "/static/"
# url that will server medai(uploaded from users)
MEDIA_URL = "/media/"
# folder that files uploaded from users go in
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# log setting
LOG_DIR = "logs"
LOGGING_LEVEL = "DEBUG"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_general": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, LOG_DIR, "general.log"),
            "formatter": "file",
        },
        "file_app": {
            "level": LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, LOG_DIR, "app.log"),
            "formatter": "file",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "level": LOGGING_LEVEL,
        },
    },
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "loggers": {
        "": {
            "handlers": ["file_general"],
            "level": LOGGING_LEVEL,
        },
        "app": {
            "handlers": ["file_app", "console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

LOGIN_REDIRECT_URL = reverse_lazy("restaurant:Index")
LOGIN_URL = reverse_lazy("user:Login")
LOGOUT_REDIRECT_URL = reverse_lazy("user:Login")

# default settings for Jalali date plugin
JALALI_DATE_DEFAULTS = {
    "Strftime": {
        "date": "%y/%m/%d",
        "datetime": "%H:%M:%S _ %y/%m/%d",
    },
    "Static": {
        "js": [
            # loading datepicker
            "admin/js/django_jalali.min.js",
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        "css": {
            "all": [
                "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            ]
        },
    },
}
