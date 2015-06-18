from datetime import datetime
from httplib2 import Http

from app import db


class PDFFile(db.Document):
    id = db.ObjectIdField(required=True)
    html_url = db.URLField()
    url = db.URLField()
    content = db.FileField(required=True)
    owner = db.EmailField()
    created_at = db.DateTimeField(default=datetime.now, required=True)


class ConversionRequest(db.Document):
    id = db.ObjectIdField(required=True)
    user_id = db.EmailField()
    url = db.URLField(required=True)
    created_at = db.DateTimeField(default=datetime.now, required=True)

    def validate(self, clean=True):
        db.Document.validate(self, clean)
        
        (head, _) = (Http()).request(self.url, 'HEAD')
        if head.status >= 400:
            raise db.ValidationError('ValidationError', errors={'url': str(self.url) + ' is unreachable (status = ' + str(head.status) + ')'})


class SearchRequest(db.Document):
    owner = db.EmailField()
    from_date = db.ListField(db.DateTimeField)
    to_date = db.ListField(db.DateTimeField)
