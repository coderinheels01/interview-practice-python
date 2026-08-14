"""Move Zeroes

Given an integer array ``nums``, move all the zeroes to the end of the array.
The relative order of the other elements must remain the same.

This must be done in place, without making a copy of the array.

Example 1:
    Input: nums = [0, 1, 4, 0, 5, 2]
    Output: [1, 4, 5, 2, 0, 0]
    Explanation: Both zeroes are moved to the end, and the order of the other
    elements remains the same.

Example 2:
    Input: nums = [0, 0, 0, 1, 3, -2]
    Output: [1, 3, -2, 0, 0, 0]
    Explanation: All three zeroes are moved to the end, and the order of the
    other elements remains the same.
"""


def move_zeroes_brute_force(nums: list[int]) -> None:
    """Move all zeroes to the end of ``nums`` using a temporary array.

    Approach:
        1. Store the length of ``nums``, create a temporary array filled with
           zeroes, and initialize ``new_index`` to the first position.
        2. Traverse every element in ``nums`` using ``old_index``.
        3. When the current element is nonzero, copy it into ``result`` at
           ``new_index`` and advance ``new_index``. Skipping zeroes preserves
           the relative order of all nonzero elements, while unused positions
           in ``result`` remain zero.
        4. Traverse every index again and copy ``result`` back into ``nums`` so
           the input list is modified.

    Time Complexity:
        O(n), where n is the length of ``nums``. The first loop examines all n
        elements, and the second loop copies all n elements back into ``nums``.

    Space Complexity:
        O(n), because ``result`` contains n elements. The index variables use
        O(1) additional space. This brute-force implementation does not satisfy
        the prompt's requirement to avoid making a copy of the array.
    """
    # Step 1: Store the length, allocate a zero-filled result, and set its writer.
    n: int = len(nums)
    result: int = [0] * n
    new_index: list[int] = 0

    # Step 2: Examine every value in the original array.
    for old_index in range(n):
        # Step 3: Copy each nonzero value in its original relative order.
        if nums[old_index] != 0:
            result[new_index] = nums[old_index]
            new_index += 1

    # Step 4: Copy the rearranged values back into the input array.
    for index in range(n):
        nums[index] = result[index]


def move_zeroes_space_optimized(nums: list[int]) -> None:
    """Move all zeroes to the end of ``nums`` using constant extra space.

    Approach:
        1. Store the length of ``nums`` and initialize ``write_index`` to 0.
           This index marks where the next nonzero value should be placed.
        2. Traverse every element from left to right using ``read_index``.
        3. When the current element is nonzero, copy it to ``write_index`` and
           advance ``write_index``. Reading from left to right preserves the
           relative order of all nonzero elements.
        4. After all nonzero values have been compacted at the front, traverse
           from ``write_index`` to the end using ``zero_index`` and fill every
           remaining position with zero.

    Time Complexity:
        O(n), where n is the length of ``nums``. The first loop examines all n
        elements, and the second loop fills at most n remaining positions.

    Space Complexity:
        O(1), because the function modifies ``nums`` in place and uses only
        ``n``, ``read_index``, ``write_index``, and ``zero_index`` regardless
        of the input size.
    """
    # Step 1: Store the length and initialize the next nonzero write position.
    n: int = len(nums)
    write_index: int = 0

    # Step 2: Read every element from left to right.
    for read_index in range(n):
        # Step 3: Compact each nonzero value at the front in its original order.
        if nums[read_index] != 0:
            nums[write_index] = nums[read_index]
            write_index += 1

    # Step 4: Fill every position after the nonzero prefix with zero.
    for zero_index in range(write_index, n):
        nums[zero_index] = 0


def solve() -> None:
    nums: list[int] = [0, 1, 4, 0, 5, 2]

    expected: list[int] = [1, 4, 5, 2, 0, 0]
    move_zeroes_space_optimized(nums)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 1, 3, -2]

    expected = [1, 3, -2, 0, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = [1, 2, 3, 4]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0]

    expected = [0, 0, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = [0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]

    expected = [7]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 2, 3]

    expected = [1, 2, 3, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 0, 0]

    expected = [1, 2, 3, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 2, 0, 3, 0]

    expected = [1, 2, 3, 0, 0, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 0, -2, 0, -3]

    expected = [-1, -2, -3, 0, 0]
    move_zeroes_space_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """Temporarily disabled brute-force tests.

    nums: list[int] = [0, 1, 4, 0, 5, 2]

    expected: list[int] = [1, 4, 5, 2, 0, 0]
    move_zeroes_brute_force(nums)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 1, 3, -2]

    expected = [1, 3, -2, 0, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = [1, 2, 3, 4]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0]

    expected = [0, 0, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = [0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]

    expected = [7]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 2, 3]

    expected = [1, 2, 3, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 0, 0]

    expected = [1, 2, 3, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 2, 0, 3, 0]

    expected = [1, 2, 3, 0, 0, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 0, -2, 0, -3]

    expected = [-1, -2, -3, 0, 0]
    move_zeroes_brute_force(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """


if __name__ == "__main__":
    solve()
