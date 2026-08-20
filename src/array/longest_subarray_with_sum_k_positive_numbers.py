"""Longest Subarray with Sum K for Positive Numbers

Given an integer array ``nums`` of size ``n`` containing only positive numbers
and a positive integer ``k``, return the length of the longest contiguous
subarray whose elements sum to ``k``. If no such subarray exists, return 0.

Example 1:
    Input: nums = [10, 5, 2, 7, 1, 9], k = 15
    Output: 4
    Explanation: The longest subarray with a sum equal to 15 is [5, 2, 7, 1].
    It starts at index 1, ends at index 4, and has a length of 4.

Example 2:
    Input: nums = [3, 2, 1], k = 10
    Output: 0
    Explanation: No contiguous subarray sums to 10, so 0 is returned.

Now your turn:
    Input: nums = [1, 1, 1], k = 2
    Possible answers: 0, 1, 2, 3

Constraints:
    - 1 <= n <= 10^5
    - 1 <= nums[i] <= 10^5
    - 1 <= k <= 10^9

Reference:
    https://www.youtube.com/watch?v=frf7qxiN2qU&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=4
"""


def longest_subarray_with_sum_k_positive_numbers(nums: list[int], k: int) -> int:
    """Return the longest contiguous subarray length whose sum equals ``k``.

    Approach: Sliding Window
        1. Initialize left and right pointers at the beginning of the array,
           along with a running window sum and the maximum matching length.
        2. Move the right pointer across the array and add its value to expand
           the current window.
        3. While the window sum is greater than ``k``, remove the value at the
           left pointer and move that pointer forward. Because every value is
           positive, shrinking the window is the only way to reduce its sum.
        4. When the resulting window sum equals ``k``, calculate its inclusive
           length and update the maximum length.
        5. Advance the right pointer and repeat until every value is processed.
        6. Return the maximum matching length, which remains 0 if no contiguous
           subarray sums to ``k``.

    Time Complexity:
        O(n), where n is the length of ``nums``. The right pointer visits each
        element once, and the left pointer also moves forward at most n times.
        Although the loops are nested, neither pointer ever moves backward.

    Space Complexity:
        O(1) auxiliary space. The algorithm stores only the array length, two
        pointers, the running sum, and length-tracking integer variables.
    """
    # Step 1: Initialize both pointers and the window-tracking variables.
    n: int = len(nums)
    left: int = 0
    right: int = 0
    current_sum: int = 0
    max_len: int = 0

    # Step 2: Traverse the array by expanding the window to the right.
    while right < n:
        current_sum += nums[right]

        # Step 3: Shrink from the left until the sum is no greater than k.
        while current_sum > k:
            current_sum -= nums[left]
            left += 1

        # Step 4: Record the current window when its sum matches k.
        if current_sum == k:
            current_len: int = (right - left) + 1
            max_len = max(max_len, current_len)

        # Step 5: Advance the right pointer to process the next value.
        right += 1

    # Step 6: Return 0 when no match exists, otherwise the longest length.
    return max_len


def solve() -> None:
    nums: list[int] = [10, 5, 2, 7, 1, 9]
    k: int = 15

    expected: int = 4
    result: int = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 1

    expected = 1
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000] * 10_000
    k = 1_000_000_000

    expected = 10_000
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1] * 100_000
    k = 100_000

    expected = 100_000
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, 4]
    k = 1

    expected = 0
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 5, 3]
    k = 5

    expected = 1
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 4]
    k = 3

    expected = 2
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 2, 3]
    k = 5

    expected = 2
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 4, 1, 1, 1]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 2, 1]
    k = 10

    expected = 0
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1]
    k = 2

    expected = 2
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 1]
    k = 3

    expected = 3
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 6

    expected = 3
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 5

    expected = 2
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 5

    expected = 1
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]
    k = 3

    expected = 0
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [100_000, 100_000]
    k = 200_000

    expected = 2
    result = longest_subarray_with_sum_k_positive_numbers(nums, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
