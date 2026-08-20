"""Intersection of Two Sorted Arrays

You are given two integer arrays ``nums1`` and ``nums2`` of lengths ``n`` and
``m``, respectively. Both arrays are sorted in non-decreasing order. Return an
array containing the intersection of the two arrays.

The intersection consists of the elements that occur in both arrays. Each
matching occurrence should appear in the result, so a duplicated value may be
included more than once when it occurs multiple times in both arrays. The
result must remain in non-decreasing order.

Example:
    Input: nums1 = [1, 2, 2, 3, 4], nums2 = [2, 2, 3, 5]
    Output: [2, 2, 3]
    Explanation: Both occurrences of 2 and one occurrence of 3 appear in both
    arrays.

    https://www.youtube.com/watch?v=wvcQg43_V8U&t=2330s
"""


def intersection_of_sorted_arrays_brute_force(
    nums1: list[int], nums2: list[int]
) -> list[int]:
    """Return the intersection of two sorted arrays, including duplicates.

    Approach:
        1. Store both array lengths, create an empty result, and create a Boolean
           list whose positions track which elements of ``nums2`` have already
           been matched.
        2. Visit each element in ``nums1`` from left to right.
        3. For the current element in ``nums1``, scan ``nums2`` from the
           beginning for an equal value at an index that has not been visited.
        4. When a match is found, append it to the result, mark its index in
           ``nums2`` as visited, and stop the current inner scan so that each
           element can participate in at most one match.
        5. Stop the inner scan early if the current value in ``nums2`` is larger
           than the current value in ``nums1`` because both arrays are sorted.
        6. Return the completed intersection after every element in ``nums1``
           has been processed.

    Time Complexity:
        O(n * m) in the worst case, where n and m are the lengths of ``nums1``
        and ``nums2``. For each of the n elements in ``nums1``, the inner loop
        may scan all m elements of ``nums2``. The early break can reduce the
        work for some inputs but does not change the worst-case complexity.

    Space Complexity:
        O(m) auxiliary space for ``visited_indices``. The returned result can
        contain up to min(n, m) elements and therefore uses O(min(n, m)) output
        space.
    """
    # Step 1: Initialize lengths, result storage, and visited-index tracking.
    nums1_len: int = len(nums1)
    nums2_len: int = len(nums2)
    result: list[int] = []
    visited_indices: list[bool] = [False] * nums2_len
    nums1_index: int = 0
    nums2_index: int

    # Step 2: Visit each element in the first sorted array.
    while nums1_index < nums1_len:
        # Step 3: Search the second array for an unused matching occurrence.
        nums2_index = 0
        while nums2_index < nums2_len:
            if (
                not visited_indices[nums2_index]
                and nums1[nums1_index] == nums2[nums2_index]
            ):
                # Step 4: Record the match and prevent this index from reuse.
                result.append(nums2[nums2_index])
                visited_indices[nums2_index] = True
                break
            elif nums2[nums2_index] > nums1[nums1_index]:
                # Step 5: No later value in the sorted second array can match.
                break
            nums2_index += 1
        nums1_index += 1

    # Step 6: Return all matched occurrences in sorted order.
    return result


def intersection_of_sorted_arrays_optimized(
    nums1: list[int], nums2: list[int]
) -> list[int]:
    """Return the intersection of two sorted arrays, including duplicates.

    Approach: Two-Pointer Intersection
        1. Initialize one index for each array, store both array lengths, and
           create an empty result list.
        2. Compare the values at both indexes while neither array is exhausted.
        3. If the current value in ``nums1`` is larger, advance the ``nums2``
           index because its smaller value cannot match any later ``nums1``
           value.
        4. If the current value in ``nums1`` is smaller, advance the ``nums1``
           index for the same reason.
        5. If the values are equal, append one occurrence to the result and
           advance both indexes so neither occurrence can be matched again.
        6. Return the result when either array is exhausted because no further
           matches are then possible.

    Time Complexity:
        O(n + m), where n and m are the lengths of ``nums1`` and ``nums2``.
        Each index moves only forward and can advance at most the length of its
        corresponding array.

    Space Complexity:
        O(1) auxiliary space because the indexes and lengths use constant
        memory. The returned result can contain up to min(n, m) elements and
        therefore uses O(min(n, m)) output space.
    """
    # Step 1: Initialize both indexes, both lengths, and the result list.

    nums1_index: int = 0
    nums2_index: int = 0

    nums1_len: int = len(nums1)
    nums2_len: int = len(nums2)
    result: list[int] = []

    # Step 2: Compare values while both arrays still have unprocessed elements.
    while nums1_index < nums1_len and nums2_index < nums2_len:
        # Step 3: Advance nums2 past a value that is too small to match.
        if nums1[nums1_index] > nums2[nums2_index]:
            nums2_index += 1

        # Step 4: Advance nums1 past a value that is too small to match.
        elif nums1[nums1_index] < nums2[nums2_index]:
            nums1_index += 1
        else:
            # Step 5: Record the match and consume one value from each array.
            result.append(nums1[nums1_index])
            nums1_index += 1
            nums2_index += 1

    # Step 6: Return every matched occurrence in sorted order.
    return result


def solve() -> None:
    nums1: list[int] = [1, 2, 2, 3, 4]
    nums2: list[int] = [2, 2, 3, 5]

    expected: list[int] = [2, 2, 3]
    result: list[int] = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 2, 3, 4]
    nums2 = [2, 2, 3, 5]

    expected = [2, 2, 3]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3, 4, 5]
    nums2 = [2, 4, 6, 8]

    expected = [2, 4]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6]

    expected = []
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 1, 2, 2, 3]
    nums2 = [1, 1, 2, 2, 3]

    expected = [1, 1, 2, 2, 3]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [2, 2, 2, 2]
    nums2 = [2, 2]

    expected = [2, 2]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [2, 2]
    nums2 = [2, 2, 2, 2]

    expected = [2, 2]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, -5, -1, 0, 3, 10_000]
    nums2 = [-10_000, -1, 0, 2, 10_000]

    expected = [-10_000, -1, 0, 10_000]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [7]

    expected = [7]
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [8]

    expected = []
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = []
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = []
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    result = intersection_of_sorted_arrays_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    nums1 = [1, 2, 3, 4, 5]
    nums2 = [2, 4, 6, 8]

    expected = [2, 4]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6]

    expected = []
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 1, 2, 2, 3]
    nums2 = [1, 1, 2, 2, 3]

    expected = [1, 1, 2, 2, 3]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [2, 2, 2, 2]
    nums2 = [2, 2]

    expected = [2, 2]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [2, 2]
    nums2 = [2, 2, 2, 2]

    expected = [2, 2]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, -5, -1, 0, 3, 10_000]
    nums2 = [-10_000, -1, 0, 2, 10_000]

    expected = [-10_000, -1, 0, 10_000]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [7]

    expected = [7]
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [8]

    expected = []
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = []
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = []
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    result = intersection_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
