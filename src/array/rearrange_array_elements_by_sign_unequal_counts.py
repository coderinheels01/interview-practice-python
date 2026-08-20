"""Rearrange Array Elements by Sign — Unequal Counts

Given an integer array ``nums`` consisting of positive and negative integers,
return an answer array that meets these conditions:

1. Every consecutive pair of integers has opposite signs while both positive
   and negative numbers remain available.
2. For all integers with the same sign, the order in which they were present in
   ``nums`` is preserved.
3. The rearranged array begins with a positive integer when at least one
   positive integer exists.
4. If any positive or negative numbers remain after alternating as long as
   possible, append them to the end without changing their relative order.

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

Example 3:
    Input: nums = [3, 1, -2, -5, 2, 4, 6]
    Output: [3, -2, 1, -5, 2, 4, 6]
    Explanation: Alternation stops after the negative numbers are exhausted.
    The remaining positive numbers 4 and 6 are appended in their original
    relative order.

Example 4:
    Input: nums = [-1, -2, 5, -3, -4]
    Output: [5, -1, -2, -3, -4]
    Explanation: The result starts with the only positive number. After it is
    paired with -1, the remaining negative numbers are appended in their
    original relative order.

Example 5:
    Input: nums = [8, 3, 2, -7]
    Output: [8, -7, 3, 2]
    Explanation: The values alternate while both signs remain, then the unused
    positive numbers are appended without changing their order.

Now your turn:
    Input: nums = [-4, 4, -4, 4, -4, 4]

    Possible answers:
        - [4, -4, 4, -4, 4, -4]
        - [-4, 4, -4, 4, -4, 4]
        - [4, 4, 4, -4, -4, -4]
        - [-4, -4, -4, 4, 4, 4]

Constraints:
    - 1 <= nums.length <= 10^5
    - 1 <= abs(nums[i]) <= 10^4
    - ``nums`` contains at least one positive integer.
    - The numbers of positive and negative integers do not have to be equal.

https://www.youtube.com/watch?v=h4aBagy4Uok&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=9

"""


def rearrange_array_elements_by_sign_unequal_counts_brute_force(
    nums: list[int],
) -> list[int]:
    """Rearrange ``nums`` by alternating signs while preserving relative order.

    The result begins with a positive value and alternates signs while values of
    both signs remain. If one sign is exhausted first, the remaining values of
    the other sign are placed at the end in their original relative order. The
    input contains no zeroes and at least one positive value, as guaranteed by
    the problem constraints.

    Approach:
        1. Store the input size and create separate lists for positive and
           negative values.
        2. Traverse ``nums`` and append each value to its corresponding sign
           list, preserving the original relative order within each sign.
        3. Initialize an index for each sign list and store their sizes.
        4. Traverse every position in ``nums``. Prefer a positive value at an
           even position and a negative value at an odd position while the
           corresponding sign list still has an unused value.
        5. When the preferred sign is exhausted, place the next unused value
           from whichever sign remains. This puts all leftovers at the end
           without changing their relative order.
        6. Return the same ``nums`` list after all positions are overwritten.

    Args:
        nums: A list of nonzero integers containing at least one positive value.
            Positive and negative counts may be unequal.

    Returns:
        The same list object, rearranged to alternate signs while possible.

    Mutation Behavior:
        The function modifies ``nums`` in place and also returns it.

    Time Complexity:
        O(n), where n is the length of ``nums``. The first loop separates all n
        values by sign, and the second loop overwrites all n positions once.

    Space Complexity:
        O(n) auxiliary space. ``positive_nums`` and ``negative_nums`` together
        store all n input values; the remaining variables use constant space.
    """
    # Step 1: Store the input size and create a list for each sign.
    size: int = len(nums)

    positive_nums: list[int] = []
    negative_nums: list[int] = []

    # Step 2: Separate values by sign while preserving their relative order.
    for num in nums:
        if num > 0:
            positive_nums.append(num)
        else:
            negative_nums.append(num)

    # Step 3: Initialize the next unused index and size for each sign list.
    positive_index: int = 0
    negative_index: int = 0
    positive_size: int = len(positive_nums)
    negative_size: int = len(negative_nums)

    # Step 4: Prefer positives at even positions and negatives at odd positions.
    for index in range(size):
        if index % 2 == 0 and positive_index < positive_size:
            nums[index] = positive_nums[positive_index]
            positive_index += 1
        elif index % 2 != 0 and negative_index < negative_size:
            nums[index] = negative_nums[negative_index]
            negative_index += 1

        # Step 5: When the preferred sign is exhausted, place either leftover.
        elif positive_index < positive_size:
            nums[index] = positive_nums[positive_index]
            positive_index += 1
        elif negative_index < negative_size:
            nums[index] = negative_nums[negative_index]
            negative_index += 1

    # Step 6: Return the same list after rearranging every position.
    return nums


def rearrange_array_elements_by_sign_unequal_counts_optimized(
    nums: list[int],
) -> list[int]:
    """Return a stable sign-alternating arrangement without mutating ``nums``.

    Values alternate positive then negative while both signs are available.
    Excess values are placed at the end in their original relative order.

    Time Complexity:
        O(n), where n is the length of ``nums``. The function counts positive
        values once and then places every value during a second linear pass.

    Space Complexity:
        O(n) for the required result list and O(1) auxiliary space beyond that
        output because only counters and output positions are stored.
    """
    size: int = len(nums)
    positive_count: int = sum(num > 0 for num in nums)
    negative_count: int = size - positive_count
    pair_count: int = min(positive_count, negative_count)

    rearranged_nums: list[int] = [0] * size

    positive_position: int = 0
    negative_position: int = 1
    leftover_position: int = pair_count * 2

    paired_positives: int = 0
    paired_negatives: int = 0

    for num in nums:
        if num > 0 and paired_positives < pair_count:
            rearranged_nums[positive_position] = num
            positive_position += 2
            paired_positives += 1
        elif num < 0 and paired_negatives < pair_count:
            rearranged_nums[negative_position] = num
            negative_position += 2
            paired_negatives += 1
        else:
            rearranged_nums[leftover_position] = num
            leftover_position += 1

    return rearranged_nums


def solve() -> None:
    nums: list[int] = [3, 1, -2, -5, 2, 4, 6]

    expected: list[int] = [3, -2, 1, -5, 2, 4, 6]
    result: list[int] = rearrange_array_elements_by_sign_unequal_counts_brute_force(
        nums
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 4, 5, -1, -3, -4]

    expected = [2, -1, 4, -3, 5, -4]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, -1, -3, -4, 2, 3]

    expected = [1, -1, 2, -3, 3, -4]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, 5, -3, -4]

    expected = [5, -1, -2, -3, -4]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [8, 3, 2, -7]

    expected = [8, -7, 3, 2]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, 4, -4, 4, -4, 4]

    expected = [4, -4, 4, -4, 4, -4]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = [1]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 1, 2, 4]

    expected = [3, 1, 2, 4]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 10_000, -10_000, 10_000, 10_000]

    expected = [10_000, -10_000, 10_000, -10_000, 10_000]
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000] * 99_999 + [10_000]

    expected = [10_000] + [-10_000] * 99_999
    result = rearrange_array_elements_by_sign_unequal_counts_brute_force(nums)

    assert result == expected
    print("Expected: one positive followed by 99,999 negative values")
    print(f"Result length: {len(result)}")


if __name__ == "__main__":
    solve()
