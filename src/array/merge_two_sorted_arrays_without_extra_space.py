"""Merge Two Sorted Arrays Without Extra Space.

Given two integer arrays, ``nums1`` and ``nums2``, both sorted in
non-decreasing order, merge their values in place without using another array.

After merging:

- ``nums1`` must contain the smallest ``m`` values in sorted order.
- ``nums2`` must contain the largest ``n`` values in sorted order.
- Combining ``nums1 + nums2`` must produce the complete sorted sequence.
- The original lengths of both arrays must remain unchanged.

Example 1:
    Input:
        nums1 = [-5, -2, 4, 5], m = 4
        nums2 = [-3, 1, 8], n = 3

    Output:
        nums1 = [-5, -3, -2, 1]
        nums2 = [4, 5, 8]

    Explanation:
        nums1 contains the four smallest values and nums2 contains the three
        largest values. Therefore, nums1 + nums2 is
        [-5, -3, -2, 1, 4, 5, 8].

Example 2:
    Input:
        nums1 = [0, 2, 7, 8], m = 4
        nums2 = [-7, -3, -1], n = 3

    Output:
        nums1 = [-7, -3, -1, 0]
        nums2 = [2, 7, 8]

    Pick your answer:
        [1, 2, 3, 4, 6, 5, 7]
        [1, 2, 3, 4, 5, 6, 7]
        [1, 2, 3, 5, 5, 6, 7]
        [7, 5, 6, 4, 3, 2, 1]

Constraints:
    - m == len(nums1)
    - n == len(nums2)
    - 0 <= m, n <= 1000
    - -10^4 <= nums1[i], nums2[i] <= 10^4
    - nums1 and nums2 are sorted in non-decreasing order.

    https://www.youtube.com/watch?v=n7uwj04E0I4&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=24
"""


def merge_two_sorted_arrays_without_extra_space_brute_force(
    nums1: list[int],
    nums2: list[int],
) -> None:
    """Merge two sorted arrays and split the sorted values between them.

    Approach — Two-Pointer Merge with a Temporary Array:
    1. Place one pointer at the beginning of each input array and initialize an
       empty array for the merged values.
    2. While both pointers are valid, compare their values, append the smaller
       value to the merged array, and advance the pointer that supplied it.
    3. After one array is exhausted, append every remaining value from
       ``nums1`` to the merged array.
    4. Append every remaining value from ``nums2`` to the merged array.
    5. Reset the index used for ``nums1`` and begin scanning the completed
       merged array from index 0.
    6. Copy the first ``m`` merged values into ``nums1`` and copy the remaining
       ``n`` values into ``nums2``.

    Args:
        nums1: The first sorted array. It receives the smallest ``m`` values.
        nums2: The second sorted array. It receives the largest ``n`` values.

    Returns:
        None. The merged ordering is stored across ``nums1`` and ``nums2``;
        concatenating ``nums1 + nums2`` produces the complete sorted sequence.

    Mutation:
        Modifies both ``nums1`` and ``nums2`` in place while preserving their
        original lengths.

    Assumptions:
        Both arrays are already sorted in non-decreasing order. Their original
        lengths determine how many merged values are copied back into each one.

    Time Complexity:
        O(m + n). Building the merged array visits every input value once, and
        copying the values back visits all ``m + n`` merged values once more.

    Space Complexity:
        O(m + n) auxiliary space for ``merged_array``. Therefore, this
        brute-force implementation does not satisfy the problem's requirement
        to merge without extra array space.
    """

    # 1. Derive both sizes, start one pointer in each array, and create the
    # temporary merged array.
    m: int = len(nums1)
    n: int = len(nums2)
    first_index: int = 0
    second_index: int = 0

    merged_array: list[int] = []

    # 2. Repeatedly append the smaller value and advance its pointer.
    while first_index < m and second_index < n:
        if nums1[first_index] <= nums2[second_index]:
            merged_array.append(nums1[first_index])
            first_index += 1
        else:
            merged_array.append(nums2[second_index])
            second_index += 1

    # 3. Append any values remaining in nums1.
    while first_index < m:
        merged_array.append(nums1[first_index])
        first_index += 1

    # 4. Append any values remaining in nums2.
    while second_index < n:
        merged_array.append(nums2[second_index])
        second_index += 1

    # 5. Reset the nums1 pointer and begin reading the merged array.
    first_index = 0
    merged_array_index: int = 0

    # 6. Restore the first m values to nums1 and the remaining n values to nums2.
    while merged_array_index < m + n:
        if merged_array_index < m:
            nums1[first_index] = merged_array[merged_array_index]
            first_index += 1
        else:
            nums2[merged_array_index - m] = merged_array[merged_array_index]

        merged_array_index += 1


