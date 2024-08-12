"""List comprehension exercises"""


def get_vowel_names(nameList: list):
    """Return a list containing all names given that start with a vowel."""
    vowelNames = [
        name for name in nameList if name.lower().startswith(("a", "e", "i", "o", "u"))
    ]
    print(vowelNames)
    return vowelNames


def words_containing(wordsList: list, letter: str):
    """Return all words that contain the given letter."""
    containedWords = [word for word in wordsList if letter.lower() in word.lower()]
    print(containedWords)
    return containedWords


def translate(sentence: str):
    """Return a transliterated version of the given sentence."""
    translated = {
        "gato": "cat",
        "el": "the",
        "en": "in",
        "casa": "house",
        "esta": "is",
        "la": "the",
    }
    translatedSentence = " ".join([translated[word] for word in sentence.split()])
    print(translatedSentence)
    return translatedSentence


def get_factors(number: int):
    """Return a list of all factors of the given number."""
    factors = [num for num in range(1, number + 1) if number % num == 0]
    print(factors)
    return factors


def identity(size: int):
    """Return an identity matrix of size x size."""
    """
    identityMatrix = []
    helper = []
    for i in range(size):
        identityMatrix = []
        for j in range(size):
            if i == j:
                identityMatrix.append(1)
            else:
                identityMatrix.append(0)
        helper.append(identityMatrix)
    print(helper)"""
    return [[1 if row == col else 0 for row in range(size)] for col in range(size)]


def triples(number: int):
    """Return list of Pythagorean triples less than input num."""
    """for a in range(number):
        for b in range(number):
            for c in range(number):
                if (a**2 + b**2 == c**2) & (a < b < c):
                    print((a, b, c))"""
    return [
        (a, b, c)
        for a in range(number)
        for b in range(number)
        for c in range(number)
        if (a**2 + b**2 == c**2) & (a < b < c)
    ]
