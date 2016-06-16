import abc
import inspect
import types

"""
Wrap abc just for a nicer interface and a unified module for lang enforcing.
"""

EnforceAbstractMeta = abc.ABCMeta


class Abstract(object):
    __metaclass__ = EnforceAbstractMeta

    pass


abstract_property = abc.abstractproperty
abstract_method = abc.abstractmethod


def override(func):
    current_line = func.__code__.co_firstlineno
    module = inspect.getmodule(func)

    func_class = None
    for potential_class in dir(module):
        candidate_class = getattr(module, potential_class)
        if potential_class.startswith('_') or not isinstance(candidate_class, (type, types.ClassType)):
            continue

        class_code = inspect.getsourcelines(candidate_class)
        if class_code[1] < current_line:
            continue

        full_code = inspect.getsource(candidate_class)
        if inspect.getsource(func) in full_code:
            func_class = candidate_class
            break

    # If we fail just let it through
    if func_class is None:
        return func
