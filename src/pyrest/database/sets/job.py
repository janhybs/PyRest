# encoding: utf-8
# author:   Jan Hybs

import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx


class Job (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.user_id = None
        self.name = None
        self.status = None
        self.settings = PersistentMapping ()
        self.scripts = PersistentList ()

    def get_scripts (self):
        return [db.scripts.get (script_id, None) for script_id in self.scripts]


class JobManagementApplication (BTreeEx):
    pass

