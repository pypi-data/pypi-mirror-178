from typing import Any, Dict, Generic, Iterator, List, Optional, Sequence, cast

from nvalues.exceptions import (
    InvalidKey,
    KeyIndexOutOfRange,
    NKeyError,
    NoDefaultValue,
)
from nvalues.types import KeysT, KeyValidator, ValueT
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

    `default_value` is optional and defaults to none. `NKeyError` will be
    raised if a key without a value or default value is read.

    `key_validator` is an optional function that validates if a key is valid.
    The function must raise an exception if the key is invalid. `InvalidKey`
    will be raised if an invalid key is accessed.
    """

    class NullDefaultValue:
        """
        An unset default value. This is distinct from `None` which is a
        legitimate default value.
        """

    def __init__(
        self,
        default_value: ValueT | NullDefaultValue = NullDefaultValue(),
        key_validator: Optional[KeyValidator[KeysT]] = None,
    ) -> None:
        self._default = default_value
        self._dim_len: Optional[int] = None  # Unknown until a value is added.
        self._values: Dict[Any, Any] = {}

        self.key_validator = key_validator
        """
        Key validator. Must raise an exception if the specified key is invalid.
        """

    def __delitem__(self, key: KeysT) -> None:
        self.validate_key(key)
        self._delete_key(key)

    def __getitem__(self, key: KeysT) -> ValueT:
        self.validate_key(key)

        context = self._values
        key_index = 0

        try:
            for index, curr_key in enumerate(key):
                key_index = index
                context = context[curr_key]
        except KeyError:
            try:
                return self.default
            except NoDefaultValue as no_default_value:
                raise NKeyError(key, key_index) from no_default_value

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

    def __setitem__(self, key: KeysT, value: ValueT) -> None:
        self.validate_key(key)

        self._dim_len = len(key)

        context = self._values
        index = 0

        while index < len(key) - 1:
            curr_key = key[index]
            if curr_key not in context:
                context[curr_key] = {}
            context = context[curr_key]
            index += 1

        context[key[-1]] = value

    def _delete_key(self, key: Sequence[Any]) -> None:
        if not key:
            # Our deletes are idempotent so fail gracefully.
            return

        context = self._values

        try:
            for curr_key in key[:-1]:
                context = context[curr_key]
        except KeyError:
            # Our deletes are idempotent so fail gracefully.
            return

        del context[key[-1]]

        # If this dict is empty now then we can delete it from its parent.
        if not context:
            self._delete_key(key[:-1])

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

    def validate_key(self, key: KeysT) -> None:
        """
        Validates that `key` is valid. Has no effect if a key validator hasn't
        been set.

        Raises `InvalidKey` if the key is invalid.
        """

        if not self.key_validator:
            return

        try:
            self.key_validator(key)
        except Exception as ex:
            raise InvalidKey(key, ex) from ex
