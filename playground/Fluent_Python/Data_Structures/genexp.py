import array

if __name__ == "__main__":
    # INFO: tuple & array
    symbols = "$¢£¥€¤"
    t = tuple(ord(symbol) for symbol in symbols)
    a = array.array("I", (ord(symbol) for symbol in symbols))
    print(f"{t} = {a}")

    # INFO: Tuples used as records
    lax_coordinates = (33.9425, -118.408056)
    city, year, pop, chg, area = ("Tokyo", 2003, 32_450, 0.66, 8014)
    traveler_ids = [
        ("USA", "31195855"), ("BRA", "CE342567"), ("ESP", "XDA205856")
    ]
    for passport in sorted(traveler_ids):
        print("%s/%s" % passport)
        # IDEA: % formatting operator understands tuples and treats each item as a separate field.
    for country, _ in traveler_ids:
        print(country)

    # INFO: Tuples as Immutable Lists

