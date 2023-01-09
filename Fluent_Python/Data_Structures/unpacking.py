import os


# INFO: * in a function
def fun(a, b, c, d, *rest):
    print(f"{a} = {b} = {c} = {d} = {rest}")
    return a, b, c, d, rest


metro_areas = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
    ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
    ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]


def main():
    print(f"{'':15} | {'latitude':>9} | {'longitude':>9}")
    for name, _, _, (lat, lon) in metro_areas:
        if lon <= 0:
            print(f"{name:15} | {lat:9.4f} | {lon:9.4f}")


if __name__ == "__main__":
    # INFO: parallel assignment
    lax_coordinates = (33.9425, -118.408056)
    latitude, longitude = lax_coordinates
    print(f"{latitude} & {longitude}")

    # INFO: swapping the values
    a, b = 3, 5
    print(f"{a} & {b}")
    b, a = a, b
    print(f"{a} & {b}")

    # INFO: using * & to grab excess items
    t = (20, 8)
    quotient, remainder = divmod(*t)
    print(f"{quotient} and {remainder}")
    c, *rest, d = range(5)
    print(f"{c}, {rest}, {d}")

    # INFO: using _
    _, filename = os.path.split("/home/xiekang/.ssh/id_rsa.pub")
    print(f"{filename}")

    # INFO: call function with * as parameter
    fun(*[1, 2], 3, *range(4, 7))

    # INFO: nested unpacking
    main()
