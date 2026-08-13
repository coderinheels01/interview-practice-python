"""53. Maximum Subarray

Given an integer array ``nums``, find the subarray with the largest sum, and
return its sum.

Example 1:
    Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6
    Explanation: The subarray [4, -1, 2, 1] has the largest sum 6.

Example 2:
    Input: nums = [1]
    Output: 1
    Explanation: The subarray [1] has the largest sum 1.

Example 3:
    Input: nums = [5, 4, -1, 7, 8]
    Output: 23
    Explanation: The subarray [5, 4, -1, 7, 8] has the largest sum 23.

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4

Follow up:
    If you have figured out the O(n) solution, try coding another solution
    using the divide and conquer approach, which is more subtle.
"""


def max_subarray(nums: list[int]) -> int:
    """Return the largest sum among all contiguous subarrays in ``nums``.

    Approach:
        1. If ``nums`` contains one number, return that number because it is
           the only possible non-empty subarray.
        2. Initialize the maximum sum with the first number, an index for
           traversing the array, and a running sum of 0.
        3. Visit each number and add it to the running sum. This represents
           the sum of the current candidate subarray.
        4. Compare the running sum with the maximum sum found so far and keep
           the larger value.
        5. If the running sum is negative, reset it to 0. A negative prefix
           would only decrease the sum of any subarray that continues after
           it, so the next number should start a new candidate subarray.
        6. Advance the index and repeat until every number has been processed.
        7. Return the maximum subarray sum found.

    Time Complexity:
        O(n), where n is the length of ``nums``. The while loop visits each
        number exactly once, and every operation inside the loop takes O(1)
        time. This satisfies the prompt's O(n) target.

    Space Complexity:
        O(1). The algorithm uses only ``max_sum``, ``right``, ``n``, and
        ``current_sum``, whose memory usage does not grow with the input size.
    """
    # 1. Return the only possible subarray sum for a single-element input.
    if len(nums) == 1:
        return nums[0]

    # 2. Initialize the maximum, traversal index, input size, and running sum.
    max_sum: int = nums[0]
    right: int = 0
    n: int = len(nums)
    current_sum: int = 0

    # 3. Visit every number and add it to the current candidate subarray.
    while right < n:
        current_sum += nums[right]

        # 4. Record the largest subarray sum seen so far.
        max_sum = max(max_sum, current_sum)

        # 5. Discard a negative running sum before considering the next number.
        if current_sum < 0:
            current_sum = 0

        # 6. Advance to the next number.
        right += 1


    # 7. Return the largest sum found.
    return max_sum


def solve() -> None:
    nums: list[int] = [2, -1, 3, -4, 5]

    expected: int = 5
    result: int = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, -2, -7, -1, -5]

    expected = -1
    result = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, -8, 6, 7, -2, 3]

    expected = 14
    result = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, -1, -1, -1, 4]

    expected = 4
    result = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 4, -1, 2, -6, 3, 5]

    expected = 8
    result = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [8, -10, 2, 3, 4, -1]

    expected = 9
    result = max_subarray(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")



if __name__ == "__main__":
    solve()
