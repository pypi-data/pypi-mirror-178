from nvalues.types import ValueT, XKeyT, YKeyT, ZKeyT
from nvalues.volume import Volume


class Cube(Volume[tuple[XKeyT, YKeyT, ZKeyT], ValueT]):
    """
    A three-dimensional volume of values.

    Four generic types are required:

    1. `x` key type
    1. `y` key type
    1. `z` key type
    1. Value type

    For example, to create a `Cube` with `x` string keys, `y` integer keys, `z`
    float keys and boolean values:

    ```python
    cube = Cube[str, int, float, bool]()
    ```

    `default_value` is optional and defaults to none. Accessing a key without a
    default value will provoke `NKeyError`.
    """

    def delete(self, x: XKeyT, y: YKeyT, z: ZKeyT) -> None:
        """
        Deletes the key `x, y, z`.
        """

        del self[x, y, z]

    def get(self, x: XKeyT, y: YKeyT, z: ZKeyT) -> ValueT:
        """
        Gets the value of key `x, y, z`.
        """

        return self[(x, y, z)]

    def set(self, x: XKeyT, y: YKeyT, z: ZKeyT, value: ValueT) -> None:
        """
        Sets the value of key `x, y, z`.
        """

        self[(x, y, z)] = value
