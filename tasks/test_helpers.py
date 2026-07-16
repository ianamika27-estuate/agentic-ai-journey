from helpers import to_uppercase, count_vowels


def test_to_uppercase():
    assert to_uppercase("hello") == "HELLO"


def test_count_vowels():
    assert count_vowels("Hello World") == 3