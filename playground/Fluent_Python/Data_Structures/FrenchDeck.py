import collections

# INFO: we use namedtuple to build classes of objects that are just bundles of attributes with no custom methods,
# INFO: like a database record.
Card = collections.namedtuple("Card", ["rank", "suit"])  # create a subclass of tuple with given first parameter


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    # INFO: enable defined collection to slice & iterable
    def __getitem__(self, position):
        return self._cards[position]


# INFO: Sort
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card1: Card):
    rank_value = FrenchDeck.ranks.index(card1.rank)
    return rank_value * len(suit_values) + suit_values[card1.suit]


if __name__ == "__main__":
    beer_card = Card("7", "diamonds")
    print(beer_card)
    deck = FrenchDeck()
    print(f"{len(deck)} + {deck[0]} + {deck[-1]} + {deck[12:15]}")
    for card in reversed(deck):
        print(card)

    print(Card("Q", "hearts") in deck)
    from random import choice

    print("------")
    print(choice(deck))

    print("******")
    for card in sorted(deck, key=spades_high):
        print(card)
