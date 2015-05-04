# encoding: utf-8
# author:   Jan Hybs

import uuid
import BTrees.OOBTree


class BTreeEx (BTrees.OOBTree.BTree):
    def add (self, value):
        return self.insert (value.id, value)

    def search (self, conditions={}):
        result = []
        for (k, v) in self.items ():
            m = { kk: getattr (v, kk, None) == vv for (kk, vv) in conditions.items () }
            t_f = list (set (m.values ()))
            if len (t_f) == 0 or (len (t_f) == 1 and t_f[0] == True):
                result.append (v)
        return result

    def search_one (self, conditions={}):
        for (k, v) in self.items ():
            m = { kk: getattr (v, kk, None) == vv for (kk, vv) in conditions.items () }
            t_f = list (set (m.values ()))
            if len (t_f) == 0 or (len (t_f) == 1 and t_f[0] == True):
                return v
        return None

    @staticmethod
    def register (db, name, btree_cls):
        if not hasattr (db, name):
            print 'no root "{:s}" found, creating'.format (name)
            db.__setattr__ (name, btree_cls ())