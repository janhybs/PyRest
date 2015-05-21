# encoding: utf-8
# author:   Jan Hybs
import uuid


class DBUtils (object):
    _id_count = 0
    debug = True

    @staticmethod
    def unique_id ():
        """
        :return: unique incremented if debug os on or unique id based on time and machine otherwise
        """
        if DBUtils.debug:
            DBUtils._id_count += 1
            return unicode ('py' + str (DBUtils._id_count))

        return unicode (str (uuid.uuid4 ()))

    @staticmethod
    def id (kwargs={ }):
        """
        :param kwargs:
        :return: extract id from given kwargs
        """
        kwargs_id = kwargs.get ('id')
        return unicode (kwargs_id if kwargs_id else DBUtils.unique_id ())