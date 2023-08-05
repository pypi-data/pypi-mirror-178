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

    `default_value` is optional and defaults to none. Accessing a key without a
    default value will provoke `NKeyError`.
    """

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
