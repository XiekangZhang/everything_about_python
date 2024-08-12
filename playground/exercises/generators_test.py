"""Test for generator exercises"""
import unittest

from generators import (
    all_together,
    sum_numbers,
    interleave,
    parse_ranges,
    is_prime,
    deep_add,
)


class AllTogetherTests(unittest.TestCase):

    """Tests for all_together."""

    def test_list_and_tuple(self):
        outputs = list(all_together([1, 2], (3, 4)))
        expected = [1, 2, 3, 4]
        self.assertEqual(outputs, expected)

    def test_with_strings(self):
        outputs = list(all_together([1, 2], (3, 4), "hello"))
        expected = [1, 2, 3, 4, 'h', 'e', 'l', 'l', 'o']
        self.assertEqual(outputs, expected)

    def test_empty_list(self):
        outputs = list(all_together([], (), '', [1, 2]))
        self.assertEqual(outputs, [1, 2])

    def test_iterator(self):
        outputs = all_together([1], [2])
        self.assertEqual(list(outputs), [1, 2])
        self.assertEqual(list(outputs), [])


class SumNumbersTests(unittest.TestCase):

    """Tests for sum_numbers."""

    def test_six_items(self):
        self.assertEqual(sum_numbers("1 2 3 4 5 6"), 21)

    def test_with_a_zero(self):
        self.assertEqual(sum_numbers("0 1 4 2 3 1"), 11)

    def test_empty_numbers(self):
        self.assertEqual(sum_numbers(""), 0)


class InterleaveTests(unittest.TestCase):

    """Tests for interleave."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_empty_lists(self):
        self.assertIterableEqual(interleave([], []), [])

    def test_single_item_each(self):
        self.assertIterableEqual(interleave([1], [2]), [1, 2])

    def test_two_items_each(self):
        self.assertIterableEqual(interleave([1, 2], [3, 4]), [1, 3, 2, 4])

    def test_four_items_each(self):
        in1 = [1, 2, 3, 4]
        in2 = [5, 6, 7, 8]
        out = [1, 5, 2, 6, 3, 7, 4, 8]
        self.assertIterableEqual(interleave(in1, in2), out)

    def test_none_value(self):
        in1 = [1, 2, 3, None]
        in2 = [4, 5, 6, 7]
        out = [1, 4, 2, 5, 3, 6, None, 7]
        self.assertIterableEqual(interleave(in1, in2), out)

    def test_non_sequences(self):
        in1 = [1, 2, 3, 4]
        in2 = (n**2 for n in in1)
        out = [1, 1, 2, 4, 3, 9, 4, 16]
        self.assertIterableEqual(interleave(in1, in2), out)

    def test_response_is_iterator(self):
        in1 = [1, 2, 3]
        in2 = [4, 5, 6]
        output = interleave(in1, in2)
        self.assertEqual(iter(output), iter(output))
        list(output)
        self.assertEqual(list(output), [])


class ParseRangesTests(unittest.TestCase):

    """Tests for parse_ranges."""

    def test_three_ranges(self):
        self.assertEqual(
            list(parse_ranges('1-2,4-4,8-10')),
            [1, 2, 4, 8, 9, 10],
        )

    def test_with_spaces(self):
        self.assertEqual(
            list(parse_ranges('0-0, 4-8, 20-21, 43-45')),
            [0, 4, 5, 6, 7, 8, 20, 21, 43, 44, 45],
        )


class PrimalityTests(unittest.TestCase):

    """Tests for is_prime."""

    def test_21(self):
        self.assertFalse(is_prime(21))

    def test_23(self):
        self.assertTrue(is_prime(23))


class DeepAddTests(unittest.TestCase):

    """Tests for deep_add."""

    def test_shallow(self):
        self.assertEqual(deep_add([1, 2, 3, 4]), 10)

    def test_deeply_nested_iterables(self):
        self.assertEqual(deep_add([(1, 2), [3, {4, 5}]]), 15)


if __name__ == "__main__":
    from helpers import error_message
    error_message()
