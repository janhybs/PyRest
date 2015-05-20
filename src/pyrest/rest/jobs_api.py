# encoding: utf-8
# author:   Jan Hybs
from flask import Response, request
from flask_classy import FlaskView
from werkzeug.exceptions import HTTPException
from pyrest import db
from pyrest.rest.api_exception import ApiException
from pyrest.server.flask_utils import json_response


class JobsApi (FlaskView):
    @json_response
    def index (self):
        jobs = db.jobs.search (sort="name")
        job_list = [job.as_dict (peek=True) for job in jobs]
        return job_list

    @json_response
    def get (self, id):
        """
        API get instance
        :param id: job id
        :return:
        """
        job = db.jobs.require (id, 'no such job')

        return job.as_dict (peek=False)

    @json_response
    def put (self, id):
        """
        API for updating instance
        :param id:
        :return:
        """
        raise ApiException ('Not supported', 500)

    @json_response
    def patch (self, id):
        """
        API for updating part of instance
        :param id:
        :return:
        """
        raise ApiException ('Not supported', 500)


    @json_response
    def delete (self, id):
        """
        API for deleting instance
        :param id:
        :return:
        """
        job = db.jobs.require (id, 'no such job')
        del db.jobs[id]
        return { 'delete': 'ok' }