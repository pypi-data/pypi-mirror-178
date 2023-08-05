from typing import Any


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
