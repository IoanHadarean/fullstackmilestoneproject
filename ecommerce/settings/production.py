from .base import *

import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['e-commerce-web-app.herokuapp.com']

DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))}

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

