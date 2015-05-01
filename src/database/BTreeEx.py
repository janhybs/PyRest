# encoding: utf-8
# author:   Jan Hybs

import uuid
import BTrees.OOBTree

class BTreeEx (BTrees.OOBTree.BTree):
    def put (self, value):
        return self.insert(uuid.uuid1(), value)