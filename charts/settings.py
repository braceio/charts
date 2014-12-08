import os
import hashlib

# load a bunch of environment

DEBUG = os.getenv('DEBUG') in ['True', 'true', '1', 'yes']

#SERVER_NAME = os.getenv('SERVER_NAME')
NONCE_SECRET = os.getenv('NONCE_SECRET')
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379/13')

SERVICE_NAME = os.getenv('SERVICE_NAME') or 'Charts'
SERVICE_URL = os.getenv('SERVICE_URL') or 'http://myapp.com'
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL') or 'team@myapp.com'
API_ROOT = os.getenv('API_ROOT') or '//api.myapp.com'
FORMS_API = os.getenv('FORMS_API') or '//forms.brace.io'
