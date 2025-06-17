"""
one example of chained functions, also called method chaining or fluent interfaces.
this script focuses on using decorators

! Any hat one specified information in Callable type hint --> at least 1

@author: XZhang
@version: 0.0.1
@since: 17.06.2025
@dependencies: python==3.12.0
@keywords: type hint, decorators, fluent interfaces
"""

import functools
from typing import TypeVar, Callable, Any, Union

T = TypeVar("T", bound="MyClass")


def chainable_with_args(
    method: Callable[[T, Any], Union[None, T]],
) -> Callable[[T, Any], T]:
    @functools.wraps(method)
    def wrapper(self: T, *args: Any, **kwargs: Any) -> T:
        result = method(self, *args, **kwargs)
        return self if result is None else result

    return wrapper


def chainable_no_args(method: Callable[[T], Union[None, T]]) -> Callable[[T], T]:
    @functools.wraps(method)
    def wrapper(self: T) -> T:
        result = method(self)
        return self if result is None else result

    return wrapper


class MyClass:
    def __init__(self):
        self.value = 0

    @chainable_with_args
    def add(self, x: int) -> None:
        self.value += x

    @chainable_with_args
    def multiply(self, y: int) -> None:
        self.value *= y

    @chainable_no_args
    def reset(self) -> None:
        self.value = 0

    def get_value(self) -> int:
        return self.value


if __name__ == "__main__":
    obj = MyClass()
    obj.add(5).multiply(2).reset().add(3)
    print(obj.value)

    obj2 = MyClass()
    result = obj2.add(5).multiply(2).get_value()
    print(result)
