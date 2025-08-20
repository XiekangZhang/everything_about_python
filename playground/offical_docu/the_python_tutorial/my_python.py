def my_func1():
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, "equals", x, "*", n // x)
                break
        else:
            print(n, "is a prime number")


def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 401 | 403 | 404:
            return "Not allowed"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teepot"
        case _:
            return "Something's wrong with the internet"


class Point:
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def compare(points):
    match points:
        case Point(x, y) if x == y:
            print(f"Y=X at {x}")
        case Point(x, y):
            print(f"Not on the diagonal")
        case []:
            print("No points")
        case [Point(0, 0)]:
            print("The origin")
        case [Point(x, y)]:
            print(f"Single point {x}, {y}")
        case [Point(0, y1), Point(0, y2)]:
            print(f"Two on the Y axis at {y1}, {y2}")
        case _:
            print("Something else")


def f1(a, L=[]):
    L.append(a)
    return L


def f(ham: str, eggs: str = "eggs") -> str:
    print(f"{ f.__annotations__  = } ")
    print(f"{ham = }, {eggs = }")
    return ham + " and " + eggs


def matrix_transpose(matrix):
    return list(zip(*matrix))


if __name__ == "__main__":
    print(r"C:\some\name", "C:\some\name", sep="||")

    # maketrans and translate example
    from_chars = "aeiou"
    to_chars = "12345"
    translation_table = str.maketrans(from_chars, to_chars)
    original_string = "hello this is a test"
    translated_string = original_string.translate(translation_table)
    print(f"{translated_string = }")

    # partition example
    email = "contact@example.com"
    parts = email.partition("@")
    print(f"{parts = }")  # ('contact', '@', 'example.com')
    print(
        "%(language)s has %(number)03d quote types."
        % {"language": "Python", "number": 2}
    )

    # else in for
    my_func1()

    print(http_error(400))
    compare(Point(0, 0))
    compare([Point(0, 0)])

    print(f1(1))
    print(f1(2))
    print(f1(3))

    f("spam")

    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    print(matrix_transpose(matrix))

    # Formatted String Literals
    import math

    print(f"The value of pi is approximately {math.pi:.3f}")
    animals = "eels"
    print(f"My hovercraft is full of {animals}.")
    print(f"My hovercraft is full of {animals!a}.")
    print(f"My hovercraft is full of {animals!s}.")
    print(f"My hovercraft is full of {animals!r}.")

    table = {k: str(v) for k, v in vars().items()}
    message = " ".join([f"{k}: " + "{" + k + "};" for k in table.keys()])
    print(message.format(**table))

    import json

    x = [1, "simple", "list"]
    print(json.dumps(x))  # JSON string representation
