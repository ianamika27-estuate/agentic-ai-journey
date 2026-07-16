from algorithms import binary_search, fibonacci_memo, flatten, is_palindrome


def test_binary_search_finds_all_elements():
    arr = [1, 3, 5, 7, 9, 11]
    for i, val in enumerate(arr):
        assert binary_search(arr, val) == i
    assert binary_search(arr, 4) == -1


def test_binary_search_single_element():
    # Classic off-by-one trap: array of length 1
    assert binary_search([42], 42) == 0
    assert binary_search([42], 7) == -1


def test_fibonacci_sequence():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    for i, val in enumerate(expected):
        assert fibonacci_memo(i) == val


def test_fibonacci_repeated_calls_are_consistent():
    # Calling with a fresh logical sequence shouldn't be corrupted by
    # whatever a PREVIOUS test already computed (mutable default arg trap)
    assert fibonacci_memo(5) == 5
    assert fibonacci_memo(3) == 2
    assert fibonacci_memo(5) == 5  # must still be correct, not stale/wrong


def test_flatten_deeply_nested():
    nested = [1, [2, 3, [4, 5, [6, 7]], 8], 9]
    assert flatten(nested) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_flatten_flat_list_unchanged():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_is_palindrome_simple():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False


def test_is_palindrome_with_punctuation_and_case():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("Was it a car or a cat I saw?") is True