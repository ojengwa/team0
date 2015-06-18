import os
import pymongo

SERVER_SETTINGS = {
    'host': os.environ.get('ANDELA_PROJECT2_BACKEND_HOST', '127.0.0.1'),
    'port': int(os.environ.get('PORT', 5000)),
    'debug': bool(int(os.environ.get('ANDELA_PROJECT2_BACKEND_DEBUG', 1)))
}

MONGODB_SETTINGS = {
    'db':   os.environ.get('ANDELA_PROJECT2_DB', 'project2'),
    'host': os.environ.get('ANDELA_PROJECT2_DB_HOST', 'localhost'),
    'port': int(os.environ.get('ANDELA_PROJECT2_DB_PORT', 27017)),
    'read_preference': pymongo.read_preferences.ReadPreference.PRIMARY
}

