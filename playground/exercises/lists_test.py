"""Tests for list comprehension exercises"""
import unittest

from lists import (
    get_vowel_names,
    words_containing,
    translate,
    get_factors,
    identity,
    triples,
)


class GetVowelNamesTests(unittest.TestCase):

    """Tests for get_vowel_names."""

    def test_one_vowel_name(self):
        names = ["Alice", "Bob", "Christy", "Jules"]
        self.assertEqual(get_vowel_names(names), ["Alice"])

    def test_multiple_vowel_names(self):
        names = ["Scott", "arthur", "Jan", "Elizabeth"]
        self.assertEqual(get_vowel_names(names), ["arthur", "Elizabeth"])

    def test_empty(self):
        self.assertEqual(get_vowel_names([]), [])


class WordsContainingTests(unittest.TestCase):

    """Tests for words_containing."""

    def test_last_letter(self):
        words = ['My', 'life', 'is', 'my', 'message']
        matching = ['My', 'my']
        self.assertEqual(words_containing(words, 'y'), matching)

    def test_different_positions(self):
        words = ['My', 'life', 'is', 'my', 'message']
        matching = ['life', 'is']
        self.assertEqual(words_containing(words, 'i'), matching)

    def test_case_insensitive(self):
        words = ['My', 'life', 'is', 'my', 'message']
        matching = ['My', 'my', 'message']
        self.assertEqual(words_containing(words, 'm'), matching)


class TranslateTests(unittest.TestCase):

    """Tests for translate."""

    def test_cat(self):
        self.assertEqual(translate("gato"), "cat")

    def test_the_cat(self):
        self.assertEqual(translate("el gato"), "the cat")

    def test_cat_in_house(self):
        inputs = "el gato esta en la casa"
        outputs = "the cat is in the house"
        self.assertEqual(translate(inputs), outputs)


class GetFactorsTests(unittest.TestCase):

    """Tests for get_factors."""

    def test_2(self):
        self.assertEqual(get_factors(2), [1, 2])

    def test_6(self):
        self.assertEqual(get_factors(6), [1, 2, 3, 6])

    def test_100(self):
        self.assertEqual(get_factors(100), [1, 2, 4, 5, 10, 20, 25, 50, 100])


class IdentityTests(unittest.TestCase):

    """Tests for identity."""

    def test_2_by_2_matrix(self):
        expected = [[1, 0], [0, 1]]
        self.assertEqual(identity(2), expected)

    def test_3_by_3_matrix(self):
        expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(identity(3), expected)

    def test_4_by_4_matrix(self):
        expected = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.assertEqual(identity(4), expected)


class TriplesTests(unittest.TestCase):

    """Tests for triples."""

    def test_triples_1(self):
        expected = []
        self.assertEqual(triples(1), expected)

    def test_triples_6(self):
        expected = [(3, 4, 5)]
        self.assertEqual(triples(6), expected)

    def test_triples_25(self):
        expected = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17),
                    (9, 12, 15), (12, 16, 20)]
        self.assertEqual(triples(25), expected)


if __name__ == "__main__":
    from helpers import error_message
    error_message()
