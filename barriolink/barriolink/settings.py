"""
Django settings for barriolink project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from decouple import config
from pathlib import Path
import os
from typing import (List, Dict, Tuple, Any)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.0','localhost', '3.86.91.69', '0.0.0.0', '127.0.0.1','*','barriolink.online', 'localhost:8000']
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') #for use on production ambient

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig', 
    'crispy_forms',
    'crispy_bootstrap5', 
    'telegram',
    'reportlab',
    'certificates',
    'storages',
    'calendarapp',
    
    
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://qmhpr9jr-8000-inspect.brs.devtunnels.ms",# Reemplaza con tu URL base
]

ROOT_URLCONF = 'barriolink.urls'

TEMPLATES: List[Dict[str, Any]] = [
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



WSGI_APPLICATION = 'barriolink.wsgi.application'


AUTH_USER_MODEL = 'main.CustomUser'

AUTHENTICATION_BACKENDS = ['main.backends.EmailBackend']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR , 'db.sqlite3'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "main/static")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/login'


EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

print(os.path.join(BASE_DIR, 'templates'))  # Imprime la ruta a la carpeta de plantillas

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'barriolink' ,'media')


print(MEDIA_URL)
print(MEDIA_ROOT)

STATIC_ROOT = os.path.join(BASE_DIR,'static')
#MEDIA_ROOT = '/home/ubuntu/barrioLink/barrioLink/barriolink/media/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#print(MEDIA_URL)
#print(MEDIA_ROOT)

# SECURE_BROWSER_XSS_FILTER: bool = True
# SECURE_CONTENT_TYPE_NOSNIFF: bool = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
# SECURE_HSTS_SECONDS: int = 31536000  # 365 days = 1 year
# SECURE_REDIRECT_EXEMPT: List[str] = []
# SECURE_SSL_REDIRECT: bool = True
# SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
# CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
# SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

use_s3 = True

if use_s3:
    
   AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.us-west-2.amazonaws.com'
  # AWS_DEFAULT_ACL = 'public-read'

# s3 static settings
   STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
   STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

else:
   STATIC_URL = '/static/'
   
   