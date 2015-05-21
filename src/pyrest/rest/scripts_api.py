# encoding: utf-8
# author:   Jan Hybs
from flask import Response, request
from flask_classy import FlaskView
import transaction
from werkzeug.exceptions import HTTPException
from pyrest import db
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.database.sets.script import ScriptManagementApplication
from pyrest.rest.api_exception import ApiException
from pyrest.server.flask_utils import json_response


class ScriptsApi (FlaskView):
    def _raise (self, detail="Script doesn't exist", status=404):
        """
        Method will raise ApiException with given details when called
        :param detail:
        :param status:
        :return:
        """
        raise ApiException (detail, status)

    @json_response
    def index (self):
        """
        API for list dir of this collection
        :return:
        """
        scripts = db.scripts.search (sort="start_at")
        script_list = [script.as_dict () for script in scripts]
        return script_list

    @json_response
    def get (self, id):
        """
        API get instance
        :param id: job id
        :return:
        """
        script = db.scripts.get (id) or self._raise ()

        return script.as_dict ()

    @json_response
    def post (self):
        """
        API for creating new instance
        :return:
        """

        # prepare for creation
        json = request.json or self._raise ('No data received')
        job_id = json.get ('job_id') or self._raise ('No job id specified')
        job = db.jobs.get (job_id) or self._raise ("Job doesn't exist")

        # create script and commands
        script = ScriptManagementApplication.create (**json)
        commands = json['commandsNew'].splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)

        # save to db
        job.add_script (script)
        db.scripts.add (script)
        transaction.commit ()

        return { 'script_id': script.id }

    @json_response
    def put (self, id):
        """
        API for updating instance
        :param id:
        :return:
        """

        # preparation
        json = request.json or self._raise ('No data received')
        job_id = json.get ('job_id') or self._raise ('No job id specified')
        job = db.jobs.get (job_id) or self._raise ("Job doesn't exist")
        script = db.scripts.get (id) or self._raise ()

        # creating new commands
        commands = json['commandsNew'].splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)
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
        script = db.scripts.get (id) or self._raise ()
        job = db.jobs.get(script.job_id) or self._raise ("Job doesn't exist")
        job.delete_script (script)

        del db.scripts[id]
        transaction.commit ()

        return { 'delete': 'ok' }