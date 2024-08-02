def f():
    n = 100
    for i in range(0, 4):
        yield i/n
    return "ok"


def g():
    i = f()
    print("i: ", list(i))
    end = yield from f()
    print("End: ", end)


if __name__ == "__main__":
    list(g())
