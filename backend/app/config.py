import os
import pymongo

MONGODB_SETTINGS = {
    'db':   os.environ.get('ANDELA_PROJECT2_DB', 'project2'),
    'host': os.environ.get('ANDELA_PROJECT2_HOST', 'localhost'),
    'port': os.environ.get('ANDELA_PROJECT2_PORT', 27017),
    'read_preference': pymongo.read_preferences.ReadPreference.PRIMARY
}
