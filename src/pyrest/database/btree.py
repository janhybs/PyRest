# encoding: utf-8
# author:   Jan Hybs

import uuid
import BTrees.OOBTree
from operator import itemgetter
from pyrest.rest.api_exception import ApiException


class BTreeEx (BTrees.OOBTree.BTree):
    """
    Extended class of btree with searching and sorting
    """

    def require (self, item_id, detail='Not found', status=404):
        """
        Method will load item by given id or raise ApiException with given details
        :param item_id: item id
        :param detail: exception detail
        :param status: exception status
        :return:
        """
        item = self.get (item_id, None)
        if item is None:
            raise ApiException (detail, status)
        return item

    def add (self, value):
        """
        adds item to this btree root whilst using value.id as id
        :param value: *
        :return: bool
        """
        return self.insert (value.id, value)

    def delete (self, value):
        """
        Removes given object by its if value or if str is given, remove
        object with this value
        :param value:
        :return:
        """
        if type (value) in (str, unicode):
            del self[value]
        else:
            del self[value.id]

    remove = delete


    def search (self, conditions={ }, sort=None):
        """
        :param conditions:
        :param sort:
        :return: search all occurrences
        """
        result = []
        for (k, v) in self.items ():
            m = { kk: getattr (v, kk, None) == vv for (kk, vv) in conditions.items () }
            t_f = list (set (m.values ()))
            if len (t_f) == 0 or (len (t_f) == 1 and t_f[0] == True):
                result.append (v)
        return result if not sort else sorted (result, key=lambda d: getattr (d, sort))

    def search_one (self, conditions={ }):
        """
        :param conditions:
        :return: search one (first if multiple) instance
        """
        for (k, v) in self.items ():
            m = { kk: getattr (v, kk, None) == vv for (kk, vv) in conditions.items () }
            t_f = list (set (m.values ()))
            if len (t_f) == 0 or (len (t_f) == 1 and t_f[0] == True):
                return v
        return None

    @staticmethod
    def register (db, name, btree_cls):
        """
        register this root to db
        :param db:
        :param name:
        :param btree_cls:
        :return:
        """
        if not hasattr (db, name):
            print 'no root "{:s}" found, creating'.format (name)
            db.__setattr__ (name, btree_cls ())