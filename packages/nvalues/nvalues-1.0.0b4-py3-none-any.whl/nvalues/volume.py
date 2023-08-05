from typing import Any, Dict, Generic, Iterator, List, Optional, Sequence, cast

from nvalues.exceptions import KeyIndexOutOfRange, NKeyError, NoDefaultValue
from nvalues.types import KeysT, ValueT
from nvalues.value import Value


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

    Values are read, set and deleted via their keys. For example:

    ```python
    from nvalues import Volume

    volume = Volume[tuple[str, int], float](0)

    volume["A", 0] = 1.2
    print(volume["A", 0])
    # 1.2

    del volume["A", 0]
    print(volume["A", 0])
    # 0
    ```

    Values can also be iterated. For example:

    ```python
    from nvalues import Volume

    volume = Volume[tuple[int, int], str]()

    volume[0, 0] = "zero-zero"
    volume[4, 0] = "four-zero"
    volume[0, 4] = "zero-four"

    for item in volume:
        print(f"Found {item.value} at {item.key}")

    # Found zero-zero at (0, 0)
    # Found zero-four at (0, 4)
    # Found four-zero at (4, 0)
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
        self._dim_len: Optional[int] = None  # Unknown until a value is added.
        self._values: Dict[Any, Any] = {}

    def __delitem__(self, keys: KeysT) -> None:
        self._delete_key(keys)

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

    def __iter__(self) -> Iterator[Value[KeysT, ValueT]]:
        if self._dim_len is None:
            # self._dim_len isn't set until a value is added. If it's None then
            # there legitimately aren't any values to yield.
            return

        indexes = [0] * self._dim_len

        while True:
            try:
                keys, value = self._from_index(indexes)
            except KeyIndexOutOfRange as out_of_range:
                if out_of_range.key_depth == 0:
                    # When the root index is eventually out of range then stop
                    # because there aren't any parents to iterate.
                    return

                # Reset the key index (and all children) that was out of range
                # to 0. We'll increment its parent in a moment.
                for index in range(out_of_range.key_depth, self._dim_len):
                    indexes[index] = 0

                # Increment the parent index of the key index that was out of
                # range. There's no guarantee that this index exists, but we'll
                # find out on the next iteration.
                indexes[out_of_range.key_depth - 1] += 1
                continue

            yield Value(cast(KeysT, tuple(keys)), value)

            # Increment the leaf key index. We don't know that a value at this
            # index will exist, but the next iteration will handle and roll-
            # over the indexes if we need to.
            indexes[-1] += 1

    def __setitem__(self, keys: KeysT, value: ValueT) -> None:
        self._dim_len = len(keys)

        context = self._values
        index = 0

        while index < len(keys) - 1:
            key = keys[index]
            if key not in context:
                context[key] = {}
            context = context[key]
            index += 1

        context[keys[-1]] = value

    def _delete_key(self, keys: Sequence[Any]) -> None:
        if not keys:
            # Our deletes are idempotent so fail gracefully.
            return

        context = self._values

        try:
            for key in keys[:-1]:
                context = context[key]
        except KeyError:
            # Our deletes are idempotent so fail gracefully.
            return

        del context[keys[-1]]

        # If this dict is empty now then we can delete it from its parent.
        if not context:
            self._delete_key(keys[:-1])

    def _from_index(
        self,
        indexes: List[int],
        context: Optional[Dict[Any, Any]] = None,
        depth: int = 0,
    ) -> tuple[List[Any], ValueT]:
        """
        Returns the key and value at the index described by `indexes`.

        Raises `KeyIndexOutOfRange` if `indexes` is out of range.
        """

        context = self._values if context is None else context

        key_index = indexes[depth]
        keys = list(context.keys())

        try:
            key = keys[key_index]
        except IndexError as index_error:
            raise KeyIndexOutOfRange(depth) from index_error

        context = context[key]

        if depth == len(indexes) - 1:
            return [key], cast(ValueT, context)

        child_keys, value = self._from_index(
            indexes,
            context=context,
            depth=depth + 1,
        )

        return [key, *child_keys], value

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
