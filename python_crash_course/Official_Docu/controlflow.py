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


if __name__ == "__main__":
    break_in_loop()
    print(http_error(100), http_error(403))
