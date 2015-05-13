# encoding: utf-8
# author:   Jan Hybs
import uuid


class DBUtils (object):
    _id_count = 0

    @staticmethod
    def unique_id ():
        if DBUtils.DEBUG:
            DBUtils._id_count += 1
            return str (DBUtils._id_count)
        return str (uuid.uuid4 ())