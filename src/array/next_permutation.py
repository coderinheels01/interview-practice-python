"""31. Next Permutation

Difficulty: Medium

A permutation of an array of integers is an arrangement of its members into a
sequence or linear order.

For example, for ``arr = [1, 2, 3]``, the following are all the permutations of
``arr``:

    [1, 2, 3]
    [1, 3, 2]
    [2, 1, 3]
    [2, 3, 1]
    [3, 1, 2]
    [3, 2, 1]

The next permutation of an array of integers is its next lexicographically
greater permutation. More formally, if all permutations of the array are sorted
in a container according to lexicographical order, the next permutation is the
permutation that immediately follows the given arrangement. If no greater
arrangement is possible, rearrange the array into its lowest possible order,
which is ascending order.

For example:

- The next permutation of ``[1, 2, 3]`` is ``[1, 3, 2]``.
- The next permutation of ``[2, 3, 1]`` is ``[3, 1, 2]``.
- The next permutation of ``[3, 2, 1]`` is ``[1, 2, 3]`` because no
  lexicographically greater rearrangement exists.

Given an integer array ``nums``, find its next permutation.

The replacement must be performed in place using only constant extra memory.

Example 1:
    Input: nums = [1, 2, 3]
    Output: [1, 3, 2]

Example 2:
    Input: nums = [3, 2, 1]
    Output: [1, 2, 3]

Example 3:
    Input: nums = [1, 1, 5]
    Output: [1, 5, 1]

Constraints:
    - 1 <= nums.length <= 100
    - 0 <= nums[i] <= 100
"""


def _reverse(nums: list[int], left_index: int, right_index: int) -> None:
    while left_index < right_index:
        nums[left_index], nums[right_index] = nums[right_index], nums[left_index]
        left_index += 1
        right_index -= 1


def next_permutation(nums: list[int]) -> None:
    """Rearrange ``nums`` into its next lexicographically greater permutation.

    Approach:
        This uses the canonical Next Permutation Algorithm.

        1. Scan from right to left for the first value that is smaller than the
           value immediately after it. Its index is the pivot index.
        2. If no pivot exists, the array is in non-increasing order and is its
           greatest permutation. Reverse the entire array to obtain its lowest
           permutation.
        3. Otherwise, scan from right to left for the first value greater than
           the pivot value and swap the two. Since the suffix is non-increasing,
           this is the smallest value that can make the permutation greater.
        4. Reverse the suffix after the pivot into ascending order, producing
           the smallest permutation that is greater than the original one.

    Parameters:
        nums: A list of integers to rearrange into its next permutation.

    Returns:
        The current implementation returns the mutated ``nums`` list, although
        the function is annotated as returning ``None``.

    Mutation Behavior:
        The function rearranges ``nums`` in place and does not create a copy.

    Assumptions:
        ``nums`` contains 1 to 100 integers, each between 0 and 100 inclusive.

    Time Complexity:
        O(n), where ``n`` is the length of ``nums``. The two backward scans and
        the suffix reversal each process at most ``n`` elements.

    Space Complexity:
        O(1) additional space. Only the size, indices, and temporary references
        used during swaps are stored.
    """
    # Step 1: Find the rightmost pivot whose value is smaller than its neighbor.
    size: int = len(nums)
    pivot_index: int = -1

    for index in range(size - 2, -1, -1):
        if nums[index] < nums[index + 1]:
            pivot_index = index
            break

    # Step 2: Wrap the greatest permutation around to the lowest permutation.
    if pivot_index == -1:
        return _reverse(nums=nums, left_index=0, right_index=size - 1)

    # Step 3: Swap the pivot with the smallest greater value in the suffix.
    for index in range(size - 1, pivot_index, -1):
        if nums[index] > nums[pivot_index]:
            nums[index], nums[pivot_index] = nums[pivot_index], nums[index]
            break

    # Step 4: Put the suffix in ascending order.
    _reverse(nums=nums, left_index=pivot_index + 1, right_index=size - 1)

    return nums


def solve() -> None:
    # Example 1: the pivot is near the end.
    nums: list[int] = [1, 2, 3]
    expected: list[int] = [1, 3, 2]
    next_permutation(nums)
    result: list[int] = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: the greatest permutation wraps to the smallest permutation.
    nums = [3, 2, 1]
    expected = [1, 2, 3]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 3: duplicate values are handled correctly.
    nums = [1, 1, 5]
    expected = [1, 5, 1]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length.
    nums = [0]
    expected = [0]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum and maximum allowed values.
    nums = [0, 100]
    expected = [100, 0]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All values are identical, so the permutation does not change.
    nums = [100, 100, 100]
    expected = [100, 100, 100]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The pivot is at the beginning and the suffix must be reordered.
    nums = [1, 3, 2]
    expected = [2, 1, 3]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The pivot is in the middle of the array.
    nums = [2, 1, 4, 3]
    expected = [2, 3, 1, 4]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicates appear on both sides of the pivot.
    nums = [1, 5, 1]
    expected = [5, 1, 1]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length in increasing order.
    nums = list(range(100))
    expected = list(range(98)) + [99, 98]
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length in decreasing order exercises full wraparound.
    nums = list(range(99, -1, -1))
    expected = list(range(100))
    next_permutation(nums)
    result = nums
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
