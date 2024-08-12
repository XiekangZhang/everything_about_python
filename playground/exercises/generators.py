"""Generator Exercises."""


def all_together(*inputValues):
    """Join together all items from the given iterables."""
    # return (list(_help(*inputValues)))
    return (item for item in _help(*inputValues))


def _help(*inputValues):
    for item in inputValues:
        for i in item:
            yield i


def sum_numbers(string):
    """Return the sum of all numbers in the given list-of-lists."""
    # breakpoint()
    return sum(int(num) for num in string.split())


def interleave():
    """Return iterable of one item at a time from each list."""


def parse_ranges():
    """Return a list of numbers corresponding to number ranges in a string"""


def is_prime():
    """Return True if candidate number is prime."""


def deep_add():
    """Return sum of values in given iterable, iterating deeply."""
