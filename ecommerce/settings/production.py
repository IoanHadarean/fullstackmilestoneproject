from .base import *

import dj_database_url

# DEBUG set to False for production
DEBUG = True

# AWS ACL
AWS_DEFAULT_ACL = None

# Allowed Hosts
ALLOWED_HOSTS = ['30549824a1f0499e91d2634f1137317f.vfs.cloud9.us-east-1.amazonaws.com', 'e-commerce-web-app.herokuapp.com']

# PostGre SQL database for production
DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}
# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }

# Get Sendgrid API key from environment
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Get Stripe API key from environment
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

