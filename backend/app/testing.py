import os
import unittest

import pymongo

from app import db
from main import main
from models import PDFFile, SearchRequest, ConversionRequest
from app import app

import json

class TestCase(unittest.TestCase):
    def setup(self):
        app.config['SERVER_SETTINGS'].host = os.environ.get('ANDELA_PROJECT2_BACKEND_HOST', '127.0.0.1')
        app.config['SERVER_SETTINGS'].port = int(os.environ.get('PORT', 5000))
        app.config['SERVER_SETTINGS'].debug = bool(int(os.environ.get('ANDELA_PROJECT2_BACKEND_DEBUG', 1)))
        app.config['MONGODB_SETTINGS'].db = os.environ.get('ANDELA_PROJECT2_DB', 'project2')
        app.config['MONGODB_SETTINGS'].host = os.environ.get('ANDELA_PROJECT2_DB_HOST', 'localhost')
        app.config['MONGODB_SETTINGS'].port = int(os.environ.get('ANDELA_PROJECT2_DB_PORT', 27017))
        app.config['MONGODB_SETTINGS'].read_preference = pymongo.read_preferences.ReadPreference.PRIMARY
        
    def test_init(self):
        init = main.it_works()
        expected = "it works!"
        self.assertEqual(expected == init)
    
    def test_files(self):
        tester = main.files(self)
        response = tester.get('//v1/files?owner=fade&from_date=10101010001&to_date=3030049495855', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # check that the result sent is "It is working"
        self.assertEqual(response.data, "It is equal")
