from nvalues.types import ValueT, WKeyT, XKeyT, YKeyT, ZKeyT
from nvalues.volume import Volume


class Tesseract(Volume[tuple[WKeyT, XKeyT, YKeyT, ZKeyT], ValueT]):
    """
    A four-dimensional volume of values.

    Five generic types are required:

    1. `w` key type
    1. `x` key type
    1. `y` key type
    1. `z` key type
    1. Value type

    For example, to create a `Tesseract` with `w` string keys, `x` string keys,
    `y` int keys, `z` float keys and boolean values:

    ```python
    tesseract = Tesseract[str, str, int, float, bool]()
    ```

    `default_value` is optional and defaults to none. Accessing a key without a
    default value will provoke `NKeyError`.
    """

    def delete(self, w: WKeyT, x: XKeyT, y: YKeyT, z: ZKeyT) -> None:
        """
        Deletes the key `w, x, y, z`.
        """

        del self[w, x, y, z]

    def get(self, w: WKeyT, x: XKeyT, y: YKeyT, z: ZKeyT) -> ValueT:
        """
        Gets the value of key `w, x, y, z`.
        """

        return self[(w, x, y, z)]

    def set(
        self,
        w: WKeyT,
        x: XKeyT,
        y: YKeyT,
        z: ZKeyT,
        value: ValueT,
    ) -> None:
        """
        Sets the value of key `w, x, y, z`.
        """

        self[(w, x, y, z)] = value
