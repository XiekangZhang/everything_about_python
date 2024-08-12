from collections import namedtuple
from datetime import date
import json
from textwrap import dedent
import unittest

from helpers import make_file


from advanced import (
    matrix_from_string,
    format_arguments,
    get_movie_data,
    flatten_dict,
    chunked,
    get_cards,
    shuffle_cards,
    deal_cards,
    parse_csv,
)


class MatrixFromStringTests(unittest.TestCase):

    """Tests for matrix_from_string."""

    def test_two_by_two_matrix(self):
        matrix = matrix_from_string("1 2\n10 20")
        self.assertEqual([[1, 2], [10, 20]], matrix)

    def test_three_by_two_matrix(self):
        matrix = matrix_from_string("9 8 7\n19 18 17")
        self.assertEqual([[9, 8, 7], [19, 18, 17]], matrix)


class FormatArgumentsTests(unittest.TestCase):

    """Tests for format_arguments."""

    def test_one_positional_argument(self):
        self.assertEqual(format_arguments(1), "1")
        self.assertEqual(format_arguments(None), "None")
        self.assertEqual(format_arguments("hello"), "'hello'")

    def test_one_keyword_argument(self):
        self.assertEqual(format_arguments(n=1), "n=1")
        self.assertEqual(format_arguments(object=None), "object=None")
        self.assertEqual(format_arguments(name="Trey"), "name='Trey'")

    def test_multiple_positional_arguments(self):
        self.assertEqual(format_arguments(1, 2), "1, 2")
        self.assertEqual(
            format_arguments(" ", ["apple", "banana"]),
            "' ', ['apple', 'banana']",
        )

    def test_multiple_keyword_arguments(self):
        self.assertEqual(
            format_arguments(file="log", mode="wt"),
            "file='log', mode='wt'",
        )

    def test_mixed_arguments(self):
        self.assertEqual(
            format_arguments(["apple", "banana"], start=1),
            "['apple', 'banana'], start=1",
        )
        self.assertEqual(
            format_arguments("log", "wt", encoding="utf-8", newline=""),
            "'log', 'wt', encoding='utf-8', newline=''",
        )


class GetMovieDataTests(unittest.TestCase):

    """Tests for get_movie_data."""

    maxDiff = 3000

    def make_file(self, *movies):
        return make_file(
            "".join(json.dumps(movie, default=str) + "\n" for movie in movies)
        )

    def test_empty_file(self):
        with self.make_file() as movie_file:
            self.assertEqual(get_movie_data(movie_file), [])

    def test_one_movie(self):
        with self.make_file(MOVIES[0]) as movie_file:
            self.assertEqual(
                get_movie_data(movie_file),
                [MOVIES[0]],
            )

    def test_two_movies(self):
        with self.make_file(*MOVIES[:2]) as movie_file:
            self.assertEqual(
                get_movie_data(movie_file),
                MOVIES[:2],
            )

    def test_four_movies(self):
        with self.make_file(*MOVIES[:4]) as movie_file:
            self.assertEqual(
                get_movie_data(movie_file),
                MOVIES[:4],
            )


class FlattenDictTests(unittest.TestCase):

    """Tests for flatten_dict."""

    flavors = {
        'savory': {
            'green': ['edamame', 'seaweed', 'wasabi'],
            'brown': ['peanut', 'bacon'],
        },
        'sweet': {
            'green': ['durian'],
            'pink': ['watermelon', 'strawberry'],
            'purple': ['blueberry', 'taro'],
        },
        'bitter': {
            'green': ['kale', 'arugula'],
        },
    }
    flattened_flavors = {
        'savory_green': ['edamame', 'seaweed', 'wasabi'],
        'savory_brown': ['peanut', 'bacon'],
        'sweet_green': ['durian'],
        'sweet_pink': ['watermelon', 'strawberry'],
        'sweet_purple': ['blueberry', 'taro'],
        'bitter_green': ['kale', 'arugula'],
    }

    def test_flattening_empty_dict(self):
        self.assertEqual(flatten_dict({}), {})

    def test_flattening_dict_of_dicts(self):
        flavors = self.flavors.copy()
        self.assertEqual(flatten_dict(flavors), self.flattened_flavors)

    def test_original_dict_not_changed(self):
        flavors = self.flavors.copy()
        flatten_dict(flavors)
        self.assertEqual(flavors, self.flavors)

    def test_flattening_does_not_copy(self):
        original = {'a': {'b': object()}}
        flattened = flatten_dict(original)
        self.assertIs(flattened['a_b'], original['a']['b'])

    def test_flatten_with_non_strings(self):
        self.assertEqual(
            flatten_dict({'a': {1: True, 2: False}, 'b': {3: True, 4: False}}),
            {'a_1': True, 'a_2': False, 'b_3': True, 'b_4': False},
        )

    def test_empty_nested_dictionaries_ignored(self):
        self.assertEqual(
            flatten_dict({'a': {'z': 8}, 'b': {}}),
            {'a_z': 8},
        )

    def test_specifying_separator(self):
        self.assertEqual(
            flatten_dict({'a': {'b': 'x'}, 'd': {'e': 'y'}}, sep='.'),
            {'a.b': 'x', 'd.e': 'y'},
        )
        self.assertEqual(flatten_dict({}, sep='.'), {})


