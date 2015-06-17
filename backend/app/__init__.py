from flask import Flask
from flask.ext.cors import CORS
from flask.ext.mongoengine import MongoEngine

from app import config

app = Flask(__name__)
CORS(app, resources=r'/v1/*', allow_headers='Content-Type')

db = MongoEngine()

app.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
app.config['SERVER_SETTINGS'] = config.SERVER_SETTINGS

db.init_app(app)

from app import main