def merge_two_sorted_arrays_without_extra_space_optimized1(
    nums1: list[int],
    nums2: list[int],
) -> None:
    """Merge two sorted arrays and split the sorted values between them.

    Approach — Boundary Comparison, Swapping, and Sorting:
    1. Derive both array lengths. Place one pointer at the final value of
       ``nums1`` and another pointer at the first value of ``nums2``.
    2. Compare the largest remaining value from ``nums1`` with the smallest
       remaining value from ``nums2``.
    3. If the ``nums1`` value is larger, the two values belong on opposite
       sides. Swap them, move the first pointer left, and move the second
       pointer right.
    4. If the ``nums1`` value is not larger, stop early. Because both original
       arrays were sorted, all remaining values are already in the correct
       array relative to the boundary.
    5. Sort each array independently. The swaps place the correct smaller
       values in ``nums1`` and larger values in ``nums2``, while these sorts
       restore the internal non-decreasing order of each array.

    Args:
        nums1: The first sorted array. It receives the smallest
            ``len(nums1)`` values from both arrays.
        nums2: The second sorted array. It receives the largest
            ``len(nums2)`` values from both arrays.

    Returns:
        None. The merged ordering is stored across ``nums1`` and ``nums2``;
        concatenating ``nums1 + nums2`` produces the complete sorted sequence.

    Mutation:
        Modifies both input arrays in place while preserving their lengths.

    Assumptions:
        Both arrays are initially sorted in non-decreasing order. Either array
        may be empty.

    Time Complexity:
        O(min(m, n) + m log m + n log n), where m and n are the two array
        lengths. The boundary scan performs at most min(m, n) comparisons and
        swaps. Sorting the arrays costs O(m log m) and O(n log n), which
        dominate the scan in the general case.

    Space Complexity:
        The boundary scan uses O(1) auxiliary space. However, Python's Timsort
        may use O(m) memory for ``nums1.sort()`` and O(n) memory for
        ``nums2.sort()``. Because the sorts run sequentially, the worst-case
        peak auxiliary space is O(max(m, n)), so this Python implementation
        does not guarantee strict O(1) auxiliary space.
    """

    # 1. Derive both sizes and place pointers at the cross-array boundary.
    m: int = len(nums1)
    n: int = len(nums2)
    first_index: int = m - 1
    second_index: int = 0

    # 2. Compare the largest remaining left value with the smallest remaining
    # right value.
    while first_index >= 0 and second_index < n:
        # 3. Swap values that belong on opposite sides and move both pointers.
        if nums1[first_index] > nums2[second_index]:
            nums1[first_index], nums2[second_index] = (
                nums2[second_index],
                nums1[first_index],
            )
            first_index -= 1
            second_index += 1
        else:
            # 4. Stop when the boundary is ordered correctly.
            break

    # 5. Restore non-decreasing order within each array.
    nums1.sort()
    nums2.sort()


def merge_two_sorted_arrays_without_extra_space_optimized2(
    nums1: list[int],
    nums2: list[int],
) -> None:
    """Merge two sorted arrays in place using the Gap Method.

    Approach — Gap Method (Shell-sort-style comparison):
    1. Treat ``nums1`` and ``nums2`` as one continuous sequence without
       actually creating that combined array. Record both lengths and define a
       helper that swaps values within or across the two arrays.
    2. Start with a gap equal to the ceiling of half the combined length.
    3. For the current gap, place two indices that distance apart and move them
       together from left to right through the combined sequence.
    4. Compare and swap the indexed values in one of three cases: both indices
       are in ``nums1``, they cross from ``nums1`` into ``nums2``, or both are
       in ``nums2``. Indices in ``nums2`` are converted by subtracting the
       length of ``nums1``.
    5. After scanning all pairs for a gap, reduce the gap using ceiling
       division and repeat. A gap of 1 performs the final adjacent comparisons.
    6. Stop after completing the gap-1 pass. The smallest ``len(nums1)`` values
       are sorted in ``nums1``, and the remaining values are sorted in
       ``nums2``.

    Args:
        nums1: The first sorted array. It receives the smallest
            ``len(nums1)`` values from both arrays.
        nums2: The second sorted array. It receives the largest
            ``len(nums2)`` values from both arrays.

    Returns:
        None. The merged ordering is stored across the two input arrays, so
        ``nums1 + nums2`` produces the complete sorted sequence.

    Mutation:
        Modifies both arrays in place while preserving their original lengths.

    Assumptions:
        Both arrays are initially sorted in non-decreasing order. Either array
        may be empty.

    Time Complexity:
        O((m + n) log(m + n)), where m and n are the array lengths. Each gap
        pass examines O(m + n) pairs, and the gap is approximately halved after
        every pass, producing O(log(m + n)) passes.

    Space Complexity:
        O(1) auxiliary space. The function stores only sizes, indices, the gap,
        and temporary references used during swaps; it creates no merged array.
    """
    # 1. Record both sizes and treat their total as one continuous length.
    m: int = len(nums1)
    n: int = len(nums2)
    total_length: int = m + n

    # 1. Swap two values that may belong to the same or different arrays.
    def swap(
        first_nums: list[int],
        second_nums: list[int],
        first_index: int,
        second_index: int,
    ) -> None:
        first_nums[first_index], second_nums[second_index] = (
            second_nums[second_index],
            first_nums[first_index],
        )

    # 2. Begin with the ceiling of half the combined length.
    gap: int = (total_length + 1) // 2

    while gap > 0:
        # 3. Scan pairs separated by the current gap.
        first_index: int = 0
        second_index: int = gap

        while second_index < total_length:
            # 4. Compare one value from nums1 with one value from nums2.
            if first_index < m and second_index >= m:
                if nums1[first_index] > nums2[second_index - m]:
                    swap(
                        first_nums=nums1,
                        second_nums=nums2,
                        first_index=first_index,
                        second_index=second_index - m,
                    )
            # 4. Compare two values that are both stored in nums2.
            elif first_index >= m:
                if nums2[first_index - m] > nums2[second_index - m]:
                    swap(
                        first_nums=nums2,
                        second_nums=nums2,
                        first_index=first_index - m,
                        second_index=second_index - m,
                    )
            # 4. Compare two values that are both stored in nums1.
            else:
                if nums1[first_index] > nums1[second_index]:
                    swap(
                        first_nums=nums1,
                        second_nums=nums1,
                        first_index=first_index,
                        second_index=second_index,
                    )

            first_index += 1
            second_index += 1

        # 5. Finish after the gap-1 pass; otherwise reduce the gap by ceiling.
        if gap == 1:
            break
        gap = (gap + 1) // 2

    # 6. Both arrays now store their correct portions of the merged ordering.


