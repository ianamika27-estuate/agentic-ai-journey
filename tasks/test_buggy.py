from buggy import add_numbers, reverse_string, is_even, subtract_numbers


def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0


def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("ab") == "ba"


def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False
    
def test_subtract_numbers():
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(10, 5) == 5
