# encoding: utf-8
# author:   Jan Hybs

import persistent
from database.BTreeEx import BTreeEx
from persistent.list import PersistentList


class Conference (persistent.Persistent):
    def __init__ (self):
        self.city = 0
        self.users = PersistentList ()

    def get_info (self):
        return "{:s}: attended {:s}, total: {:d}".format (self.city, ','.join (self.users), len (self.users))

class ConferenceManagementApplication (BTreeEx):
    pass

