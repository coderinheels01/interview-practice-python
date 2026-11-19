"""Partitions With Given Difference

Difficulty: Medium

Problem Statement:
    Given an array ARR, partition it into two subsets, possibly empty,
    such that together they contain all elements of the original array.
    Let their sums be S1 and S2.

    Given a difference D, count the partitions for which S1 >= S2 and
    S1 - S2 == D. Return the count modulo 10**9 + 7.

    Each array position belongs to exactly one subset. Selections using
    different sets of indexes are distinct, even when values are equal.
    The two subsets are identified as the first and second subset.

Practice Example (added; no original example is visible):
    Input: arr = [1, 2, 3], d = 2
    Output: 1
    The first subset [1, 3] sums to 4, and the second subset [2] sums
    to 2. Their difference is 2. No other partition has this difference.

Additional Examples (added for practice):
    1. Duplicate values give distinct index selections:
        Input: arr = [1, 1, 2], d = 2
        Output: 2
        Either occurrence of 1 can form the second subset. The first
        subset contains the other 1 and the 2, giving sums 3 and 1.

    2. Equal sums:
        Input: arr = [1, 1], d = 0
        Output: 2
        The first subset can contain index 0 and the second index 1,
        or the first can contain index 1 and the second index 0.

    3. An empty second subset:
        Input: arr = [2, 3], d = 5
        Output: 1
        Put both elements in the first subset and leave the second empty.
        Their sums are 5 and 0.

    4. No valid partition:
        Input: arr = [1, 2, 3], d = 1
        Output: 0
        The total is 6. No two integer subset sums adding to 6 differ by 1.

Source Notes:
    Numeric constraints, input/output format, and examples are not visible
    in the screenshot. The formal definition of distinct partitions is
    partially cut off and contains inconsistent subset labels in the visible
    text; the index-based interpretation is stated above. All examples are
    added for practice. The function accepts arr and d directly.

    https://www.youtube.com/watch?v=zoilQD1kYSg&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=19
"""


def partitions_with_given_difference_recursion(arr: list[int], d: int) -> int:
    """Count partitions with difference d using recursive subset selection.

    Args:
        arr: A list of nonnegative integers. Each index belongs to exactly
            one of two identified subsets. Duplicate values are separate
            choices, and either subset may be empty.
        d: A nonnegative required difference S1 - S2, with S1 >= S2.

    Returns:
        The number of index-distinct partitions modulo 10**9 + 7.
        Impossible differences return zero. Empty input returns one for
        d == 0 and zero otherwise, although the prompt does not specify
        whether empty input is allowed. Swapping different index groups
        when d == 0 counts as a different assignment to the identified groups.

    Mutation and assumptions:
        The input is not modified. Nonnegative integer elements and d are
        assumed and are not validated. Negative values are unsupported by
        the pruning condition. Long arrays may exceed Python's recursion
        limit. Numeric input limits are not visible in the screenshot.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. Calculate size, total_sum, and smaller_subset_sum. Since
           S1 + S2 = total_sum and S1 - S2 = d, subtracting the equations
           gives 2 * S2 = total_sum - d. Therefore S2 must equal
           (total_sum - d) / 2. Each subset of indexes forming S2 leaves
           exactly one complementary S1. Choosing the smaller target also
           avoids considering unnecessarily large remaining sums.
        2. Reject a negative smaller sum or an odd total_sum - d. An odd
           remainder would require a fractional subset sum. Integer division
           rounds down, so it cannot replace this check: total 6 and d 1
           require 2.5, not the rounded-down value 2.
        3. In count_ways, track the last available index and remaining
           target. Only stop when index is negative: return one if target
           is zero, otherwise zero. Index zero still has arr[0] available.
           A target of zero with elements remaining must keep recursing
           because each remaining zero can be selected or skipped.
        4. Calculate not_take by skipping the current position and searching
           earlier indexes with the same target. This counts all valid
           selections excluding the current index.
        5. Initialize take to zero. If arr[index] <= target, select the
           element and search earlier indexes for target - arr[index].
           Decreasing index prevents reuse. Positive elements are skipped
           when target is zero, but a zero fits and creates a second branch.
        6. Add not_take and take and apply modulo 10**9 + 7. The branches
           represent disjoint index selections, so both counts contribute.
           For [0, 0] and target zero, skipping the second zero yields two
           selections of the first; taking it yields another two, totaling
           four. Each completed branch returns one only after all positions
           have been processed.
        7. Begin at size - 1 with smaller_subset_sum as the target and
           return the count. The recursion tracks numbers and indexes
           rather than constructing or storing the actual partitions.

    Time Complexity:
        O(2**N) in the worst case, where N is the array length. Each element
        can create a take and skip branch; impossible differences return
        after the O(N) total-sum calculation.

    Space Complexity:
        O(N) extra space, excluding the input list. The recursive stack
        holds at most N + 1 helper calls with constant local storage per
        call; no collection of subsets is stored.
    """
    # Step 1: Reduce the partition count to subsets forming the smaller sum.
    size: int = len(arr)
    total_sum: int = sum(arr)
    smaller_subset_sum: int = (total_sum - d) // 2

    # Step 2: Reject negative or fractional required subset sums.
    if smaller_subset_sum < 0 or (total_sum - d) % 2 != 0:
        return 0

    def count_ways(index: int, target: int) -> int:

        # Step 3: Count a completed selection only after every index is processed.
        if index < 0:
            return 1 if target == 0 else 0

        # Step 4: Count selections excluding the current index.
        not_take: int = count_ways(index=index - 1, target=target)

        # Step 5: Count selections including it when its value fits, including zero.
        take: int = 0

        if arr[index] <= target:
            take = count_ways(index=index - 1, target=target - arr[index])

        # Step 6: Add the disjoint branch counts and apply the required modulus.
        return (not_take + take) % (10**9 + 7)

    # Step 7: Start with all indexes available and the smaller group target.
    return count_ways(index=size - 1, target=smaller_subset_sum)


