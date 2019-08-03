from .base import *

import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['30549824a1f0499e91d2634f1137317f.vfs.cloud9.us-east-1.amazonaws.com', 'e-commerce-web-app.herokuapp.com']

DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

