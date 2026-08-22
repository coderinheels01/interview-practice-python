"""Count Subarrays with Given Sum

Given an array of integers ``nums`` and an integer ``k``, return the total
number of subarrays whose sum equals ``k``.

A subarray is a contiguous, non-empty sequence of elements within an array.

Example 1:
    Input: nums = [1, 1, 1], k = 2
    Output: 2

    Explanation: There are two subarrays that sum to 2: the first two
    elements, [1, 1], and the last two elements, [1, 1].

Example 2:
    Input: nums = [1, 2, 3], k = 3
    Output: 2

    Explanation: The two subarrays that sum to 3 are [1, 2] and [3].

Example 3:
    Input: nums = [3, 1, 2, 4], k = 6
    Output: 2

    Explanation: The two subarrays that sum to 6 are [3, 1, 2] and [2, 4].

Example 4:
    Input: nums = [1, -1, 0], k = 0
    Output: 3

    Explanation: The three subarrays that sum to 0 are [1, -1], [0], and
    [1, -1, 0].

Example 5:
    Input: nums = [2, 4, 6], k = 5
    Output: 0

    Explanation: No contiguous subarray has a sum equal to 5.

Example 6:
    Input: nums = [0, 0, 0], k = 0
    Output: 6

    Explanation: Every possible subarray has a sum of 0. There are three
    subarrays of length 1, two of length 2, and one of length 3.

Constraints:
    - 1 <= nums.length <= 10^5
    - -1000 <= nums[i] <= 1000
    - -10^7 <= k <= 10^7

https://www.youtube.com/watch?v=xvNwoz-ufXA&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=17
"""

from collections import defaultdict


def count_subarrays_with_given_sum_brute_force(nums: list[int], k: int) -> int:
    """Return the number of contiguous subarrays whose sum equals ``k``.

    Approach:
        Use brute-force enumeration to generate every possible non-empty
        contiguous subarray.

        1. Store the array size and initialize the matching-subarray count to
           zero.
        2. Choose every possible starting index with ``outer_index``.
        3. For each starting index, choose every possible ending index with
           ``inner_index``. It starts at ``outer_index`` so the ending index
           never appears before the starting index.
        4. Calculate the sum of the selected subarray by visiting every index
           from ``outer_index`` through ``inner_index``. Because the stopping
           value of Python's ``range`` is excluded, use ``inner_index + 1`` to
           include the ending element. For example, a one-element subarray at
           index 0 uses ``range(0, 1)``, which produces index 0.
        5. Increment the count when the completed subarray sum equals ``k``.
        6. Return the total number of matching subarrays.

    Parameters:
        nums: The integer array whose contiguous subarrays are examined.
        k: The target sum each counted subarray must equal.

    Returns:
        The number of non-empty contiguous subarrays with a sum equal to ``k``.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n^3), where ``n`` is the length of ``nums``. The first two loops
        choose O(n^2) start-and-end pairs, and the third loop may visit O(n)
        elements to calculate each subarray sum. This will be too slow for the
        maximum constraint of 10^5 elements.

    Space Complexity:
        O(1) additional space. The function uses only integer variables and
        does not create a separate list for any subarray.

    Assumptions:
        The problem guarantees at least one element, although this function
        would return 0 for an empty input list.
    """

    # 1. Store the input size and initialize the match count.
    size: int = len(nums)
    count: int = 0

    # 2. Choose each possible starting index.
    for outer_index in range(size):
        # 3. Choose each possible ending index at or after the start.
        for inner_index in range(outer_index, size):
            sub_array_sum: int = 0

            # 4. Sum every value from the start through the inclusive end.
            for sub_array_index in range(outer_index, inner_index + 1):
                sub_array_sum += nums[sub_array_index]

            # 5. Count the completed subarray when its sum matches k.
            if sub_array_sum == k:
                count += 1

    # 6. Return the total number of matching subarrays.
    return count


def count_subarrays_with_given_sum_time_optimized(nums: list[int], k: int) -> int:
    """Return the number of contiguous subarrays whose sum equals ``k``.

    Approach:
        Enumerate every possible starting index while maintaining an
        incremental running sum for each possible ending index. This improves
        on the three-loop brute-force approach by reusing the previous sum
        instead of recalculating each subarray from the beginning.

        1. Store the input size and initialize the number of matches to zero.
        2. Choose each possible subarray starting index with ``outer_index``.
        3. Reset ``sub_array_sum`` to zero for the new starting index.
        4. Move ``inner_index`` from the starting index to the end of the list.
           Add each new value to ``sub_array_sum``. At each position, the
           running sum represents the contiguous subarray from
           ``outer_index`` through ``inner_index``.
        5. Increment the count whenever the current running sum equals ``k``.
           The traversal must continue even after a match because negative
           numbers and zeroes may produce additional matches with the same
           starting index.
        6. Return the total number of matching subarrays.

    Parameters:
        nums: The integer array whose contiguous subarrays are examined.
        k: The target sum each counted subarray must equal.

    Returns:
        The number of non-empty contiguous subarrays whose sum equals ``k``.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n^2), where ``n`` is the length of ``nums``. The nested loops examine
        every possible start-and-end pair once, and each pair requires only an
        O(1) addition and comparison. This is faster than the O(n^3)
        brute-force implementation, but it is still too slow for the maximum
        constraint of 10^5 elements.

    Space Complexity:
        O(1) additional space. Only the size, count, running sum, and loop
        indices are stored; no subarray or other input-sized structure is
        created.

    Assumptions:
        The problem guarantees that ``nums`` contains at least one element.
        Negative numbers and zeroes are allowed.
    """
    # 1. Store the input size and initialize the match count.
    size: int = len(nums)
    count: int = 0

    # 2. Choose each possible starting index.
    for outer_index in range(size):
        # 3. Reset the running sum for this new starting index.
        sub_array_sum: int = 0

        # 4. Extend the subarray one ending index at a time.
        for inner_index in range(outer_index, size):
            sub_array_sum += nums[inner_index]

            # 5. Count every running sum that equals the target.
            if sub_array_sum == k:
                count += 1

    # 6. Return the total number of matching subarrays.
    return count


