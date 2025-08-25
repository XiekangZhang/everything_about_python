from fractions import Fraction

if __name__ == "__main__":
    print(f"string lower vs cassfold: {'my_ßTest'.lower()} vs {'my_ßTest'.casefold()}")
    print(f"{'Python'.center(40, '-')}")
    print(f"{'Python'.ljust(40, '-')}")
    print(f"{'abc_1'.isalnum()} vs {'abc1'.isalnum()}")
    print(f"{'abc.com'.lstrip('c.')}")
    print(f"{'10'.zfill(5)}")

    # create the translate table
    # a -> 4, e -> 3
    translation_table = str.maketrans("ae", "43")
    text = "Python is a great language"
    translated_text = text.translate(translation_table)
    print(f"{text}: {translated_text}")

    print(f"{Fraction(1, 3)}")

    # printf
    print(
        "%(language)-s has %(number)+010d quote types."
        % {"language": "Python", "number": 2}
    )

    # byte and bytearray
    a = b"abc"
    print(a.replace(b"a", b"f"))
