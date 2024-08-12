from enum import Enum


# Python supports ENUM
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def colorValue(color: "Color") -> None:
    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("I see green")
        case Color.BLUE:
            print("I'm feeling the blues :(")


def break_in_loop() -> None:
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, "equals", x, "*", n // x)
                break
        else:
            # else will be fired without break
            print(n, "is a prime number")


def http_error(status: int):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case 401 | 403 | 405:
            return "Not allowed"
        case _:
            return "Something is wrong with the internet"


def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)


if __name__ == "__main__":
    break_in_loop()
    print(http_error(100), http_error(403))
    combined_example(1, 2, kwd_only=3)
    # combined_example(pos_only=1, 2, 3) # error
    pairs = [(1, "one"), (2, "two"), (3, "three"), (4, "four")]
    pairs.sort(key=lambda pair: pair[1])
    print(pairs)

    # color = Color(input("Enter your choice of 'red', 'blue' or 'green' "))
    # colorValue(color)
