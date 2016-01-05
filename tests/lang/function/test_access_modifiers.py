import pytest
from lang.exceptions import ProtectedMemberAccessException


def test_protected_member(protected_class, protected_meta):
    classes = [protected_class, protected_meta]
    for cls in classes:
        with pytest.raises(ProtectedMemberAccessException):
            assert cls._var == 2