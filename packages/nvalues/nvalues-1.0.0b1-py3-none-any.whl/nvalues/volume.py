from typing import Any, Dict, Generic, cast

from nvalues.exceptions import NKeyError, NoDefaultValue
from nvalues.types import KeysT, ValueT


class Volume(Generic[KeysT, ValueT]):
    """
    An n-dimensional volume of values.

    Two generic types are required:

    1. Tuple of key types
    2. Value type

    For example, to create a spreadsheet of floats with `x` string keys and `y`
    integer keys:

    ```python
    volume = Volume[tuple[str, int], float]()
    ```

    `default_value` is optional and defaults to none. Accessing a key without a
    default value will provoke `NKeyError`.

    Values are read and set via their keys. For example:

    ```python
    volume = Volume[tuple[str, int], float]()
    volume["A", 0] = 1.2
    print(volume["A", 0])
    # 1.2
    ```
    """

    class NullDefaultValue:
        """
        An unset default value. This is distinct from `None` which is a
        legitimate default value.
        """

    def __init__(
        self,
        default_value: ValueT | NullDefaultValue = NullDefaultValue(),
    ) -> None:
        self._default = default_value
        self._values: Dict[Any, Any] = {}

    def __getitem__(self, keys: KeysT) -> ValueT:
        context = self._values
        key_index = 0

        try:
            for index, key in enumerate(keys):
                key_index = index
                context = context[key]
        except KeyError:
            try:
                return self.default
            except NoDefaultValue as no_default_value:
                raise NKeyError(keys, key_index) from no_default_value

        return cast(ValueT, context)

    def __setitem__(self, keys: KeysT, value: ValueT) -> None:
        context = self._values
        index = 0

        while index < len(keys) - 1:
            key = keys[index]
            if key not in context:
                context[key] = {}
            context = context[key]
            index += 1

        context[keys[-1]] = value

    def clear_default(self) -> None:
        """
        Clears the default value.
        """

        self._default = Volume.NullDefaultValue()

    @property
    def default(self) -> ValueT:
        """
        Default value to return when accessing a key that doesn't exist.
        """

        if isinstance(self._default, Volume.NullDefaultValue):
            raise NoDefaultValue()
        return self._default

    @default.setter
    def default(self, value: ValueT) -> None:
        self._default = value
