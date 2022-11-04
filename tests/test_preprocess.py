"""Unit tests for preprocessing"""
from preprocess import preprocess


def test_that_punctations_are_removed():
    string = 'Hello, World!'

    cleaned_string = preprocess(string)

    assert ',' not in cleaned_string
    assert '!' not in cleaned_string


def test_that_is_lower_case():
    string = 'Hello, World!'

    cleaned_string = preprocess(string)

    assert all(map(lambda word: word.islower(), cleaned_string))