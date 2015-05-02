# encoding: utf-8
# author:   Jan Hybs

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx


class Script (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.job_id = None
        self.timestamp = None
        self.result = None
        self.commands = PersistentList ()

    def get_commands (self):
        return [db.commands.get (command_id, None) for command_id in self.commands]


class ScriptManagementApplication (BTreeEx):
    pass

