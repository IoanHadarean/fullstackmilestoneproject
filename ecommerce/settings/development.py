from .base import *

DEBUG = True

ALLOWED_HOSTS = ['30549824a1f0499e91d2634f1137317f.vfs.cloud9.us-east-1.amazonaws.com']

# Database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
SENDGRID_API_KEY = ''
STRIPE_SECRET_KEY = ''