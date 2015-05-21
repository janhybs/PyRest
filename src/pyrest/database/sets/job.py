# encoding: utf-8
# author:   Jan Hybs

import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from pyrest import db
from pyrest.database.btree import BTreeEx
from pyrest.database.dbutils import DBUtils
from pyrest.database.sets.script import ScriptManagementApplication, ScriptExitCode


class Job (persistent.Persistent):
    """ class representing several scripts
    """
    def __init__ (self):
        self.id = None
        self.user_id = None
        self.name = None
        self.status = None
        self.settings = PersistentMapping ()
        self.scripts = PersistentList ()

    def get_scripts (self):
        """
        :return: list of Script objects
        """
        return [db.scripts.get (script_id, None) for script_id in self.scripts]

    def add_script (self, script):
        """
        adds Script to internal list of scripts
        :param script: Script
        :return: None
        """
        self.scripts.append (script.id)


    def delete_script (self, script):
        """
        :param script: script to be removed
        :return: None
        """
        self.scripts.remove (script.id)


    def get_user (self):
        """
        :return: User object, creator of this job
        """
        return db.users.get (self.user_id)


    def get_script_at (self, position=-1):
        """
        :param position:
        :return: Script or None
        :rtype Script:
        """
        try:
            return db.scripts.get (self.scripts[position])
        except:
            return None

    def script (self):
        """
        :return: current Script (last one)
        :rtype Script:
        """
        return self.get_script_at (-1)


    def get_result_cls (self):
        """
        :return: css class for this instance result
        :rtype str:
        """
        return self.script ().get_result_cls () if self.scripts else 'default'

    def get_result_str (self):
        """
        :return: str representation for this instance result
        :rtype str:
        """
        return self.script ().get_result_str () if self.scripts else 'No results'


    def __repr__ (self):
        return u"<Job '{self.id}' '{self.name}', scripts=[{scripts}]>".format (self=self, scripts=self.get_scripts ())

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self, peek=False):
        """
        :param peek: whether to load script from db
        :return: dict representation of this object
        :rtype: dict
        """
        d = dict (
            id=self.id,
            name=self.name, status=self.status,
            settings=dict (self.settings),
            user=self.get_user ().as_dict (),
            scripts_id=[script_id for script_id in self.scripts]
        )

        if not peek:
            d['scripts'] = [script.as_dict () for script in self.get_scripts ()]
        return d


    remove_script = delete_script


class JobManagementApplication (BTreeEx):
    def add_default (self):
        """
        Add default values
        """
        job = JobManagementApplication.create (user_id=db.users.search_one ().id, name="Job 1")
        script = ScriptManagementApplication.create (job_id=job.id,commandsNew=
            """
java -versioncas
java -version 2>&1
java -version
            """)

        job.add_script (script)
        db.scripts.add (script)
        self.add (job)

        job = JobManagementApplication.create (user_id=db.users.search_one ().id, name="Job 2")
        script = ScriptManagementApplication.create (job_id=job.id, commandsNew=
        """ping -c 4 www.tul.cz
        echo 'uname'
        uname -a

        sleep 1
        echo 'bar'
        """)
        job.add_script (script)
        db.scripts.add (script)

        script = ScriptManagementApplication.create (job_id=job.id, commandsNew=
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
        """
        register db root
        :param db:
        :param name:
        :param btree_cls:
        """
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
        job.status = kwargs.get ('status', ScriptExitCode.unknown)

        return job

