# encoding: utf-8
# author:   Jan Hybs
from flask import Response, request
from flask_classy import FlaskView
import transaction
from werkzeug.exceptions import HTTPException
from pyrest import db
from pyrest.rest.api_exception import ApiException
from pyrest.server.flask_utils import json_response


class JobsApi (FlaskView):
    def _raise (self, detail="Job doesn't exist", status=404):
        """
        Method will raise ApiException with given details when called
        :param detail:
        :param status:
        :return:
        """
        raise ApiException (detail, status)

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
        job = db.jobs.get (id) or self._raise ()

        return job.as_dict (peek=False)

    @json_response
    def put (self, id):
        """
        API for updating instance
        :param id:
        :return:
        """
        json = request.json or self._raise ('No data received')
        job_name = json.get ('name') or self._raise ('No job name specified')
        job = db.jobs.get (id) or self._raise ()

        job.name = job_name
        transaction.commit ()

        return { 'update': 'ok' }


    @json_response
    def patch (self, id):
        """
        API for updating part of instance
        :param id:
        :return:
        """
        self._raise ('Not supported', 500)


    @json_response
    def delete (self, id):
        """
        API for deleting instance
        :param id:
        :return:
        """
        job = db.jobs.get (id) or self._raise ('no such job')
        for script in job.get_scripts():
            job.remove_script (script)
            del db.scripts[script.id]
        del db.jobs[id]
        transaction.commit ()

        return { 'delete': 'ok' }