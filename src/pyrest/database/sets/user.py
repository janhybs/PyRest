# encoding: utf-8
# author:   Jan Hybs
import uuid

import persistent
from persistent.list import PersistentList

from pyrest import db
from pyrest.database.btree import BTreeEx
from pyrest.database.dbutils import DBUtils
from pyrest.server.auth import SessionUser


class User (persistent.Persistent):
    """ class representing user
    """
    def __init__ (self):
        self.id = None
        self.username = None
        self.password = None
        self.jobs = PersistentList ()

    def create_session_user (self):
        """
        :return: instance of SessionUser created from this user
        """
        return SessionUser (self, str (uuid.uuid1 ()))

    def get_jobs (self):
        """
        :return: list all job aval
        """
        return [db.jobs.get (job_id, None) for job_id in self.jobs]

    def __repr__ (self):
        return "<User '{self.username}'>".format (self=self)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self):
        """
        :return: dict repr
        """
        return dict (
            id=self.id,
            username=self.username, password=self.password,
            jobs=list (self.jobs),
        )


class UserManagementApplication (BTreeEx):
    def add_default (self):
        """
        :return: dummy instances of users
        """
        u = User ()
        u.id = str (uuid.uuid1 ())
        u.username = 'Hans'
        u.password = 'foo'
        self.add (u)

        u = User ()
        u.id = str (uuid.uuid1 ())
        u.username = 'root'
        u.password = 'root'
        self.add (u)

    @staticmethod
    def register (db, name, btree_cls):
        """
        :param db:
        :param name:
        :param btree_cls:
        :return:
         """
        if not hasattr (db, name):
            print 'no root "{:s}" found, creating'.format (name)
            instance = btree_cls ()
            db.__setattr__ (name, instance)
            instance.add_default ()

    @staticmethod
    def create (username=None, password=None, **kwargs):
        """
        :param username:
        :param password:
        :param kwargs:
        :return: instance of User
        """
        user = User ()
        user.id = DBUtils.id (kwargs)
        user.username = username
        user.password = password

        return user
