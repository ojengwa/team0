from datetime import datetime, date
from httplib2 import ServerNotFoundError, CertificateHostnameMismatch

from flask import request, jsonify, url_for, make_response,json
from pdfkit import from_url as pdf_from_url

from time import clock

from app import app
from app import db
from models import ConversionRequest, PDFFile


@app.route('/')
def it_works():
    # Just to check if everything is correctly set up.
    return 'it works!'


@app.route('/v1/files', methods=['GET', 'POST'])
def files():
    """Creates a new PDF file from a web page or retrieves a list of PDF
       files stored in the database, depending on the HTTP method of the request."""
    if request.method == 'GET':
        return get_files()

    conversion_request = ConversionRequest(**request.get_json())

    # Call save() to validate the URL provided in the request body.
    conversion_request.save()

    initial_time = clock()

    pdf = PDFFile(html_url=conversion_request.url, owner=conversion_request.user_id)
    pdf.content.new_file()
    pdf.content.write(pdf_from_url(str(conversion_request.url), False))
    pdf.content.close()
    pdf.save()

    processing_time = clock() - initial_time

    return jsonify(id=str(pdf.id),
                   html_url=pdf.html_url,
                   url=url_for('get_file', id=pdf.id, _external=True),
                   created_at=pdf.created_at.isoformat(),
                   owner=pdf.owner,
                   processing_time=str(processing_time) + " second(s)"), 201


@app.route('/v1/files/<id>', methods=['GET'])
def get_file(id):
    """Retrieves the PDF file matching <id>."""
    pdf = PDFFile.objects.get(id=id)

    return pdf.content.read(), 200, {'Content-Disposition': 'attachment; filename=' + str(id) + '.pdf'}


def get_files():
    """Retrieves a list of PDF files stored in the database.
       Depending on the request URL parameters, the list may be
       filtered on the properties <owner> and <created_at>.
       The list is sorted in decreasing order by the property <created_at>."""
    user_id = request.args.get('owner')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    files = PDFFile.objects

    if user_id is not None:
        files = files.filter(owner=user_id)

    if from_date is not None:
        files = files.filter(created_at__gte=datetime.strptime(from_date, '%d/%m/%Y'))

    if to_date is not None:
        files = files.filter(created_at__lte=datetime.strptime(to_date, '%d/%m/%Y'))

    files = files.order_by('-created_at')

    return jsonify(files=[{'id': str(file.id),
                           'html_url': file.html_url,
                           'url': url_for('get_file', id=file.id, _external=True),
                           'created_at': file.created_at.isoformat(),
                           'owner': file.owner} for file in files]), 200


@app.errorhandler(db.ValidationError)
def handle_validation_error(error):
    """Returns a 422 HTTP response if there is an error when validating a model."""
    if error.message.find('not a valid ObjectId') != -1:
        return jsonify(error='no pdf file here'), 404

    return jsonify(errors=[{'field': key, 'message': value} for key, value in error.to_dict().iteritems()]), 422


@app.errorhandler(ServerNotFoundError)
def handle_server_not_found_error(error):
    """Returns a 422 HTTP response if the server at the URL specified in the request."""
    return jsonify(errors=[{'field': 'url', 'message': error.message}]), 422


@app.errorhandler(db.DoesNotExist)
def handle_does_not_exist(error):
    """Returns a 404 HTTP response if there is no PDF matching the ID
       specified in the request GET /v1/files/<id>."""
    return jsonify(error='no pdf file here'), 404


@app.errorhandler(db.FieldDoesNotExist)
def handle_field_does_not_exist(error):
    """Returns a 422 HTTP response if there is an unrecognized field
       in a request body."""
    return jsonify(error='unrecognized field'), 422


@app.errorhandler(CertificateHostnameMismatch)
def handle_certificate_hostname_mismatch(error):
    """Returns a 422 HTTP response if there is a certificate problem with an URL provided in a request."""
    return jsonify(errors=[{'field': 'url', 'message': 'the certificate presented by the server does not match the host ' + str(error.host)}]), 422


@app.errorhandler(IOError)
def handle_io_error(error):
    """Returns a 422 HTTP response if an IOError is raised, mainly when the document at
       the URL to convert to PDF is not a web page."""
    return jsonify(errors=[{'field': 'url', 'message': 'the document at this URL does not seem to be a web page'}]), 422
