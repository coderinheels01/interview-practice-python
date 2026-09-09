"""Valid Palindrome Using Recursion

Given a string ``text``, return ``True`` if it is a palindrome and ``False``
otherwise. You must solve the problem using recursion.

A palindrome is a string that reads the same forward and backward.

Example 1:
    Input: text = "racecar"
    Output: True
    Explanation: "racecar" reads the same forward and backward.

Example 2:
    Input: text = "hello"
    Output: False
    Explanation: "hello" and "olleh" are different.

Now your turn:
    Input: text = "level"

Constraints:
    - 1 <= text.length <= 1000
    - ``text`` consists only of lowercase English letters.
"""


def is_palindrome(text: str) -> bool:
    """Return whether ``text`` reads the same forward and backward.

    Approach: Recursion with Mirrored Character Comparisons
        1. Start with a shared result of True and record the string length.
        2. Define a recursive helper whose ``start`` index identifies the
           next character to compare. The helper updates the enclosing
           result through ``nonlocal`` instead of returning a boolean.
        3. Stop when ``start`` reaches or passes half the string length.
           For odd lengths, this implementation also compares the middle
           character with itself before reaching the stopping condition.
        4. Compare the character at ``start`` with its mirrored character
           at ``text_length - start - 1``. On a mismatch, set the shared
           result to False and return without making another recursive call.
        5. If the characters match, recurse with ``start + 1`` to check the
           next inner pair. Returning calls perform no further comparisons.
        6. Call the helper starting at index zero.
        7. Return the shared result: True if all comparisons matched,
           otherwise False.

    Parameters:
        text: A string of 1 to 1000 lowercase English letters. Comparisons
            are exact; no characters are removed or normalized.

    Returns:
        True for a palindrome, including a single character; False when
        any mirrored pair differs.

    Mutation Behavior:
        The input string is not modified. Only the local result captured
        by the recursive helper is updated.

    Time Complexity:
        O(n) in the worst case, where n is the string length. At most
        ceil(n / 2) character comparisons occur, each taking O(1) time.
        A mismatch in the first pair takes O(1) time.

    Space Complexity:
        O(n) auxiliary space in the worst case for ceil(n / 2) + 1 helper
        call frames. Each frame stores a start index and constant bookkeeping;
        the shared result, length, and input reference take O(1) space.
        No substring copies or additional collections are created.

    Assumptions:
        The caller supplies an input within the stated constraints; these
        are not validated. Python must have sufficient recursion capacity
        for the helper's depth (up to 501 frames for the allowed lengths),
        in addition to the caller's existing stack.
    """
    # Step 1: Initialize the shared result and record the string length.
    is_valid: bool = True
    text_length: int = len(text)

    # Step 2: Define a helper that can update the enclosing result.
    def valid_palindrome(start: int):
        nonlocal is_valid
        # Step 3: Stop after reaching or passing the midpoint.
        if start >= text_length / 2:
            return
        # Step 4: Mark a mismatch and stop this recursive chain.
        if text[start] != text[text_length - start - 1]:
            is_valid = False
            return
        # Step 5: Move inward to compare the next mirrored pair.
        valid_palindrome(start=start + 1)

    # Step 6: Begin comparisons at the first character.
    valid_palindrome(0)

    # Step 7: Return the result after the recursive calls finish.
    return is_valid


def solve() -> None:
    text: str = "racecar"

    expected: bool = True
    result: bool = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum allowed length.
    text: str = "a"

    expected: bool = True
    result: bool = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest even-length palindrome.
    text = "aa"

    expected = True
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest non-palindrome.
    text = "ab"

    expected = False
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd-length palindrome.
    text = "level"

    expected = True
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even-length palindrome.
    text = "abccba"

    expected = True
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The outer characters match, but an inner pair does not.
    text = "abca"

    expected = False
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every character is identical.
    text = "zzzzzzz"

    expected = True
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed length containing a palindrome.
    text = "a" * 1000

    expected = True
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed length with different first and last characters.
    text = ("a" * 999) + "b"

    expected = False
    result = is_palindrome(text)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
