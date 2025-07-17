from functools import (
    cache,
    cached_property,
    cmp_to_key,
    lru_cache,
    total_ordering,
    partial,
    partialmethod,
)
import locale
import statistics
import time


# ! the cache is threadsafe so that the wrapped function can be used in multiple threads. This means that the underlying data structure will remain coherent during concurrent updates.
@cache
def factorial(n):
    return n * factorial(n - 1)


# ! transform a method of a class into a property whose value is computed once and then cached as a normal attribute for the life of the instance
# ! a regular property blocks attribute writes unless a setter is defined. In contrast, a cached_property allows writes
# ! if synchronization is needed, implement the necessary locking inside the decorated getter function or around the cached property access
# ! if a mutable mapping is not available or if space-efficient key sharing is desired, an effect similar to cached_property() can also be achieved by stacking property() on top of lru_cache()
class DataSet:
    def __init__(self, sequence_of_numbers):
        self._data = tuple(sequence_of_numbers)

    @cached_property
    def stdev(self):
        return statistics.stdev(self._data)


# ! decorator to wrap a function with a memoizing callable that saves up to the maxsize most recent calls
# ! the cache is threadsafe so that the wrapped function can be used in multiple threads.
@lru_cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ! __eq__(), __lt__(), __le__(), __gt__(), __ge__() --> rich comparison ordering methods
# ! using this decoratos, you only need implements __eq__(), __lt__() or/and __gt__() --> the __le__() and __ge__() will be automatically useful
# ! e.g., __le__() = __eq__() & __lt__() etc. However, it needs more resources.
@total_ordering
class Student:
    def __eq__(self):
        pass

    def __lt__(self):
        pass

    def __gt__(self):
        pass


# ! partial creates a new function with partial application of the given arguments and keywords
def power(base, exponent):
    return base**exponent


# ! partialmethod: same to partial but for a method of a class. It is better to use with __get__ together.
class Cell:
    def __init__(self):
        self._alive = False

    @property
    def alive(self):
        return self._alive

    def set_state(self, state):
        self._alive = bool(state)

    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)


if __name__ == "__main__":
    my_list = {"b": 12, "a": 1, "c": 3}
    # ! transform an old-style comparison function to a key_function
    print(sorted(my_list, key=cmp_to_key(locale.strcoll)))

    start_time = time.time()
    print([fib(n) for n in range(16)])
    print(fib.cache_info())
    print(f"First call duration: {time.time() - start_time:.4f} seconds")
    start_time = time.time()
    print([fib(n) for n in range(16)])
    print(fib.cache_info())
    print(f"Second call duration: {time.time() - start_time:.4f} seconds")

    square = partial(power, exponent=2)
    print(square(5))  # Output: 25

    c = Cell()
    print(c.alive)
    c.set_alive()
    print(c.alive)
