"""Union of Two Sorted Arrays

Given two sorted arrays ``nums1`` and ``nums2``, return an array containing the
union of the two arrays. The elements in the union must be in ascending order.

The union of two arrays contains every distinct value that is present in the
first array, the second array, or both arrays.

Example 1:
    Input: nums1 = [1, 2, 3, 4, 5], nums2 = [1, 2, 7]
    Output: [1, 2, 3, 4, 5, 7]
    Explanation: The values 1 and 2 are common to both arrays; 3, 4, and 5 are
    from nums1; and 7 is from nums2.

Example 2:
    Input: nums1 = [3, 4, 6, 7, 9, 9], nums2 = [1, 5, 7, 8, 8]
    Output: [1, 3, 4, 5, 6, 7, 8, 9]
    Explanation: The value 7 is common to both arrays; 3, 4, 6, and 9 are from
    nums1; and 1, 5, and 8 are from nums2.
"""


def union_of_sorted_arrays_brute_force(nums1: list[int], nums2: list[int]) -> list[int]:
    """Return the sorted union of two sorted integer arrays.

    Approach:
        1. Remove duplicates from each input array while preserving its sorted
           order by creating dictionaries from the values and converting their
           keys back to lists.
        2. Initialize an empty result and one index for each deduplicated list.
        3. Compare the current values while both indexes are valid. Append the
           smaller value and advance its index. When the values are equal,
           append the value once and advance both indexes.
        4. Append any values remaining in the second deduplicated list.
        5. Append any values remaining in the first deduplicated list.
        6. Return the completed sorted union.

    Time Complexity:
        O(n + m), where n and m are the lengths of the input arrays. Creating
        the dictionaries and lists processes every input value once, and the
        two-pointer merge processes each deduplicated value at most once.

    Space Complexity:
        O(n + m). The two dictionaries and deduplicated lists can contain all
        input values, and the returned result can contain up to n + m values.
    """
    # Step 1: Remove duplicates from both sorted arrays while preserving order.
    nums1 = list(dict.fromkeys(nums1))
    nums2 = list(dict.fromkeys(nums2))

    # Step 2: Store the lengths and initialize the result and both indexes.
    nums1_len = len(nums1)
    nums2_len = len(nums2)

    nums1_index: int = 0
    nums2_index: int = 0

    result: list[int] = []

    # Step 3: Merge the lists, adding values shared by both lists only once.
    while nums1_index < nums1_len and nums2_index < nums2_len:
        if nums1[nums1_index] < nums2[nums2_index]:
            result.append(nums1[nums1_index])
            nums1_index += 1
        elif nums1[nums1_index] > nums2[nums2_index]:
            result.append(nums2[nums2_index])
            nums2_index += 1
        else:
            result.append(nums2[nums2_index])
            nums2_index += 1
            nums1_index += 1

    # Step 4: Append any values remaining in the second list.
    while nums2_index < nums2_len:
        result.append(nums2[nums2_index])
        nums2_index += 1

    # Step 5: Append any values remaining in the first list.
    while nums1_index < nums1_len:
        result.append(nums1[nums1_index])
        nums1_index += 1

    # Step 6: Return the sorted union.
    return result


def union_of_sorted_arrays_space_optimized(
    nums1: list[int], nums2: list[int]
) -> list[int]:
    """Return the sorted union of two sorted integer arrays.

    Approach:
        1. Store both array lengths and initialize one index for each array,
           along with an empty result list.
        2. While both indexes are valid, select the smaller current value. If
           the values are equal, select the value from the first array. Advance
           the index belonging to the selected value.
        3. Append the selected value when the result is empty or its last value
           is different. Because the inputs are sorted, comparing against only
           the last appended value is enough to prevent duplicates.
        4. Process any values remaining in the first array, appending each value
           only when it differs from the last value in the result.
        5. Process any values remaining in the second array in the same way.
        6. Return the completed sorted union.

    Time Complexity:
        O(n + m), where n and m are the lengths of the two arrays. Each index
        moves forward through its array once, so every input element is
        processed at most once.

    Space Complexity:
        O(1) auxiliary space because the indexes, lengths, and current value use
        constant additional memory. The returned result requires O(n + m)
        output space in the worst case when every input value is distinct.
    """
    # Step 1: Initialize the lengths, indexes, result, and current value.
    nums1_len: int = len(nums1)
    nums2_len: int = len(nums2)

    nums1_index: int = 0
    nums2_index: int = 0
    result: list[int] = []
    value: int

    # Steps 2 and 3: Select values in order and append each distinct value once.
    while nums1_index < nums1_len and nums2_index < nums2_len:
        if nums1[nums1_index] <= nums2[nums2_index]:
            value = nums1[nums1_index]
            nums1_index += 1
        else:
            value = nums2[nums2_index]
            nums2_index += 1

        if not result or result[-1] != value:
            result.append(value)

    # Step 4: Add the distinct values remaining in the first array.
    while nums1_index < nums1_len:
        value = nums1[nums1_index]

        if not result or result[-1] != value:
            result.append(value)

        nums1_index += 1

    # Step 5: Add the distinct values remaining in the second array.
    while nums2_index < nums2_len:
        value = nums2[nums2_index]

        if not result or result[-1] != value:
            result.append(value)

        nums2_index += 1

    # Step 6: Return the sorted union.
    return result


def solve() -> None:
    nums1: list[int] = [1, 2, 3, 4, 5]
    nums2: list[int] = [1, 2, 7]

    expected: list[int] = [1, 2, 3, 4, 5, 7]
    result: list[int] = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [3, 4, 6, 7, 9, 9]
    nums2 = [1, 5, 7, 8, 8]

    expected = [1, 3, 4, 5, 6, 7, 8, 9]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6]

    expected = [1, 2, 3, 4, 5, 6]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 1, 1, 2, 2]
    nums2 = [2, 2, 3, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-5, -3, -1, 0]
    nums2 = [-4, -3, 0, 2]

    expected = [-5, -4, -3, -1, 0, 2]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3, 4]
    nums2 = [2, 3]

    expected = [1, 2, 3, 4]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [7]

    expected = [7]
    result = union_of_sorted_arrays_brute_force(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3, 4, 5]
    nums2 = [1, 2, 7]

    expected = [1, 2, 3, 4, 5, 7]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [3, 4, 6, 7, 9, 9]
    nums2 = [1, 5, 7, 8, 8]

    expected = [1, 3, 4, 5, 6, 7, 8, 9]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6]

    expected = [1, 2, 3, 4, 5, 6]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 1, 1, 2, 2]
    nums2 = [2, 2, 3, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = [1, 2, 3]

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3]
    nums2 = []

    expected = [1, 2, 3]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = []
    nums2 = []

    expected = []
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [-10_000, -5, -3, -1, 0]
    nums2 = [-10_000, -4, -3, 0, 2, 10_000]

    expected = [-10_000, -5, -4, -3, -1, 0, 2, 10_000]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [1, 2, 3, 4]
    nums2 = [2, 3]

    expected = [1, 2, 3, 4]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums1 = [7]
    nums2 = [7]

    expected = [7]
    result = union_of_sorted_arrays_space_optimized(nums1, nums2)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
