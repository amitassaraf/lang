import abc

"""
Wrap abc just for a nicer interface and a unified module for lang enforcing.
"""

EnforceAbstractMeta = abc.ABCMeta


class Abstract(object):
    __metaclass__ = EnforceAbstractMeta

    pass


abstract_property = abc.abstractproperty
abstract_method = abc.abstractmethod
