if __name__ == "__main__":
    # * underscores in numbers
    universe_age = 14_000_000_000 # = 140_0000_0000
    print(universe_age)

    # * List Comprehensions
    squares = [value ** 2 for value in range(1, 11)]
    print(squares)

    # * input
    message = input("Tell me something, and I will repeat it back to you: ")
    print(message) # ! input() -> str, a convertor is needed