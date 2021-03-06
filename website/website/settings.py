"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy

load_dotenv(verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False) != 'False'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    os.getenv('DOMAIN', ''),
    'www.' + os.getenv('DOMAIN', ''),
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'taggit',
    'mptt',
    'diggers',
    'django.contrib.admin',
    'django.contrib.auth',
    'django_cleanup.apps.CleanupConfig',
    'widget_tweaks',
    'captcha',
    'django.forms',
    'django_bleach',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'diggers.middlewares.BanManagement',
    'diggers.middlewares.LastActivityMiddleware',
]

ROOT_URLCONF = 'website.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', ''),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PROFILE_AVATAR_SIZE = (80, 80)

TAGGIT_CASE_INSENSITIVE = True

AUTH_USER_MODEL = 'diggers.User'

POSTS_PER_PAGE = 10

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
REGISTRATION_SALT = os.getenv('REGISTRATION_SALT', '')

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False) == 'True'
DEFAULT_FROM_EMAIL = 'noreply@diggers.kiev.ua'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

LOGIN_URL = reverse_lazy('login')
LOGOUT_REDIRECT_URL = 'diggers:post_list'

BLEACH_ALLOWED_TAGS = [
    'p',
    'b',
    'i',
    'u',
    'em',
    'ul',
    'ol',
    'li',
    'dl',
    'dd',
    'dt',
    'strong',
    'del',
    'small',
    'code',
    'abbr',
    'mark',
    'a',
    'table',
    'tr',
    'td',
    'th',
    'thead',
    'tbody',
    'caption',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'span',
    'img',
    'br',
    'iframe',
    'figure',
    'figcaption',
    'blockquote',
    'cite',
    'aside',
]
BLEACH_ALLOWED_ATTRIBUTES = [
    'href',
    'allow',
    'title',
    'target',
    'alt',
    'src',
    'height',
    'width',
    'class',
    'cite',
    'href',
    'data-oembed-url',
    'style',
    'allowfullscreen',
    'frameborder',
    'mozallowfullscreen',
    'webkitallowfullscreen',
]
BLEACH_ALLOWED_STYLES = [
    'width',
    'height',
    'position',
]
BLEACH_ALLOWED_IFRAME_SRC = [
    'youtube.com',
    'www.youtube.com',
]
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

admin_name = os.getenv('ADMIN_NAME', None)
admin_email = os.getenv('ADMIN_EMAIL', None)

if admin_email and admin_name:
    ADMINS = [(admin_name, admin_email)]
