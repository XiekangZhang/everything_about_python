"""Advanced exercises"""
from collections import namedtuple
import csv

import random


def matrix_from_string():
    """Convert rows of numbers to list of lists."""


def format_arguments():
    """Return string representing given positional and keyword arguments."""


def get_movie_data(filename):
    """Return list of JSON-parsed objects, given a JSONL path."""


def flatten_dict():
    """Flatten given dict-of-dictionaries with a separator."""


def chunked(sequence, n):
    """Return n-length chunks of the given sequence."""


def parse_csv(file_obj):
    """Return namedtuple list representing data from given file object."""
    csv_reader = csv.reader(file_obj)
    Row = namedtuple('Row', next(csv_reader))
    return []


def get_cards():
    """Create a list of namedtuples representing a deck of playing cards."""
    Card = namedtuple('Card', 'rank suit')
    ranks = ['A'] + [] + ['J', 'Q', 'K']
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    return [Card('A', 'spades')]


def shuffle_cards(deck):
    """Shuffles a list in-place"""
    random.shuffle(deck)


def deal_cards(deck, count=5):
    """Remove the given number of cards from the deck and returns them"""
