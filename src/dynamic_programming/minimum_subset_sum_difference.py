"""Partition a Set into Two Subsets with Minimum Subset Sum Difference

Difficulty: Hard

Problem Statement:
    You are given an array containing N nonnegative integers. Partition
    this array into two subsets such that the absolute difference between
    their sums is minimum.

    Return the minimum absolute difference over all valid divisions of
    the array elements.

Notes:
    1. Each element of the array must belong to exactly one subset.
    2. Subsets do not need to be contiguous. For the array [1, 2, 3],
       possible divisions include [1, 2] and [3], or [1, 3] and [2].
    3. A subset's sum is the sum of all elements in that subset.

Example (using the array in the question's notes):
    Input: arr = [1, 2, 3]
    Output: 0

    The division [1, 2] and [3] has sums 3 and 3. Their absolute
    difference is 0, which is the minimum possible difference.

Additional Examples (added for practice):
    1. An odd total with a minimum difference of one:
        Input: arr = [1, 2, 4]
        Output: 1
        Divide into [1, 2] and [4], with sums 3 and 4.
        A difference of zero is impossible because the total is odd.

    2. An even total without an equal partition:
        Input: arr = [1, 2, 5]
        Output: 2
        Divide into [1, 2] and [5], with sums 3 and 5.
        No subset sums to 4, so an equal partition is impossible.

    3. Zero-valued elements:
        Input: arr = [0, 3, 0, 5]
        Output: 2
        Divide into [0, 3] and [0, 5], with sums 3 and 5.
        The zeros do not change either subset's sum.

    4. A dominant element:
        Input: arr = [20, 1, 2, 3]
        Output: 14
        Divide into [20] and [1, 2, 3], with sums 20 and 6.
        The smaller elements together cannot balance the value 20.

Source Notes:
    Numeric constraints and the input/output format are not visible in
    the screenshot. The function accepts the array directly; its length
    provides N. The example output is derived from the question's notes.

https://www.youtube.com/watch?v=GS_OqZb2CWc&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=17
"""


