# encoding: utf-8
# author:   Jan Hybs
import persistent
from persistent.list import PersistentList

from pyrest.database.btree import BTreeEx

from unidecode import unidecode
from pyrest.database.dbutils import DBUtils



class Command (persistent.Persistent):
    """ class representing single statement with all related info
    """
    def __init__ (self):
        self.id = None
        self.script_id = None
        self.source_code = None
        self.outputLines = []
        self.exit_code = None
        self.start_at = None
        self.duration = None

    def is_valid (self):
        """
        :return: true if source is not empty
        :rtype: bool
        """
        return bool (self.get_source ())

    def get_source (self):
        """
        :return: stripped statements source code
        :rtype: str
        """
        return self.source_code.strip ()

    def __repr__ (self):
        sc = unidecode (unicode (self.source_code)) if self.source_code else "''"
        return u"{sc}".format (self=self, sc=sc)

    def __str__ (self):
        return self.__repr__ ()

    def __unicode__ (self):
        return self.__repr__ ()

    def as_dict (self):
        """
        :return: dict representation of this object
        :rtype: dict
        """
        return dict (
            id=self.id, script_id=self.script_id,
            source_code=self.source_code,
            outputLines=self.outputLines,
            exit_code=self.exit_code,
            start_at=self.start_at,
            duration=self.duration
        )


class CommandManagementApplication (BTreeEx):
    @staticmethod
    def create (*args, **kwargs):
        command = Command ()
        command.id = DBUtils.id (kwargs)
        command.script_id = kwargs.get ('script_id')
        command.source_code = kwargs.get ('source_code')
        command.outputLines = kwargs.get ('outputLines', [])
        command.exit_code = kwargs.get ('exit_code')
        command.start_at = kwargs.get ('start_at')
        command.duration = kwargs.get ('duration')
        return command

    @staticmethod
    def create_command_list (script_id, commands):
        """
        :param script_id:
        :param commands: list of string
        :return: list of Commands created from given list
        :rtype: PersistentList
        """
        result = PersistentList ()
        for source_code in commands:
            command = CommandManagementApplication.create (script_id=script_id, source_code=source_code)
            result.append (command)

        return result

