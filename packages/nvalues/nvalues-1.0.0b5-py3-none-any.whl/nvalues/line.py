from nvalues.types import ValueT, XKeyT
from nvalues.volume import Volume


class Line(Volume[tuple[XKeyT], ValueT]):
    """
    A one-dimensional volume of values.

    Two generic types are required:

    1. Key type
    2. Value type

    For example, to create a `Line` with integer keys and string values:

    ```python
    line = Line[int, str]()
    ```

    `default_value` is optional and defaults to none. `NKeyError` will be
    raised if a key without a value or default value is read.

    `key_validator` is an optional function that validates if a key is valid.
    The function must raise an exception if the key is invalid. `InvalidKey`
    will be raised if an invalid key is accessed.
    """

    def delete(self, x: XKeyT) -> None:
        """
        Deletes the key `x`.
        """

        del self[(x,)]

    def get(self, x: XKeyT) -> ValueT:
        """
        Gets the value of key `x`.
        """

        return self[(x,)]

    def set(self, x: XKeyT, value: ValueT) -> None:
        """
        Sets the value of key `x`.
        """

        self[(x,)] = value
