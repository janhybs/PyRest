# encoding: utf-8
# author:   Jan Hybs
import uuid, time

import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from pyrest import db
from pyrest.database.btree import BTreeEx
from pyrest.database.dbutils import DBUtils
from pyrest.database.sets.script import ScriptManagementApplication, ScriptExitCode


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

    def add_script (self, script):
        self.scripts.append (script.id)


    def get_user (self):
        return db.users.get (self.user_id)


    def get_script_at (self, position=-1):
        try:
            return db.scripts.get (self.scripts[position])
        except:
            return None

    def script (self):
        return self.get_script_at (-1)


    def get_result_cls (self):
        return self.script ().get_result_cls () if self.scripts else 'default'

    def get_result_str (self):
        return self.script ().get_result_str () if self.scripts else 'No results'


    def __repr__ (self):
        return u"<Job '{self.id}' '{self.name}', scripts=[{scripts}]>".format (self=self, scripts=self.get_scripts ())

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self, peek=False):
        return dict (
            id=self.id,
            name=self.name, status=self.status,
            settings=dict (self.settings),
            scripts=[script.as_dict () for script in self.get_scripts ()] if not peek else [script_id for script_id in
                                                                                            self.scripts],
            user=self.get_user ().as_dict ()
        )


class JobManagementApplication (BTreeEx):
    def add_default (self):
        job = JobManagementApplication.create (user_id=db.users.search_one ().id, name="Job 1")
        script = ScriptManagementApplication.create (job_id=job.id,commands=
            """ping -c 4 www.tul.cz
            echo 'foo'
            ls
            ls -la
            sleep 1
            java -versioncas
            java -version 2>&1
            java -version
            """)

        job.add_script (script)
        db.scripts.add (script)
        self.add (job)

        job = JobManagementApplication.create (user_id=db.users.search_one ().id, name="Job 2")
        script = ScriptManagementApplication.create (job_id=job.id, commands=
        """echo 'uname'
        uname -a

        sleep 1
        echo 'bar'
        """)
        job.add_script (script)
        db.scripts.add (script)

        script = ScriptManagementApplication.create (job_id=job.id, commands=
        """echo 'uname'
        uname
        uname -a
        echo 'bar'
        """)

        job.add_script (script)
        db.scripts.add (script)
        self.add (job)

        job = JobManagementApplication.create (user_id=db.users.search_one ().id, name="Job 3")
        self.add (job)

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
        job.id = DBUtils.id (kwargs)
        job.name = kwargs.get ('name')
        job.user_id = kwargs.get ('user_id')
        job.scripts = kwargs.get ('scripts', PersistentList ())
        job.status = kwargs.get ('status', JobStatus.unknown)

        return job

