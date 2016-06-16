import exceptions
import access


class LangMetaObject(type):
    """
    Meta class that is used to enforce language constraint rules on the object that uses it.
    """

    def __new__(cls, *args, **kwargs):
        inst = super(LangMetaObject, cls).__new__(cls, *args)
        access.enforce(inst)
        return inst


class LangObject(object):
    """
    Represents a class that follows the lang rules
    """

    __metaclass__ = LangMetaObject