class ChunkedTests(unittest.TestCase):

    """Tests for chunked."""

    def assertNestedIterableEqual(self, iterable1, iterable2):
        self.assertEqual(
            [tuple(x) for x in iterable1],
            [tuple(x) for x in iterable2],
        )

    def test_chunking_a_list(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2),
            [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]],
        )

    def test_empty_list(self):
        self.assertNestedIterableEqual(
            chunked([], 3),
            [],
        )

    def test_last_chunk_is_smaller(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4),
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]],
        )

    def test_chunking_other_sequences(self):
        self.assertNestedIterableEqual(
            chunked(('a', 'b', 'c', 'd', 'e', 'f'), 3),
            ['abc', 'def'],
        )
        self.assertNestedIterableEqual(
            chunked('abcdef', 3),
            ['abc', 'def'],
        )
        self.assertNestedIterableEqual(
            chunked(range(100), 50),
            [range(50), range(50, 100)],
        )

    def test_chunk_size_greater_than_length(self):
        self.assertNestedIterableEqual(
            chunked([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 15),
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
        )


class GetCardsTest(unittest.TestCase):

    """Tests for get_cards."""

    def test_get_cards(self):
        Card = namedtuple('Card', 'rank suit')

        deck = [Card(rank='A', suit='spades'), Card(rank='2', suit='spades'),
                Card(rank='3', suit='spades'), Card(rank='4', suit='spades'),
                Card(rank='5', suit='spades'), Card(rank='6', suit='spades'),
                Card(rank='7', suit='spades'), Card(rank='8', suit='spades'),
                Card(rank='9', suit='spades'), Card(rank='10', suit='spades'),
                Card(rank='J', suit='spades'), Card(rank='Q', suit='spades'),
                Card(rank='K', suit='spades'), Card(rank='A', suit='hearts'),
                Card(rank='2', suit='hearts'), Card(rank='3', suit='hearts'),
                Card(rank='4', suit='hearts'), Card(rank='5', suit='hearts'),
                Card(rank='6', suit='hearts'), Card(rank='7', suit='hearts'),
                Card(rank='8', suit='hearts'), Card(rank='9', suit='hearts'),
                Card(rank='10', suit='hearts'), Card(rank='J', suit='hearts'),
                Card(rank='Q', suit='hearts'), Card(rank='K', suit='hearts'),
                Card(rank='A', suit='diamonds'), Card(rank='2', suit='diamonds'),
                Card(rank='3', suit='diamonds'), Card(rank='4', suit='diamonds'),
                Card(rank='5', suit='diamonds'), Card(rank='6', suit='diamonds'),
                Card(rank='7', suit='diamonds'), Card(rank='8', suit='diamonds'),
                Card(rank='9', suit='diamonds'), Card(rank='10', suit='diamonds'),
                Card(rank='J', suit='diamonds'), Card(rank='Q', suit='diamonds'),
                Card(rank='K', suit='diamonds'), Card(rank='A', suit='clubs'),
                Card(rank='2', suit='clubs'), Card(rank='3', suit='clubs'),
                Card(rank='4', suit='clubs'), Card(rank='5', suit='clubs'),
                Card(rank='6', suit='clubs'), Card(rank='7', suit='clubs'),
                Card(rank='8', suit='clubs'), Card(rank='9', suit='clubs'),
                Card(rank='10', suit='clubs'), Card(rank='J', suit='clubs'),
                Card(rank='Q', suit='clubs'), Card(rank='K', suit='clubs')]

        self.assertEqual(get_cards(), deck)


class ShuffleTest(unittest.TestCase):

    """Test for shuffle_cards."""

    def test_shuffle(self):
        things = [1, 2, 3, 4, 5]
        original = list(things)
        shuffle_cards(things)
        self.assertNotEqual(original, things)
        self.assertEqual(set(original), set(things))


class DealCardsTest(unittest.TestCase):

    """Test for deal_cards."""

    def test_deal_cards(self):
        Card = namedtuple('Card', 'rank suit')
        deck = [Card(rank='A', suit='spades'), Card(rank='2', suit='spades'),
                Card(rank='3', suit='spades'), Card(rank='4', suit='spades'),
                Card(rank='5', suit='spades'), Card(rank='6', suit='spades'),
                Card(rank='7', suit='spades'), Card(rank='8', suit='spades'),
                Card(rank='9', suit='spades'), Card(rank='10', suit='spades'),
                Card(rank='J', suit='spades'), Card(rank='Q', suit='spades'),
                Card(rank='K', suit='spades'), Card(rank='A', suit='hearts'),
                Card(rank='2', suit='hearts'), Card(rank='3', suit='hearts'),
                Card(rank='4', suit='hearts'), Card(rank='5', suit='hearts'),
                Card(rank='6', suit='hearts'), Card(rank='7', suit='hearts'),
                Card(rank='8', suit='hearts'), Card(rank='9', suit='hearts'),
                Card(rank='10', suit='hearts'), Card(rank='J', suit='hearts'),
                Card(rank='Q', suit='hearts'), Card(rank='K', suit='hearts'),
                Card(rank='A', suit='diamonds'), Card(rank='2', suit='diamonds'),
                Card(rank='3', suit='diamonds'), Card(rank='4', suit='diamonds'),
                Card(rank='5', suit='diamonds'), Card(rank='6', suit='diamonds'),
                Card(rank='7', suit='diamonds'), Card(rank='8', suit='diamonds'),
                Card(rank='9', suit='diamonds'), Card(rank='10', suit='diamonds'),
                Card(rank='J', suit='diamonds'), Card(rank='Q', suit='diamonds'),
                Card(rank='K', suit='diamonds'), Card(rank='A', suit='clubs'),
                Card(rank='2', suit='clubs'), Card(rank='3', suit='clubs'),
                Card(rank='4', suit='clubs'), Card(rank='5', suit='clubs'),
                Card(rank='6', suit='clubs'), Card(rank='7', suit='clubs'),
                Card(rank='8', suit='clubs'), Card(rank='9', suit='clubs'),
                Card(rank='10', suit='clubs'), Card(rank='J', suit='clubs'),
                Card(rank='Q', suit='clubs'), Card(rank='K', suit='clubs')]
        hand = [Card(rank='K', suit='clubs'), Card(rank='Q', suit='clubs'),
                Card(rank='J', suit='clubs'), Card(rank='10', suit='clubs'),
                Card(rank='9', suit='clubs')]
        self.assertEqual(deal_cards(deck), hand)


class ParseCSVTests(unittest.TestCase):

    """Tests for parse_csv."""

    def test_sample_file(self):
        csv_data = dedent("""
            col1,col2,more_data
            1,2,3
            "a,b","c\td","e f"
        """).lstrip()
        with make_file(csv_data) as filename:
            with open(filename) as csv_file:
                csv_rows = list(parse_csv(csv_file))
        self.assertEqual(len(csv_rows), 2)
        row1, row2 = csv_rows
        self.assertEqual(row1.col1, '1')
        self.assertEqual(row1.col2, '2')
        self.assertEqual(row1.more_data, '3')
        self.assertEqual(row1, ('1', '2', '3'))
        self.assertEqual(row2, ('a,b', 'c\td', 'e f'))

    def test_state_capitals(self):
        with open('us-state-capitals.csv') as capitals_file:
            csv_rows = list(parse_csv(capitals_file))
        self.assertEqual(len(csv_rows), 50)
        self.assertEqual(csv_rows[0].state, 'Alabama')
        self.assertEqual(csv_rows[0].capital, 'Montgomery')
        self.assertEqual(csv_rows[0], ('Alabama', 'Montgomery'))


MOVIES = [
    {
        "title": "My Neighbor Totoro",
        "release_date": date(1988, 4, 16),
        "runtime": 86,
        "genres": ["Fantasy", "Animation", "Family"],
        "collection": None,
        "cast": [
            {"character": "Satsuki (voice)", "name": "Noriko Hidaka"},
            {"character": "Totoro (voice)", "name": "Hitoshi Takagi"},
            {"character": "Mei (voice)", "name": "Chika Sakamoto"},
            {
                "character": "Tatsuo Kusakabe (voice)",
                "name": "Shigesato Itoi",
            },
            {
                "character": "Yasuko Kusakabe (voice)",
                "name": "Sumi Shimamoto",
            },
            {
                "character": "Kanta no obâsan (voz)",
                "name": "Tanie Kitabayashi",
            },
            {
                "character": "Kanta no otôsan (voice)",
                "name": "Masashi Hirose",
            },
            {
                "character": "Kanta no okâsan (voice)",
                "name": "Yûko Maruyama",
            },
            {
                "character": "Kusakari-Otoko (voice)",
                "name": "Shigeru Chiba",
            },
            {"character": "Kanta (voice)", "name": "Toshiyuki Amagasa"},
        ],
    },
    {
        "title": "Bicycle Thieves",
        "release_date": date(1948, 11, 24),
        "runtime": 89,
        "genres": ["Drama"],
        "collection": None,
        "cast": [
            {"name": "Lamberto Maggiorani", "character": "Antonio Ricci"},
            {"name": "Enzo Staiola", "character": "Bruno Ricci"},
            {"name": "Lianella Carell", "character": "Maria Ricci"},
            {"name": "Elena Altieri", "character": "The Charitable Lady"},
            {"name": "Gino Saltamerenda", "character": "Baiocco"},
            {"name": "Giulio Chiari", "character": "The Beggar"},
            {
                "name": "Vittorio Antonucci",
                "character": "Alfredo Catelli, the Thief",
            },
            {
                "name": "Michele Sakara",
                "character": "Secretary of the Charity Organization",
            },
            {"name": "Fausto Guerzoni", "character": "Amateur Actor"},
            {"name": "Carlo Jachino", "character": "A Beggar"},
            {"name": "Emma Druetti", "character": ""},
            {
                "name": "Giulio Battiferri",
                "character": "Citizen Who Protects the Real Thief (uncredited)",
            },
            {
                "name": "Sergio Leone",
                "character": "A Seminary Student (uncredited)",
            },
            {
                "name": "Mario Meniconi",
                "character": "Meniconi, the Street Sweeper (uncredited)",
            },
            {
                "name": "Checco Rissone",
                "character": "Guard in Piazza Vittorio (uncredited)",
            },
            {
                "name": "Peppino Spadaro",
                "character": "Police Officer (uncredited)",
            },
            {"name": "Nando Bruno", "character": "(uncredited)"},
            {"name": "Eolo Capritti", "character": "(uncredited)"},
            {"name": "Memmo Carotenuto", "character": "(uncredited)"},
            {"name": "Umberto Spadaro", "character": "(uncredited)"},
        ],
    },
    {
        "title": "The Intouchables",
        "release_date": date(2011, 11, 2),
        "runtime": 113,
        "genres": ["Drama", "Comedy"],
        "collection": None,
        "cast": [
            {"name": "François Cluzet", "character": "Philippe"},
            {"name": "Omar Sy", "character": "Driss"},
            {"name": "Audrey Fleurot", "character": "Magalie"},
            {"name": "Anne Le Ny", "character": "Yvonne"},
            {"name": "Clotilde Mollet", "character": "Marcelle"},
            {"name": "Alba Gaïa Bellugi", "character": "Elisa"},
            {"name": "Cyril Mendy", "character": "Adama"},
            {"name": "Christian Ameri", "character": "Albert"},
            {"name": "Marie-Laure Descoueaux", "character": "Chantal"},
            {"name": "Salimata Kamate", "character": "Fatou"},
            {"name": "Absa Diatou Toure", "character": "Mina"},
            {
                "name": "Dominique Daguier",
                "character": "Friend of Philippe",
            },
            {"name": "François Caron", "character": "Friend of Philippe"},
            {"name": "Thomas Solivérès", "character": "Bastien"},
            {"name": "Grégoire Oestermann", "character": "Antoine"},
            {"name": "Dorothée Brière", "character": "Eléonore"},
            {
                "name": "Joséphine de Meaux",
                "character": "Nathalie Lecomte",
            },
            {"name": "Émilie Caen", "character": "Gallery owner"},
            {"name": "Caroline Bourg", "character": "Frédérique"},
            {"name": "Sylvain Lazard", "character": "New auxiliary"},
            {
                "name": "Jean-François Cayrey",
                "character": "2nd candidate for the post of auxiliary",
            },
            {"name": "Ian Fenelon", "character": "Candidate"},
            {"name": "Renaud Barse", "character": "Candidate"},
            {"name": "François Bureloup", "character": "Candidate"},
            {"name": "Nicky Marbot", "character": "Policeman"},
            {"name": "Benjamin Baroche", "character": "Policeman"},
            {
                "name": "Jérôme Pauwels",
                "character": "First badly parked neighbor",
            },
            {
                "name": "Antoine Laurent",
                "character": "Second badly parked neighbor",
            },
            {"name": "Fabrice Mantegna", "character": "Opera singer"},
            {"name": "Hedi Bouchenafa", "character": "Garage owner"},
            {
                "name": "Michel Winogradoff",
                "character": 'Server of "Deux Magots"',
            },
            {"name": "Elliot Latil", "character": "Schoolboy"},
            {"name": "Yun-Ping He", "character": "Passerby"},
            {"name": "Kévin Wamo", "character": "Friend of Driss"},
            {
                "name": "Pierre-Laurent Barneron",
                "character": "Butler (uncredited)",
            },
            {
                "name": "Philippe Pozzo di Borgo",
                "character": "Himself (archive footage) (uncredited)",
            },
        ],
    },
    {
        "title": "Back to the Future",
        "release_date": date(1985, 7, 3),
        "runtime": 116,
        "genres": ["Adventure", "Comedy", "Science Fiction", "Family"],
        "collection": "Back to the Future Collection",
        "cast": [
            {"name": "Michael J. Fox", "character": "Marty McFly"},
            {"name": "Christopher Lloyd", "character": "Dr. Emmett Brown"},
            {"name": "Lea Thompson", "character": "Lorraine Baines"},
            {"name": "Crispin Glover", "character": "George McFly"},
            {"name": "Thomas F. Wilson", "character": "Biff Tannen"},
            {"name": "Claudia Wells", "character": "Jennifer Parker"},
            {"name": "Marc McClure", "character": "Dave McFly"},
            {"name": "Wendie Jo Sperber", "character": "Linda McFly"},
            {"name": "George DiCenzo", "character": "Sam Baines"},
            {"name": "Frances Lee McCain", "character": "Stella Baines"},
            {"name": "James Tolkan", "character": "Mr. Strickland"},
            {"name": "J.J. Cohen", "character": "Skinhead"},
            {"name": "Casey Siemaszko", "character": "3-D"},
            {"name": "Billy Zane", "character": "Match"},
            {"name": "Harry Waters, Jr.", "character": "Marvin Berry"},
            {"name": "Donald Fullilove", "character": "Goldie Wilson"},
            {"name": "Lisa Freeman", "character": "Babs"},
            {"name": "Cristen Kauffman", "character": "Betty"},
            {"name": "Elsa Raven", "character": "Clocktower Lady"},
            {"name": "Will Hare", "character": "Pa Peabody"},
            {"name": "Ivy Bethune", "character": "Ma Peabody"},
            {"name": "Jason Marin", "character": "Sherman Peabody"},
            {"name": "Katherine Britton", "character": "Daughter Peabody"},
            {"name": "Jason Hervey", "character": "Milton Baines"},
            {"name": "Maia Brewton", "character": "Sally Baines"},
            {"name": "Courtney Gains", "character": "Dixon"},
            {"name": "Richard L. Duran", "character": "Terrorist"},
            {"name": "Jeff O'Haco", "character": "Terrorist Van Driver"},
            {"name": "Johnny Green", "character": "Scooter Kid #1"},
            {"name": "Jamie Abbott", "character": "Scooter Kid #2"},
            {"name": "Norman Alden", "character": "Lou"},
            {"name": "Read Morgan", "character": "Cop"},
            {"name": "Sachi Parker", "character": "Bystander #1"},
            {"name": "Robert Krantz", "character": "Bystander #2"},
            {"name": "Gary Riley", "character": "Guy #1"},
            {"name": "Karen Petrasek", "character": "Girl #1"},
            {"name": "George Buck Flower", "character": "Bum"},
            {"name": "Tommy Thomas", "character": "Starlighter"},
            {
                "name": "Granville 'Danny' Young",
                "character": "Starlighter",
            },
            {"name": "David Harold Brown", "character": "Starlighter"},
            {"name": "Lloyd L. Tolbert", "character": "Starlighter"},
            {"name": "Paul Hanson", "character": "Pinhead"},
            {"name": "Lee Brownfield", "character": "Pinhead"},
            {"name": "Robert DeLapp", "character": "Pinhead"},
            {
                "name": "Huey Lewis",
                "character": "High School Band Audition Judge",
            },
        ],
    },
    {
        "title": "Green Book",
        "release_date": date(2018, 11, 16),
        "runtime": 130,
        "genres": ["Drama", "Comedy", "Music"],
        "collection": None,
        "cast": [
            {"name": "Viggo Mortensen", "character": "Tony Lip"},
            {"name": "Mahershala Ali", "character": "Dr. Don Shirley"},
            {"name": "Linda Cardellini", "character": "Dolores"},
            {"name": "Sebastian Maniscalco", "character": "Johnny Venere"},
            {"name": "Dimiter D. Marinov", "character": "Oleg"},
            {"name": "Mike Hatton", "character": "George"},
            {"name": "P. J. Byrne", "character": "Record Exec"},
            {"name": "Joe Cortese", "character": "Gio Loscudo"},
            {"name": "Maggie Nixon", "character": "Copa Coat Check Girl"},
            {"name": "Von Lewis", "character": "Bobby Rydell"},
            {"name": "Jon Sortland", "character": "Rydell Band Leader"},
            {"name": "Don Stark", "character": "Jules Podell"},
            {"name": "Anthony Mangano", "character": "Copa Bouncer Danny"},
            {"name": "Paul Sloan", "character": "Copa Maitre D' Carmine"},
            {"name": "Quinn Duffy", "character": "Mikey Cerrone"},
            {"name": "Seth Hurwitz", "character": "Johnny Randazzo"},
            {"name": "Hudson Galloway", "character": "Nick Vallelonga"},
            {"name": "Gavin Foley", "character": "Frankie Vallelonga"},
            {
                "name": "Rodolfo Vallelonga",
                "character": "Grandpa Nicola Vallelonga",
            },
            {
                "name": "Louis Venere",
                "character": "Grandpa Anthony Venere",
            },
            {"name": "Frank Vallelonga", "character": "Rudy Vallelonga"},
            {"name": "Don DiPetta", "character": "Louie Venere"},
            {"name": "Jenna Laurenzo", "character": "Fran Venere"},
            {"name": "Suehyla El-Attar", "character": "Lynn Venere"},
            {
                "name": "Kenneth Israel",
                "character": "Bronx Floor Repairman #1",
            },
            {
                "name": "Derrick Spears",
                "character": "Bronx Floor Repairman #2",
            },
            {"name": "Johnny Williams", "character": "Fat Paulie"},
            {"name": "Randal Gonzalez", "character": "Gorman"},
            {"name": "Iqbal Theba", "character": "Amit"},
            {
                "name": "Sharon Landry",
                "character": "Carnegie Hall Manager",
            },
            {"name": "Nick Vallelonga", "character": "Augie"},
            {"name": "David An", "character": "Bobby"},
            {
                "name": "Mike Cerrone",
                "character": "Joe and Joe's Customer",
            },
            {"name": "Peter Gabb", "character": "Charlie the Pawn Guy"},
            {"name": "Gertrud Sigle", "character": "Marie"},
            {"name": "Geraldine Singer", "character": "Pittsburgh MC"},
            {"name": "Ron Flagge", "character": "Pittsburgh Chauffeur"},
            {
                "name": "Martin Bats Bradford",
                "character": "Pittsburgh Busboy",
            },
            {"name": "Ted Huckabee", "character": "Indiana Stage Manager"},
            {
                "name": "Gralen Bryant Banks",
                "character": "Horseshoe Man #1",
            },
            {"name": "Sam Malone", "character": "Horseshoe Man #2"},
            {"name": "Floyd Miles", "character": "Floyd"},
            {"name": "David Kallaway", "character": "Redneck #1"},
            {"name": "James W. Evermore", "character": "Redneck #2"},
            {"name": "Harrison Stone", "character": "Redneck #3"},
            {"name": "Ricky Muse", "character": "Barkeep"},
            {"name": "Tom Virtue", "character": "Morgan Anderson"},
            {
                "name": "Christina Simpkins",
                "character": "Margaret Anderson",
            },
            {
                "name": "Kermit Burns III",
                "character": "Pimento Cheese Waiter",
            },
            {"name": "Lindsay Brice", "character": "Frances Selden"},
            {"name": "Shane Partlow", "character": "Tailor"},
            {"name": "Daniel Greene", "character": "Macon Cop #1"},
            {"name": "Brian Distance", "character": "Macon Cop #2"},
            {"name": "Craig DiFrancia", "character": "Dominic"},
            {"name": "Dennis W. Hall", "character": "Mags"},
            {"name": "Leslie Castay", "character": "Well-Dressed Woman"},
            {"name": "David Simpson", "character": "Louisiana Host"},
            {"name": "Jim Klock", "character": "Patrolman #1"},
            {"name": "Billy Breed", "character": "Patrolman #2"},
            {"name": "Dane Rhodes", "character": "Police Chief"},
            {"name": "Brian Stepanek", "character": "Graham Kindell"},
            {
                "name": "Jon Michael Davis",
                "character": "Birmingham Hotel Maitre D'",
            },
            {
                "name": "Montrel Miller",
                "character": "Birmingham Hotel Waiter",
            },
            {
                "name": "Ninja N. Devoe",
                "character": "Orange Bird Bartender",
            },
            {
                "name": "Brian Hayes Currie",
                "character": "Maryland State Trooper",
            },
        ],
    },
    {
        "title": "The Matrix",
        "release_date": date(1999, 3, 30),
        "runtime": 136,
        "genres": ["Action", "Science Fiction"],
        "collection": "The Matrix Collection",
        "cast": [
            {
                "name": "Keanu Reeves",
                "character": "Thomas A. Anderson / Neo",
            },
            {"name": "Laurence Fishburne", "character": "Morpheus"},
            {"name": "Carrie-Anne Moss", "character": "Trinity"},
            {"name": "Hugo Weaving", "character": "Agent Smith"},
            {"name": "Joe Pantoliano", "character": "Cypher"},
            {"name": "Gloria Foster", "character": "Oracle"},
            {"name": "Marcus Chong", "character": "Tank"},
            {"name": "Paul Goddard", "character": "Agent Brown"},
            {"name": "Robert Taylor", "character": "Agent Jones"},
            {"name": "Julian Arahanga", "character": "Apoc"},
            {"name": "Belinda McClory", "character": "Switch"},
            {"name": "Anthony Ray Parker", "character": "Dozer"},
            {"name": "Matt Doran", "character": "Mouse"},
            {"name": "Ada Nicodemou", "character": "DuJour"},
            {"name": "David Aston", "character": "Rhineheart"},
            {"name": "Marc Aden Gray", "character": "Choi"},
            {"name": "Deni Gordon", "character": "Priestess"},
            {"name": "Rowan Witt", "character": "Spoon Boy"},
            {"name": "Eleanor Witt", "character": "Potential"},
            {"name": "Janaya Pender", "character": "Potential"},
            {"name": "Adryn White", "character": "Potential"},
            {"name": "Natalie Tjen", "character": "Potential"},
            {"name": "Bill Young", "character": "Lieutenant"},
            {"name": "David O'Connor", "character": "FedEx Man"},
            {"name": "Jeremy Ball", "character": "Businessman"},
            {"name": "Fiona Johnson", "character": "Woman in Red"},
            {"name": "Harry Lawrence", "character": "Old Man"},
            {"name": "Steve Dodd", "character": "Blind Man"},
            {"name": "Luke Quinton", "character": "Security Guard"},
            {"name": "Lawrence Woodward", "character": "Guard"},
            {
                "name": "Michael Butcher",
                "character": "Cop Who Captures Neo",
            },
            {"name": "Bernard Ledger", "character": "Big Cop"},
            {"name": "Chris Pattinson", "character": "Cop"},
            {"name": "Robert Simper", "character": "Cop"},
            {"name": "Nigel Harbach", "character": "Parking Cop"},
            {"name": "Rana Morrison", "character": "Shaylea"},
            {"name": "Tamara Brown", "character": "Potential"},
        ],
    },
    {
        "title": "Spirited Away",
        "release_date": date(2001, 7, 20),
        "runtime": 125,
        "genres": ["Animation", "Family", "Fantasy"],
        "collection": None,
        "cast": [
            {
                "name": "Rumi Hiiragi",
                "character": "Chihiro Ogino / Sen (voice)",
            },
            {"name": "Miyu Irino", "character": "Haku (voice)"},
            {"name": "Mari Natsuki", "character": "Yubaba / Zeniba (voice)"},
            {"name": "Takashi Naitō", "character": "Akio Ogino (voice)"},
            {"name": "Yasuko Sawaguchi", "character": "Yûko Ogino (voice)"},
            {"name": "Tatsuya Gashūin", "character": "Aogaeru (voice)"},
            {"name": "Ryunosuke Kamiki", "character": "Bô (voice)"},
            {"name": "Yumi Tamai", "character": "Rin (voice)"},
            {"name": "Yo Oizumi", "character": "Bandai-gaeru (voice)"},
            {"name": "Koba Hayashi", "character": "Kawa no Kami (voice)"},
            {"name": "Tsunehiko Kamijô", "character": "Chichiyaku (voice)"},
            {"name": "Takehiko Ono", "character": "Aniyaku (voice)"},
            {"name": "Bunta Sugawara", "character": "Kamaji (voice)"},
            {"name": "Shigeru Wakita", "character": "(voice)"},
            {"name": "Shiro Saito", "character": "(voice)"},
            {"name": "Michiko Yamamoto", "character": "(voice)"},
            {"name": "Keiko Tsukamoto", "character": "(voice)"},
            {"name": "Akio Nakamura", "character": "Kaonashi (voice)"},
            {"name": "Shinji Tokumaru", "character": "(voice)"},
            {"name": "Kaori Yamagata", "character": "(voice)"},
            {"name": "Yayoi Kazuki", "character": "(voice)"},
            {"name": "Masahiro Asano", "character": "(voice)"},
            {"name": "Kazutaka Hayashida", "character": "(voice)"},
            {"name": "Ikuko Yamamoto", "character": "(voice)"},
            {"name": "Mina Meguro", "character": "(voice)"},
            {"name": "Tetsurô Ishibashi", "character": "(voice)"},
            {"name": "Katsutomo Shîbara", "character": "(voice)"},
            {"name": "Shinobu Katabuchi", "character": "(voice)"},
            {"name": "Noriko Kitou", "character": "(voice)"},
            {"name": "Naoto Kaji", "character": "(voice)"},
            {"name": "Yoshitaka Sukegawa", "character": "(voice)"},
            {"name": "Aki Tachikawa", "character": "(voice)"},
            {"name": "Noriko Yamaya", "character": "(voice)"},
            {"name": "Katsuhisa Matsuo", "character": "(voice)"},
            {"name": "Masayuki Kizu", "character": "(voice)"},
            {"name": "Yôko Ôno", "character": "(voice)"},
            {"name": "Sachie Azuma", "character": "(voice)"},
            {"name": "Ken Yasuda", "character": "Oshirasama (voice)"},
            {"name": "Shigeyuki Totsugi", "character": "(voice)"},
            {"name": "Mayumi Sako", "character": "(voice)"},
            {"name": "Sonoko Soeda", "character": "(voice)"},
            {"name": "Akiko Tomihira", "character": "(voice)"},
            {"name": "Minako Masuda", "character": "(voice)"},
            {"name": "Orika Ono", "character": "(voice)"},
            {"name": "Rina Yamada", "character": "(voice)"},
            {"name": "Miwa Takachi", "character": "(voice)"},
            {"name": "Hiromi Takeuchi", "character": "(voice)"},
            {"name": "Makiko Oku", "character": "(voice)"},
        ],
    },
    {
        "title": "Once Upon a Time in America",
        "release_date": date(1984, 5, 23),
        "runtime": 229,
        "genres": ["Drama", "Crime"],
        "collection": None,
        "cast": [
            {
                "name": "Robert De Niro",
                "character": "David 'Noodles' Aaronson",
            },
            {"name": "James Woods", "character": "Maximilian 'Max' Bercovicz"},
            {"name": "Elizabeth McGovern", "character": "Deborah Gelly"},
            {"name": "Joe Pesci", "character": "Frankie Monaldi"},
            {"name": "Tuesday Weld", "character": "Carol"},
            {"name": "Burt Young", "character": "Joe"},
            {"name": "Treat Williams", "character": "James Conway O'Donnell"},
            {
                "name": "Danny Aiello",
                "character": "Police Chief Vincent Aiello",
            },
            {"name": "Richard Bright", "character": "Chicken Joe"},
            {"name": "James Hayden", "character": "Patrick 'Patsy' Goldberg"},
            {
                "name": "William Forsythe",
                "character": "Philip 'Cockeye' Stein",
            },
            {"name": "Darlanne Fluegel", "character": "Eve"},
            {"name": "Larry Rapp", "character": "'Fat' Moe Gelly"},
            {
                "name": "Olga Karlatos",
                "character": "Woman in the Puppet Theatre",
            },
            {"name": "Frank Gio", "character": "Beefy"},
            {"name": "Jennifer Connelly", "character": "Young Deborah"},
            {"name": "Scott Schutzman Tiler", "character": "Young Noodles"},
            {"name": "Rusty Jacobs", "character": "Young Max / David Bailey"},
            {"name": "Brian Bloom", "character": "Young Patsy"},
            {"name": "Mike Monetti", "character": "Young 'Fat' Moe Gelly"},
            {"name": "Adrian Curran", "character": "Young Cockeye"},
            {"name": "Julie Cohen", "character": "Young Peggy"},
            {"name": "Noah Moazezi", "character": "Dominic"},
            {"name": "James Russo", "character": "Bugsy"},
            {"name": "Clem Caserta", "character": "Al Capuano"},
            {"name": "Frank Sisto", "character": "Fred Capuano"},
            {"name": "Jerry Strivelli", "character": "Johnny Capuano"},
            {"name": "Mike Gendel", "character": "Irving Gold"},
            {"name": "Sandra Solberg", "character": "Friend of Young Deborah"},
            {"name": "Margherita Pace", "character": "Young Deborah (Double)"},
            {
                "name": "Louise Fletcher",
                "character": "The Cemetery Directress (Extended Cut)",
            },
            {"name": "Paul Herman", "character": "Monkey"},
            {"name": "Bruno Iannone", "character": "Thug"},
            {
                "name": "Bruno Bilotta",
                "character": "Chinese Theater Spectator (uncredited)",
            },
            {"name": "Ray Dittrich", "character": "Trigger"},
            {"name": "Richard Foronjy", "character": "Officer Whitey"},
            {"name": "Mario Brega", "character": "Mandy"},
            {"name": "Angelo Florio", "character": "Willie the Ape"},
            {"name": "Marcia Jean Kurtz", "character": "Max's Mother"},
            {
                "name": "Salvatore Billa",
                "character": "One of Beefy's Thugs (uncredited)",
            },
            {"name": "Gerard Murphy", "character": "Crowning"},
            {"name": "Scott Coffey", "character": "Bugsy's Gang (uncredited)"},
            {"name": "Dutch Miller", "character": "Van Linden"},
            {"name": "Robert Harper", "character": "Sharkey"},
            {"name": "Amy Ryder", "character": "Peggy"},
            {"name": "Karen Shallo", "character": "Mrs. Aiello"},
            {"name": "Frankie Caserta", "character": "Bugsy's Gang"},
            {"name": "Joey Marzella", "character": "Bugsy's Gang"},
            {"name": "Marvin Scott", "character": "Interviewer"},
            {"name": "Ann Neville", "character": "Girl in Coffin"},
            {"name": "Joey Faye", "character": "Adorable Old Man"},
            {"name": "Linda Ipanema", "character": "Nurse Thompson"},
            {"name": "Tandy Cronyn", "character": "Reporter 1"},
            {"name": "Richard Zobel", "character": "Reporter 2"},
            {"name": "Baxter Harris", "character": "Reporter 3"},
            {"name": "Arnon Milchan", "character": "Chauffeur"},
            {"name": "Marty Licata", "character": "Cemetery Caretaker"},
            {"name": "Estelle Harris", "character": "Peggy's Mother"},
            {"name": "Gerritt Debeer", "character": "Drunk"},
            {"name": "Alexander Godfrey", "character": "Newstand Man"},
            {"name": "Cliff Cudney", "character": "Mounted Policeman"},
            {"name": "Paul Farentino", "character": "2nd Mounted Policeman"},
            {"name": "Bruce Bahrenburg", "character": "Sgt. P. Halloran"},
            {"name": "Mort Freeman", "character": "Street Singer"},
            {"name": "Jay Zeely", "character": "Foreman"},
            {"name": "Massimo Liti", "character": "Young Macrò"},
            {
                "name": "Greg Anthony",
                "character": "Bar Room Patron (uncredited)",
            },
            {"name": "Matteo Cafiso", "character": "Boy in Park (uncredited)"},
            {
                "name": "Nelson Camp",
                "character": "Newspaper Salesman (uncredited)",
            },
            {
                "name": "Nunzio Giuliani",
                "character": "Speakeasy Drum Player (uncredited)",
            },
            {
                "name": "Dario Iori",
                "character": "Speakeasy Banjo Player (uncredited)",
            },
            {
                "name": "Ole Jorgensen",
                "character": "Speakeasy Percussionist (uncredited)",
            },
            {
                "name": "Francesca Leone",
                "character": "David Bailey's Girlfriend (uncredited)",
            },
            {
                "name": "Chuck Low",
                "character": "Deborah Gelly's Father (uncredited)",
            },
            {"name": "Ron Nummi", "character": "Waiter (uncredited)"},
            {
                "name": "Ryan Paris",
                "character": "Speakeasy Patron (uncredited)",
            },
            {
                "name": "Nicola Roberto",
                "character": "Speakeasy Trumpet Player (uncredited)",
            },
            {
                "name": "Gianni Sanjust",
                "character": "Speakeasy Clarinet Player (uncredited)",
            },
            {
                "name": "Alex Serra",
                "character": "Speakeasy Vocalist (uncredited)",
            },
            {"name": "Susan Spafford", "character": "Nurse (uncredited)"},
            {"name": "Mark Frazer", "character": "Pimp (uncredited)"},
        ],
    },
    {
        "title": "City of God",
        "release_date": date(2002, 2, 5),
        "runtime": 130,
        "genres": ["Drama", "Crime"],
        "collection": None,
        "cast": [
            {"name": "Alexandre Rodrigues", "character": "Buscapé"},
            {"name": "Leandro Firmino", "character": "Zé Pequeno"},
            {"name": "Phellipe Haagensen", "character": "Bené"},
            {"name": "Douglas Silva", "character": "Dadinho"},
            {"name": "Jonathan Haagensen", "character": "Cabeleira"},
            {"name": "Matheus Nachtergaele", "character": "Sandro Cenoura"},
            {"name": "Seu Jorge", "character": "Mané Galinha"},
            {"name": "Jefechander Suplino", "character": "Alicate"},
            {"name": "Alice Braga", "character": "Angélica"},
            {"name": "Roberta Rodrigues", "character": "Berenice"},
            {"name": "Luis Otávio", "character": "Buscapé Criança"},
            {"name": "Darlan Cunha", "character": "Filé-com-Fritas"},
            {"name": "Thiago Martins", "character": "Lampião"},
            {"name": "Gero Camilo", "character": "Paraíba - Shorty"},
            {"name": "Daniel Zettel", "character": "Thiago - Tiago"},
            {"name": "Charles Paraventi", "character": "Tio Sam - Uncle Sam"},
            {
                "name": "Danielle Ornelas",
                "character": "Vizinha do Paraíba - Shorty's Neighbor",
            },
            {"name": "Micael Borges", "character": "Caixa Baixa - Runts"},
            {
                "name": "Lúcio Andrey",
                "character": "Bando Zé Pequeno - Li'l Zé's Gang",
            },
            {
                "name": "Marcello Melo Jr.",
                "character": "Bando Zé Pequeno - Li'l Zé's Gang",
            },
            {"name": "Babu Santana", "character": "Grande"},
            {"name": "Mary Sheila", "character": "Mulher do Neguinho"},
            {"name": "Paulo Lins", "character": "Pastor da Igreja"},
            {"name": "Olivia Araújo", "character": "Recepcionista do Motel"},
            {"name": "Graziella Moretto", "character": "Marina Cintra"},
            {
                "name": "Tulé Peak",
                "character": "Newspaper Employee (uncredited)",
            },
            {"name": "Kikito Junqueira", "character": "Otávio"},
            {"name": "Renato de Souza", "character": "Marreco"},
        ],
    },
    {
        "title": "Howl's Moving Castle",
        "release_date": date(2004, 11, 19),
        "runtime": 119,
        "genres": ["Fantasy", "Animation", "Adventure"],
        "collection": None,
        "cast": [
            {"name": "Chieko Baisho", "character": "Sophie (voice)"},
            {"name": "Takuya Kimura", "character": "Howl (voice)"},
            {
                "name": "Akihiro Miwa",
                "character": "Witch of the Waste (voice)",
            },
            {"name": "Tatsuya Gashūin", "character": "Calcifer (voice)"},
            {"name": "Ryunosuke Kamiki", "character": "Markl (voice)"},
            {"name": "Haruko Kato", "character": "Madame Suliman (voice)"},
            {"name": "Yayoi Kazuki", "character": "Lettie (voice)"},
            {"name": "Mayuno Yasokawa", "character": "Honey (voice)"},
            {
                "name": "Yo Oizumi",
                "character": "Prince Justin / Turnip Head (voice)",
            },
            {"name": "Rio Kanno", "character": "Madge (voice)"},
            {"name": "Akio Otsuka", "character": "King of Ingary (voice)"},
            {"name": "Daijirō Harada", "character": "Heen (voice)"},
        ],
    },
    {
        "title": "Jurassic Park",
        "release_date": date(1993, 6, 11),
        "runtime": 127,
        "genres": ["Adventure", "Science Fiction"],
        "collection": "Jurassic Park Collection",
        "cast": [
            {"name": "Sam Neill", "character": "Dr. Alan Grant"},
            {"name": "Laura Dern", "character": "Dr. Ellie Sattler"},
            {"name": "Jeff Goldblum", "character": "Dr. Ian Malcolm"},
            {"name": "Richard Attenborough", "character": "John Hammond"},
            {"name": "Bob Peck", "character": "Robert Muldoon"},
            {"name": "Martin Ferrero", "character": "Donald Gennaro"},
            {"name": "BD Wong", "character": "Dr. Henry Wu"},
            {"name": "Joseph Mazzello", "character": "Tim Murphy"},
            {"name": "Ariana Richards", "character": "Lex Murphy"},
            {"name": "Samuel L. Jackson", "character": "Arnold"},
            {"name": "Wayne Knight", "character": "Dennis Nedry"},
            {"name": "Gerald R. Molen", "character": "Gerry Harding"},
            {"name": "Miguel Sandoval", "character": "Juanito Rostagno"},
            {"name": "Cameron Thor", "character": "Lewis Dodgson"},
            {"name": "Christopher John Fields", "character": "Volunteer #1"},
            {"name": "Whit Hertford", "character": "Volunteer Boy"},
            {"name": "Dean Cundey", "character": "Mate"},
            {"name": "Jophery C. Brown", "character": "Worker in Raptor Pen"},
            {"name": "Tom Mishler", "character": "Helicopter Pilot"},
            {"name": "Greg Burson", "character": "'Mr. D.N.A.' Voice (voice)"},
            {"name": "Adrian Escober", "character": "Worker at Amber Mine"},
            {
                "name": "Richard Kiley",
                "character": "Jurassic Park Tour Voice (voice)",
            },
            {
                "name": "Brad M. Bucklin",
                "character": "Lab Technician (uncredited)",
            },
            {
                "name": "Laura Burnett",
                "character": "Archeologist (uncredited)",
            },
            {
                "name": "Michael Lantieri",
                "character": "Customer at San Jose restaurant (uncredited)",
            },
            {
                "name": "Gary Rodriguez",
                "character": "Miner - Dug Out Mosquito (uncredited)",
            },
            {
                "name": "Lata Ryan",
                "character": "Control Room technician (uncredited)",
            },
            {
                "name": "Brian Smrz",
                "character": "Driver of Grant, Sattler & Malcolm's Jeep (uncredited)",
            },
            {"name": "Rip Lee Walker", "character": "Raptor #1 (uncredited)"},
            {
                "name": "Robert 'Bobby Z' Zajonc",
                "character": "InGen Helicopter Pilot (uncredited)",
            },
        ],
    },
    {
        "title": "Eternal Sunshine of the Spotless Mind",
        "release_date": date(2004, 3, 19),
        "runtime": 108,
        "genres": ["Science Fiction", "Drama", "Romance"],
        "collection": None,
        "cast": [
            {"name": "Jim Carrey", "character": "Joel Barish"},
            {"name": "Kate Winslet", "character": "Clementine Kruczynski"},
            {"name": "Kirsten Dunst", "character": "Mary Svevo"},
            {"name": "Mark Ruffalo", "character": "Stan Fink"},
            {"name": "Elijah Wood", "character": "Patrick"},
            {"name": "Tom Wilkinson", "character": "Dr. Howard Mierzwiak"},
            {"name": "Jane Adams", "character": "Carrie Eakin"},
            {"name": "David Cross", "character": "Rob Eakin"},
            {"name": "Deirdre O'Connell", "character": "Hollis Mierzwiak"},
            {"name": "Thomas Jay Ryan", "character": "Frank"},
            {"name": "Ryan Whitney", "character": "Young Joel"},
            {"name": "Lola Daehler", "character": "Young Clementine"},
            {"name": "Debbon Ayer", "character": "Joel's Mother"},
            {"name": "Gerry Robert Byrne", "character": "Train Conducter"},
            {"name": "Brian Price", "character": "Young Bully"},
            {"name": "Josh Flitter", "character": "Young Bully"},
            {"name": "Paulie Litt", "character": "Young Bully"},
            {"name": "Amir Ali Said", "character": "Young Bully"},
            {"name": "Lauren Adler", "character": "Rollerblader"},
        ],
    },
    {
        "title": "Good Will Hunting",
        "release_date": date(1997, 12, 5),
        "runtime": 127,
        "genres": ["Drama"],
        "collection": None,
        "cast": [
            {"name": "Matt Damon", "character": "Will Hunting"},
            {"name": "Robin Williams", "character": "Sean Maguire"},
            {"name": "Ben Affleck", "character": "Chuckie Sullivan"},
            {"name": "Stellan Skarsg\u00e5rd", "character": "Gerald Lambeau"},
            {"name": "Minnie Driver", "character": "Skylar"},
            {"name": "Casey Affleck", "character": "Morgan O'Mally"},
            {"name": "Cole Hauser", "character": "Billy McBride"},
            {"name": "Vik Sahay", "character": "MIT Student"},
            {"name": "John Mighton", "character": "Tom"},
            {"name": "Rachel Majorowski", "character": "Krystyn"},
            {"name": "Colleen McCauley", "character": "Cathy"},
            {"name": "Matt Mercier", "character": "Barbershop Quartet #1"},
            {"name": "Ralph St. George", "character": "Barbershop Quartet #2"},
            {"name": "Rob Lynds", "character": "Barbershop Quartet #3"},
            {"name": "Dan Washington", "character": "Barbershop Quartet #4"},
            {"name": "Alison Folland", "character": "MIT Student"},
            {"name": "Derrick Bridgeman", "character": "MIT Student"},
            {"name": "Shannon Egleson", "character": "Girl on Street"},
            {"name": "Rob Lyons", "character": "Carmine Scarpaglia"},
            {"name": "Steven Kozlowski", "character": "Carmine Friend #1"},
            {"name": "Jennifer Deathe", "character": "Lydia"},
            {"name": "Scott William Winters", "character": "Clark"},
            {"name": "Philip Williams", "character": "Head Custodian"},
            {"name": "Patrick O'Donnell", "character": "Assistant Custodian"},
            {"name": "Kevin Rushton", "character": "Courtroom Guard"},
            {"name": "Jimmy Flynn", "character": "Judge Malone"},
            {"name": "Joe Cannon", "character": "Prosecutor"},
            {"name": "Ann Matacunas", "character": "Court Officer"},
            {"name": "George Plimpton", "character": "Psychologist"},
            {"name": "Francesco Clemente", "character": "Hypnotist"},
            {"name": "Jessica Morton", "character": "Bunker Hill Student"},
            {"name": "Barna Moricz", "character": "Bunker Hill Student"},
            {"name": "Libby Geller", "character": "Toy Store Cashier"},
            {"name": "Chas Lawther", "character": "MIT Professor"},
            {"name": "Richard Fitzpatrick", "character": "Timmy"},
            {"name": "Frank Nakashima", "character": "Executive #1"},
            {"name": "Christopher Britton", "character": "Executive #2"},
            {"name": "David Eisner", "character": "Executive #3"},
            {"name": "Bruce Hunter", "character": "NSA Agent"},
            {"name": "Robert Talvano", "character": "NSA Agent #2"},
            {"name": "James Allodi", "character": "Security Guard"},
            {
                "name": "Michael Arthur",
                "character": "Reunion Guest (uncredited)",
            },
            {"name": "Christian Harmony", "character": "Student (uncredited)"},
            {"name": "Riva Di Paola", "character": "MIT Student (uncredited)"},
            {"name": "Harmony Korine", "character": "Herv\u00e9 (uncredited)"},
            {"name": "Thomas Lundy", "character": "Waiter (uncredited)"},
            {
                "name": "Paul McGillicuddy",
                "character": "Race Track Fan (uncredited)",
            },
            {"name": "Daniel Olsen", "character": "MIT Student (uncredited)"},
        ],
    },
    {
        "title": "The Truman Show",
        "release_date": date(1998, 6, 4),
        "runtime": 103,
        "genres": ["Comedy", "Drama"],
        "collection": None,
        "cast": [
            {"name": "Jim Carrey", "character": "Truman Burbank"},
            {
                "name": "Laura Linney",
                "character": "Meryl Burbank / Hannah Gill",
            },
            {"name": "Noah Emmerich", "character": "Marlon / Louis Coltrane"},
            {
                "name": "Natascha McElhone",
                "character": "Lauren / Sylvia Garland",
            },
            {"name": "Ed Harris", "character": "Christof"},
            {
                "name": "Holland Taylor",
                "character": "Alanis Montclair / Angela Burbank",
            },
            {"name": "Paul Giamatti", "character": "Simeon"},
            {
                "name": "Brian Delate",
                "character": "Walter Moore / Kirk Burbank",
            },
            {"name": "Peter Krause", "character": "Laurence"},
            {"name": "Blair Slater", "character": "Young Truman"},
            {"name": "Heidi Schanz", "character": "Vivien"},
            {"name": "Una Damon", "character": "Chloe"},
            {"name": "Krista Lynn Landolfi", "character": "Bar Waitress"},
            {"name": "O-Lan Jones", "character": "Bar Waitress"},
            {"name": "Ron Taylor", "character": "Ron"},
            {"name": "Don Taylor", "character": "Don"},
            {"name": "Ted Raymond", "character": "Spencer"},
            {"name": "Harry Shearer", "character": "Mike Michaelson"},
            {"name": "Jeanette Miller", "character": "Senior Citizen"},
            {"name": "Philip Glass", "character": "Keyboard Artist"},
            {"name": "Joe Minjares", "character": "Bartender"},
            {"name": "Philip Baker Hall", "character": "Network Executive"},
            {"name": "John Pleshette", "character": "Network Executive"},
            {"name": "Terry Camilleri", "character": "Man in Bathtub"},
            {"name": "Joel McKinnon Miller", "character": "Garage Attendant"},
            {"name": "Judy Clayton", "character": "Travel Agent"},
            {"name": "Fritz Dominique", "character": "Truman's Neighbor"},
            {"name": "Angel Schmiedt", "character": "Truman's Neighbor"},
            {"name": "Nastassja Schmiedt", "character": "Truman's Neighbor"},
            {"name": "Muriel Moore", "character": "Teacher"},
            {"name": "Mal Jones", "character": "News Vendor"},
            {"name": "Judson Vaughn", "character": "Insurance Co-Worker"},
            {"name": "Earl Hilliard Jr.", "character": "Ferry Worker"},
            {
                "name": "David Andrew Nash",
                "character": "Bus Driver / Ferry Captain",
            },
            {"name": "Jim Towers", "character": "Bus Supervisor"},
            {"name": "Savannah Swafford", "character": "Little Girl in Bus"},
            {"name": "Antoni Corone", "character": "Security Guard"},
            {"name": "Mario Ernesto Sánchez", "character": "Security Guard"},
            {"name": "John Roselius", "character": "Man at Beach"},
            {"name": "Kade Coates", "character": "Truman (4 years)"},
            {"name": "Marcia DeBonis", "character": "Nurse"},
            {"name": "Sam Kitchin", "character": "Surgeon"},
            {"name": "Sebastian Youngblood", "character": "Orderly"},
            {"name": "Dave Corey", "character": "Hospital Security Guard"},
            {
                "name": "Mark Alan Gillott",
                "character": "Policeman at Power Plant",
            },
            {"name": "Jay Saiter", "character": "Policeman at Truman's House"},
            {"name": "Tony Todd", "character": "Policeman at Truman's House"},
            {"name": "Marco Rubeo", "character": "Man in Christmas Box"},
            {"name": "Daryl Davis", "character": "Couple at Picnic Table"},
            {"name": "Robert Davis", "character": "Couple at Picnic Table"},
            {"name": "R.J. Murdock", "character": "Production Assistant"},
            {"name": "Matthew McDonough", "character": "Man at Newsstand"},
            {"name": "Larry McDowell", "character": "Man at Newsstand"},
            {"name": "Joseph Lucus", "character": "Ticket Taker"},
            {"name": "Logan Kirksey", "character": "TV Host"},
            {"name": "Adam Tomei", "character": "Control Room Director"},
            {"name": "John Pramik", "character": "Keyboard Artist"},
            {"name": "Al Foster", "character": "Bar Patron"},
            {"name": "Zoaunne LeRoy", "character": "Bar Patron"},
            {"name": "Millie Slavin", "character": "Bar Patron"},
            {"name": "Dona Hardy", "character": "Senior Citizen"},
            {"name": "Tom Simmons", "character": "Garage Attendant"},
            {"name": "Susan Angelo", "character": "Mother"},
            {"name": "Carly Smiga", "character": "Daughter"},
            {"name": "Yuji Okumoto", "character": "Japanese Family"},
            {"name": "Kiyoko Yamaguchi", "character": "Japanese Family"},
            {"name": "Saemi Nakamura", "character": "Japanese Family"},
        ],
    },
    {
        "title": "Princess Mononoke",
        "release_date": date(1997, 7, 12),
        "runtime": 134,
        "genres": ["Adventure", "Fantasy", "Animation"],
        "collection": None,
        "cast": [
            {"name": "Y\u014dji Matsuda", "character": "Ashitaka (voice)"},
            {"name": "Yuriko Ishida", "character": "San (voice)"},
            {"name": "Y\u016bko Tanaka", "character": "Eboshi-gozen (voice)"},
            {"name": "Kaoru Kobayashi", "character": "Jiko-b\u00f4 (voice)"},
            {"name": "Masahiko Nishimura", "character": "Kouroku (voice)"},
            {"name": "Tsunehiko Kamij\u00f4", "character": "Gonza (voice)"},
            {"name": "Sumi Shimamoto", "character": "Toki (voice)"},
            {"name": "Tetsu Watanabe", "character": "Yama-inu (voice)"},
            {"name": "Mitsuru Sat\u00f4", "character": "Tatari-gami (voice)"},
            {"name": "Akira Nagoya", "character": "Usi-kai (voice)"},
            {"name": "Akihiro Miwa", "character": "Moro-no-kimi (voice)"},
            {"name": "Mitsuko Mori", "character": "Hii-sama (voice)"},
            {"name": "Hisaya Morishige", "character": "Okkoto-nusi (voice)"},
        ],
    },
    {
        "title": "Up",
        "release_date": date(2009, 5, 28),
        "runtime": 96,
        "genres": ["Animation", "Comedy", "Family", "Adventure"],
        "collection": None,
        "cast": [
            {"name": "Edward Asner", "character": "Carl Fredricksen (voice)"},
            {
                "name": "Christopher Plummer",
                "character": "Charles F. Muntz (voice)",
            },
            {"name": "Jordan Nagai", "character": "Russell (voice)"},
            {"name": "Bob Peterson", "character": "Dug / Alpha (voice)"},
            {"name": "Delroy Lindo", "character": "Beta (voice)"},
            {"name": "Jerome Ranft", "character": "Gamma (voice)"},
            {
                "name": "John Ratzenberger",
                "character": "Construction Foreman Tom (voice)",
            },
            {"name": "David Kaye", "character": "Newsreel Announcer (voice)"},
            {"name": "Elie Docter", "character": "Young Ellie (voice)"},
            {"name": "Jeremy Leary", "character": "Young Carl (voice)"},
            {
                "name": "Mickie McGowan",
                "character": "Police Officer Edith (voice)",
            },
            {
                "name": "Danny Mann",
                "character": "Construction Worker Steve (voice)",
            },
            {"name": "Donald Fullilove", "character": "Nurse George (voice)"},
            {"name": "Jess Harnell", "character": "Nurse AJ (voice)"},
            {"name": "Josh Cooley", "character": "Omega (voice)"},
            {"name": "Pete Docter", "character": "Campmaster Strauch (voice)"},
            {"name": "Mark Andrews", "character": "Additional Voices (voice)"},
            {"name": "Bob Bergen", "character": "Additional Voices (voice)"},
            {
                "name": "Brenda Chapman",
                "character": "Additional Voices (voice)",
            },
            {"name": "Emma Coats", "character": "Additional Voices (voice)"},
            {"name": "John Cygan", "character": "Additional Voices (voice)"},
            {"name": "Paul Eiding", "character": "Additional Voices (voice)"},
            {"name": "Tony Fucile", "character": "Additional Voices (voice)"},
            {
                "name": "Teresa Ganzel",
                "character": "Additional Voices (voice)",
            },
            {"name": "Sherry Lynn", "character": "Additional Voices (voice)"},
            {
                "name": "Laraine Newman",
                "character": "Additional Voices (voice)",
            },
            {"name": "Teddy Newton", "character": "Additional Voices (voice)"},
            {"name": "Jeff Pidgeon", "character": "Additional Voices (voice)"},
            {
                "name": "Valerie LaPointe",
                "character": "Additional Voices (voice)",
            },
            {"name": "Jan Rabson", "character": "Additional Voices (voice)"},
            {"name": "Bob Scott", "character": "Additional Voices (voice)"},
        ],
    },
]


if __name__ == '__main__':
    from helpers import error_message
    error_message()
