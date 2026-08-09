"""
Valid Palindrome

Difficulty: Easy
Topics: Two Pointers
Company Tags
Hints

Given a string s, return True if it is a palindrome; otherwise, return False.

A palindrome is a string that reads the same forward and backward. The check
is case-insensitive and ignores all non-alphanumeric characters.

Note:
    Alphanumeric characters consist of letters (A-Z, a-z) and numbers (0-9).

Example 1:
    Input:
        s = "Was it a car or a cat I saw?"

    Output:
        True

    Explanation:
        After considering only alphanumeric characters, the string becomes
        "wasitacaroracatisaw", which is a palindrome.

Example 2:
    Input:
        s = "tab a cat"

    Output:
        False

    Explanation:
        "tabacat" is not a palindrome.

Constraints:
    - 1 <= len(s) <= 1000
    - s contains only printable ASCII characters.
"""


def is_valid_palindrome(s: str) -> bool:

    left: int = 0
    riight: int = len(s) - 1
    pass


def solve():
    s = "Was it a car or a cat I saw?"
    expected = True
    result = is_valid_palindrome(s)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "tab a cat"
    expected = False
    result = is_valid_palindrome(s)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "A man, a plan, a canal: Panama"
    expected = True
    result = is_valid_palindrome(s)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "0P"
    expected = False
    result = is_valid_palindrome(s)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


solve()
