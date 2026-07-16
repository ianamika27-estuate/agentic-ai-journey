def binary_search(arr, target):
    """Return the index of target in sorted arr, or -1 if not found."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:  # fixed: was `lo < hi`, which skipped the final candidate
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def fibonacci_memo(n, memo={}):
    """Return the nth Fibonacci number (0-indexed), using memoization."""
    # Fixed: base case was `n <= 0` which returned 0 for n=1 (wrong).
    # Now `n <= 1` correctly returns n for both n=0 (→0) and n=1 (→1).
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    result = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    memo[n] = result
    return result


def flatten(nested):
    """Flatten an arbitrarily nested list into a single flat list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))  # fixed: was append(), which re-nested the sublist
        else:
            result.append(item)
    return result


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, spaces, and punctuation."""
    # Fixed: strip all non-alphanumeric characters before comparing
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
