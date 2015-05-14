# encoding: utf-8
# author:   Jan Hybs
import time
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.btree import BTreeEx
from pyrest.database.dbutils import DBUtils
from pyrest.database.sets.command import CommandManagementApplication


class ScriptExitCode (object):
    _classes = ['default', 'success', 'warning', 'danger']
    _strings = ['No results', 'Success', 'Running', 'Error']

    ok = 0
    success = 1
    running = 2
    error = 3
    unknown = 666


class Script (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.job_id = None
        self.start_at = None
        self.duration = None
        self.exit_code = None
        self.commands = PersistentList ()


    def copy (self):
        script = Script()
        script.job_id = self.job_id
        script.start_at = self.start_at
        script.duration = self.duration
        script.exit_code = self.exit_code
        script.commands = self.commands
        script.id = DBUtils.unique_id()

        return script



    def get_commands (self):
        return [db.commands.get (command_id, None) for command_id in self.commands]

    def get_result_cls (self):
        return ScriptExitCode._classes[self.result]

    def get_result_str (self):
        return ScriptExitCode._strings[self.result]

    def __repr__ (self):
        return u"<Script {self.id} '{self.exit_code}', commands=[{self.commands}]>".format (self=self)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self):
        return dict (
            id=self.id, job_id=self.job_id,
            start_at=int(self.start_at) if self.start_at else None, exit_code=self.exit_code,
            duration=self.duration,
            commands=[command.as_dict () for command in self.commands]
        )


class ScriptManagementApplication (BTreeEx):
    @staticmethod
    def create (*args, **kwargs):
        script = Script ()
        script.id = DBUtils.id (kwargs)
        script.job_id = kwargs.get ('job_id')
        script.start_at = kwargs.get ('start_at')
        script.exit_code = kwargs.get ('exit_code', ScriptExitCode.unknown)
        script.duration = kwargs.get ('duration')

        commands = kwargs.get ('commands', '').splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)
        return script

