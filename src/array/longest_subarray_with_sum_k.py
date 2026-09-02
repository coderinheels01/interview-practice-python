"""Longest Subarray with Sum K

Given an integer array ``nums`` of size ``n`` and an integer ``k``, return the
length of the longest contiguous subarray whose elements sum to ``k``. If no
such subarray exists, return 0.

Example 1:
    Input: nums = [10, 5, 2, 7, 1, 9], k = 15
    Output: 4
    Explanation: The longest subarray with a sum equal to 15 is [5, 2, 7, 1].
    It starts at index 1, ends at index 4, and has a length of 4.

Example 2:
    Input: nums = [-3, 2, 1], k = 6
    Output: 0
    Explanation: No subarray sums to 6, so 0 is returned.

Now your turn:
    Input: nums = [-1, 1, 1], k = 1
    Possible answers: 2, 4, 3, 1

Constraints:
    - 1 <= n <= 10^5
    - -10^5 <= nums[i] <= 10^5
    - -10^9 <= k <= 10^9

    https://www.youtube.com/watch?v=frf7qxiN2qU&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=4
"""


def longest_subarray_with_sum_k_brute_force(nums: list[int], k: int) -> int:
    """Return the longest subarray length by examining every start and end.

    Approach:
        1. Store the array length and initialize the maximum matching length.
        2. Treat every index as the possible start of a contiguous subarray and
           reset the running sum for that new starting position.
        3. Move the ending index from the starting position through the rest of
           the array, adding each value to the running sum. Reusing the running
           sum avoids recalculating each subarray's sum from scratch.
        4. Whenever the running sum equals ``k``, calculate the current subarray
           length and update the maximum length if the current one is longer.
        5. Return the maximum length found, which remains 0 when no subarray
           sums to ``k``.

    Time Complexity:
        O(n^2), where n is the length of ``nums``. Each of the n starting
        positions considers every possible ending position at or after it.

    Space Complexity:
        O(1) auxiliary space because only the length, indexes, running sum,
        current length, and maximum length are stored.
    """
    # Step 1: Store the array length and initialize the maximum length.
    n: int = len(nums)

    max_len: int = 0
    current_sum: int
    current_len: int

    # Step 2: Treat every index as a possible subarray starting position.
    for i in range(n):
        current_sum = 0

        # Step 3: Extend the subarray and maintain its running sum.
        for j in range(i, n):
            current_sum += nums[j]

            # Step 4: Update the maximum when the current subarray sums to k.
            if current_sum == k:
                current_len = (j - i) + 1
                max_len = max(max_len, current_len)

    # Step 5: Return 0 when no match exists, otherwise the longest match.
    return max_len


def longest_subarray_with_sum_k_optimized(nums: list[int], k: int) -> int:
    """Return the longest subarray length using prefix sums and a dictionary.

    Approach: Prefix Sum with Hash Map
        1. Initialize a running prefix sum, the maximum matching length, and a
           dictionary that maps each prefix sum to its earliest index.
        2. Traverse the array once, adding each number to the running prefix
           sum, which represents the sum from index 0 through the current index.
        3. If the running prefix sum equals ``k``, update the maximum length
           using the entire prefix from index 0 through the current index.
        4. Otherwise, look for ``current_sum - k`` in the dictionary. If it was
           seen previously, the elements after that index through the current
           index sum to ``k``; calculate their length and update the maximum.
        5. Store the current prefix sum only whexn it has not appeared before.
           Preserving its earliest index allows future matches to be as long as
           possible.
        6. Return the maximum matching length, which remains 0 when no subarray
           sums to ``k``.

    Time Complexity:
        O(n) average time, where n is the length of ``nums``. The array is
        traversed once, and each dictionary lookup and insertion takes O(1)
        average time.

    Space Complexity:
        O(n) additional space because the dictionary may store one entry for
        each distinct prefix sum. The remaining numeric variables use O(1)
        space.
    """
    # Step 1: Initialize the length, prefix-sum map, and tracking variables.
    n: int = len(nums)

    prefix_sum: dict[int, int] = {}  # sum is key and value is index
    current_sum: int = 0
    max_len: int = 0
    current_len: int
    previous_sum_index: int

    # Step 2: Traverse the array while maintaining its running prefix sum.
    for index in range(n):
        current_sum += nums[index]

        # Step 3: Handle a matching subarray that begins at index 0.
        if current_sum == k:
            max_len = max(max_len, index + 1)
        # Step 4: Use an earlier prefix sum to find a matching subarray.
        elif (current_sum - k) in prefix_sum:
            previous_sum_index = prefix_sum[current_sum - k]
            current_len = index - previous_sum_index
            max_len = max(max_len, current_len)

        # Step 5: Preserve the earliest index for each distinct prefix sum.
        if current_sum not in prefix_sum:
            prefix_sum[current_sum] = index

    # Step 6: Return 0 when no match exists, otherwise the longest length.
    return max_len


def solve() -> None:
    """
    nums: list[int] = [10, 5, 2, 7, 1, 9]
    k: int = 15

    expected: int = 4
    result: int = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, 2, 1]
    k = 6

    expected = 0
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 1, 1]
    k = 1

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 6

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 5

    expected = 1
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 3

    expected = 0
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, -1, 2, 1]
    k = 0

    expected = 4
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0]
    k = 0

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """
    nums = [2, 0, 0, 3]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """
    nums = [1, 2, 1, 1, 1]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000, -100_000, 100_000]
    k = 100_000

    expected = 3
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000, -100_000]
    k = 1_000_000_000

    expected = 0
    result = longest_subarray_with_sum_k_brute_force(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, 5, 2, 7, 1, 9]
    k = 15

    expected = 4
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, 5, 2, 7, 1, 9]
    k = 24

    expected = 5
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 6

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 5

    expected = 1
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 3

    expected = 0
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0]
    k = 0

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """
    nums = [2, 0, 0, 3]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """
    nums = [1, 1, 1, 1, 1]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 1, 1]
    k = 1

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, -1, 2, 1]
    k = 0

    expected = 4
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000, -100_000, 100_000]
    k = 100_000

    expected = 3
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000, -100_000]
    k = 1_000_000_000

    expected = 0
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1] * 100_000
    k = 100_000

    expected = 100_000
    result = longest_subarray_with_sum_k_optimized(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    """


if __name__ == "__main__":
    solve()
