# encoding: utf-8
# author:   Jan Hybs

import persistent
from persistent.list import PersistentList

from pyrest.database.BTreeEx import BTreeEx


class Conference (persistent.Persistent):
    def __init__ (self):
        self.city = 0
        self.users = PersistentList ()

    def get_info (self):
        return "{:s}: attended {:s}, total: {:d}".format (self.city, ','.join (self.users), len (self.users))

class ConferenceManagementApplication (BTreeEx):
    pass

