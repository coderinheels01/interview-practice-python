"""Reverse Pairs.

Given an integer array ``nums``, return the number of reverse pairs in the
array.

An index pair ``(i, j)`` is called a reverse pair when:

- ``0 <= i < j < len(nums)``
- ``nums[i] > 2 * nums[j]``

Example 1:
    Input: nums = [6, 4, 1, 2, 7]
    Output: 3

    Explanation:
        The reverse pairs are:

        - (0, 2): nums[0] = 6, nums[2] = 1, and 6 > 2 * 1
        - (0, 3): nums[0] = 6, nums[3] = 2, and 6 > 2 * 2
        - (1, 2): nums[1] = 4, nums[2] = 1, and 4 > 2 * 1

Example 2:
    Input: nums = [5, 4, 4, 3, 3]
    Output: 0

    Explanation:
        No pairs satisfy both conditions.

Example 3:
    Input: nums = [6, 4, 4, 2, 2]
    Output: 2

    Explanation:
        The reverse pairs are (0, 3) and (0, 4) because 6 > 2 * 2.
        The values 4 and 2 do not form reverse pairs because 4 is equal to,
        rather than greater than, 2 * 2.

Example 4:
    Input: nums = [2, 4, 3, 5, 1]
    Output: 3

    Explanation:
        The reverse pairs are (1, 4), (2, 4), and (3, 4).

Example 5:
    Input: nums = [-5, -5]
    Output: 1

    Explanation:
        The pair (0, 1) is a reverse pair because -5 > 2 * -5.

Example 6:
    Input: nums = [7]
    Output: 0

    Explanation:
        A single element cannot form an index pair.

Constraints:
    - 1 <= len(nums) <= 5 * 10^4
    - -2^31 <= nums[i] <= 2^31 - 1

https://www.youtube.com/watch?v=0e4bZaP3MDI&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=27
"""


def count_reverse_pairs_brute_force(nums: list[int]) -> int:
    """Count reverse pairs in ``nums`` using pairwise comparison.

    A reverse pair is a pair of indices ``(i, j)`` where ``i < j`` and
    ``nums[i] > 2 * nums[j]``. Equal negative values can form reverse pairs;
    for example, ``-5 > 2 * -5``. The input list is not modified. The function
    assumes the values and list length satisfy the constraints stated in the
    problem. Python integers also prevent overflow when a value is doubled.

    Args:
        nums: The list of integers whose reverse pairs should be counted.

    Returns:
        The total number of reverse pairs in ``nums``.

    Approach:
        1. Record the input size and initialize the reverse-pair count.
        2. Visit each index as the first index of a possible reverse pair.
        3. Visit every later index as the second index of that pair.
        4. Increment the count when the first value is strictly greater than
           twice the second value.
        5. Return the count after every valid index pair has been examined.

    Time Complexity:
        O(n^2), where ``n`` is the length of ``nums``. The nested loops examine
        ``n * (n - 1) / 2`` index pairs. This does not scale well to the stated
        maximum input length of ``5 * 10^4``.

    Space Complexity:
        O(1) additional space. The function uses only the input size, count,
        and loop indices regardless of the input length.
    """
    # Step 1: Record the input size and initialize the reverse-pair count.
    size: int = len(nums)
    count: int = 0

    # Step 2: Visit each index as the first index of a possible reverse pair.
    for first_index in range(size):
        # Step 3: Compare it with every value at a later index.
        for second_index in range(first_index + 1, size):
            # Step 4: Count the pair when it satisfies the strict condition.
            if nums[first_index] > 2 * nums[second_index]:
                count += 1

    # Step 5: Return the number of reverse pairs found.
    return count


