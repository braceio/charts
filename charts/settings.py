import os

# load a bunch of environment
DEBUG = os.getenv('DEBUG', '').lower() in ['true', '1', 'yes']

NONCE_SECRET = os.getenv('NONCE_SECRET')
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

SERVICE_NAME = os.getenv('SERVICE_NAME') or 'Charts'
SERVICE_URL = os.getenv('SERVICE_URL') or 'http://example.com'
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL') or 'team@example.com'
API_ROOT = os.getenv('API_ROOT') or '//example.com'
FORMS_API = os.getenv('FORMS_API') or '//forms.brace.io' # for collecting feedback on the landing page
