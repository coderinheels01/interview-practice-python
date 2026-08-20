"""Rearrange Array Elements by Sign

Given an integer array ``nums`` of even length consisting of an equal number of
positive and negative integers, return an answer array that meets these
conditions:

1. Every consecutive pair of integers has opposite signs.
2. For all integers with the same sign, their relative order from ``nums`` is
   preserved.
3. The rearranged array begins with a positive integer.

Example 1:
    Input: nums = [2, 4, 5, -1, -3, -4]
    Output: [2, -1, 4, -3, 5, -4]
    Explanation: The positive numbers 2, 4, and 5 preserve their relative
    positions, and the negative numbers -1, -3, and -4 preserve theirs.

Example 2:
    Input: nums = [1, -1, -3, -4, 2, 3]
    Output: [1, -1, 2, -3, 3, -4]
    Explanation: The positive numbers 1, 2, and 3 preserve their relative
    positions, and the negative numbers -1, -3, and -4 preserve theirs.

Now your turn:
    Input: nums = [-4, 4, -4, 4, -4, 4]

    Possible answers:
        - [4, -4, 4, -4, 4, -4]
        - [-4, 4, -4, 4, -4, 4]
        - [4, 4, 4, -4, -4, -4]
        - [-4, -4, -4, 4, 4, 4]

Constraints:
    - 2 <= nums.length <= 10^5
    - 1 <= abs(nums[i]) <= 10^4
    - nums.length is even.
    - The numbers of positive and negative integers are equal.
"""


def rearrange_array_elements_by_sign_brute_force(nums: list[int]) -> list[int]:
    """Rearrange ``nums`` so positive and negative values alternate.

    The rearranged list begins with a positive value and preserves the relative
    order of values having the same sign. The input must have an even length,
    contain no zeroes, and contain equal numbers of positive and negative
    values, as guaranteed by the problem constraints.

    Approach:
        1. Store the input size and create separate lists for positive and
           negative values.
        2. Traverse ``nums`` once and append each value to its corresponding
           sign list. Appending in traversal order preserves relative order.
        3. Initialize separate indexes for the positive and negative lists.
        4. Traverse every position in ``nums``. Fill even positions from the
           positive list and odd positions from the negative list, advancing
           only the index belonging to the value just written.
        5. Return the rearranged input list.

    Args:
        nums: An even-length list containing equal counts of positive and
            negative integers.

    Returns:
        The same list object, rearranged to alternate signs starting positive.

    Mutation Behavior:
        The function modifies ``nums`` in place and also returns it.

    Time Complexity:
        O(n), where n is the length of ``nums``. One pass separates all values
        by sign and a second pass writes all n values back into the list.

    Space Complexity:
        O(n) auxiliary space. ``positive_nums`` and ``negative_nums`` together
        store all n input values; the remaining variables use constant space.
    """
    # Step 1: Store the size and create a list for each sign.
    size: int = len(nums)
    positive_nums: list[int] = []
    negative_nums: list[int] = []

    # Step 2: Separate values by sign while preserving their relative order.
    for num in nums:
        if num > 0:
            positive_nums.append(num)
        else:
            negative_nums.append(num)

    # Step 3: Track the next unused value in each sign list independently.
    positive_index: int = 0
    negative_index: int = 0

    # Step 4: Place positives at even indexes and negatives at odd indexes.
    for index in range(size):
        if index % 2 == 0:
            nums[index] = positive_nums[positive_index]
            positive_index += 1
        else:
            nums[index] = negative_nums[negative_index]
            negative_index += 1

    # Step 5: Return the same list after rearranging it in place.
    return nums


def rearrange_array_elements_by_sign_optimized(
    nums: list[int],
) -> list[int]:
    """Return a new list whose values alternate between positive and negative.

    The result begins with a positive value and preserves the relative order of
    values having the same sign. The input must have an even length, contain no
    zeroes, and contain equal numbers of positive and negative values, as
    guaranteed by the problem constraints.

    Approach:
        1. Create a result list with the same length as ``nums``.
        2. Initialize separate occurrence indexes for positive and negative
           values. Each index tracks how many values of that sign have already
           been placed.
        3. Traverse ``nums`` once from left to right so values of each sign are
           encountered and placed in their original relative order.
        4. Place each positive value at ``positive_index * 2``, which produces
           the even result positions 0, 2, 4, and so on. Then advance the
           positive index.
        5. Place each negative value at ``negative_index * 2 + 1``, which
           produces the odd result positions 1, 3, 5, and so on. Then advance
           the negative index.
        6. Return the completed result list after every input value is placed.

    Args:
        nums: An even-length list containing equal counts of positive and
            negative integers.

    Returns:
        A new list containing the values rearranged with alternating signs,
        beginning with a positive value.

    Mutation Behavior:
        The function does not modify ``nums``.

    Time Complexity:
        O(n), where n is the length of ``nums``. Creating the result list and
        traversing all input values each take O(n) time.

    Space Complexity:
        O(n) additional space because ``rearranged_array`` contains n elements.
        Excluding the returned output list, the algorithm uses O(1) auxiliary
        space for ``size`` and the two occurrence indexes.
    """
    # Step 1: Create the result list with one position per input value.
    size: int = len(nums)
    rearranged_array: list[int] = [0] * size

    # Step 2: Track how many positive and negative values have been placed.
    positive_index: int = 0
    negative_index: int = 0

    # Step 3: Process values left to right to preserve relative sign order.
    for num in nums:
        # Step 4: Place positive values into consecutive even positions.
        if num > 0:
            rearranged_array[positive_index * 2] = num
            positive_index += 1

        # Step 5: Place negative values into consecutive odd positions.
        else:
            rearranged_array[(negative_index * 2) + 1] = num
            negative_index += 1

    # Step 6: Return the completed rearranged list without mutating nums.
    return rearranged_array


def solve() -> None:
    nums: list[int] = [2, 4, 5, -1, -3, -4]

    expected: list[int] = [2, -1, 4, -3, 5, -4]
    result: list[int] = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1, -3, -4, 2, 3]

    expected = [1, -1, 2, -3, 3, -4]
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1]

    expected = [1, -1]
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 1]

    expected = [1, -1]
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, 4, -4, 4, -4, 4]

    expected = [4, -4, 4, -4, 4, -4]
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -2, -10_000, 10_000, 1, 10_000]

    expected = [10_000, -10_000, 1, -2, 10_000, -10_000]
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1] * 50_000 + [-1] * 50_000

    expected = [1, -1] * 50_000
    result = rearrange_array_elements_by_sign_brute_force(nums)

    assert result == expected
    print("Expected: alternating signs for 100,000 values")
    print(f"Result length: {len(result)}")

    nums = [2, 4, 5, -1, -3, -4]

    expected = [2, -1, 4, -3, 5, -4]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1, -3, -4, 2, 3]

    expected = [1, -1, 2, -3, 3, -4]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1]

    expected = [1, -1]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, 1]

    expected = [1, -1]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, -2, 1, -5, 4, -6]

    expected = [3, -2, 1, -5, 4, -6]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, 4, -4, 4, -4, 4]

    expected = [4, -4, 4, -4, 4, -4]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -2, -10_000, 10_000, 1, 10_000]

    expected = [10_000, -10_000, 1, -2, 10_000, -10_000]
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1] * 50_000 + [-1] * 50_000

    expected = [1, -1] * 50_000
    result = rearrange_array_elements_by_sign_optimized(nums)

    assert result == expected
    print("Expected: alternating signs for 100,000 values")
    print(f"Result length: {len(result)}")


if __name__ == "__main__":
    solve()
