"""
Minimum right Substring — Case-Insensitive Twist
Difficulty: Hard | Topic: Sliding right + Hash Maps

Problem:
    Given strings s and t, return the minimum right substring of s such that
    every character in t, including duplicate characters, is contained in the
    right.

    Characters must be matched case-insensitively, but the returned substring
    must preserve the original casing from s.

    If no such right exists, return "".

Example 1:
    Input: s = "xxAyzB", t = "ab"
    Output: "AyzB"

    The characters "A" and "B" match "a" and "b" case-insensitively. The
    returned right uses the original characters and casing from s.

Example 2:
    Input: s = "ADOBECODEBANC", t = "abc"
    Output: "BANC"

    "BANC" contains "A", "B", and "C", which match the characters in t
    case-insensitively.

Example 3:
    Input: s = "aAaBb", t = "aab"
    Output: "AaB"

    Duplicate characters matter: the right must contain two occurrences of
    "a" and one occurrence of "b", regardless of their casing.

Example 4:
    Input: s = "hello", t = "WORLD"
    Output: ""

    No right contains every required character, so return an empty string.

Example 5:
    Input: s = "xYz", t = "y"
    Output: "Y"

    The match is case-insensitive, while the returned character preserves the
    uppercase "Y" from s.

Important details:
    - Every character in t must appear in the right with the required
      frequency.
    - Matching is case-insensitive.
    - The result preserves the original casing from s.
    - Return "" when no valid right exists.
"""

import math


def get_index(c: str) -> int:
    return ord(c.lower()) - ord("a")


def minimum_window(s: str, t: str) -> str:
    """
    Return the smallest case-insensitive window containing every character in t.

    Approach:
        Use a sliding window with left (L) and right (R) pointers.
        Expand R until the window contains all the required characters. Then move
        L to remove unnecessary characters and make the valid window as small as
        possible. The frequency array records how many of each letter are still
        needed, and missing records the total number of characters still needed.

    Time complexity:
        O(N + M) for the sliding-window work, where N is the length of s and M is
        the length of t. Creating each substring with s[L:R + 1] copies characters,
        so this implementation can take O(N^2 + M) time in the worst case.

    Space complexity:
        O(1) auxiliary space because the frequency array always has 26 entries.
        The returned substring can use O(N) space, where N is the length of s.
    """

    # A window cannot contain t if s has fewer characters than t.
    if len(s) < len(t):
        return ""

    # Step 1: Set up the frequency array and the two window pointers.
    frequency: list[int] = [0] * 26  # frequency of characters where index is a-z
    L: int = 0
    R: int = 0
    n: int = len(s)
    min_window: int = math.inf
    result: str = ""
    missing: int = len(t)

    # Step 2: Count every character required by t, ignoring case.
    for i in range(len(t)):
        index: int = get_index(t[i])
        frequency[index] += 1

    # Step 3: Expand the window by moving R through s.
    while R < n:
        index: int = get_index(s[R])

        # This character fills a requirement only when its count is positive.
        if frequency[index] > 0:
            missing -= 1

        # Add s[R] to the current window.
        frequency[index] -= 1

        # Step 4: Once valid, shrink the window from the left.
        while missing == 0:
            current = s[L : R + 1]

            # Save this window if it is the smallest valid one seen so far.
            if len(current) < min_window:
                min_window = len(current)
                result = current

            # Remove s[L] and restore its count in the frequency array.
            left_index: int = get_index(s[L])
            frequency[left_index] += 1

            # A positive count means the window now lacks this required letter.
            if frequency[left_index] > 0:
                missing += 1

            # Continue shrinking until the window is no longer valid.
            L += 1

        # Move R only after all possible shrinking is finished.
        R += 1

    # Step 5: Return the smallest valid window, or "" if none was found.
    return result


def minimum_window_hash_map(s: str, t: str) -> str:
    """
    Return the smallest case-insensitive window containing every character in t.

    Approach:
        Use one hash map for the character frequencies required by t and another
        for the frequencies inside the current window. Expand the window by moving
        the right pointer. Once the window has every required frequency, move the
        left pointer to make the window as small as possible. Store only the best
        window's indexes so the original casing from s is preserved.

    Time complexity:
        O(N + M), where N is the length of s and M is the length of t. Each
        character is added by the right pointer and removed at most once by the
        left pointer.

    Space complexity:
        O(N + M) in the general case because the hash maps can contain characters
        from s and t. If the character set is fixed, the auxiliary space is O(1).
    """

    # Step 1: Set up the frequency maps, result indexes, and left pointer.
    window: dict[str, int] = {}
    frequency_of_t: dict[str, int] = {}
    result: tuple[int, int] = [-1, -1]
    min_len: int = math.inf
    have, need = 0, len(t)
    l: int = 0

    # Step 2: Count the required characters using lowercase dictionary keys.
    for c in t:
        c = c.lower()
        frequency_of_t[c] = frequency_of_t.get(c, 0) + 1

    # Step 3: Expand the window by moving the right pointer through s.
    for r in range(len(s)):
        right_char = s[r].lower()
        window[right_char] = window.get(right_char, 0) + 1

        # One required character frequency has now been completely satisfied.
        if (
            right_char in frequency_of_t
            and window[right_char] == frequency_of_t[right_char]
        ):
            have += 1

        # Step 4: While valid, save the result and shrink from the left.
        while have == need:
            # Store indexes when this is the smallest valid window so far.
            if (r - l + 1) < min_len:
                result = [l, r]
                min_len = r - l + 1

            # Remove the left character using its lowercase dictionary key.
            left_char = s[l].lower()

            window[left_char] = window.get(left_char, 0) - 1

            # The window is no longer valid if a required count falls too low.
            if (
                left_char in frequency_of_t
                and window[left_char] < frequency_of_t[left_char]
            ):
                have -= 1

            l += 1

    # Step 5: Slice the original string to preserve its casing.
    left, right = result
    return s[left : right + 1]


def solve():
    s: str = "xxAyzB"
    t: str = "ab"
    # Expected Output: "AyzB"
    print(f"s = {s}, t = {t}, result = {minimum_window(s, t)!r}")
    print(f"s = {s}, t = {t}, result = {minimum_window_hash_map(s, t)!r}")

    s = "ADOBECODEBANC"
    t = "abc"
    # Expected Output: "BANC"
    print(f"s = {s}, t = {t}, result = {minimum_window(s, t)!r}")
    print(f"s = {s}, t = {t}, result = {minimum_window_hash_map(s, t)!r}")

    s = "aAaBb"
    t = "aab"
    # Expected Output: "AaB"
    print(f"s = {s}, t = {t}, result = {minimum_window(s, t)!r}")
    print(f"s = {s}, t = {t}, result = {minimum_window_hash_map(s, t)!r}")

    s = "hello"
    t = "WORLD"
    # Expected Output: ""
    print(f"s = {s}, t = {t}, result = {minimum_window(s, t)!r}")
    print(f"s = {s}, t = {t}, result = {minimum_window_hash_map(s, t)!r}")

    s = "xYz"
    t = "y"
    # Expected Output: "Y"
    print(f"s = {s}, t = {t}, result = {minimum_window(s, t)!r}")
    print(f"s = {s}, t = {t}, result = {minimum_window_hash_map(s, t)!r}")


solve()
