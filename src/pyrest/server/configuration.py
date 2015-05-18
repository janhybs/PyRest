# encoding: utf-8
# author:   Jan Hybs
from optparse import OptionParser


class Configuration (object):
    """
    class which holds global config
    """
    instance = None

    def __init__ (self):
        parser = OptionParser()
        parser.add_option ("-n", "--noserver", dest="noserver", default=False,
                         action="store_true", help="Do not run flask server")

        parser.add_option ("-d", "--debug", dest="debug", default=False,
                         action="store_true", help="User debug mode")

        parser.add_option ("-m", "--memorystorage", dest="memorystorage", default=False,
                         action="store_true", help="Use memory database instead of database in local file")


        (options, args) = parser.parse_args ()

        self.noserver = options.noserver
        self.debug = options.debug
        self.memorystorage = options.memorystorage

        if self.debug:
            print ":: Debug is On"

        if self.noserver:
            print ":: Flask server won't be run"

        if self.memorystorage:
            print ":: Storage will be in memory only"


    @staticmethod
    def get_instance ():
        """
        Singleton getter
        :return: Configuration
        """
        if Configuration.instance is None:
            Configuration.instance = Configuration ()
        return Configuration.instance
