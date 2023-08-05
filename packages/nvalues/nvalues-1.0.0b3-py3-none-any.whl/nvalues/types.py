from typing import Any, TypeVar

# TODO: Use TypeVarTuple when mypy supports it.
# KeysT = TypeVarTuple("KeysT")
KeysT = TypeVar("KeysT", bound=tuple[Any, ...])
ValueT = TypeVar("ValueT")

VKeyT = TypeVar("VKeyT")
WKeyT = TypeVar("WKeyT")
XKeyT = TypeVar("XKeyT")
YKeyT = TypeVar("YKeyT")
ZKeyT = TypeVar("ZKeyT")
