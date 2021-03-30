"""
Django settings for mb_initiative project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!qof+ch(!97u_q#@=t_x*ctj)&4xi%sf@v6btijm%$mtvkyeu&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.izboljsajmo-maribor.djnd.si', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'behaviors.apps.BehaviorsConfig',
    'rest_framework',
    'django_filters',
    'rest_framework_gis',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'corsheaders',
    'admin_ordering',
    'import_export',

    'initiatives',
    'about',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'mb_initiative.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mb_initiative.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': ({
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('SECRET_DB_NAME', ''),
        'USER': os.getenv('SECRET_DB_USERNAME', ''),
        'PASSWORD': os.getenv('SECRET_DB_PASSWORD', ''),
        'HOST': os.getenv('POSTGIS_SERVICE_HOST', ''),
        'PORT': '5432',
    } if os.getenv('APP_ENV', 'development') == 'production' else {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'postgis',
        'NAME': 'mb-initiative',
        'USER': 'postgres',
        'PASSWORD': 'initititit'
    })
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files')
]

STATIC_URL = os.getenv('STATIC_URL_BASE', '') + '/static/'
MEDIA_URL = os.getenv('MEDIA_URL_BASE', '') + '/media/'

ROOT_DIR = '/files/' if os.getenv('APP_ENV', 'development') == 'production' else BASE_DIR

STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

AUTH_USER_MODEL = "initiatives.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',

    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '290563391104397'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b3fea1fb795be35953e003404675c3c4'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '751466585012-48dl84f6odf3bejj6t5p8uofp22mlphf.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '-pZ_G2ox72IG1LerwZc8uNtw'

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}

CORS_ALLOW_ALL_ORIGINS = True

FRONT_URL = os.getenv('FRONT_URL', 'http://localhost:3000/')

if os.getenv('APP_ENV', 'development') == 'production':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', '')
    EMAIL_PORT = os.getenv('EMAIL_PORT', '')
    EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_USE_TLS = True
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'dummy@email.com')

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FROM_EMAIL = 'dummy@email.com'