def minimum_subset_sum_difference(arr: list[int]) -> int:
    """Return the smallest absolute difference between two subset sums.

    Args:
        arr: A nonempty list of nonnegative integers. Each position must
            belong to exactly one subset; duplicate values are separate
            elements. Subsets may have different sizes and need not be
            contiguous. The input need not be sorted.

    Returns:
        The minimum absolute difference over all partitions. An equal
        partition returns zero. All-zero input returns zero; a single
        element returns its value, using an empty complementary subset.

    Mutation and assumptions:
        The input list is not modified. Nonempty input and nonnegative
        integers are assumed and are not validated. Empty input and
        negative values are unsupported. Large total sums require wide
        rows. Numeric limits are not visible in the problem statement.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Calculate size and total_sum. Create prev_subset_sum with
           total_sum + 1 False entries, one for each possible sum from
           zero through the total. A True entry means that sum can be
           formed using the elements processed so far; the index itself
           represents the numeric sum.
        2. Initialize sums zero and arr[0] to True. These represent
           skipping or taking the first element. If that element is zero,
           both assignments correctly mark the same entry.
        3. Process remaining elements from index 1 onward. For each, create
           a fresh curr_subset_sum and mark zero True. Keep the previous
           row unchanged while calculating every target through total_sum,
           including the endpoint.
        4. For each target, read not_pick from the previous row at that
           same target. Skipping the current element preserves any sum
           reachable using earlier elements.
        5. Start pick as False. If arr[index] <= target, read the previous
           row at target - arr[index]. Taking 2 toward a target of 5
           succeeds if earlier elements can form 3. Reading the previous
           row prevents using one position repeatedly; a zero value also
           reads the previous row without creating a dependency on itself.
        6. Store pick or not_pick at the current target. After every
           target is calculated, assign curr_subset_sum to prev_subset_sum.
           This shares the completed row rather than copying it; the next
           iteration creates a fresh current row. Only two rows are needed.
        7. Initialize min_subset_sum_diff to total_sum, a valid difference
           obtained by putting every element in one subset and none in
           the other. This also works when all values are zero.
        8. Check reachable sums from zero through total_sum // 2 inclusive.
           Every partition has a smaller subset sum at most half the total,
           so larger sums would repeat the same divisions in reverse.
           Include the half-sum endpoint so an exact equal partition is
           considered, such as sum 5 for [3, 5, 2].
        9. For each reachable possible_sum, set sum_1 to that sum and
           sum_2 to total_sum - sum_1. The remaining elements automatically
           form the second subset. Compare abs(sum_1 - sum_2) with the
           smallest difference so far, then return the smallest found.

    Time Complexity:
        O(N * (S + 1)), where N is the array length and S is its total sum.
        Creating and filling a row takes O(S + 1) per element; the final
        half-sum scan takes O(S + 1). This also covers all-zero input.

    Space Complexity:
        O(S + 1) extra space, excluding the input list. At most two boolean
        rows of S + 1 entries are needed, while other variables use constant
        space and there is no recursive call stack.
    """
    # Step 1: Allocate reachability entries for sums zero through the total.
    size: int = len(arr)
    total_sum: int = sum(arr)
    prev_subset_sum: list[bool] = [False] * (total_sum + 1)

    # Step 2: Initialize the choices to skip or take the first element.
    prev_subset_sum[0] = True
    prev_subset_sum[arr[0]] = True

    # Step 3: Build a fresh row for each later element, keeping zero reachable.
    for index in range(1, size):
        curr_subset_sum: list[bool] = [False] * (total_sum + 1)
        curr_subset_sum[0] = True

        for target in range(1, (total_sum + 1)):
            # Step 4: Skip this element and preserve the same reachable sum.
            not_pick: bool = prev_subset_sum[target]

            # Step 5: Taking it needs a reachable remainder in the previous row.
            pick: bool = False

            if arr[index] <= target:
                pick = prev_subset_sum[target - arr[index]]

            # Step 6: Either choice can establish reachability of this target.
            curr_subset_sum[target] = pick or not_pick
        # Step 6: Publish the completed row only after every target is filled.
        prev_subset_sum = curr_subset_sum

    # Step 7: Start with the valid difference between all elements and none.
    min_subset_sum_diff: int = total_sum

    # Step 8: Include the half-sum endpoint and avoid mirrored partitions.
    for possible_sum in range(total_sum // 2 + 1):
        if prev_subset_sum[possible_sum]:
            # Step 9: Compare this reachable split with the best difference.
            sum_1: int = possible_sum
            sum_2: int = total_sum - sum_1
            min_subset_sum_diff = min(min_subset_sum_diff, abs(sum_1 - sum_2))

    return min_subset_sum_diff


def solve() -> None:
    # Array from the question's notes.
    arr = [1, 2, 3]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero.
    arr = [0]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive element.
    arr = [7]
    expected = 7
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal minimum positive values.
    arr = [1, 1]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two unequal values.
    arr = [2, 7]
    expected = 5
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros.
    arr = [0, 0, 0, 0]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero before positive values.
    arr = [0, 3, 5]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero between positive values.
    arr = [3, 0, 5]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero after positive values.
    arr = [3, 5, 0]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One positive value among zeros.
    arr = [0, 0, 7, 0]
    expected = 7
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact half at the search endpoint.
    arr = [3, 5, 2]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd total with closest sums differing by one.
    arr = [1, 2, 4]
    expected = 1
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd total with a larger unavoidable difference.
    arr = [2, 2, 7]
    expected = 3
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even total without an equal partition.
    arr = [1, 2, 5]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated identical values with an even count.
    arr = [3, 3, 3, 3]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated identical values with an odd count.
    arr = [2, 2, 2]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A dominant value exceeds all remaining values combined.
    arr = [20, 1, 2, 3]
    expected = 14
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different subset sizes.
    arr = [1, 5, 11, 5]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent selections.
    arr = [1, 4, 2, 5]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest value appears first.
    arr = [6, 1, 2, 3]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest value appears in the middle.
    arr = [1, 6, 2, 3]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest value appears last.
    arr = [1, 2, 3, 6]
    expected = 0
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A value must not be reused.
    arr = [2, 6]
    expected = 4
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger values.
    arr = [1000, 1002]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Many repeated values.
    arr = [
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
    ]
    expected = 2
    result = minimum_subset_sum_difference(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
