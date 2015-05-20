# encoding: utf-8
# author:   Jan Hybs
from flask import Response, request
from flask_classy import FlaskView
from werkzeug.exceptions import HTTPException
from pyrest import db
from pyrest.database.sets.command import CommandManagementApplication
from pyrest.database.sets.script import ScriptManagementApplication
from pyrest.rest.api_exception import ApiException
from pyrest.server.flask_utils import json_response


class ScriptsApi (FlaskView):
    @json_response
    def index (self):
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
        script = db.scripts.require (id, 'no such script')

        return script.as_dict ()

    @json_response
    def post (self):
        """
        API for creating new instance
        :return:
        """
        # todo job id

        if request.json is None:
            raise ApiException ('No data received')

        script = ScriptManagementApplication.create ()
        commands = request.json['commandsNew'].splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)

    @json_response
    def put (self, id):
        """
        API for updating instance
        :param id:
        :return:
        """
        if request.json is None:
            raise ApiException ('No data received')
        script = db.scripts.require (id, 'no such script')
        commands = request.json['commandsNew'].splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)

        return script.as_dict ()

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
        script = db.scripts.require (id, 'no such script')
        del db.scripts[id]
        return { 'delete': 'ok' }