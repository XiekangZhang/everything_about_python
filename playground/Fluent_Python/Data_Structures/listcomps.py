if __name__ == "__main__":
    # INFO: := operator
    x = "ABC"
    codes = [last := ord(c) for c in x]
    print(f"{codes} + {last}")

    # INFO: Listcomps vs map & filter
    symbols = "$¢£¥€¤"
    beyond_ascii1 = [ord(s) for s in symbols if ord(s) > 127]
    beyond_ascii2 = list(filter(lambda c: c > 127, map(ord, symbols)))
    print(f"{beyond_ascii1} = {beyond_ascii2}")

    # INFO: Cartesian Products
    colors = ["black", "white"]
    sizes = ["S", "M", "L"]
    tshirts = [(color, size) for color in colors
               for size in sizes]
    print(tshirts)
