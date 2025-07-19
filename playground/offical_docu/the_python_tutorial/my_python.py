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
