"""Subsets I — Subset Sums

Given an array nums of n integers, return a list containing the sum of every
subset of nums. The output may be returned in any order.

Each array position may be selected at most once. Include the empty subset,
whose sum is zero. Preserve repeated sums: different position selections
contribute separate entries even if their sums are equal.

Example 1:
    Input: nums = [2, 3]
    Output: [0, 2, 3, 5]
    Explanation:
        The empty subset has sum 0.
        [2] has sum 2.
        [3] has sum 3.
        [2, 3] has sum 5.

Example 2:
    Input: nums = [5, 2, 1]
    Output: [0, 1, 2, 3, 5, 6, 7, 8]
    Explanation:
        The empty subset has sum 0.
        The single-element subsets have sums 5, 2, and 1.
        [2, 1], [5, 1], and [5, 2] have sums 3, 6, and 7.
        [5, 2, 1] has sum 8.

Example 3:
    Input: nums = [1]
    Output: [0, 1]

Constraints:
    - 1 <= len(nums) <= 15
    - 0 <= nums[i] <= 10**4
"""


def subset_sums(nums: list[int]) -> list[int]:
    """Return one sum for every subset of input positions, including empty.

    Args:
        nums: Integers under the module's constraints. Zeros and duplicate
            values are allowed. The input list is not modified.

    Returns:
        A list of 2**n sums, where n = len(nums). The empty subset contributes
        zero. Equal sums from different selections remain separate entries.
        The current search visits inclusion before exclusion; the problem
        allows any output order, so the result is not sorted.

    Approach:
        Depth-First Search using include/exclude recursion.
        1. Initialize the output and start at index zero with a sum of zero.
        2. When index == len(nums), all positions have been considered.
           Append the accumulated sum and return. The last valid index is
           len(nums) - 1, so it must be processed before this stopping point.
        3. Include nums[index] by recursing to index + 1 with its value added
           to subset_sum. Passing the new integer leaves the parent's sum
           unchanged; there is no working subset list to copy or restore.
        4. Exclude nums[index] by recursing to index + 1 with the unchanged
           sum. Both branches advance the index, using each position at most
           once. Do not skip equal values: different position selections
           must contribute separately, even when their sums are identical.
        5. Return the collected sums after both branches finish. The path
           that excludes every element records the empty subset's sum, zero.

        Example walkthrough:
            For nums=[2, 3], include 2 and include 3 to record 5; include 2
            and exclude 3 to record 2; exclude 2 and include 3 to record 3;
            exclude both to record 0. The returned list is [5, 2, 3, 0].

    Examples:
        >>> subset_sums([2, 3])
        [5, 2, 3, 0]
        >>> subset_sums([1])
        [1, 0]
        >>> subset_sums([0])
        [0, 0]
        >>> subset_sums([2, 2])
        [4, 2, 2, 0]

    Time Complexity:
        O(2**n), where n = len(nums). Every position offers two choices,
        producing 2**n leaves and 2**(n + 1) - 1 calls in total. Each call
        does constant work, with amortized O(1) appends at leaves. Only an
        integer sum is saved, so there is no O(n) subset-copying factor.
        Integer arithmetic is constant time under the stated constraints.

    Space Complexity:
        O(2**n) total space for the returned sums and recursion stack.
        The output contains exactly 2**n entries. The stack uses O(n)
        auxiliary space: only one path of n + 1 calls is active at a time,
        and each call holds its index and sum. No subset lists are built.
    """
    # Step 1: Initialize the input size and output.
    size: int = len(nums)
    result: list[int] = []

    def generate_subset_sums(index: int, subset_sum: int) -> None:
        # Step 2: Record one sum after deciding on every position.
        if index == size:
            result.append(subset_sum)
            return

        # Step 3: Include this value without modifying the parent sum.
        generate_subset_sums(index=index + 1, subset_sum=subset_sum + nums[index])
        # Step 4: Exclude this value, preserving repeated sums.
        generate_subset_sums(index=index + 1, subset_sum=subset_sum)

    # Steps 1 and 5: Explore from sum zero and return every recorded sum.
    generate_subset_sums(index=0, subset_sum=0)

    return result


def solve() -> None:
    nums: list[int] = [2, 3]
    expected: list[int] = [0, 2, 3, 5]
    result: list[int] = subset_sums(nums)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    from math import comb

    # Minimum length and minimum value: both selections sum to zero.
    nums = [0]
    expected = [0, 0]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive value.
    nums = [1]
    expected = [0, 1]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single maximum value.
    nums = [10_000]
    expected = [0, 10_000]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal example with unsorted input.
    nums = [5, 2, 1]
    expected = [0, 1, 2, 3, 5, 6, 7, 8]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values preserve repeated sums.
    nums = [2, 2]
    expected = [0, 2, 2, 4]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different selections can have the same sum.
    nums = [1, 2, 3]
    expected = [0, 1, 2, 3, 3, 4, 5, 6]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input has the same subset sums.
    nums = [3, 2, 1]
    expected = [0, 1, 2, 3, 3, 4, 5, 6]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero at the beginning doubles each sum.
    nums = [0, 2, 3]
    expected = [0, 0, 2, 2, 3, 3, 5, 5]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero in the middle doubles each sum.
    nums = [2, 0, 3]
    expected = [0, 0, 2, 2, 3, 3, 5, 5]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero at the end doubles each sum.
    nums = [2, 3, 0]
    expected = [0, 0, 2, 2, 3, 3, 5, 5]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All identical positive values count selections by position.
    nums = [1, 1, 1]
    expected = [0, 1, 1, 1, 2, 2, 2, 3]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed minimum and maximum values.
    nums = [10_000, 0, 10_000]
    expected = [0, 0, 10_000, 10_000, 10_000, 10_000, 20_000, 20_000]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of zeros produces 32768 zero sums.
    nums = [0] * 15
    expected = [0] * (2**15)
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of ones preserves binomial multiplicities.
    nums = [1] * 15
    expected = [total for total in range(16) for _ in range(comb(15, total))]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and values reach the maximum sum of 150000.
    nums = [10_000] * 15
    expected = [10_000 * count for count in range(16) for _ in range(comb(15, count))]
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with distinct values and overlapping sum ranges.
    nums = [2**index for index in range(14)] + [10_000]
    expected = sorted(list(range(2**14)) + list(range(10_000, 10_000 + 2**14)))
    result = subset_sums(nums)

    assert sorted(result) == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
