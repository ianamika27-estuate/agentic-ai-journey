def to_uppercase(s):
    """Should return the string in all uppercase."""
    return s.lower()  # bug: should be s.upper()


def count_vowels(s):
    """Should return the number of vowels (a, e, i, o, u) in s, case-insensitive."""
    return sum(1 for ch in s if ch in "aeiou")  # bug: doesn't handle uppercase input