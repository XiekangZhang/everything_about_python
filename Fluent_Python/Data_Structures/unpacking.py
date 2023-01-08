import os

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