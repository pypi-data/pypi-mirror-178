from typing import Any


class InvalidKey(LookupError):
    """
    Raised when a key fails a validation check.
    """

    def __init__(self, key: tuple[Any, ...], exception: Exception) -> None:
        super().__init__(f"Key {key} failed validation ({exception})")
        self._exception = exception
        self._key = key

    @property
    def exception(self) -> Exception:
        """
        Validation exception.
        """

        return self._exception

    @property
    def key(self) -> tuple[Any, ...]:
        """
        The key that failed validation.
        """

        return self._key


class KeyIndexOutOfRange(LookupError):
    """
    Raised when requesting a value by its index and that index is out of range.
    """

    def __init__(self, key_depth: int) -> None:
        self._key_depth = key_depth

    @property
    def key_depth(self) -> int:
        """
        Depth of the key that fell outside of its range.
        """

        return self._key_depth


class NKeyError(LookupError):
    """
    Raised when requesting the value of a key that doesn't exist and a default
    value hasn't been set.
    """

    def __init__(self, keys: tuple[Any, ...], key_index: int) -> None:
        msg = f"Key {key_index} of {keys} ({keys[key_index]}) does not exist"
        super().__init__(msg)


class NoDefaultValue(Exception):
    """
    Raised when requesting a volume's default value when one hasn't been set.
    """

    def __init__(self) -> None:
        super().__init__("The volume does not have a default value")
