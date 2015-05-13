# encoding: utf-8
# author:   Jan Hybs
import uuid


class DBUtils (object):
    _id_count = 0
    debug = True

    @staticmethod
    def unique_id ():
        if DBUtils.debug:
            DBUtils._id_count += 1
            return unicode ('py' + str (DBUtils._id_count))

        return unicode (str (uuid.uuid4 ()))

    @staticmethod
    def id (kwargs={ }):
        kwargs_id = kwargs.get ('id', None)
        return unicode (kwargs_id if kwargs_id is not None else DBUtils.unique_id ())