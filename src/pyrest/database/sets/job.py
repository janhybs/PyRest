# encoding: utf-8
# author:   Jan Hybs
import uuid

import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from pyrest import db
from pyrest.database.BTreeEx import BTreeEx
from pyrest.database.sets.script import ScriptManagementApplication


class JobStatus (object):
    not_created = 0
    running = 1
    success = 2
    error = 3
    unknown = 4


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

    def get_user (self):
        return db.users.get (self.user_id)


    def __repr__ (self):
        return u"<Job '{self.name}', scripts=[{self.scripts}]>".format (self=self)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()


class JobManagementApplication (BTreeEx):
    def add_default (self):
        job = JobManagementApplication.create (user_id=db.users.search_one().id, name="Job 1")
        script = ScriptManagementApplication.create (job_id=job.id, commands=
"""echo 'foo'

sleep 1
echo 'bar'
""")
        job.scripts.append (script)
        self.add(job)

        job = JobManagementApplication.create (user_id=db.users.search_one().id, name="Job 2")
        script = ScriptManagementApplication.create (job_id=job.id, commands=
"""echo 'uname'
uname -a

sleep 1
echo 'bar'
""")
        job.scripts.append (script)
        self.add(job)

    @staticmethod
    def register (db, name, btree_cls):
        if not hasattr (db, name):
            print 'no root "{:s}" found, creating'.format (name)
            instance = btree_cls ()
            db.__setattr__ (name, instance)
            instance.add_default ()

    @staticmethod
    def create (*args, **kwargs):
        job = Job ()
        job.id = kwargs.get ('id', str (uuid.uuid4 ()))
        job.name = kwargs.get ('name')
        job.user_id = kwargs.get ('user_id')
        job.scripts = kwargs.get ('scripts', PersistentList ())
        job.status = kwargs.get ('status', JobStatus.unknown)

        return job

