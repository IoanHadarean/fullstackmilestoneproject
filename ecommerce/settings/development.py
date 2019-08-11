from .base import *

# DEBUG set to True for development
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = ['30549824a1f0499e91d2634f1137317f.vfs.cloud9.us-east-1.amazonaws.com']

# SQLite database for development
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Empty Sendgrid API key for development
SENDGRID_API_KEY = ''

# Empty Stripe secret key for development
STRIPE_SECRET_KEY = ''
