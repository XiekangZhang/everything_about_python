from __future__ import annotations 
from typing import (
    TYPE_CHECKING,
    List,
    TypeAlias,
    Tuple,
    Union,
    Optional,
    Callable,
    Concatenate,
    ParamSpec,
    TypeVar,
    Type,
    final,
    overload,
    Literal,
    ClassVar,
    Final,
    Annotated,
    TypeGuard,
    Generic,
    ParamSpecArgs,
    ParamSpecKwargs,
    AnyStr,
    Protocol,
    runtime_checkable,
    NamedTuple,
    NewType,
    TypedDict,
)
import logging
from threading import Lock
import threading
import math
import sys
import collections

# * Concatenate: Used with Callable and ParamSpec to type annotate a higher order
# * callable which adds, removes, or transforms parameters of another callable
P = ParamSpec("P")
R = TypeVar("R")

# Use this lock to ensure that only one thread is executing a function at any time
my_lock = Lock()


def with_lock(f: Callable[Concatenate[Lock, P], R]) -> Callable[P, R]:
    """A type-safe decorator which provides a lock."""

    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        # Provide the lock as the first argument
        return f(my_lock, *args, **kwargs)

    return inner


@with_lock
def sum_threadsafe(lock: Lock, numbers: list[float]) -> float:
    """Add a list of numbers together in a thread-safe manner."""
    with lock:
        return sum(numbers)


# * Type[C] is covariant
class User:
    pass


class BasicUser(User):
    pass


class ProUser(User):
    pass


class TeamUser(User):
    pass


def make_new_user(
    user_class: Type[User],
) -> User:  # Accept User, BasicUser, ProUser, TeamUser, ...
    return user_class()


# * Literal
def accepts_only_four(x: Literal[4]) -> None:
    pass


# * ClassVar: class varialbe
class Starship:
    stats: ClassVar[dict[str, int]] = {}  # class variable
    damage: int = 10  # instance variable


# * TypeGuard
def is_str_list(val: List[object]) -> TypeGuard[List[str]]:
    """Determines whether all objects in the list are strings"""
    return all(isinstance(x, str) for x in val)


def func1(val: List[object]):  # if ture, List[object] narrows to List[str]
    if is_str_list(val):
        print(" ".join(val))
    else:
        print("Not a list of strings!")


# * Generic
KT = TypeVar("KT")
VT = TypeVar("VT")


class Mapping(Generic[KT, VT]):
    def __getitem__(self, key: KT) -> VT:
        return None  # type: ignore


X = TypeVar("X")
Y = TypeVar("Y")


def lookup_name(mapping: Mapping[X, Y], key: X, default: Y) -> Y:
    try:
        return mapping[key]
    except KeyError:
        return default


# * TypeVar
T = TypeVar("T")  # Can be anything
S = TypeVar("S", bound=str)  # Can be any subtype of str
A = TypeVar("A", str, bytes)  # Must be exactly str or bytes
C = TypeVar("C", bound="Circle")


class Circle:
    """An abstract circle"""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    # Use a type variable to show that the return type will always be an instance of whatever 'cls' is
    @classmethod
    def with_circumference(cls: type[C], circumference: float) -> C:
        """Create a circle with the specified circumference"""
        radius = circumference / (math.pi * 2)
        return cls(radius)


class Tire(Circle):
    """A specialised circle (made out of rubber)"""

    MATERIAL: ClassVar = "rubber"


# * ParamSpec: they are used to forward the parameter types of one callable to another callable
T = TypeVar("T")
P = ParamSpec("P")


def add_logging(f: Callable[P, T]) -> Callable[P, T]:
    """A type-safe decorator to add logging to a function."""

    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        logging.info(f"{f.__name__} was called!")
        return f(*args, **kwargs)

    return inner


@add_logging
def add_two(x: float, y: float) -> float:
    """Add two numbers together."""
    return x + y


# * AnyStr = TypeVar('AnyStr', str, bytes)
def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b


# * runtime_checkable & Protocol: structural subtyping
@runtime_checkable
class Named(Protocol):
    name: str


# * NamedTuple = collections.namedtuple("Employee", [('name', str), ('id', int)])
class Employee(NamedTuple):
    name: str
    id: int


# * TypedDict --> Point2D = TypedDict('Point2D', x=int, y=int, label=str) | Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})
class Point2D(TypedDict):
    x: int
    y: int
    label: str


# * @overload
@overload
def myfunc(arg: Literal[True]) -> str:
    ...


@overload
def myfunc(arg: Literal[False]) -> int:
    ...


@overload
def myfunc(arg: bool) -> str | int:
    ...


def myfunc(arg: bool) -> str | int:
    if arg:
        return "something"
    else:
        return 0


# * @final --> method or class can not be overwritten
@final
class Leaf:
    pass


class Base:
    @final
    def done(self) -> None:
        pass

# * for expensive mod
if TYPE_CHECKING:
    import collections
    test = collections.namedtuple("test", ["name", "id"])
    def fun(arg: test) -> None:


if __name__ == "__main__":
    # * TypeAlias
    Factors: TypeAlias = list[int]  # distinct parameter initialization and typealias
    print(type(Factors))

    # * Tuple, Union --> Union[X, Y] = X | Y
    print(Union[str, int] == str | int)

    # * Optional = X | None
    print(Optional[str] == str | None)

    # * Callable[[int], str] --> function(int) -> str

    # * Concatenate
    print(sum_threadsafe([1.1, 2.2, 3.3]))

    # * Type[class]

    # * Literal: could be understood as enum --> some expression has literally a specific value
    # accepts_only_four(4)
    # accepts_only_four(19) --> error

    # * FINAL: value not changeable
    MAX_SIZE: Final[int] = 9000
    MAX_SIZE += 1
    print(MAX_SIZE)

    # * Annotated: a type to decorate with existing type
    T1 = Annotated[int, range(-10, 5)]
    T2 = Annotated[T1, range(-20, 3)]

    # * TypeGuard aims to benefit type narrowing - a technique used by static type checkers to determine a more precise type of an expression within a program's code flow.
    # the return value is aboolean , if the return value is True, the type of its argument is the type inside TypeGuard
    func1(["jfdksl", "fj", "psl"])

    # * TypeVar
    print(type(Circle.with_circumference(3)))
    print(type(Tire.with_circumference(4)))

    # * ParamSpec --> ParamSpecArgs: P.args & ParamSpecKwargs: P.kwargs
    print(add_two(1.3, 3.4))

    # * AnyStr
    print(concat("foo", "bar"))
    print(concat(b"foo", b"bar"))

    # * runtime_checkable & Protocol
    print(isinstance(threading.Thread(name="Bob"), Named))

    # * NewType
    UserId = NewType("UserId", int)
    first_user = UserId(1)
    print(first_user)

    # * TypedDict
    a: Point2D = {"x": 1, "y": 2, "label": "good"}
    print(a)
