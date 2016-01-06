import inspect
import types
import re
from lang.abstract import Abstract
from lang.exceptions import BadInterfaceImplementationException, VariablesInInterfaceException


class EnforceInterfaceMeta(type):
    INTERFACE_IGNORE_DICT_ITEMS = ['__dict__', '__doc__', '__module__', '__weakref__']
    INTERFACE_FUNCTION_IMPL_REGEX = re.compile('^pass$')
    INTERFACE_RESTRICTED_FUNCTIONS = ['__init__', '__new__']

    def __new__(cls, name, bases, attrs):
        for name, item in cls.__dict__.iteritems():
            if name in EnforceInterfaceMeta.INTERFACE_IGNORE_DICT_ITEMS:
                continue

            if isinstance(item, types.FunctionType) or isinstance(item, types.MethodType):
                source = inspect.getsourcelines(item)[0]
                if item.func_name in EnforceInterfaceMeta.INTERFACE_RESTRICTED_FUNCTIONS or not re.match(
                        EnforceInterfaceMeta.INTERFACE_FUNCTION_IMPL_REGEX, source[-1].strip()):
                    raise BadInterfaceImplementationException()
            else:
                raise VariablesInInterfaceException()

        return type.__new__(cls, name, bases, attrs)


class Interface(Abstract):
    __metaclass__ = EnforceInterfaceMeta
