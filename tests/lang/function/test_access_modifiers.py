import pytest
from lang.exceptions import ProtectedMemberAccessException, PrivateMemberAccessException
import logging

TEST_LOGGER = logging.Logger('Test Access Modifiers')

def test_protected_member(protected_class, protected_meta, protected_decorate):
    for obj in [protected_class, protected_meta, protected_decorate]:
        with pytest.raises(ProtectedMemberAccessException):
            assert obj._var == 2

def test_private_member(private_class, private_meta, private_decorate):
    for obj in [private_class, private_meta, private_decorate]:
        with pytest.raises(PrivateMemberAccessException):
            assert obj._var_ == 2
