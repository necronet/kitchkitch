from werkzeug.exceptions import default_exceptions, HTTPException
from flask import make_response, abort as flask_abort, request
from flask.exceptions import JSONHTTPException


def abort(status_code, body=None, headers={}):
    """
    Content negiate the error response.

    """

    if 'text/html' in request.headers.get("Accept", ""):
        error_cls = HTTPException
    else:
        error_cls = JSONHTTPException

    class_name = error_cls.__name__
    bases = [error_cls]
    attributes = {'code': status_code}

    if status_code in default_exceptions:
        # Mixin the Werkzeug exception
        bases.insert(0, default_exceptions[status_code])

    error_cls = type(class_name, tuple(bases), attributes)
    flask_abort(make_response(error_cls(body), status_code, headers))


def bad_request_response():

    if not request.json:
        reason='Empty body is not allowed please submit the proper data'
    elif not request.json.has_key('items'):
        reason='Body content should include items array. For call %s' % request.url
    elif not isinstance(request.json['items'], (list,tuple)):
        reason='Items must be a json array. Enclose with brackets items:[{}]'

    return abort(400,'Error has occurred, reason %s' % reason )