"""
this script is about using type hint within python.

basic types: int, float, str, bool, bytes, List, Tuple, Dict, Set, None, Any
advanced types: Union, Optional, Callable[*input_parameters, *outputs], NewType
type aliases, generic type, structural typing

@author: XZhang
@version: 0.0.1
@since: 17.06.2025
@dependencies: python==3.12.0
@keywords: type aliases, generic type, structural typing
"""

from typing import (
    List,
    Tuple,
    Dict,
    Set,
    Union,
    Optional,
    Any,
    Callable,
    NewType,
    TypeVar,
    Protocol,
)


def base_type_hint():
    string: str
    num: int
    numeric: float
    boolean: bool
    strings: List[str]
    tuples: Tuple[str, int, float]
    tests: Tuple[int, ...]
    dictionary: Dict[str, str]
    sets: Set[str]


# Union[str, int] --> new feature: str | int, python version > 3.9
# Optional[int] = Union[type, None]
def union_types_for_or(value: Union[str, int], others: Any = "") -> Optional[int]:
    if isinstance(value, int):
        pass
    elif isinstance(value, str):
        pass
    return others


# Callable[*inputs, *outputs] --> Callable[[int, int], int] takes 2 input parameters and delivers 1 output
def callable_types(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)


# type aliases
Point = Tuple[float, float]
Color = Tuple[int, int, int]


def type_aliases(p1: Point, p2: Point) -> Color:
    return (0, 0, 0)


# New Type: distinguish between two types that have the same underlying representing but different meaning
UserId = NewType("UserId", int)


def get_user_name(user_id: UserId) -> str:
    new_id = UserId(123)
    return ""


# generic type --> bound defines that a type variable must be a subtype of a given type
T = TypeVar("T", bound="MyClass")


def first(items: List[T]) -> T:
    return items[0]


class MyClass:
    pass


# structural typing
class SupportsRead(Protocol):
    pass


def read_data(reader: SupportsRead) -> None:
    pass
