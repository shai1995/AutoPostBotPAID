from os import environ


API_ID = int(environ.get('API_ID', ''))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
ADMIN = environ.get('ADMIN', '')

MONGO_DB_URL = environ.get('MONGO_DB_URL', '')

