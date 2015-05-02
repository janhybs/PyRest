# encoding: utf-8
# author:   Jan Hybs

import persistent

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx


class Command (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.script_id = None
        self.source_code = None
        self.output = None
        self.error = None
        self.exit_code = None
        self.duration = None


class CommandManagementApplication (BTreeEx):
    pass

