import pytest
from lang.function.access_modifiers import EnforceProtected, EnforceProtectedMeta, EnforcePrivate, \
    EnforcePrivateMeta, enforce_protected, enforce_private


@pytest.fixture
def protected_class():
    class Sample(EnforceProtected):
        def __init__(self):
            self._var = 5

    return Sample()


@pytest.fixture
def protected_meta():
    class Sample(object):
        __metaclass__ = EnforceProtectedMeta
        def __init__(self):
            self._var = 5

    return Sample()

@pytest.fixture
def protected_decorate():
    @enforce_protected
    class Sample(object):
        def __init__(self):
            self._var = 5

    return Sample()

@pytest.fixture
def private_class():
    class Sample(EnforcePrivate):
        def __init__(self):
            self._var_ = 5
        pass

    return Sample()


@pytest.fixture
def private_meta():
    class Sample(object):
        __metaclass__ = EnforcePrivateMeta
        def __init__(self):
            self._var_ = 5

    return Sample()

@pytest.fixture
def private_decorate():
    @enforce_private
    class Sample(object):
        def __init__(self):
            self._var_ = 5

    return Sample()
