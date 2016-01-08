class LangException(Exception):
    """
    The base class for all language exceptions
    """
    MESSAGE_MEMBER_NAME = 'MESSAGE'

    def __str__(self):
        return getattr(self, LangException.MESSAGE_MEMBER_NAME, None)


class PrivateMemberAccessException(LangException):
    MESSAGE = 'You cannot access a member of a class, that is a private member.'


class ProtectedMemberAccessException(LangException):
    MESSAGE = 'You cannot access a member of a class, that is a protected member not from inside the class.'


class BadInterfaceImplementationException(LangException):
    MESSAGE = 'A class that was declared as an interface, had function implementations.'


class FinalClassSubclassedException(LangException):
    MESSAGE = 'Type is not a final class and cannot be subclassed'
