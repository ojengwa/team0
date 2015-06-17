from datetime import datetime
from httplib2 import Http

from app import db


class User(db.Document):
    id = db.ObjectIdField(required=True)


class PDFFile(db.Document):
    id = db.ObjectIdField(required=True)
    url = db.URLField()
    content = db.FileField(required=True)
    owner = db.ObjectIdField()
    created_at = db.DateTimeField(default=datetime.now, required=True)


class ConversionRequest(db.Document):
    user_id = db.ObjectIdField()
    url = db.URLField(required=True)
    created_at = db.DateTimeField(default=datetime.now, required=True)

    def validate(self, clean=True):
        db.Document.validate(self, clean)
        
        (head, _) = (Http()).request(self.url, 'HEAD')
        if head.status >= 400:
            raise db.ValidationError('ValidationError', errors={'url': str(self.url) + ' is unreachable (status = ' + str(head.status) + ')'})