def partitions_with_given_difference(arr: list[int], d: int) -> int:
    """Count index-distinct partitions with difference d, modulo 10**9 + 7.

    Args:
        arr: A nonempty list of nonnegative integers. Each position goes
            into exactly one of two identified subsets. Equal values at
            different positions are separate choices; zeros are supported.
        d: A nonnegative difference required between the larger subset
            sum S1 and the smaller subset sum S2.

    Returns:
        The number of partitions with S1 >= S2 and S1 - S2 == d, reduced
        modulo 10**9 + 7. Impossible differences return zero. Empty subsets
        are allowed; when d is zero, different index assignments to the
        identified groups remain distinct, including swapped groups.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, nonnegative integer
        elements, and nonnegative d are assumed and are not validated.
        Empty input and negative values are unsupported. Large target sums
        require wide rows. Numeric input limits are not visible in the prompt.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Calculate size and total_sum. The group sums satisfy
           S1 + S2 = total_sum and S1 - S2 = d. Subtracting the second
           equation from the first gives 2 * S2 = total_sum - d, so the
           required smaller sum is (total_sum - d) / 2. Each index subset
           making S2 determines exactly one partition: all remaining indexes
           form S1. Many different subsets can make this same fixed sum.
           Counting S1 would also work, but S2 uses a smaller DP row and
           fewer target updates when d is positive.
        2. Reject a negative smaller sum or an odd total_sum - d. With
           nonnegative elements S2 cannot be negative, and twice an integer
           sum must be even. Integer division alone is insufficient because
           it rounds a fractional target down rather than rejecting it.
        3. Create prev_subset_sum_dp with one count per sum from zero to
           smaller_subset_sum. Set the zero count to one for skipping the
           first element, and add one at its value if it fits for taking
           it. When the first value is zero, these are two different index
           selections making zero, so that entry correctly becomes two.
        4. For each later element, create a fresh zero-filled current row.
           Visit every target including zero so later zeros are counted.
           Keep the previous row unchanged until this entire row is ready.
        5. Read not_take from the previous row at the same target. These
           selections exclude the current position. If the element fits,
           read take at target - arr[index]; these earlier selections make
           the remainder and become matches by including the current index.
           Reading the previous row prevents reusing an index.
        6. Add not_take and take, then reduce modulo 10**9 + 7. These are
           disjoint groups of selections, so both contribute. A zero makes
           both lookups read the same count and therefore doubles it: each
           existing selection can skip or take that zero. The modulus is
           required by the question and keeps stored counts bounded.
        7. After every target is calculated, assign curr_subset_sum_dp to
           prev_subset_sum_dp. This shares the completed list rather than
           copying it; the next iteration creates a fresh current list.
           Only the previous and current rows are needed at a time.
        8. Return the count for smaller_subset_sum. For [1, 1, 2] and d = 2,
           that sum is 1. Either index containing 1 can form S2, leaving
           sum 3 for S1, so there are two partitions.

    Time Complexity:
        O(N * (T + 1)) for valid targets, where N is the array length and
        T = (sum(arr) - d) // 2. Each element creates and fills a row with
        constant work per entry; impossible differences return after O(N).

    Space Complexity:
        O(T + 1) extra space for valid targets, excluding the input list.
        At most two rows of T + 1 counts are needed, with constant storage
        otherwise and no recursive call stack.
    """
    # Step 1: Calculate the total and derive the target for the smaller group.
    size: int = len(arr)
    total_sum: int = sum(arr)
    # S1 + S2 = total_sum and S1 - S2 = d, with S1 >= S2.
    # Subtract the second equation from the first:
    # (S1 + S2) - (S1 - S2) = total_sum - d
    # 2 * S2 = total_sum - d, hence S2 = (total_sum - d) / 2.
    # Count subsets making S2; their remaining indexes automatically form S1.
    # Different selections making this fixed sum give different partitions.
    # We choose S2 because it is no larger than S1, so its DP row needs
    # fewer entries (or the same number when d == 0). Counting S1 also works.
    # The following check rejects negative or fractional sums before using
    # this integer-divided value as a valid target.
    smaller_subset_sum: int = (total_sum - d) // 2

    # Step 2: Reject negative targets and remainders that are not even.
    if smaller_subset_sum < 0 or (total_sum - d) % 2 != 0:
        return 0

    # Step 3: Initialize skip/take counts for the first element, including zero.
    prev_subset_sum_dp: list[int] = [0] * (smaller_subset_sum + 1)
    prev_subset_sum_dp[0] = 1

    if arr[0] <= smaller_subset_sum:
        prev_subset_sum_dp[arr[0]] += 1

    # Step 4: Build a fresh row for each later element, including target zero.
    for index in range(1, size):
        curr_subset_sum_dp: list[int] = [0] * (smaller_subset_sum + 1)
        for target in range(smaller_subset_sum + 1):
            # Step 5: Count selections excluding or including the current index.
            not_take: int = prev_subset_sum_dp[target]

            take: int = 0

            if arr[index] <= target:
                take = prev_subset_sum_dp[target - arr[index]]

            # Step 6: Add both groups of selections and apply the required modulus.
            curr_subset_sum_dp[target] = (not_take + take) % (10**9 + 7)

        # Step 7: Publish the row after all target counts are complete.
        prev_subset_sum_dp = curr_subset_sum_dp

    # Step 8: Each selection for the smaller sum determines a valid partition.
    return prev_subset_sum_dp[smaller_subset_sum]


