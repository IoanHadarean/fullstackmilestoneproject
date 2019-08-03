from .base import *

import env
import dj_database_url

DEBUG = os.environ.get('DEBUG', cast=bool)

ALLOWED_HOSTS = ['e-commerce-web-app.herokuapp.com']

DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}

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

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

