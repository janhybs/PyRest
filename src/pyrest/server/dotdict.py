# encoding: utf-8
# author:   Jan Hybs

class DotDict(dict):
    """
    Dictionary class with dot (.) access
    """
    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)

    def __getattribute__(self, name):
        try:
            return dict.__getattribute__(self, name)
        except AttributeError:
            if name in self:
                return self[name]

            name = name.replace('_', '-')
            if name in self:
                return self[name]
            raise

    def __setattr__(self, key, value):
        dict.__setitem__(self, key, value)

    def copy(self):
        return DotDict (self)