def count_reverse_pairs_optimized(nums: list[int]) -> int:
    """Count reverse pairs using a modified Merge Sort Algorithm.

    A reverse pair is a pair of indices ``(i, j)`` where ``i < j`` and
    ``nums[i] > 2 * nums[j]``. The comparison is strict, so equality does not
    qualify. This function sorts ``nums`` in ascending order as a side effect.
    It assumes the input satisfies the constraints stated in the problem,
    although an empty list also returns zero. Python integers prevent overflow
    when values are doubled and when a large pair count is accumulated.

    Args:
        nums: The list of integers whose reverse pairs should be counted.

    Returns:
        The number of reverse pairs in the original ordering of ``nums``.

    Approach:
        1. Initialize the shared reverse-pair count and the last valid index.
        2. Recursively divide each index range until it contains at most one
           element.
        3. After both halves are sorted, count cross-half reverse pairs before
           merging so their left and right ranges remain separate.
        4. Scan the sorted left half while moving one right pointer forward.
           The pointer never moves backward because successive left values are
           nondecreasing.
        5. For each left value, add the number of right-half values that satisfy
           the strict reverse-pair condition.
        6. Merge the two sorted halves into a temporary list in ascending order.
        7. Append any remaining values and copy the completed merge back into
           the corresponding range of ``nums``.
        8. Process the full range and return the accumulated count.

    Time Complexity:
        O(n log n), where ``n`` is the length of ``nums``. Merge sort has
        O(log n) levels, and the counting and merging work across each level is
        O(n).

    Space Complexity:
        O(n) additional space. The temporary merge lists require up to O(n)
        space, and the recursive call stack requires O(log n) space.
    """
    # Step 1: Initialize the count and record the final valid list index.
    count: int = 0
    size: int = len(nums) - 1

    def count_pairs(left: int, mid: int, right: int) -> None:
        nonlocal count
        right_index: int = mid + 1

        # Step 4: Scan the left half while advancing one monotonic right pointer.
        for left_index in range(left, mid + 1):
            while right_index <= right and nums[left_index] > 2 * nums[right_index]:
                right_index += 1

            # Step 5: Add every qualifying right-half value for this left value.
            count += right_index - (mid + 1)

    def merge(left: int, mid: int, right: int) -> None:
        temporary: list[int] = []
        left_index: int = left
        right_index: int = mid + 1

        # Step 6: Merge both sorted halves in ascending order.
        while left_index <= mid and right_index <= right:
            if nums[left_index] <= nums[right_index]:
                temporary.append(nums[left_index])
                left_index += 1
            else:
                temporary.append(nums[right_index])
                right_index += 1

        # Step 7: Append leftovers and copy the merged range back into nums.
        while left_index <= mid:
            temporary.append(nums[left_index])
            left_index += 1

        while right_index <= right:
            temporary.append(nums[right_index])
            right_index += 1

        nums[left : right + 1] = temporary

    def merge_sort(left: int, right: int) -> None:
        if left >= right:
            return

        # Step 2: Divide the range and recursively sort its two halves.
        mid: int = left + (right - left) // 2
        merge_sort(left=left, right=mid)
        merge_sort(left=mid + 1, right=right)

        # Step 3: Count cross-half pairs before combining the sorted halves.
        count_pairs(left=left, mid=mid, right=right)
        merge(left=left, mid=mid, right=right)

    # Step 8: Process the complete list and return its reverse-pair count.
    merge_sort(0, size)
    return count


def solve() -> None:
    # nums: list[int] = [6, 4, 1, 2, 7]
    #
    # expected: int = 3
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [7]
    #
    # expected: int = 0
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [5, 4, 4, 3, 3]
    #
    # expected: int = 0
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [6, 4, 4, 2, 2]
    #
    # expected: int = 2
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [2, 4, 3, 5, 1]
    #
    # expected: int = 3
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [-5, -5]
    #
    # expected: int = 1
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [-1, -2, -3]
    #
    # expected: int = 3
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [0, 0, 0]
    #
    # expected: int = 0
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [2**31 - 1, -(2**31)]
    #
    # expected: int = 1
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [-(2**31), 2**31 - 1]
    #
    # expected: int = 0
    # result: int = count_reverse_pairs_brute_force(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # nums: list[int] = [6, 4, 1, 2, 7]
    #
    # expected: int = 3
    # result: int = count_reverse_pairs_optimized(nums)
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    nums: list[int] = [2**31 - 1]

    expected: int = 0
    result: int = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5, 4, 4, 3, 3]

    expected = 0
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [6, 4, 4, 2, 2]

    expected = 2
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 4, 3, 5, 1]

    expected = 3
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-5, -5]

    expected = 1
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3]

    expected = 3
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0]

    expected = 0
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2**31 - 1, -(2**31)]

    expected = 1
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-(2**31), 2**31 - 1]

    expected = 0
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-(2**31)] * (5 * 10**4)

    expected = ((5 * 10**4) * (5 * 10**4 - 1)) // 2
    result = count_reverse_pairs_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
