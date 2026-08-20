"""Majority Element I

Given an integer array ``nums`` of size ``n``, return the majority element of
the array.

The majority element is the value that appears more than ``n / 2`` times. The
array is guaranteed to contain a majority element.

Example 1:
    Input: nums = [7, 0, 0, 1, 7, 7, 2, 7, 7]
    Output: 7
    Explanation: The number 7 appears 5 times in the array of size 9.

Example 2:
    Input: nums = [1, 1, 1, 2, 1, 2]
    Output: 1
    Explanation: The number 1 appears 4 times in the array of size 6.

Now your turn:
    Input: nums = [-1, -1, -1, -1]
    Output: -1

Constraints:
    - n == len(nums)
    - 1 <= n <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - One value appears more than n / 2 times

    https://www.youtube.com/watch?v=nP_ns3uSh80&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=7
"""

from collections import Counter


def majority_element_brute_force(nums: list[int]) -> int:
    """Return the majority element by counting every candidate directly.

    ``nums`` is a non-empty list that is guaranteed to contain a value appearing
    more than half the time. The function reads the list without mutating it and
    returns the majority value as an integer.

    Approach: Brute-Force Frequency Counting
        1. Store the input size and initialize a counter.
        2. Treat each position in ``nums`` as a possible majority candidate.
        3. Reset the counter before evaluating each candidate.
        4. Traverse the entire list and increment the counter whenever an
           element matches the current candidate.
        5. If the candidate's count is greater than half the input size, return
           that candidate as the majority element.
        6. Continue until the guaranteed majority is found. If every candidate
           is checked without finding one, raise ``ValueError`` to signal that
           the input violated the majority-element guarantee. This exception is
           unreachable for inputs that satisfy the problem constraints.

    Time Complexity:
        O(n^2), where n is the length of ``nums``. In the worst case, the outer
        loop considers O(n) candidates, and the inner loop performs n
        comparisons for each candidate. This is impractical near the maximum
        constraint of n = 100,000.

    Space Complexity:
        O(1) auxiliary space. The function stores only the input size, two loop
        indexes, and a counter, regardless of the size of ``nums``.
    """
    # Step 1: Store the input size and initialize the candidate counter.
    size: int = len(nums)
    count: int = 0

    # Step 2: Treat each array position as a possible majority candidate.
    for index in range(size):
        # Step 3: Reset the frequency before counting the current candidate.
        count = 0

        # Step 4: Compare the candidate with every value in the input.
        for inner_index in range(size):
            if nums[index] == nums[inner_index]:
                count += 1

        # Step 5: Return the candidate once its count is greater than half.
        if count > (size // 2):
            return nums[index]

    # Step 6: Reject input that violates the guaranteed-majority requirement.
    raise ValueError("No majority element exists")


def majority_element_time_optimized(nums: list[int]) -> int:
    """Return the value that appears more than half the time in ``nums``.

    ``nums`` is a non-empty list of integers that is guaranteed to contain one
    majority element. The function reads the list without mutating it and
    returns that majority value as an integer.

    Approach: Frequency Counter
        1. Build a Counter that maps each distinct number to its frequency.
        2. Ask the Counter for one ``(number, frequency)`` pair with the highest
           frequency by calling ``most_common(1)``.
        3. Access the first pair in the returned list, then access the number at
           index 0 of that pair and return it. The majority-element guarantee
           ensures that this most frequent number is the required answer.

    Time Complexity:
        O(n), where n is the length of ``nums``. Constructing the Counter scans
        all n values. Finding the single most common entry examines at most k
        distinct entries, where k <= n, so the total remains O(n).

    Space Complexity:
        O(k), where k is the number of distinct values in ``nums``. The Counter
        stores one frequency entry per distinct value. In the worst case,
        k can grow with n, giving O(n) auxiliary space.
    """
    # Step 1: Count the frequency of every distinct number.
    frequency_map: Counter[int] = Counter(nums)

    # Steps 2 and 3: Get the most frequent pair and return its number.
    return frequency_map.most_common(1)[0][0]


def majority_element_optimized(nums: list[int]) -> int:
    """Return the value that appears more than half the time in ``nums``.

    Approach — Boyer-Moore Majority Vote Algorithm:
        1. Start with the first value as the candidate and a vote count of zero.
        2. Scan the list. When the count is zero, select the current value as
           the new candidate.
        3. Add one vote when the current value matches the candidate; otherwise,
           subtract one vote. A true majority cannot be completely canceled by
           all other values, so it remains as the candidate after this pass.
        4. Reset the count and scan the list again to count the candidate's
           actual occurrences.
        5. Raise ``ValueError`` when the verification does not find a majority;
           otherwise, return the candidate.

    Args:
        nums: A non-empty list of integers expected to contain a majority value.

    Returns:
        The integer that occurs more than ``len(nums) / 2`` times.

    Raises:
        ValueError: If the candidate does not pass the function's majority
            verification.

    Mutation Behavior:
        The input list is not modified.

    Time Complexity:
        O(n), where n is the length of ``nums``. The function performs two
        linear scans, and each operation inside the scans takes constant time.

    Space Complexity:
        O(1) auxiliary space because only ``size``, ``candidate``, ``count``,
        and loop variables are stored, regardless of the input size.
    """
    # Step 1: Initialize the candidate and its current vote balance.
    size: int = len(nums)
    candidate: int = nums[0]
    count: int = 0

    # Steps 2 and 3: Select candidates and cancel votes from different values.
    for index in range(size):
        if count == 0:
            candidate = nums[index]
        if candidate == nums[index]:
            count += 1
        else:
            count -= 1

    # Step 4: Reset the count and verify the remaining candidate's frequency.
    count = 0

    for num in nums:
        if num == candidate:
            count += 1

    # Step 5: Reject an invalid candidate or return the verified candidate.
    if count < (size // 2):
        raise ValueError("No majority element exists")

    return candidate


def solve() -> None:
    nums: list[int] = [7, 0, 0, 1, 7, 7, 2, 7, 7]

    expected: int = 7
    result: int | None = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 2, 1, 2]

    expected = 1
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -1, -1]

    expected = -1
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000]

    expected = -10_000
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -3, 10_000]

    expected = 10_000
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 2, 0]

    expected = 0
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 1, 1, 1, 2, 2]

    expected = 2
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 4, 4, 4]

    expected = 4
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 6, 6, 6, 6]

    expected = 6
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 10_000, -10_000, 10_000, -10_000]

    expected = -10_000
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 1, 2, 2, 3]
    original_nums: list[int] = nums.copy()

    expected = True
    majority = majority_element_optimized(nums)
    result = majority == 2 and nums == original_nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = ([-10_000] * 49_999) + ([10_000] * 50_001)

    expected = 10_000
    result = majority_element_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [7, 0, 0, 1, 7, 7, 2, 7, 7]

    expected: int = 7
    result: int = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 2, 1, 2]

    expected = 1
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -1, -1]

    expected = -1
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000]

    expected = -10_000
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -3, 10_000]

    expected = 10_000
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 2, 0]

    expected = 0
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 4, 4, 4]

    expected = 4
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 6, 6, 6, 6]

    expected = 6
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 10_000, -10_000, 10_000, -10_000]

    expected = -10_000
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000] * 100_000

    expected = 10_000
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 0, 0, 1, 7, 7, 2, 7, 7]

    expected = 7
    result = majority_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 2, 1, 2]

    expected = 1
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -1, -1]

    expected = -1
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000]

    expected = -10_000
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000, -3, 10_000]

    expected = 10_000
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 2, 0]

    expected = 0
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 4, 2, 3, 4]

    expected = 4
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 6, 6, 6, 6]

    expected = 6
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 10_000, -10_000, 10_000, -10_000]

    expected = -10_000
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = ([10_000] * 50_001) + ([-10_000] * 49_999)

    expected = 10_000
    result = majority_element_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
