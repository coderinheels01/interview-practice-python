"""Single Number - I

Given an integer array ``nums`` containing ``n`` values, every integer appears
exactly twice except for one integer that appears once. Return the integer that
appears only once.

Example 1:
    Input: nums = [1, 2, 2, 4, 3, 1, 4]
    Output: 3
    Explanation: The integer 3 appears only once.

Example 2:
    Input: nums = [5]
    Output: 5
    Explanation: The integer 5 appears only once.

    https://www.youtube.com/watch?v=bYWLJb3vCWY&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=3
"""

from collections import Counter


def single_number_brute_force(nums: list[int]) -> int:
    """Return the value that appears once by counting each candidate.

    Approach:
        1. Store the length of the input array.
        2. Visit every element and treat it as the current candidate.
        3. Initialize the candidate's occurrence count to zero.
        4. Scan the entire array and increment the count whenever an element
           equals the candidate.
        5. After the inner scan, return the candidate if its count is 1. The
           problem guarantees that exactly one candidate appears once.

    Time Complexity:
        O(n^2), where n is the length of ``nums``. For each of the n candidates,
        the function scans all n elements to count its occurrences.

    Space Complexity:
        O(1) auxiliary space because only indexes, the current candidate, and
        its count are stored regardless of the input size.
    """
    # Step 1: Store the input length.
    n: int = len(nums)

    # Step 2: Treat every array element as a candidate.
    for i in range(n):
        candidate: int = nums[i]

        # Step 3: Initialize the current candidate's occurrence count.
        count: int = 0

        # Step 4: Count the candidate across the entire array.
        for j in range(n):
            if candidate == nums[j]:
                count += 1

        # Step 5: Return the only candidate that occurs once.
        if count == 1:
            return candidate


def single_number_time_optimized(nums: list[int]) -> int:
    """Return the value that appears exactly once in the array.

    Approach:
        1. Build a frequency map with ``Counter`` so every distinct number maps
           to the number of times it appears in ``nums``.
        2. Traverse each number and its frequency in the counter.
        3. Return the number whose frequency is 1. The problem guarantees that
           exactly one such number exists.

    Time Complexity:
        O(n), where n is the length of ``nums``. Building the counter processes
        all n elements, and scanning its entries examines at most n distinct
        values.

    Space Complexity:
        O(n) auxiliary space in the worst case because the counter can contain
        up to n distinct keys.
    """
    # Step 1: Count how many times each number appears.
    counts: Counter[int] = Counter(nums)

    # Step 2: Examine every distinct number and its frequency.
    for num, count in counts.items():
        # Step 3: Return the only number that occurs once.
        if count == 1:
            return num


def single_number_space_optimized(nums: list[int]) -> int:
    """Return the value that appears once by canceling pairs with XOR.

    Approach: XOR Cancellation
        1. Initialize an XOR accumulator to 0, which is the identity value for
           XOR because ``value ^ 0 == value``.
        2. Traverse every number in ``nums``.
        3. XOR each number into the accumulator. Because ``value ^ value == 0``,
           every value that appears twice cancels itself. XOR is associative
           and commutative, so the array order does not affect the result.
        4. Return the accumulator, which contains the only unpaired number.

    Time Complexity:
        O(n), where n is the length of ``nums``, because every element is
        processed exactly once.

    Space Complexity:
        O(1) auxiliary space because only one XOR accumulator and the current
        number are stored regardless of the input size.
    """
    # Step 1: Initialize the XOR accumulator with the identity value 0.
    xor: int = 0

    # Step 2: Traverse every number in the array.
    for n in nums:
        # Step 3: XOR the number so paired values cancel each other.
        xor ^= n

    # Step 4: Return the only value that was not canceled by a matching pair.
    return xor


def solve() -> None:
    nums: list[int] = [1, 2, 2, 4, 3, 1, 4]

    expected: int = 3
    result: int = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 4, 3, 1, 4]

    expected = 3
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = 5
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 3, 3, 4, 4]

    expected = 7
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 3, 4, 4, 7]

    expected = 7
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 0, 2, 2]

    expected = 0
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -5, 2, 2]

    expected = -5
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, 8, -3, 4, 4]

    expected = 8
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -10_000, 10_000]

    expected = -10_000
    result = single_number_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = 5
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 3, 3, 4, 4]

    expected = 7
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 3, 4, 4, 7]

    expected = 7
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 0, 2, 2]

    expected = 0
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -5, 2, 2]

    expected = -5
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, 8, -3, 4, 4]

    expected = 8
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -10_000, 10_000]

    expected = -10_000
    result = single_number_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 2, 4, 3, 1, 4]

    expected = 3
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = 5
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 3, 3, 4, 4]

    expected = 7
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 3, 4, 4, 7]

    expected = 7
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 0, 2, 2]

    expected = 0
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -5, 2, 2]

    expected = -5
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, 8, -3, 4, 4]

    expected = 8
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -10_000, 10_000]

    expected = -10_000
    result = single_number_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
