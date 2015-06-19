import os
import unittest
import tempfile

from flask import current_app
from flask.ext.mongoengine import MongoEngine

from app import main
from app import models
from app import db
from app import app


class MainTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['MONGODB_SETTINGS']['db'] = 'project2_test'
        app.config['TESTING'] = True
        db = MongoEngine()
        db.init_app(app)
        self.app = app.test_client()


    def test_it_works(self):
        rv = self.app.get('/')
        self.assertEqual(rv.data, 'it works!', 'GET / should return "it works!"')


    def test_get_pdf_with_invalid_id(self):
        rv = self.app.get('/v1/files/55qfqf')
        self.assertEqual(rv.status_code, 404, 'GET /v1/files/<id> should return a 404 status if <id> is invalid')


    def test_get_files(self):
        rv = self.app.get('/v1/files')
        self.assertEqual(rv.status_code, 200, 'GET /v1/files returns with a 200 status code')


class ConversionRequestTestCase(unittest.TestCase):

    def test_invalid_url(self):
        req = models.ConversionRequest(url='invalid')
        with self.assertRaises(db.ValidationError):
            req.validate()


    def test_invalid_user_id(self):
        req = models.ConversionRequest(user_id='invalidemail@')
        with self.assertRaises(db.ValidationError):
            req.validate()

if __name__ == '__main__':
    unittest.main()