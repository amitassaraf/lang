import inspect

from src.lang import PrivateMemberAccessException, ProtectedMemberAccessException


#TODO: Add decorators for private & protected

def _private_member_access_protection(function, orig_class, self, item, *args, **kwargs):
    """
    Function for protecting __getattribute__ and __setattr__ methods from private variable access.
    :param function: Either __getattribute__ or __setattr__
    :param item: The item that we want to get
    :param args: Extra arguments
    :param kwargs: Extra keyword arguments
    :return:
    """
    if not item.startswith('__') and item.startswith('_') and item.endswith('_'):
        f = inspect.currentframe().f_back.f_back  # Twice because we skip lambda
        caller_func_name = inspect.getframeinfo(f).function
        code_context = inspect.getsourcelines(f)
        if caller_func_name in orig_class.__dict__:
            original_code_context = inspect.getsourcelines(orig_class.__dict__[caller_func_name])

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
    :return:
    """
    if not item.startswith('__') and item.startswith('_') and not item.endswith('_'):
        f = inspect.currentframe().f_back.f_back  # Twice because we skip lambda
        args_info = inspect.getargvalues(f)
        if args_info.args:
            caller_self = args_info.locals[args_info.args[0]]
            if isinstance(caller_self, type(self)):  # Allow anyone with the same class or below to change us!
                return function(self, item, *args, **kwargs)
        raise ProtectedMemberAccessException()
    return function(self, item, *args, **kwargs)


class EnforcePrivateMeta(type):
    """
    Metaclass that is used to enforce private members. Private members are denoted with a '_' in the begging of the name
    of the member and a '_' in the end of the name of the member. Example _values_.
    Every member that matches that will now be protected and if tried to be accessed from
    a class that is not it's defining class, a PrivateMemberAccessException will be raised.
    """

    def __new__(cls, name, bases, attrs):
        fake_cls = None
        if len(bases) == 1 and bases[0] is object:
            fake_cls = type.__new__(cls, name, bases, attrs)
        else:
            for candidate in bases:
                if type(candidate) is EnforcePrivateMeta:
                    fake_cls = candidate
                    break

        attrs['__getattribute__'] = lambda *args, **kwargs: _private_member_access_protection(object.__getattribute__,
                                                                                              fake_cls,
                                                                                              *args,
                                                                                              **kwargs)
        attrs['__setattr__'] = lambda *args, **kwargs: _private_member_access_protection(object.__setattr__,
                                                                                         fake_cls,
                                                                                         *args,
                                                                                         **kwargs)
        return type.__new__(cls, name, bases, attrs)


class EnforcePrivate(object):
    """
    Class that is used to enforce private members. Private members are denoted with a '_' in the begging of the name
    of the member and a '_' in the end of the name of the member. Example _values_.
    Every member that matches that will now be protected and if tried to be accessed from
    a class that is not it's defining class, a PrivateMemberAccessException will be raised.
    """

    def __new__(typ, *args, **kwargs):
        orig_class = typ
        try:
            orig_class = typ.__mro__[typ.__mro__.index(EnforcePrivate) - 1]
        except:
            pass

        setattr(typ, '__getattribute__',
                lambda *args, **kwargs: _private_member_access_protection(object.__getattribute__, orig_class, *args,
                                                                          **kwargs))
        setattr(typ, '__setattr__',
                lambda *args, **kwargs: _private_member_access_protection(object.__setattr__, orig_class, *args,
                                                                          **kwargs))
        return super(EnforcePrivate, typ).__new__(typ, *args, **kwargs)


class EnforceProtectedMeta(type):
    """
    Metaclass that is used to enforce the convention of '_' in the begging of private member names.
    Every member that begins with the letter '_' will now be protected and if tried to be accessed from
    a class that is not it's defining class or a subclass of it, a ProtectedMemberAccessException will be raised.
    """

    def __new__(cls, name, bases, attrs):
        attrs['__getattribute__'] = lambda *args, **kwargs: _protected_member_access_protection(object.__getattribute__,
                                                                                                *args,
                                                                                                **kwargs)
        attrs['__setattr__'] = lambda *args, **kwargs: _protected_member_access_protection(object.__setattr__, *args,
                                                                                           **kwargs)
        return type.__new__(cls, name, bases, attrs)


class EnforceProtected(object):
    """
    Class that is used to enforce the convention of '_' in the begging of private member names.
    Every member that begins with the letter '_' will now be protected and if tried to be accessed from
    a class that is not it's defining class or a subclass of it, a ProtectedMemberAccessException will be raised.
    """

    def __new__(typ, *args, **kwargs):
        setattr(typ, '__getattribute__',
                lambda *args, **kwargs: _protected_member_access_protection(object.__getattribute__,
                                                                            *args,
                                                                            **kwargs))
        setattr(typ, '__setattr__',
                lambda *args, **kwargs: _protected_member_access_protection(object.__setattr__, *args,
                                                                            **kwargs))
        return super(EnforceProtected, typ).__new__(typ, *args, **kwargs)