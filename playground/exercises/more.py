"""More comprehension exercises."""


def join_items(items: list, sep: str = " "):
    """Return a string representing the given iterable joined together."""
    return sep.join(str(item) for item in items)


def flatten(matrix: list[list]) -> list:
    """Return a flattened version of the given 2-D matrix (list-of-lists)."""
    return [item for sublist in matrix for item in sublist]


def transpose(lists: list) -> list:
    """Return a transposed version of given list of lists."""
    result = []
    for index, listRow in enumerate(lists):
        print(index)
        if len(listRow) > 1:
            pass
        else:
            return lists
    return result

def movies_from_year():
    """Return titles of all movies released in the given year."""


def matrix_add():
    """Add corresponding numbers in given 2-D matrices."""
