from lang.exceptions import FinalClassSubclassedException


class FinalClassMeta(type):
    """
    Metaclass that makes the class a final class that cannot be subclassed.

    """

    def __new__(cls, name, bases, classdict):
        for b in bases:
            if isinstance(b, FinalClassMeta):
                raise FinalClassSubclassedException()
        return type.__new__(cls, name, bases, dict(classdict))
