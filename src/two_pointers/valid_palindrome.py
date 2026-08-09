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

Approach:
    1. Normalize the input by keeping only letters and numbers and converting
       them to lowercase. This lets us ignore punctuation, spaces, and case.
    2. Place one pointer at the beginning of the normalized string and another
       pointer at the end.
    3. Compare the characters at both pointers. If they differ, return False.
    4. Move both pointers toward the center. If every pair matches, return True.

Time Complexity:
    O(n), where n is the input length. Normalization takes O(n), and the
    two-pointer comparison takes O(n), giving O(n) total time.

Space Complexity:
    O(n) because normalized_s may contain up to n characters. The two pointer
    variables use O(1) additional space.
"""


def is_valid_palindrome(s: str) -> bool:
    # Step 1: Keep only letters and numbers and convert letters to lowercase.
    # isalnum() already excludes spaces and punctuation.
    normalized_s = "".join(c.lower() for c in s if c.isalnum())

    # Step 2: Start one pointer at each end of the normalized string.
    left = 0
    right = len(normalized_s) - 1

    # Step 3: Compare pairs of characters while moving toward the center.
    while left < right:
        # A mismatched pair means the string cannot be a palindrome.
        if normalized_s[left] != normalized_s[right]:
            return False

        # Move both pointers inward to compare the next pair.
        left += 1
        right -= 1

    # Step 4: Every pair matched. Empty and one-character strings also reach
    # this line because they do not need any pair comparisons.
    return True


def is_valid_palindrome_space_optimized(s: str) -> bool:
    """
    Approach: Two pointers directly on the original string, skipping
    non-alphanumeric characters in place instead of building a cleaned copy.

    Why this is more space efficient than is_valid_palindrome:
        - is_valid_palindrome builds normalized_s, a new string that can be
          up to n characters — O(n) extra space.
        - This version never allocates that string. The two pointers operate
          directly on the input, so extra space is just two integers — O(1).

    Steps:
        1. Start left at index 0, right at the last index.
        2. If left points to a non-alphanumeric character, skip it by moving left forward.
        3. If right points to a non-alphanumeric character, skip it by moving right backward.
        4. Both pointers now point to valid characters — compare them case-insensitively.
           If they differ, it's not a palindrome.
        5. If they match, move both pointers inward and repeat.
        6. If the pointers meet or cross without a mismatch, it's a palindrome.

    Time:  O(n) — each character is visited at most once by either pointer.
        Worst case: a string like "a" * 1000 where every character is valid and
        matches, so both pointers traverse the entire string before meeting in
        the middle.

    Space: O(1) — only two integer pointer variables regardless of input size.
        This is the key improvement over is_valid_palindrome which uses O(n)
        space for the normalized copy.
    """

    left: int = 0
    right: int = len(s) - 1

    while left < right:
        # Step 2: left is on a non-alphanumeric character — skip it
        if not s[left].isalnum() or s[left].isspace():
            left += 1
        # Step 3: right is on a non-alphanumeric character — skip it
        elif not s[right].isalnum() or s[right].isspace():
            right -= 1
        # Step 4: both pointers are on valid characters — compare case-insensitively
        elif s[left].lower() != s[right].lower():
            return False
        # Step 5: characters match, move both pointers inward
        else:
            left += 1
            right -= 1

    # Step 6: all valid character pairs matched
    return True


def solve():
    s = "Was it a car or a cat I saw?"
    expected = True
    result = is_valid_palindrome(s)
    result_optimized = is_valid_palindrome_space_optimized(s)
    assert result == expected
    assert result_optimized == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "tab a cat"
    expected = False
    result = is_valid_palindrome(s)
    result_optimized = is_valid_palindrome_space_optimized(s)
    assert result == expected
    assert result_optimized == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "A man, a plan, a canal: Panama"
    expected = True
    result = is_valid_palindrome(s)
    result_optimized = is_valid_palindrome_space_optimized(s)
    assert result == expected
    assert result_optimized == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    s = "0P"
    expected = False
    result = is_valid_palindrome(s)
    result_optimized = is_valid_palindrome_space_optimized(s)
    assert result == expected
    assert result_optimized == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


solve()
