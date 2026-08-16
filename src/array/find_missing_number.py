"""Find Missing Number

Given an integer array ``nums`` of size ``n`` containing distinct values in the
range from 0 to n, inclusive, return the only number missing from the array
within this range.

Example 1:
    Input: nums = [0, 2, 3, 1, 4]
    Output: 5
    Explanation: nums contains 0, 1, 2, 3, and 4, leaving 5 as the only missing
    number in the range [0, 5].

Example 2:
    Input: nums = [0, 1, 2, 4, 5, 6]
    Output: 3
    Explanation: nums contains 0, 1, 2, 4, 5, and 6, leaving 3 as the only
    missing number in the range [0, 6].

Now your turn:
    Input: nums = [1, 3, 6, 4, 2, 5]
    Possible answers: 6, 7, 0, 8

Constraints:
    - n == nums.length
    - 1 <= n <= 10^4
    - 0 <= nums[i] <= n
    - All values in nums are unique.
"""


def find_missing_number_time_optimized(nums: list[int]) -> int:
    """Return the missing value from the inclusive range 0 through n.

    Approach:
        1. Convert ``nums`` to a set so that each possible number can be checked
           for membership efficiently.
        2. Store the length ``n`` of the input array.
        3. Check every candidate from 0 through n, inclusive. The inclusive
           upper bound is necessary because n itself may be the missing value.
        4. Return the first candidate that is absent from the set. The problem
           guarantees that exactly one candidate is missing.

    Time Complexity:
        O(n) on average. Creating the set processes n values, and the loop makes
        at most n + 1 average O(1) set-membership checks.

    Space Complexity:
        O(n) auxiliary space because the set can contain all n input values.
    """
    # Step 1: Store every present number in a set for fast membership checks.
    present_numbers: set[int] = set(nums)

    # Step 2: Store n, which is both the array length and maximum allowed value.
    n: int = len(nums)

    # Steps 3 and 4: Check every candidate from 0 through n and return the gap.
    for candidate in range(n + 1):
        if candidate not in present_numbers:
            return candidate


def find_missing_number_time_and_space_optimized1(nums: list[int]) -> int:
    """Return the missing value using the difference between two sums.

    Approach:
        1. Store the input length ``n``. Because the valid range is 0 through n,
           the complete range contains n + 1 possible values.
        2. Calculate the expected sum of every integer from 0 through n using
           the arithmetic-series formula ``n * (n + 1) // 2``.
        3. Initialize the sum of the values actually present in ``nums``.
        4. Traverse ``nums`` once and add each value to the actual sum.
        5. Subtract the actual sum from the expected sum. Every present value
           cancels out, leaving only the missing value.

    Time Complexity:
        O(n), where n is the length of ``nums``, because the function traverses
        the array once. Calculating the expected sum takes constant time.

    Space Complexity:
        O(1) auxiliary space because only ``n``, the two sums, and the current
        value are stored regardless of the input size.
    """
    # Step 1: Store the input length and maximum value in the complete range.
    n: int = len(nums)

    # Step 2: Calculate the sum that all values from 0 through n should have.
    expected_sum: int = n * (n + 1) // 2

    # Step 3: Initialize the sum of the values that are actually present.
    actual_sum: int = 0

    # Step 4: Add every input value to the actual sum.
    for num in nums:
        actual_sum += num

    # Step 5: The difference between both sums is the missing value.
    return expected_sum - actual_sum


def find_missing_number_time_and_space_optimized2(nums: list[int]) -> int:
    """Return the missing value by canceling matching values with XOR.

    Approach:
        1. Initialize ``xor1`` for the values present in ``nums`` and ``xor2``
           for every expected value in the complete range.
        2. Traverse every valid array index from 0 through n - 1.
        3. XOR the current array value into ``xor1``.
        4. XOR ``index + 1`` into ``xor2``. The problem's complete range remains
           0 through n, but the loop produces the values 1 through n. This is
           equivalent to XORing 0 through n because ``value ^ 0 == value``, so
           including zero would not change the accumulated result.
        5. XOR both accumulated values. Every number present in both groups
           cancels itself, leaving only the missing number.

    Time Complexity:
        O(n), where n is the length of ``nums``, because the function traverses
        the array once and performs constant-time XOR operations per element.

    Space Complexity:
        O(1) auxiliary space because only two XOR accumulators and the current
        index are stored regardless of the input size.
    """
    # Step 1: Initialize the XOR accumulators for actual and expected values.

    xor1: int = 0
    xor2: int = 0

    # Step 2: Visit every valid index in nums once.
    for index in range(len(nums)):
        # Step 3: Accumulate the values that are present in the input.
        xor1 = xor1 ^ nums[index]

        # Step 4: Accumulate 1 through n; XORing the omitted 0 has no effect.
        xor2 = xor2 ^ index + 1

    # Step 5: Matching values cancel, leaving the missing number.
    return xor1 ^ xor2


def find_missing_number_brute_force(nums: list[int]) -> int:
    """Return the missing value by searching the array for every candidate.

    Approach:
        1. Store the input length ``n`` and declare a Boolean used to track
           whether the current candidate appears in the array.
        2. Consider every candidate from 0 through n, inclusive, because n may
           itself be the missing number.
        3. Initially assume the current candidate has not been found.
        4. Scan every value in ``nums``. If a value equals the candidate, mark
           it as found and stop the inner scan early.
        5. After scanning, return the candidate if it was not found. The problem
           guarantees that exactly one candidate will be missing.

    Time Complexity:
        O(n^2) in the worst case. There are n + 1 possible candidates, and each
        candidate may require scanning all n values in the input array.

    Space Complexity:
        O(1) auxiliary space because only the length, candidate, current value,
        and Boolean flag are stored regardless of the input size.
    """
    # Step 1: Store n and declare the flag used for each candidate search.
    n: int = len(nums)
    found: bool

    # Step 2: Consider every possible value from 0 through n.
    for candidate in range(n + 1):
        # Step 3: Assume the candidate is absent before scanning nums.
        found = False

        # Step 4: Search the entire array until the candidate is found.
        for num in nums:
            if candidate == num:
                found = True
                break

        # Step 5: Return the candidate when no matching value was found.
        if not found:
            return candidate


def solve() -> None:
    nums: list[int] = [0, 2, 3, 1, 4]

    expected: int = 5
    result: int = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2, 3, 1, 4]

    expected = 5
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 2, 4, 5, 6]

    expected = 3
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 6, 4, 2, 5]

    expected = 0
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 0, 1]

    expected = 2
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = 1
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = 0
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 10_001))

    expected = 0
    result = find_missing_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 2, 4, 5, 6]

    expected = 3
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 6, 4, 2, 5]

    expected = 0
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 0, 1]

    expected = 2
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = 1
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = 0
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(10_000))

    expected = 10_000
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 10_001))

    expected = 0
    result = find_missing_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2, 3, 1, 4]

    expected = 5
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 2, 4, 5, 6]

    expected = 3
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 6, 4, 2, 5]

    expected = 0
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 0, 1]

    expected = 2
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = 1
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = 0
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(10_000))

    expected = 10_000
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 10_001))

    expected = 0
    result = find_missing_number_time_and_space_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 2, 3, 1, 4]

    expected = 5
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 2, 4, 5, 6]

    expected = 3
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 6, 4, 2, 5]

    expected = 0
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 0, 1]

    expected = 2
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = 1
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = 0
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(10_000))

    expected = 10_000
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(1, 10_001))

    expected = 0
    result = find_missing_number_time_and_space_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
