# encoding: utf-8
# author:   Jan Hybs
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx

from unidecode import unidecode


class CommandExitCode (object):
    unknown = 0
    success = 1
    error = 2


class Command (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.script_id = None
        self.source_code = None
        self.output = None
        self.error = None
        self.exit_code = None
        self.duration = None

    def __repr__ (self):
        sc = unidecode (unicode (self.source_code)) if self.source_code else "''"
        return u"{sc}".format (self=self, sc=sc)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self):
        return dict (
            id=self.id, script_id=self.script_id,
            source_code=self.source_code,
            output=self.output, error=self.error,
            exit_code=self.exit_code,
            duration=self.duration
        )


class CommandManagementApplication (BTreeEx):
    @staticmethod
    def create (*args, **kwargs):
        command = Command ()
        command.id = kwargs.get ('id', str (uuid.uuid4 ()))
        command.script_id = kwargs.get ('script_id')
        command.source_code = kwargs.get ('source_code')
        command.output = kwargs.get ('output')
        command.error = kwargs.get ('error')
        command.exit_code = kwargs.get ('exit_code', CommandExitCode.unknown)
        command.duration = kwargs.get ('commands')
        return command

    @staticmethod
    def create_command_list (script_id, commands):
        result = PersistentList ()
        for source_code in commands:
            command = CommandManagementApplication.create (script_id=script_id, source_code=source_code)
            result.append (command)

        return result

