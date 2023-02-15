from .base import *

import dj_database_url
# from ecommerce import env

# DEBUG set to False for production
DEBUG = False

# Allowed Hosts
ALLOWED_HOSTS = ['30549824a1f0499e91d2634f1137317f.vfs.cloud9.us-east-1.amazonaws.com', 'e-commerce-web-app.herokuapp.com',
                 '127.0.0.1']

# PostGre SQL database for production
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASES = {
    'default': dj_database_url.config(),
}

# Get Sendgrid API key from environment
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Get Stripe API key from environment
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# Get Django secret key from environment
SECRET_KEY = os.environ.get("SECRET_KEY")

# Get AWS ACCESS KEY ID and AWS SECRET ACCESS KEY from environment
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

