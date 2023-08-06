from typing import Any, Generic

from nvalues.types import KeysT, ValueT


class Value(Generic[KeysT, ValueT]):
    """
    A value plucked from a volume.
    """

    def __init__(self, key: KeysT, value: ValueT) -> None:
        self._key = key
        self._value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Value):
            return False

        other_value: Value[Any, Any] = other

        if self.key != other_value.key:
            return False

        if self.value != other_value.value:
            return False

        return True

    def __repr__(self) -> str:
        return f"{repr(self.value)} @{repr(self.key)}"

    @property
    def key(self) -> KeysT:
        """
        Volume key.
        """

        return self._key

    @property
    def value(self) -> ValueT:
        """
        Value.
        """

        return self._value
