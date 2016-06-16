"""

Author: Amit Assaraf
TODOs: Add protect/private decorator for functions

"""

from functools import partial
import inspect

from lang.exceptions import PrivateMemberAccessException, ProtectedMemberAccessException


# Logic functions
def _private_member_access_protection(function, orig_class, self, item, *args, **kwargs):
    """
    Function for protecting __getattribute__ and __setattr__ methods from private variable access.
    :param function: Either __getattribute__ or __setattr__
    :param item: The item that we want to get
    :param args: Extra arguments
    :param kwargs: Extra keyword arguments
    :return: The attribute
    """
    if not item.startswith('__') and item.startswith('_') and item.endswith('_'):
        frame = inspect.currentframe().f_back.f_back.f_back  # Twice because we skip lambda
        caller_func_name = inspect.getframeinfo(frame).function
        code_context = inspect.getsourcelines(frame)
        if caller_func_name in orig_class.__dict__:
            original_code_context = inspect.getsourcelines(orig_class.__dict__[caller_func_name])
            if code_context == original_code_context:
                return function(self, item, *args, **kwargs)
        else:
            if orig_class.mro()[0].__name__ == 'LangObject':  # If we inherit directly from langobject allow all
                return function(self, item, *args, **kwargs)
            for cls in orig_class.mro()[1:-1]:
                if caller_func_name in cls.__dict__:
                    original_code_context = inspect.getsourcelines(cls.__dict__[caller_func_name])
                    if code_context == original_code_context:
                        return function(self, item, *args, **kwargs)
        raise PrivateMemberAccessException()
    return function(self, item, *args, **kwargs)


def _protected_member_access_protection(function, self, item, *args, **kwargs):
    """
    Function for protecting __getattribute__ and __setattr__ methods from protected variable access.
    :param function: Either __getattribute__ or __setattr__
    :param item: The item that we want to get
    :param args: Extra arguments
    :param kwargs: Extra keyword arguments
    :return: The attribute
    """
    if not item.startswith('__') and item.startswith('_') and not item.endswith('_'):
        frame = inspect.currentframe().f_back.f_back.f_back  # Twice because we skip lambda
        args_info = inspect.getargvalues(frame)
        if args_info.args:
            caller_self = args_info.locals[args_info.args[0]]
            function_name = inspect.getframeinfo(frame).function

            # Allow anyone with the same class or below to access us!
            if function_name in dir(self) and isinstance(caller_self, type(self)):
                return function(self, item, *args, **kwargs)
        raise ProtectedMemberAccessException()
    return function(self, item, *args, **kwargs)


def _protected_property_access_protection(function, self, *args, **kwargs):
    frame = inspect.currentframe().f_back
    args_info = inspect.getargvalues(frame)
    if args_info.args:
        caller_self = args_info.locals[args_info.args[0]]
        function_name = inspect.getframeinfo(frame).function

        # Allow anyone with the same class or below to access us!
        if function_name in dir(self) and isinstance(caller_self, type(self)):
            return function(self, *args, **kwargs)
    raise ProtectedMemberAccessException()


def _private_property_access_protection(function, self, *args, **kwargs):
    frame = inspect.currentframe().f_back
    args_info = inspect.getargvalues(frame)
    if args_info.args:
        caller_self = args_info.locals[args_info.args[0]]
        for item in caller_self.__class__.__mro__:
            if item.__name__ in frame.f_globals and function.func_name in item.__dict__:
                func_name = inspect.getframeinfo(frame).function
                if caller_self.__class__ == item or (
                                func_name in item.__dict__ and inspect.getsourcelines(frame) == inspect.getsourcelines(
                            item.__dict__[func_name])):
                    return function(self, *args, **kwargs)
    raise PrivateMemberAccessException()


# Protected Property

class protected_property(property):
    """
    property that is used to enforce protected properties regardless of convention.
    The wrapped property will now be protected and if tried to be accessed from a class that is not it's
    defining class or a subclass of it, a ProtectedMemberAccessException will be raised.
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fset = partial(_protected_property_access_protection, fset)
        new_fget = partial(_protected_property_access_protection, fget)
        super(protected_property, self).__init__(new_fget, new_fset, fdel, doc)


############
## Properties for protecting only specific property type (Getter or Setter)
############

class protected_setter_only(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fset = partial(_protected_property_access_protection, fset)
        super(protected_setter_only, self).__init__(fget, new_fset, fdel, doc)


class protected_getter_only(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fget = partial(_protected_property_access_protection, fget)
        super(protected_getter_only, self).__init__(new_fget, fset, fdel, doc)


# Private Property

class private_property(property):
    """
    property that is used to enforce protected properties regardless of convention.
    The wrapped property will now be protected and if tried to be accessed from a class that is not it's
    defining class, a PrivateMemberAccessException will be raised.
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fset = partial(_private_property_access_protection, fset)
        new_fget = partial(_private_property_access_protection, fget)
        super(private_property, self).__init__(new_fget, new_fset, fdel, doc)


############
## Properties for protecting only specific property type (Getter or Setter)
############

class private_setter_only(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fset = partial(_private_property_access_protection, fset)
        super(private_setter_only, self).__init__(fget, new_fset, fdel, doc)


class private_getter_only(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        new_fget = partial(_private_property_access_protection, fget)
        super(private_getter_only, self).__init__(new_fget, fset, fdel, doc)


def enforce(inst):
    """
    Method called to enforce the access rules on the new class
    :param cls: The class that is created
    :param what: The name of the class that is created
    :param bases: A tuple of the class's bases
    :param attrs: The extra attrs the class has
    :return: None
    """

    def protected_members(func, *args, **kwargs):
        # Enforce private members
        fake_cls = inst.mro()[1]

        value = _protected_member_access_protection(func, *args, **kwargs)
        value_p = _private_member_access_protection(func, fake_cls, *args, **kwargs)
        return value or value_p

    # Enforce protected members
    setattr(inst, '__getattribute__',
            lambda *args, **kwargs: protected_members(object.__getattribute__, *args, **kwargs))
    setattr(inst, '__setattr__', lambda *args, **kwargs: protected_members(object.__setattr__, *args, **kwargs))
