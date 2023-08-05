from nvalues.types import ValueT, VKeyT, WKeyT, XKeyT, YKeyT, ZKeyT
from nvalues.volume import Volume


class Penteract(Volume[tuple[VKeyT, WKeyT, XKeyT, YKeyT, ZKeyT], ValueT]):
    """
    A five-dimensional volume of values.

    Six generic types are required:

    1. `v` key type
    1. `w` key type
    1. `x` key type
    1. `y` key type
    1. `z` key type
    1. Value type

    For example, to create a `Tesseract` with `v` integer keys, `w` string
    keys, `x` string keys, `y` int keys, `z` float keys and boolean values:

    ```python
    penteract = Penteract[int, str, str, int, float, bool]()
    ```

    `default_value` is optional and defaults to none. `NKeyError` will be
    raised if a key without a value or default value is read.

    `key_validator` is an optional function that validates if a key is valid.
    The function must raise an exception if the key is invalid. `InvalidKey`
    will be raised if an invalid key is accessed.
    """

    def delete(self, v: VKeyT, w: WKeyT, x: XKeyT, y: YKeyT, z: ZKeyT) -> None:
        """
        Deletes the key `v, w, x, y, z`.
        """

        del self[v, w, x, y, z]

    def get(self, v: VKeyT, w: WKeyT, x: XKeyT, y: YKeyT, z: ZKeyT) -> ValueT:
        """
        Gets the value of key `v, w, x, y, z`.
        """

        return self[(v, w, x, y, z)]

    def set(
        self,
        v: VKeyT,
        w: WKeyT,
        x: XKeyT,
        y: YKeyT,
        z: ZKeyT,
        value: ValueT,
    ) -> None:
        """
        Sets the value of key `v, w, x, y, z`.
        """

        self[(v, w, x, y, z)] = value
