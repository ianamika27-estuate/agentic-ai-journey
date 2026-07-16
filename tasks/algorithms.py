def binary_search(arr, target):
    """Return the index of target in sorted arr, or -1 if not found."""
    lo, hi = 0, len(arr) - 1
    while lo < hi:  # bug: should be <=, otherwise misses the case where
                    # lo == hi could still be the target
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
    # Two layered issues here:
    # 1. The base case is off by one — should be `n <= 1`, not `n <= 0` —
    #    which produces wrong values for n=1 and cascades into every n above it.
    # 2. `memo={}` is a mutable default argument, shared across ALL calls for
    #    the life of the program — a real anti-pattern, though it happens not
    #    to corrupt correctness here since only correct (once fixed) values
    #    ever get cached. Worth noticing and fixing anyway.
    if n <= 0:
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
            result.append(flatten(item))  # bug: should extend, not append —
                                           # this nests one level too deep
                                           # instead of fully flattening
        else:
            result.append(item)
    return result


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, spaces, and punctuation."""
    cleaned = s.lower()  # bug: doesn't strip spaces/punctuation, so
                         # "A man, a plan, a canal: Panama" fails
    return cleaned == cleaned[::-1]