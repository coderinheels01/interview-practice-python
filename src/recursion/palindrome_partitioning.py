"""131. Palindrome Partitioning

Given a string s, partition s such that every substring in the partition is
a palindrome. Return all possible palindrome partitions of s.

A palindrome is a string that reads the same backward as forward.
A partition divides s into nonempty, contiguous substrings that together
reconstruct s in their original order. Return each partition as a list of
strings. The outer list of partitions may be returned in any order.

Example 1:
    Input: s = "aab"
    Output: [["a", "a", "b"], ["aa", "b"]]

Example 2:
    Input: s = "a"
    Output: [["a"]]

Constraints:
    - 1 <= len(s) <= 16
    - s contains only lowercase English letters.

https://www.youtube.com/watch?v=WBgsABoClE0&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=19
"""

from functools import cache


def palindrome_partitioning(s: str) -> list[list[str]]:
    """Return all ways to split s into nonempty palindrome substrings.

    Args:
        s: A string of 1 to 16 lowercase English letters. It is not modified.

    Returns:
        Independent partition lists whose substrings concatenate to s in
        their original order. Every substring is a palindrome. Outer result
        order is unrestricted; this implementation tries shorter prefixes first.

    Approach:
        Depth-First Search with Backtracking and memoized palindrome checks.
        1. Initialize the output and an empty current_partition. Start at
           index zero, the first character not yet included in the partition.
        2. If start == len(s), the entire string has been partitioned. Save
           current_partition.copy() and return. The working list changes during
           backtracking, so saving its reference would not preserve a result.
           A shallow copy is sufficient because the contained strings are immutable.
        3. Try every ending index from start through len(s) - 1. Including
           start permits a single-character substring, which is a palindrome.
        4. Check s[start:index + 1] using two pointers. Compare the endpoint
           characters and move inward until a mismatch or the pointers meet.
           @cache stores the boolean for the original (start, end) arguments;
           repeated checks of the same range reuse it. The cache is fresh for
           each outer function call, so results do not leak between strings.
           A failed check does not end the loop: 'ab' fails but 'aba' succeeds.
        5. For a palindrome, append the substring and recurse from index + 1.
           This selects a contiguous piece and advances past it, ensuring no
           gaps or overlap. The parent waits while the child explores deeper.
        6. Pop the selected substring after recursion returns, restoring the
           working partition before trying another ending index.
        7. Return all saved partitions after the search finishes. Only the
           palindrome checker is cached; the partition search still explores
           every valid sequence of cuts and saves every completed result.

        Example walkthrough:
            For 'aab', choose 'a', then 'a', then 'b', and save ['a', 'a', 'b'].
            Backtracking tries 'ab', rejects it, and eventually returns to the
            initial position. Choosing 'aa' followed by 'b' saves ['aa', 'b'].
            The whole substring 'aab' is rejected.

    Examples:
        >>> palindrome_partitioning("aab")
        [['a', 'a', 'b'], ['aa', 'b']]
        >>> palindrome_partitioning("aba")
        [['a', 'b', 'a'], ['aba']]
        >>> palindrome_partitioning("a")
        [['a']]
        >>> palindrome_partitioning("ab")
        [['a', 'b']]

    Time Complexity:
        O(n * 2**n) worst case, where n = len(s). There are n - 1 gaps
        between characters; choosing cut or no cut at each gap gives at most
        2**(n - 1) complete partitions. When all characters are equal, every
        cut pattern is valid. Saving a partition copies up to n references.
        The candidate-loop and substring-slicing work also fit this bound:
        even without pruning, the recursion has O(2**n) candidate extensions,
        each creating a substring of at most n characters.
        There are O(n**2) distinct palindrome ranges. Each uncached check
        can scan O(n) characters, giving O(n**3) total first-time checking
        work, with constant-time cache hits afterward. This polynomial term
        is dominated by the stated exponential worst-case bound. Caching
        avoids repeated checking, but cannot avoid generating the output.

    Space Complexity:
        O(n * 2**n) worst-case total space, including the returned partitions.
        There can be exponentially many partitions, with up to n string
        references and n characters' worth of content per partition. List
        copies share immutable strings rather than deep-copying their contents.
        Auxiliary space is O(n**2), dominated by cached index pairs and
        booleans. The recursion stack and working partition use O(n) space;
        substrings along the current path cover at most n characters in total.
        Unlike the uncached version, the cache adds quadratic auxiliary memory.

        Cache example: for s="abc" (n=3), the possible (start, end) pairs are:
            start=0: (0,0), (0,1), (0,2) -> 3 ranges
            start=1:        (1,1), (1,2) -> 2 ranges
            start=2:               (2,2) -> 1 range
        There are 3 + 2 + 1 = 6 entries, each storing an index pair and a
        boolean result. In general, the count is n + (n - 1) + ... + 1,
        which equals n(n + 1) / 2 and grows quadratically.
        This uses addition, not factorial multiplication. For n=4:
            Substring ranges: 4 + 3 + 2 + 1 = 10
            Factorial:        4 * 3 * 2 * 1 = 24
        We add the separate groups of ranges starting at each index; we are
        not multiplying choices to construct permutations.
    """
    # Step 1: Initialize the output and shared working partition.
    result: list[list[str]] = []
    current_partition: list[str] = []
    size: int = len(s)

    # Step 4: Remember palindrome results for each original index pair.
    @cache
    def is_valid_palindrome(start: int, end: int) -> bool:
        # Step 4: Compare characters inward without creating a substring.
        while start < end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1

        return True

    def find_partitions(start: int) -> None:
        # Step 2: Save a snapshot only after consuming the whole string.
        if start == size:
            result.append(current_partition.copy())
            return
        # Steps 3 and 4: Try every endpoint, including single characters.
        for index in range(start, size):
            if is_valid_palindrome(start=start, end=index):
                # Step 5: Choose this palindrome and partition the remaining suffix.
                current_partition.append(s[start : index + 1])
                find_partitions(start=index + 1)
                # Step 6: Undo the choice before trying another endpoint.
                current_partition.pop()

    # Steps 1 and 7: Search from the first character, then return all partitions.
    find_partitions(start=0)

    return result


