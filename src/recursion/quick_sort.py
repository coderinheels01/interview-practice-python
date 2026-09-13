"""Quick Sort

Given an integer array nums, sort its elements in nondecreasing order using
recursive quick sort. Preserve all duplicate values.

Modify nums in place and return the same list. Do not use sorted() or
list.sort(). Use in-place partitioning rather than additional sublists.
Aim for O(n log n) average time; quick sort can take O(n**2) in the worst
case. Recursion stack space depends on how balanced the partitions are.

Example 1:
    Input: nums = [5, 2, 3, 1]
    Output: [1, 2, 3, 5]

Example 2:
    Input: nums = [5, 1, 1, 2, 0, 0]
    Output: [0, 0, 1, 1, 2, 5]

Example 3:
    Input: nums = []
    Output: []

Practice constraints:
    - 0 <= len(nums) <= 500
    - -100_000 <= nums[i] <= 100_000
    - Negative values, zeros, and duplicate values are allowed.
"""

import random


def quick_sort(nums: list[int]) -> list[int]:
    """Sort nums in place using randomized quick sort and return the same list.

    Args:
        nums: Integer list under the module's practice constraints. Empty
            lists, negative values, zeros, and duplicates are supported.

    Returns:
        The original list, modified into nondecreasing order. Duplicate values
        are preserved. No additional sublists are created. This sort is not
        stable: swaps can change the relative order of equal-valued elements.

    Approach:
        Randomized Quick Sort (divide and conquer) with two-pointer partitioning.
        1. Return immediately for an empty or single-element list. Otherwise,
           begin sorting the inclusive range from 0 through len(nums) - 1.
        2. For each range containing at least two elements, choose a random
           pivot index between low_index and high_index, inclusive. Swap that
           element into low_index, then read the pivot from its new location.
           The original pivot_index is no longer its location after the swap.
        3. Scan left_index forward past values <= pivot and right_index
           backward past values > pivot, staying within the current range.
           If the pointers have not crossed, swap the misplaced values and
           continue scanning. The pivot stays at low_index during this scan:
           the left pointer advances past it before any scanning swap.
        4. When the pointers meet or cross, swap the pivot at low_index with
           nums[right_index]. Return right_index as its final sorted index.
           Values to its left are <= pivot; values to its right are > pivot.
           The two sides are partitioned but may still be internally unsorted.
        5. Recursively sort the ranges before and after that final pivot index.
           Exclude the pivot itself, and stop on empty or single-element ranges.
        6. Return nums after all recursive calls finish. Random choices can
           change the intermediate partitions, but not the sorted result.

        Pivot example:
            With [5, 2, 3, 1], choosing index 1 selects pivot 2. Moving it to
            low_index gives [2, 5, 3, 1]. Scanning swaps 5 and 1 to produce
            [2, 1, 3, 5]. The final pivot swap gives [1, 2, 3, 5], and the
            partition returns index 1. Recursion then sorts the two sides.

    Examples:
        >>> quick_sort([5, 2, 3, 1])
        [1, 2, 3, 5]
        >>> quick_sort([5, 1, 1, 2, 0, 0])
        [0, 0, 1, 1, 2, 5]
        >>> quick_sort([])
        []
        >>> values = [2, -1, 0]
        >>> quick_sort(values) is values
        True
        >>> values
        [-1, 0, 2]

    Time Complexity:
        Partitioning a range of m elements takes O(m): the two pointers move
        monotonically across the range. For distinct values, random pivots give
        expected O(n log n) total time, where n = len(nums), even if the input
        is initially sorted. Worst-case time remains O(n**2) when partitions
        repeatedly have sizes 0 and n - 1. This implementation also takes
        O(n**2) on all-equal inputs regardless of random pivot choices, because
        equal values all go to the left. The expected O(n log n) guarantee
        therefore does not apply to all duplicate-heavy inputs allowed here.

    Space Complexity:
        Each partition uses O(1) extra space for indices and the pivot value.
        The recursion stack uses O(log n) space for balanced partitions and
        in expectation with random pivots on distinct values, but O(n) in the
        worst case, including all-equal inputs. Sorting in place avoids extra
        arrays; it does not eliminate the recursion stack.
    """
    # Step 1: Handle inputs that are already trivially sorted.
    size: int = len(nums)

    if size <= 1:
        return nums

    def partition(low_index: int, high_index: int):
        left_index: int = low_index
        right_index: int = high_index
        # Step 2: Choose a random pivot and move it to the protected first slot.
        pivot_index: int = random.randint(low_index, high_index)
        nums[pivot_index], nums[low_index] = (
            nums[low_index],
            nums[pivot_index],
        )
        # Read the pivot at its new location, not its original random index.
        pivot: int = nums[low_index]
        # Step 3: Scan inward and swap values that belong on opposite sides.
        while left_index < right_index:
            while left_index < high_index and nums[left_index] <= pivot:
                left_index += 1

            while right_index > low_index and nums[right_index] > pivot:
                right_index -= 1

            if left_index < right_index:
                nums[left_index], nums[right_index] = (
                    nums[right_index],
                    nums[left_index],
                )

        # Step 4: Put the pivot in its final position and return that index.
        nums[low_index], nums[right_index] = (
            nums[right_index],
            nums[low_index],
        )

        return right_index

    def sort_sub_array(low_index: int, high_index: int) -> None:
        # Step 5: Partition nontrivial ranges and recurse outside the pivot.
        if low_index < high_index:
            pivot_index: int = partition(low_index=low_index, high_index=high_index)
            sort_sub_array(low_index=low_index, high_index=pivot_index - 1)
            sort_sub_array(low_index=pivot_index + 1, high_index=high_index)

    # Steps 1 and 6: Sort the full inclusive range and return the original list.
    sort_sub_array(0, size - 1)

    return nums