def solve() -> None:
    nums1: list[int] = [-5, -2, 4, 5]
    nums2: list[int] = [-3, 1, 8]

    expected: list[int] = [-5, -3, -2, 1, 4, 5, 8]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1: list[int] = [0, 2, 7, 8]
    nums2: list[int] = [-7, -3, -1]

    expected: list[int] = [-7, -3, -1, 0, 2, 7, 8]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6, 7]

    expected = [1, 2, 3, 4, 5, 6, 7]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 2]
    nums2 = [2, 2, 3]

    expected = [1, 2, 2, 2, 2, 3]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = [4, 5, 6]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [4, 5, 6]
    nums2 = [1, 2, 3]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, 0, 10_000]
    nums2 = [-10_000, 10_000]

    expected = [-10_000, -10_000, 0, 10_000, 10_000]
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-1] * 1_000
    nums2 = [1] * 1_000

    expected = ([-1] * 1_000) + ([1] * 1_000)
    merge_two_sorted_arrays_without_extra_space_brute_force(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1: list[int] = [-5, -2, 4, 5]
    nums2: list[int] = [-3, 1, 8]

    expected: list[int] = [-5, -3, -2, 1, 4, 5, 8]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1: list[int] = [0, 2, 7, 8]
    nums2: list[int] = [-7, -3, -1]

    expected: list[int] = [-7, -3, -1, 0, 2, 7, 8]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6, 7]

    expected = [1, 2, 3, 4, 5, 6, 7]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 2]
    nums2 = [2, 2, 3]

    expected = [1, 2, 2, 2, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = [4, 5, 6]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [4, 5, 6]
    nums2 = [1, 2, 3]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, 0, 10_000]
    nums2 = [-10_000, 10_000]

    expected = [-10_000, -10_000, 0, 10_000, 10_000]
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-1] * 1_000
    nums2 = [1] * 1_000

    expected = ([-1] * 1_000) + ([1] * 1_000)
    merge_two_sorted_arrays_without_extra_space_optimized1(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1: list[int] = [-5, -2, 4, 5]
    nums2: list[int] = [-3, 1, 8]

    expected: list[int] = [-5, -3, -2, 1, 4, 5, 8]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1: list[int] = [0, 2, 7, 8]
    nums2: list[int] = [-7, -3, -1]

    expected: list[int] = [-7, -3, -1, 0, 2, 7, 8]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result: list[int] = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3]
    nums2 = [2, 4, 5, 6]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = [1, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 2]
    nums2 = [2, 2, 3]

    expected = [1, 2, 2, 2, 2, 3]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = [4, 5, 6]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [4, 5, 6]
    nums2 = [1, 2, 3]

    expected = [1, 2, 3, 4, 5, 6]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, 0, 10_000]
    nums2 = [-10_000, 10_000]

    expected = [-10_000, -10_000, 0, 10_000, 10_000]
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-1] * 1_000
    nums2 = [1] * 1_000

    expected = ([-1] * 1_000) + ([1] * 1_000)
    merge_two_sorted_arrays_without_extra_space_optimized2(nums1, nums2)
    result = nums1 + nums2
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
