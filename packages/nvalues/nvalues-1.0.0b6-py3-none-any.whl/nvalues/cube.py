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

    `default` is the default value to return if a non-existent key is read.
    `default_maker` is a function that returns the default value for a given
    key. You must specify neither or one of these; not both. `NKeyError` will
    be raised if a non-existent key is read without a default value.

    `key_validator` is an optional function that validates if a key is valid.
    The function must raise an exception if the key is invalid. `InvalidKey`
    will be raised if an invalid key is accessed.
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