def solve() -> None:
    # s: str = "aab"
    # expected: list[list[str]] = [["a", "a", "b"], ["aa", "b"]]
    # result: list[list[str]] = palindrome_partitioning(s)

    # Ignore partition order while preserving substring order within each one.
    # assert sorted(result) == sorted(expected)
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    from itertools import combinations

    # Minimum length and first lowercase letter.
    s = 'a'
    expected = [["a"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single last lowercase letter.
    s = 'z'
    expected = [["z"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two different letters.
    s = 'ab'
    expected = [["a", "b"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal letters.
    s = 'aa'
    expected = [["a", "a"], ["aa"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example.
    s = 'aab'
    expected = [["a", "a", "b"], ["aa", "b"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd palindrome after a shorter non-palindrome.
    s = 'aba'
    expected = [["a", "b", "a"], ["aba"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even palindrome with a palindromic interior.
    s = 'abba'
    expected = [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal endpoints do not guarantee a palindrome.
    s = 'abca'
    expected = [["a", "b", "c", "a"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated letters allow every cut pattern.
    s = 'aaa'
    expected = [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A longer palindrome at the beginning.
    s = 'abac'
    expected = [["a", "b", "a", "c"], ["aba", "c"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A longer palindrome in the middle.
    s = 'cabad'
    expected = [["c", "a", "b", "a", "d"], ["c", "aba", "d"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A longer palindrome at the end.
    s = 'caba'
    expected = [["c", "a", "b", "a"], ["c", "aba"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Overlapping palindrome choices.
    s = 'abab'
    expected = [["a", "b", "a", "b"], ["a", "bab"], ["aba", "b"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Independent palindrome groups.
    s = 'aabb'
    expected = [["a", "a", "b", "b"], ["aa", "b", "b"], ["a", "a", "bb"], ["aa", "bb"]]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with no multi-character palindrome.
    s = 'abcdefghijklmnop'
    expected = [list("abcdefghijklmnop")]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with a whole-string even palindrome.
    s = 'abcdefghhgfedcba'
    expected = [list("abcdefgh"[:depth]) + ["abcdefghhgfedcba"[depth:16-depth]] + list("abcdefgh"[:depth][::-1]) for depth in range(8)] + [list("abcdefghhgfedcba")]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of equal letters yields all 32768 partitions.
    s = 'aaaaaaaaaaaaaaaa'
    expected = [["a" * (end - start) for start, end in zip((0,) + cuts, cuts + (16,))] for cut_count in range(16) for cuts in combinations(range(1, 16), cut_count)]
    result = palindrome_partitioning(s)

    assert sorted(result) == sorted(expected)
    assert len({id(partition) for partition in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
