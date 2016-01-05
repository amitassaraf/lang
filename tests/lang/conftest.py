import pytest
from lang.function.access_modifiers import EnforceProtected, EnforceProtectedMeta, EnforcePrivate, \
    EnforcePrivateMeta


@pytest.fixture
def protected_class():
    class Sample(EnforceProtected):
        _var = 5

    return Sample


@pytest.fixture
def protected_meta():
    class Sample(object):
        __metaclass__ = EnforceProtectedMeta
        _var = 5

    return Sample


@pytest.fixture
def private_class():
    class Sample(EnforcePrivate):
        _var_ = 5
        pass

    return Sample


@pytest.fixture
def private_meta():
    class Sample(object):
        __metaclass__ = EnforcePrivateMeta
        _var_ = 5

    return Sample
