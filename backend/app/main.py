from datetime import datetime, date
from httplib2 import ServerNotFoundError

from flask import request, jsonify, url_for, make_response,json
from pdfkit import from_url as pdf_from_url

from time import clock

from app import app
from app import db
from models import ConversionRequest, PDFFile, SearchRequest


@app.route('/')
def it_works():
    return 'it works!'


@app.route('/v1/files', methods=['GET', 'POST'])
def files():
    if request.method == 'GET':
        return get_files()

    conversion_request = ConversionRequest(**request.get_json())
    conversion_request.save()

    initial_time = clock()

    pdf = PDFFile(html_url=conversion_request.url, owner=conversion_request.user_id)
    pdf.content.new_file()
    pdf.content.write(pdf_from_url(str(conversion_request.url), False))
    pdf.content.close()
    pdf.save()

    pdf.url = url_for('get_file', id=pdf.id, _external=True)

    final_time = clock() - initial_time

    return jsonify(id=str(pdf.id), html_url=pdf.html_url, url=pdf.url, created_at=pdf.created_at.isoformat(), owner=pdf.owner,
        final_time=str(final_time)), 201


@app.route('/v1/files/<id>', methods=['GET'])
def get_file(id):
    pdf = PDFFile.objects.get(id=id)

    return pdf.content.read(), 200, {'Content-Disposition': 'attachment; filename=' + str(id) + '.pdf'}


def get_files():
    searchRequest = SearchRequest(owner=request.args.get('owner'), from_date=request.args.get('from_date'),
        to_date=request.args.get('to_date'))
    searchRequest.save()

    history = []
    user_name = searchRequest.owner
    from_date = searchRequest.from_date
    to_date = searchRequest.to_date

    if to_date is not None and from_date is not None:
        for pdfFile in PDFFile.objects(owner=user_name):
            if pdfFile.created_at.date >= from_date.date and pdfFile.created_at.date <= to_date.date:
                history.append(pdfFile)

    elif to_date is not None and from_date is not None and user_name is None:
        for pdfFile in PDFFile.objects():
            history.append(pdfFile)

    else:
        for pdfFile in PDFFile.objects(owner=user_name):
            history.append(pdfFile)

    if history:
        return jsonify(pdfFile = history), 200
    else:
        return "It is working"

@app.errorhandler(db.ValidationError)
def handle_validation_error(error):
    if error.message.find('not a valid ObjectId') != -1:
        return jsonify(error='no pdf file here'), 404

    return jsonify(errors=[{'field': key, 'message': value} for key, value in error.to_dict().iteritems()]), 422


@app.errorhandler(ServerNotFoundError)
def handle_server_not_found_error(error):
    return jsonify(errors=[{'field': 'url', 'message': error.message}]), 422


@app.errorhandler(db.DoesNotExist)
def handle_does_not_exist(error):
    return jsonify(error='no pdf file here'), 404

@app.errorhandler(db.FieldDoesNotExist)
def handle_field_does_not_exist(error):
    return jsonify(error='unrecognized field'), 422
