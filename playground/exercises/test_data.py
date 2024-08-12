TESTS = {
    "chunked": "advanced_test.ChunkedTests",
    "deal_cards": "advanced_test.DealCardsTest",
    "flatten_dict": "advanced_test.FlattenDictTests",
    "format_arguments": "advanced_test.FormatArgumentsTests",
    "get_cards": "advanced_test.GetCardsTest",
    "get_movie_data": "advanced_test.GetMovieDataTests",
    "matrix_from_string": "advanced_test.MatrixFromStringTests",
    "parse_csv": "advanced_test.ParseCSVTests",
    "shuffle_cards": "advanced_test.ShuffleTest",
    "decode": "atbash_cipher_test.DecodeTests",
    "encode": "atbash_cipher_test.EncodeTests",
    "dict_from_truple": "dictionaries_test.DictFromTrupleTests",
    "dict_from_tuple": "dictionaries_test.DictFromTupleTests",
    "flip_dict": "dictionaries_test.FlipDictTests",
    "get_ascii_codes": "dictionaries_test.GetASCIICodeTests",
    "get_all_factors": "dictionaries_test.GetAllFactorsTests",
    "all_together": "generators_test.AllTogetherTests",
    "deep_add": "generators_test.DeepAddTests",
    "interleave": "generators_test.InterleaveTests",
    "parse_ranges": "generators_test.ParseRangesTests",
    "is_prime": "generators_test.PrimalityTests",
    "sum_numbers": "generators_test.SumNumbersTests",
    "get_factors": "lists_test.GetFactorsTests",
    "get_vowel_names": "lists_test.GetVowelNamesTests",
    "identity": "lists_test.IdentityTests",
    "translate": "lists_test.TranslateTests",
    "triples": "lists_test.TriplesTests",
    "words_containing": "lists_test.WordsContainingTests",
    "meetup_day": "meetup_test.MeetupTest",
    "flatten": "more_test.FlattenTests",
    "matrix_add": "more_test.MatrixAddTests",
    "movies_from_year": "more_test.MoviesFromYearTests",
    "join_items": "more_test.TestJoinItems",
    "transpose": "more_test.TransposeTests"
}

MODULES = {
    "advanced": [
        "matrix_from_string",
        "format_arguments",
        "get_movie_data",
        "flatten_dict",
        "chunked",
        "parse_csv",
        "get_cards",
        "deal_cards",
        "shuffle_cards"
    ],
    "atbash_cipher": [
        "decode",
        "encode"
    ],
    "meetup": [
        "meetup_day"
    ],
    "lists": [
        "get_vowel_names",
        "words_containing",
        "translate",
        "get_factors",
        "identity",
        "triples"
    ],
    "generators": [
        "all_together",
        "sum_numbers",
        "interleave",
        "parse_ranges",
        "is_prime",
        "deep_add"
    ],
    "more": [
        "join_items",
        "flatten",
        "transpose",
        "movies_from_year",
        "matrix_add"
    ],
    "dictionaries": [
        "flip_dict",
        "get_ascii_codes",
        "dict_from_truple",
        "dict_from_tuple",
        "get_all_factors"
    ]
}
