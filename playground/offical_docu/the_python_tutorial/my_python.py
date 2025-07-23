def my_func1():
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, "equals", x, "*", n / x)
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

    f("spam")

    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    print(matrix_transpose(matrix))