def solve() -> None:
    nums: list[int] = [5, 2, 3, 1]
    expected: list[int] = [1, 2, 3, 5]
    result: list[int] = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length: empty input.
    nums = []
    expected = []
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero.
    nums = [0]
    expected = [0]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single minimum value.
    nums = [-100_000]
    expected = [-100_000]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single maximum value.
    nums = [100_000]
    expected = [100_000]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements already sorted.
    nums = [1, 2]
    expected = [1, 2]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements reversed.
    nums = [2, 1]
    expected = [1, 2]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal elements.
    nums = [2, 2]
    expected = [2, 2]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal example with duplicates and zeros.
    nums = [5, 1, 1, 2, 0, 0]
    expected = [0, 0, 1, 1, 2, 5]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd length with elements on both sides of the first pivot.
    nums = [3, 5, 1, 4, 2]
    expected = [1, 2, 3, 4, 5]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First pivot is the minimum.
    nums = [1, 4, 2, 5, 3]
    expected = [1, 2, 3, 4, 5]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First pivot is the maximum.
    nums = [5, 2, 4, 1, 3]
    expected = [1, 2, 3, 4, 5]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated pivot values mixed with smaller and larger values.
    nums = [3, 5, 3, 1, 3, 4, 2, 3]
    expected = [1, 2, 3, 3, 3, 3, 4, 5]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All negative values.
    nums = [-3, -1, -5, -2, -4]
    expected = [-5, -4, -3, -2, -1]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed signs and repeated boundary values.
    nums = [100_000, 0, -100_000, -1, 1, 100_000, -100_000]
    expected = [-100_000, -100_000, -1, 0, 1, 100_000, 100_000]
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length already sorted.
    nums = list(range(500))
    expected = list(range(500))
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length in descending order.
    nums = list(range(499, -1, -1))
    expected = list(range(500))
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all equal zeros.
    nums = [0] * 500
    expected = [0] * 500
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all minimum values.
    nums = [-100_000] * 500
    expected = [-100_000] * 500
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all maximum values.
    nums = [100_000] * 500
    expected = [100_000] * 500
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length alternating minimum and maximum values.
    nums = [100_000, -100_000] * 250
    expected = [-100_000] * 250 + [100_000] * 250
    result = quick_sort(nums)

    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
