# heruko import
import django_heroku

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    'https://urbancommunications.herokuapp.com',
    'urbancommunications.herokuapp.com'
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'clientApp.apps.ClientappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'secondProject.middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'secondProject.urls'

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

WSGI_APPLICATION = 'secondProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("db_name"),
        'USER': os.getenv("db_user"),
        'PASSWORD': os.getenv("db_password"),
        'HOST': os.getenv("db_host"),
        'PORT': os.getenv("db_port"),
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
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# login redirects
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/client'
LOGOUT_REDIRECT_URL = '/accounts/login'

LOGIN_EXEMPT_URLS = (
    r'^accounts/login/$',
    r'^accounts/logout/$',
    r'^client/signup/$',
    r'^accounts/password_reset/$',
    r'^accounts/password_reset/done/$',
    r'^accounts/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
    r'^accounts/reset/done/$',
    r'^accounts/password_reset/complete/$',   
)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'secondProject/media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static'),]


DEBUG_PROPAGATE_EXCEPTIONS = True


# heruku setting
django_heroku.settings(locals())