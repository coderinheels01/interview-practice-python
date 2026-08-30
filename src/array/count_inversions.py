"""Count Inversions.

Given an integer array ``nums``, return the number of inversions in the array.

Two elements ``nums[i]`` and ``nums[j]`` form an inversion when:

- ``nums[i] > nums[j]``
- ``i < j``

The inversion count indicates how close an array is to being sorted:

- An array sorted in ascending order has 0 inversions.
- An array sorted in descending order has the maximum number of inversions.

Example 1:
    Input: nums = [2, 3, 7, 1, 3, 5]
    Output: 5

    Explanation:
        The inversion pairs are:

        - Indices (0, 3): 2 > 1
        - Indices (1, 3): 3 > 1
        - Indices (2, 3): 7 > 1
        - Indices (2, 4): 7 > 3
        - Indices (2, 5): 7 > 5

Example 2:
    Input: nums = [-10, -5, 6, 11, 15, 17]
    Output: 0

    Explanation:
        The array is already sorted in ascending order, so it has no
        inversions.

Example 3:
    Input: nums = [4, 3, 2, 1]
    Output: 6

    Explanation:
        Every pair is an inversion because the array is sorted in descending
        order: (4, 3), (4, 2), (4, 1), (3, 2), (3, 1), and (2, 1).

Example 4:
    Input: nums = [2, 2, 1]
    Output: 2

    Explanation:
        Each 2 forms an inversion with 1. Equal values do not form an inversion
        because the first value must be strictly greater than the second.

Example 5:
    Input: nums = [-1, -3, -2]
    Output: 2

    Explanation:
        The inversion pairs are (-1, -3) and (-1, -2).

Example 6:
    Input: nums = [5]
    Output: 0

    Explanation:
        A single element cannot form a pair, so there are no inversions.

Constraints:
    - 1 <= len(nums) <= 10^5
    - -10^5 <= nums[i] <= 10^5

    https://www.youtube.com/watch?v=AseUmwVNaoY&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=26
"""


def count_inversions_brute_force(nums: list[int]) -> int:
    """Count the inversions in ``nums`` using pairwise comparison.

    An inversion is a pair of indices ``(i, j)`` where ``i < j`` and
    ``nums[i] > nums[j]``. Equal values do not form an inversion. The input
    list is not modified. The function assumes the values and list length
    satisfy the constraints stated in the problem.

    Args:
        nums: The list of integers whose inversions should be counted.

    Returns:
        The total number of inversions in ``nums``.

    Approach:
        1. Record the input size and initialize the inversion count to zero.
        2. Visit every element as the first value in a possible inversion.
        3. Compare it with every value positioned after it in the list.
        4. Increment the count when the first value is strictly greater than
           the second value.
        5. Return the total inversion count after examining every pair.

    Time Complexity:
        O(n^2), where ``n`` is the length of ``nums``. The nested loops examine
        ``n * (n - 1) / 2`` pairs. Consequently, this brute-force solution is
        not practical for the stated maximum input size of ``10^5``.

    Space Complexity:
        O(1) additional space. The function uses only ``size``, ``count``, and
        the two loop indices, regardless of the input size.
    """
    # Step 1: Record the input size and initialize the inversion count.
    size: int = len(nums)
    count: int = 0

    # Step 2: Visit each element as the first value in a possible inversion.
    for first_index in range(size):
        # Step 3: Compare it with every value that appears after it.
        for second_index in range(first_index + 1, size):
            # Step 4: Count the pair when the earlier value is greater.
            if nums[first_index] > nums[second_index]:
                count += 1

    # Step 5: Return the number of inversions found across all pairs.
    return count


def count_inversions_optimized(nums: list[int]) -> int:
    """Count inversions using the Merge Sort Inversion Counting Algorithm.

    An inversion is a pair of indices ``(i, j)`` for which ``i < j`` and
    ``nums[i] > nums[j]``. Equal values are not inversions. This function sorts
    ``nums`` in ascending order as a side effect while counting its inversions.
    It assumes the input satisfies the constraints stated in the problem.

    Args:
        nums: The list of integers whose inversions should be counted.

    Returns:
        The number of inversions in the original order of ``nums``.

    Approach:
        1. Initialize a shared inversion counter.
        2. Recursively divide the current index range into left and right
           halves until each range contains at most one element.
        3. Merge the two sorted halves by comparing their current elements.
        4. When a right-half element is smaller, count an inversion with every
           unmerged element in the left half.
        5. Append any remaining elements and copy the merged values back into
           the corresponding range of ``nums``.
        6. Sort the full index range and return the accumulated count.

    Time Complexity:
        O(n log n), where ``n`` is the length of ``nums``. Merge sort has
        O(log n) recursive levels, and merging processes O(n) elements across
        each level.

    Space Complexity:
        O(n) additional space. The temporary merge lists use O(n) space at
        their largest combined active size, and the recursion stack uses
        O(log n) space.
    """
    # Step 1: Initialize the inversion counter shared by all recursive calls.
    count: int = 0

    def merge(left: int, mid: int, right: int) -> None:
        nonlocal count
        temporary: list[int] = []
        left_index: int = left
        right_index: int = mid + 1

        # Step 3: Merge the sorted halves by comparing their current values.
        while left_index <= mid and right_index <= right:
            if nums[left_index] <= nums[right_index]:
                temporary.append(nums[left_index])
                left_index += 1
            else:
                temporary.append(nums[right_index])
                # Step 4: Count all remaining left values as inversions.
                # Because both halves are sorted, nums[right_index] is smaller
                # than every remaining value from left_index through mid. Each
                # of those values forms an inversion with nums[right_index].
                count += mid - left_index + 1
                right_index += 1

        # Step 5: Append leftovers and copy the merged range back into nums.
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

        # Step 2: Divide the range and recursively sort both halves.
        mid: int = left + (right - left) // 2

        merge_sort(left, mid)
        merge_sort(mid + 1, right)
        merge(left, mid, right)

    # Step 6: Process the complete list and return its inversion count.
    merge_sort(0, len(nums) - 1)

    return count


def solve() -> None:
    nums: list[int] = [2, 3, 7, 1, 3, 5]

    expected: int = 5
    result: int = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = 0
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = 0
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 3, 2, 1]

    expected = 6
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 1]

    expected = 2
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2]

    expected = 0
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -3, -2]

    expected = 2
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, -1, 1, 0]

    expected = 2
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10**5, -(10**5)]

    expected = 1
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 1, 2, 0, 4]

    expected = 5
    result = count_inversions_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, 7, 1, 3, 5]

    expected = 5
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [5]

    expected: int = 0
    result: int = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-(10**5), 0, 10**5]

    expected = 0
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 3, 2, 1]

    expected = 6
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 1]

    expected = 2
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2]

    expected = 0
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -3, -2, 0]

    expected = 2
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 3, 7, 1, 3, 5]

    expected = 5
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = list(range(10**5, 0, -1))

    expected = (10**5 * (10**5 - 1)) // 2
    result = count_inversions_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
