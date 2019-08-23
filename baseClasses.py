#################### HELPER CLASSES ####################################

class maplike_meta(type):
    def __getitem__(cls, key):
        if type(key) == int or key[0].isdigit(): # handle int keys by 
                                                 # adding prefix "for"
            return getattr(cls, "for{}".format(key))
        else:
            return getattr(cls, key)
    def __setitem__(cls, key, value):
        if type(key) == int or key[0].isdigit(): # handle int keys by
                                                 # adding prefix "for"
            setattr(cls, "for{}".format(key), value)
        else:
            setattr(cls, key, value)

#################### INHERIT FROM THESE ################################

# like a map but for static members of classes
class maplike(object):
    __metaclass__=maplike_meta
    pass


