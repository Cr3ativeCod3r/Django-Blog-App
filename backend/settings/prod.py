"""
Django production settings for backend project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# TODO: Configure production hosts
ALLOWED_HOSTS = ['yourdomain.com']


# CORS Configuration for production
# TODO: Configure production origins
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
]

CORS_ALLOW_CREDENTIALS = True

# Database connection pooling for production
DATABASES['default']['CONN_MAX_AGE'] = 600
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
}

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

