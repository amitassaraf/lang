import abc

"""
Wrap abc just for a nicer interface and a unified module for lang enforcing.
"""

AbstractMeta = abc.ABCMeta

class Abstract(object):

    __metaclass__ = AbstractMeta

    pass

abstract_property = abc.abstractproperty
abstract_method = abc.abstractmethod
