 # * Type aliases
Vector = list[float]
def scale (scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

from collections.abc import Sequence, Sized, Mapping
ConnectionOptions = dict[str, str]
Address = tuple[str, int]
Server = tuple[Address, ConnectionOptions]
def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    pass

def broadcast_message_1(message: str, servers: Sequence[tuple[tuple[str, int], dict[str, str]]]) -> None:
    pass

# * NewType
from typing import NewType
UserId = NewType("UserId", int)
# some_id = UserId(524313)
def get_user_name(user_id: UserId) -> str:
    return "no name"
# class AdminUserId(UserId): pass --> NewType does not create a new class
ProUserId = NewType("ProUserId", UserId)

# * Callable --> Callable[[Arg1Type, Arg2Type], ReturnType]
from collections.abc import Callable, Iterable, Iterator
def feeder(get_next_item: Callable[[], str]) -> None:
    pass

def async_query(on_success: Callable[[int], None], on_error: Callable[[int, Exception], None]) -> None:
    pass

async def on_update(value: str) -> None:
    pass

# * Generics
from typing import TypeVar, Generic, ParamSpec
from logging import Logger
T = TypeVar("T")
def first(l: Sequence[T]) -> T:
    return l[0]

class LoggedVar(Generic[T]):
    def __init__(self, value:T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log("Set " + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log("Get " + repr(self.value))
        return self.value
    
    def log(self, message: str) -> None:
        self.logger.info("%s: %s", self.name, message)

def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None: # todo: analyse and learn later!
    for var in vars:
        var.set(0)

# * a generic type can have any number of type variables. All varieties of TypeVar are permissible as parameters for a generic type
T = TypeVar("T", contravariant=True) # todo: learn later
B = TypeVar("B", bound=Sequence[bytes], covariant=True)
S = TypeVar("S", int, str) # S is either int or str
class WeirdTrio(Generic[T, B, S]): pass 
# ! Each type variable argument to Generic must be distinct. 
# class Pair(Generic[T, T]): pass # INVALID
class LinkedList(Sized, Generic[T]): pass
T = TypeVar("T")
class MyDict(Mapping[str, T]): pass
class MyIterable(Iterable): pass # Same as Iterable[Any] 
S = TypeVar("S")
Response = Iterable[S] | int
def response(query: str) -> Response[str]: return query

T = TypeVar('T', int, float, complex)
Vec = Iterable[tuple[T, T]]
def inproduct(v: Vec[T]) -> T: # Same as Iterable[tuple[T, T]]
    return sum(x*y for x, y in v) # type: ignore

T = TypeVar("T")
P = ParamSpec("P") # TODO: learn later
class Z(Generic[T, P]): pass

# * Any
from typing import Any
a: Any = None
def foo(item: Any): pass # * every type <--> Any
def hash_a(item: object): pass # * every type --> object, object !-> every other type

# ! subclassing
class Bucket: # Note: no base classes
    def __len__(self) -> int: return 0
    def __iter__(self) -> Iterator[int]: return None # type: ignore
def collect(items: Iterable[int]) -> int: return 0

if __name__ == "__main__":
    print(scale(2.0, [1.0, -4,2, 5.4]))
    print(get_user_name(UserId(42351)))
    print(get_user_name(-1)) # fails type checking but still compilable 
    print(type(UserId(12345) + UserId(12333))) # <class 'int'>
    collect(Bucket())