# encoding: utf-8
# author:   Jan Hybs
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx
from pyrest.server.auth import SessionUser


class User (persistent.Persistent):
    def __init__ (self):
        self.id = None
        self.username = None
        self.password = None
        self.jobs = PersistentList ()

    def __repr__ (self):
        return "<User '{self.username}'>".format (self=self)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def create_session_user (self):
        return SessionUser (self, str (uuid.uuid1 ()))

    def get_jobs (self):
        return [db.jobs.get (job_id, None) for job_id in self.jobs]

    @staticmethod
    def create_user ():
        user = User ()
        user.id = str (uuid.uuid1 ())
        return user


class UserManagementApplication (BTreeEx):
    def add_default (self):
        u = User ()
        u.id = str (uuid.uuid1 ())
        u.username = 'Hans'
        u.password = 'foo'
        self.insert (u.id, u)

        u = User ()
        u.id = str (uuid.uuid1 ())
        u.username = 'root'
        u.password = 'root'
        self.insert (u.id, u)

    @staticmethod
    def register (db, name, btree_cls):
        if not hasattr (db, name):
            print 'no root "{:s}" found, creating'.format (name)
            instance = btree_cls ()
            db.__setattr__ (name, instance)
            instance.add_default ()


