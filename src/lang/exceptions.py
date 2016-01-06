class ExceptionMessageMeta(type):
    """
    Metaclass for initializing the message variable of the Exception class by a class variable
    named <MESSAGE_MEMBER_NAME>.
    """
    MESSAGE_MEMBER_NAME = 'MESSAGE'

    def __init__(cls, what=None, bases=None, dict=None):
        super(ExceptionMessageMeta, cls).__init__(what, bases, dict)
        setattr(cls, 'message', getattr(cls, ExceptionMessageMeta.MESSAGE_MEMBER_NAME, None))


class LangException(Exception):
    """
    The base class for all language exceptions
    """
    __metaclass__ = ExceptionMessageMeta


class PrivateMemberAccessException(LangException):
    MESSAGE = 'You cannot access a member of a class, that is a private member.'


class ProtectedMemberAccessException(LangException):
    MESSAGE = 'You cannot access a member of a class, that is a protected member not from inside the class.'


class BadInterfaceImplementationException(LangException):
    MESSAGE = 'A class that was declared as an interface, had function implementations.'


class VariablesInInterfaceException(LangException):
    MESSAGE = 'A class that was declared as an interface, had class variables.'
