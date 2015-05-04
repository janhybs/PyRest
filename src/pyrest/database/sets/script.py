# encoding: utf-8
# author:   Jan Hybs
import time
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx
from pyrest.database.sets.command import CommandManagementApplication


class ScriptResult (object):
    not_created = 0
    running = 1
    success = 2
    error = 3
    unknown = 4


class Script (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.job_id = None
        self.timestamp = None
        self.result = None
        self.commands = PersistentList ()

    def get_commands (self):
        return [db.commands.get (command_id, None) for command_id in self.commands]

    def __repr__ (self):
        return u"<Script '{self.timestamp}', commands=[{self.commands}]>".format (self=self)


    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()


class ScriptManagementApplication (BTreeEx):
    @staticmethod
    def create (*args, **kwargs):
        script = Script ()
        script.id = kwargs.get ('id', str (uuid.uuid4 ()))
        script.job_id = kwargs.get ('job_id')
        script.timestamp = kwargs.get ('timestamp', time.time ())
        script.result = kwargs.get ('result', ScriptResult.unknown)

        commands = kwargs.get ('commands', '').splitlines ()
        script.commands = CommandManagementApplication.create_command_list (script_id=script.id, commands=commands)
        return script

