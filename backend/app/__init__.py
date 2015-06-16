from flask import Flask
from flask.ext.mongoengine import MongoEngine

from app import config

app = Flask(__name__)
db = MongoEngine()

app.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS

db.init_app(app)

from app import main
