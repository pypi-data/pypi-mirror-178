from nvalues.types import ValueT, XKeyT, YKeyT
from nvalues.volume import Volume


class Grid(Volume[tuple[XKeyT, YKeyT], ValueT]):
    """
    A two-dimensional volume of values.

    Three generic types are required:

    1. `x` key type
    1. `y` key type
    1. Value type

    For example, to create a `Grid` with `x` string keys, `y` integer keys and
    boolean values:

    ```python
    grid = Grid[str, int, bool]()
    ```

    `default_value` is optional and defaults to none. Accessing a key without a
    default value will provoke `NKeyError`.
    """

    def delete(self, x: XKeyT, y: YKeyT) -> None:
        """
        Deletes the key `x, y`.
        """

        del self[x, y]

    def get(self, x: XKeyT, y: YKeyT) -> ValueT:
        """
        Gets the value of key `x, y`.
        """

        return self[(x, y)]

    def set(self, x: XKeyT, y: YKeyT, value: ValueT) -> None:
        """
        Sets the value of key `x, y`.
        """

        self[(x, y)] = value
