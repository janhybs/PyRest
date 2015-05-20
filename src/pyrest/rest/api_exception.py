# encoding: utf-8
# author:   Jan Hybs
from flask import Response
from werkzeug.exceptions import HTTPException


class ApiException (HTTPException):
    def __init__ (self, detail='not Found', status=404):
        HTTPException.__init__ (self)
        self.detail = detail
        self.status = status

    def get_response (self, environ=None):
        return Response (self.detail, mimetype='application/json', status=self.status)