def solve() -> None:
    # Added practice example; no original example is visible.
    arr = [1, 2, 3]
    d = 2
    expected = 1
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive element with an empty second subset.
    arr = [5]
    d = 5
    expected = 1
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive element cannot form equal sums.
    arr = [2]
    d = 0
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Difference exceeds total by one.
    arr = [2, 3]
    d = 6
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Difference exceeds total with matching parity.
    arr = [2, 3]
    d = 7
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd remainder cannot form an integer subset sum.
    arr = [1, 2, 3]
    d = 1
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate indexes give distinct partitions.
    arr = [1, 1, 2]
    d = 2
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal sums count both index assignments.
    arr = [1, 1]
    d = 0
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All elements in the first subset.
    arr = [2, 3]
    d = 5
    expected = 1
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even remainder but no reachable target.
    arr = [2, 4]
    d = 0
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values forming equal halves.
    arr = [2, 2, 2, 2]
    d = 0
    expected = 6
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with unequal group sizes.
    arr = [2, 2, 2]
    d = 2
    expected = 3
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent choices for the smaller group.
    arr = [1, 2, 3, 4]
    d = 2
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero can go into either subset.
    arr = [0]
    d = 0
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two zeros have four index assignments.
    arr = [0, 0]
    d = 0
    expected = 4
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros with a positive difference.
    arr = [0, 0, 0]
    d = 1
    expected = 0
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Leading zero doubles a valid partition count.
    arr = [0, 1, 2]
    d = 1
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Middle zero doubles a valid partition count.
    arr = [1, 0, 2]
    d = 1
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Trailing zero doubles a valid partition count.
    arr = [1, 2, 0]
    d = 1
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple zeros with zero smaller sum.
    arr = [0, 0, 2]
    d = 2
    expected = 4
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zeros and duplicate positive elements.
    arr = [0, 0, 1, 1]
    d = 0
    expected = 8
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input.
    arr = [4, 3, 2, 1]
    d = 2
    expected = 2
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger values with a small reachable target.
    arr = [1000, 1002]
    d = 2
    expected = 1
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Modulo reduction for many zero assignments.
    arr = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    d = 0
    expected = 511620083
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Modulo reduction for many positive index choices.
    arr = [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ]
    d = 0
    expected = 846527861
    result = partitions_with_given_difference(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: duplicate indexes give distinct partitions.
    arr = [1, 1, 2]
    d = 2
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Single positive element with an empty second subset.
    arr = [5]
    d = 5
    expected = 1
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Single positive element cannot form equal sums.
    arr = [2]
    d = 0
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Difference exceeds total by one.
    arr = [2, 3]
    d = 6
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Difference exceeds total with matching parity.
    arr = [2, 3]
    d = 7
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Odd remainder cannot form an integer subset sum.
    arr = [1, 2, 3]
    d = 1
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Duplicate indexes give distinct partitions.
    arr = [1, 1, 2]
    d = 2
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Equal sums count both index assignments.
    arr = [1, 1]
    d = 0
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: All elements in the first subset.
    arr = [2, 3]
    d = 5
    expected = 1
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Even remainder but no reachable target.
    arr = [2, 4]
    d = 0
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Identical values forming equal halves.
    arr = [2, 2, 2, 2]
    d = 0
    expected = 6
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Identical values with unequal group sizes.
    arr = [2, 2, 2]
    d = 2
    expected = 3
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Nonadjacent choices for the smaller group.
    arr = [1, 2, 3, 4]
    d = 2
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Single zero can go into either subset.
    arr = [0]
    d = 0
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Two zeros have four index assignments.
    arr = [0, 0]
    d = 0
    expected = 4
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: All zeros with a positive difference.
    arr = [0, 0, 0]
    d = 1
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Leading zero doubles a valid partition count.
    arr = [0, 1, 2]
    d = 1
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Middle zero doubles a valid partition count.
    arr = [1, 0, 2]
    d = 1
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Trailing zero doubles a valid partition count.
    arr = [1, 2, 0]
    d = 1
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Multiple zeros with zero smaller sum.
    arr = [0, 0, 2]
    d = 2
    expected = 4
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Zeros and duplicate positive elements.
    arr = [0, 0, 1, 1]
    d = 0
    expected = 8
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Descending input.
    arr = [4, 3, 2, 1]
    d = 2
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: Larger values with a small reachable target.
    arr = [1000, 1002]
    d = 2
    expected = 1
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: zero remains after selecting the positive element.
    arr = [0, 1]
    d = 1
    expected = 2
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: two zeros remain after reaching target zero.
    arr = [0, 0, 1]
    d = 1
    expected = 4
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: odd total with zero requested difference.
    arr = [1]
    d = 0
    expected = 0
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recursion: several zero choices.
    arr = [0] * 12
    d = 0
    expected = 4096
    result = partitions_with_given_difference_recursion(arr, d)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
