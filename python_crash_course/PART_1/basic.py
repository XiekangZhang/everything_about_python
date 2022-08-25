if __name__ == "__main__":
    # info: underscores in numbers
    universe_age = 14_000_000_000 # = 140_0000_0000
    print(universe_age)

    # info: List Comprehensions
    squares = [value ** 2 for value in range(1, 11)]
    print(squares)

    # info: input
    message = input("Tell me something, and I will repeat it back to you: ")
    print(message) # info: input() -> str, a convertor is needed