def count_subarrays_with_given_sum_prefix_sum_optimized(nums: list[int], k: int) -> int:
    """Return the number of contiguous subarrays whose sum equals ``k``.

    Approach:
        Use a prefix sum with a frequency map. A prefix sum is the total of all
        values visited from the beginning of the array through the current
        position.

        If ``current_sum`` is the prefix sum at the current position and an
        earlier prefix sum is ``previous_sum``, then the sum of the elements
        between those two positions is:

            current_sum - previous_sum

        To make that subarray sum equal ``k``:

            current_sum - previous_sum = k
            previous_sum = current_sum - k

        Therefore, for every current prefix sum, look up how many times
        ``current_sum - k`` has previously appeared.

        1. Create a frequency map for previously seen prefix sums and initialize
           the result count to zero.
        2. Record prefix sum ``0`` once before traversing the array. This
           represents the empty prefix before index 0 and allows a subarray
           beginning at index 0 to be counted when its sum equals ``k``.
        3. Initialize ``current_sum`` to zero.
        4. Traverse ``nums`` and add each number to ``current_sum``.
        5. Calculate the required earlier prefix sum as ``current_sum - k``.
        6. If that required sum has appeared, add its frequency to ``count``.
           Every occurrence represents a different starting position for a
           valid subarray ending at the current position.
        7. Record the current prefix sum after counting matches. Recording it
           afterward prevents the current position from being treated as an
           earlier prefix, which would incorrectly count an empty subarray when
           ``k`` is zero.
        8. Return the total number of matching subarrays.

    Parameters:
        nums: The integer array whose contiguous subarrays are examined.
        k: The target sum each counted subarray must equal.

    Returns:
        The number of non-empty contiguous subarrays whose sum equals ``k``.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n) expected time, where ``n`` is the length of ``nums``. The function
        visits every number once, and dictionary lookup and update operations
        take O(1) expected time.

    Space Complexity:
        O(n) additional space. In the worst case, the frequency map stores a
        different prefix sum for every position in the array.

    Assumptions:
        The problem guarantees at least one element. Negative numbers, zeroes,
        and duplicate prefix sums are supported, and Python integers safely
        handle sums beyond fixed-width integer limits.
    """
    # 1. Create the prefix-sum frequency map and initialize the match count.
    previous_sums: defaultdict[int, int] = defaultdict(int)
    count: int = 0

    # 2. Record the empty prefix so subarrays starting at index 0 can match.
    previous_sums[0] = 1

    # 3. Initialize the running prefix sum.
    current_sum: int = 0

    # 4. Add each number to the running prefix sum.
    for num in nums:
        current_sum += num

        # 5. Find the earlier prefix sum needed to create a sum of k.
        prev: int = current_sum - k

        # 6. Count every earlier occurrence of that required prefix sum.
        if prev in previous_sums:
            count += previous_sums[prev]

        # 7. Record this prefix sum for subarrays ending at later positions.
        previous_sums[current_sum] += 1

    # 8. Return the total number of matching subarrays.
    return count


def solve() -> None:
    # nums: list[int] = [1, 1, 1]
    # k: int = 2
    # expected: int = 2
    # result: int = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1, 2, 3]
    # k = 3
    # expected = 2
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [3, 1, 2, 4]
    # k = 6
    # expected = 2
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [2, 4, 6]
    # k = 5
    # expected = 0
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1, -1, 0]
    # k = 0
    # expected = 3
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [0, 0, 0]
    # k = 0
    # expected = 6
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000]
    # k = 1000
    # expected = 1
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [-1000]
    # k = -1000
    # expected = 1
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000, -1000]
    # k = 10_000_000
    # expected = 0
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000, -1000]
    # k = -10_000_000
    # expected = 0
    # result = count_subarrays_with_given_sum_brute_force(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1, 1, 1]
    # k = 2
    # expected = 2
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1, 2, 3]
    # k = 3
    # expected = 2
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [3, 1, 2, 4]
    # k = 6
    # expected = 2
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1, -1, 0]
    # k = 0
    # expected = 3
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [0, 0, 0]
    # k = 0
    # expected = 6
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [2, 4, 6]
    # k = 5
    # expected = 0
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000]
    # k = 1000
    # expected = 1
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [-1000]
    # k = -1000
    # expected = 1
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000, -1000]
    # k = 10_000_000
    # expected = 0
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums = [1000, -1000]
    # k = -10_000_000
    # expected = 0
    # result = count_subarrays_with_given_sum_time_optimized(nums, k)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    nums = [1, 1, 1]
    k = 2
    expected = 2
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 3

    expected = 2
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 1, 2, 4]
    k = 6
    expected = 2
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1, 0]
    k = 0
    expected = 3
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0]
    k = 0
    expected = 6
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 4, 6]
    k = 5
    expected = 0
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1000]
    k = 1000
    expected = 1
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1000]
    k = -1000
    expected = 1
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1000, -1000]
    k = 10_000_000
    expected = 0
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1000, -1000]
    k = -10_000_000
    expected = 0
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1000] * 100_000
    k = 10_000_000
    expected = 90_001
    result = count_subarrays_with_given_sum_prefix_sum_optimized(nums, k)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
