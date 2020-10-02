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
    'storages'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# login redirects
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/client/'
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

# For development
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails")

# Send Email using Gmail Account
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'urbancommunication12@gmail.com'
EMAIL_HOST_PASSWORD = "m7FGW@vw1"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'urbancommunication12@gmail.com'  

# AWS SES E-mail Settings
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_REGION = 'eu-west-2'
# AWS_SES_REGION_ENDPOINT = 'email-smtp.eu-west-2.amazonaws.com'



# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'secondProject/media')

# DEBUG_PROPAGATE_EXCEPTIONS = True

# AWS Congifuration
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATICFILES_STORAGE = "secondProject.storage_backends.StaticStorage"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'secondProject.storage_backends.MediaStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# heruku setting
django_heroku.settings(locals())
