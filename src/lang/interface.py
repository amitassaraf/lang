import inspect
import types
import re
from lang.abstract import Abstract, EnforceAbstractMeta, abstract_method, abstract_property
from lang.exceptions import BadInterfaceImplementationException

_INTERFACE_IGNORE_DICT_ITEMS = ['__dict__', '__doc__', '__module__', '__weakref__']
_INTERFACE_FUNCTION_IMPL_REGEX = re.compile('^pass$')
_INTERFACE_RESTRICTED_FUNCTIONS = ['__init__', '__new__']
_STATIC_BUILTIN_IGNORES = ['__new__', '__metaclass__']
_INTERFACE_ALLOWED_FUNCTION_TYPES = (types.FunctionType, types.MethodType, property)


class EnforceInterfaceMeta(EnforceAbstractMeta):
    """
    Metaclass for enforcing an interface implementation.
    """

    def __new__(cls, name, bases, attrs):
        for name, item in attrs.iteritems():
            if name in _INTERFACE_IGNORE_DICT_ITEMS:
                continue

            if isinstance(item, _INTERFACE_ALLOWED_FUNCTION_TYPES):
                source = inspect.getsourcelines(item)[0]
                if item.func_name in _INTERFACE_RESTRICTED_FUNCTIONS or not re.match(
                        _INTERFACE_FUNCTION_IMPL_REGEX, source[-1].strip()):
                    raise BadInterfaceImplementationException()
                else:
                    if isinstance(item, property):
                        attrs[name] = abstract_property(item)
                    else:
                        attrs[name] = abstract_method(item)

        return super(EnforceInterfaceMeta, cls).__new__(cls, name, bases, attrs)


class Interface(Abstract):
    """

    A interface is a bit like a class, except a interface can only contain method signatures and fields.
    An interface cannot contain an implementation of the methods, only the signature (name, parameters
    and exceptions) of the method.

    """

    __metaclass__ = EnforceInterfaceMeta
