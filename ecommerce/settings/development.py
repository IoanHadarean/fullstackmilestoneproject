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

# Stripe secret key for development (not used in production)
STRIPE_SECRET_KEY = ''

# Django secret key for development (not used in production)
SECRET_KEY = '!4xm)v#w)=7pv)d8z+8p_o8t)bb5p3kbucoj%a0h2t)b1h)e(r'
