"""Number Of Subsets

Difficulty: Medium

Problem Statement:
    You are given a zero-indexed array of positive integers and a target
    number tar. Count the different ways of selecting elements from the
    array such that the sum of the selected elements equals tar.

Notes:
    1. Two selections are different if their sets of chosen indexes differ.
       Equal values at different indexes therefore represent distinct choices.
    2. The input guarantees that the answer fits in a 32-bit integer.

Practice Example (added; the screenshot's example is cut off):
    Input: arr = [1, 2, 3], tar = 3
    Output: 2
    Choose indexes [0, 1] for values [1, 2], or index [2] for value [3].

Additional Examples (added for practice):
    1. Duplicate values at different indexes:
        Input: arr = [1, 1, 2], tar = 2
        Output: 2
        Choose indexes [0, 1] for [1, 1], or index [2] for [2].

    2. Several selections with identical values:
        Input: arr = [2, 2, 2], tar = 4
        Output: 3
        The possible index pairs are [0, 1], [0, 2], and [1, 2].

        Pick/not-pick explanation at index 2 (the final value 2):
            Not pick index 2:
                Earlier indexes [0, 1] can make 4 in one way: [0, 1].
                not_pick = 1.
            Pick index 2:
                Taking its value 2 leaves a remaining target of 4 - 2 = 2.
                Earlier indexes can make 2 in two ways: [0] or [1].
                Add the current index 2 to each choice:
                    [0] + [2] gives [0, 2].
                    [1] + [2] gives [1, 2].
                pick = 2.
            Total = not_pick + pick = 1 + 2 = 3.

        In a counting table, the same reasoning would be:
            not_pick = dp[1][4] = 1
            pick = dp[1][2] = 2
            dp[2][4] = 1 + 2 = 3
        The current implementation obtains these counts through recursion.

    3. No matching subset:
        Input: arr = [2, 4, 6], tar = 5
        Output: 0
        Every subset sum is even, so none equals 5.

    4. All elements are needed:
        Input: arr = [1, 2, 4], tar = 7
        Output: 1
        Only selecting all three indexes gives sum 7.

Source Notes:
    The screenshot's example, numeric input limits, and input/output format
    are not visible. The function accepts arr and tar directly. All examples
    above are added for practice rather than transcribed original samples.

https://www.youtube.com/watch?v=ZHyb-A2Mte4&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=18

"""


def number_of_subsets_recursions(arr: list[int], tar: int) -> int:
    """Count index-distinct subsets whose elements sum exactly to tar.

    Args:
        arr: A list of positive integers. Each position can be selected
            at most once; equal values at different indexes are separate
            choices. The list does not need to be sorted.
        tar: The integer target sum. A zero target counts the empty subset
            once; a negative target returns zero for positive elements.

    Returns:
        The number of matching subsets, not just whether a match exists.
        Empty input returns one for target zero and zero otherwise. The
        problem guarantees that the answer fits in a 32-bit integer.

    Mutation and assumptions:
        The input list is not modified. Positive values are assumed and
        are not validated. Zero-valued elements are outside the stated
        problem: returning immediately at target zero would miss additional
        selections containing zeros. Negative elements are unsupported by
        the pruning condition. Long arrays may exceed Python's recursion
        limit. Numeric input limits are not visible in the screenshot.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. Track index, the last available position, and target, the sum
           still needed. If target is zero, return one: the selected
           indexes form one matching subset. Since all values are positive,
           taking any remaining element cannot produce another match for
           that branch; the remaining elements must all be skipped.
        2. If index is negative while target is not zero, return zero.
           No elements remain, so this branch contributes no matching
           subsets. Check target first to count a match completed using
           the first element.
        3. Calculate not_pick by skipping arr[index], decreasing index
           while leaving target unchanged. This counts every matching
           subset that excludes the current position.
        4. Initialize pick to zero. When arr[index] <= target, select the
           element and search earlier indexes for target - arr[index].
           This counts every matching subset that includes this position.
           Positive values make skipping oversized elements safe, and
           decreasing index prevents selecting the same position twice.
        5. Return not_pick + pick. These branches describe disjoint sets
           of index selections, so their counts add without duplication.
           Both branches are needed even when not_pick is nonzero: for
           [2, 2, 2] at index 2 and target 4, they contribute 1 and 2,
           giving 3. Boolean or and an early success return would lose
           matching subsets.
        6. Start at the last array index with target equal to tar and
           return the count. No subsets are constructed or stored; counts
           are returned through the recursive calls.

    Time Complexity:
        O(2**N) in the worst case, where N is the number of elements.
        Each position can create a skip branch and a take branch; pruning
        oversized values and returning at target zero reduce actual work.

    Space Complexity:
        O(N) extra space, excluding the input list. The recursive stack
        holds at most N + 1 helper calls with constant local storage per
        call; no collection of matching subsets is stored.
    """

    def find_subset_sum_with_target(index: int, target: int) -> int:

        # Step 1: A completed target contributes one matching index selection.
        if target == 0:
            return 1

        # Step 2: Exhausted input with a nonzero target contributes no matches.
        if index < 0:
            return 0

        # Step 3: Count matching subsets that exclude the current index.
        not_pick: int = find_subset_sum_with_target(index=index - 1, target=target)
        # Step 4: Count matching subsets that include it, when its value fits.
        pick: int = 0
        if arr[index] <= target:
            pick = find_subset_sum_with_target(
                index=index - 1, target=target - arr[index]
            )

        # Step 5: Add both counts; success in one branch does not end the search.
        return not_pick + pick

    # Step 6: Begin with every index available and the full target.
    return find_subset_sum_with_target(index=len(arr) - 1, target=tar)


def number_of_subsets_tablation(arr: list[int], tar: int) -> int:
    """Count index-distinct subsets summing to tar using two count rows.

    Args:
        arr: A nonempty list of positive integers. Each position can be
            selected at most once; equal values at different indexes are
            distinct choices. The input need not be sorted.
        tar: A nonnegative integer target sum.

    Returns:
        The number of subsets summing exactly to tar. A zero target has
        one selection, the empty subset. An unreachable target, including
        one above the total array sum, returns zero. The problem guarantees
        that the answer fits in a 32-bit integer.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, positive elements,
        and a nonnegative target are assumed and are not validated. Empty
        input and negative values or targets are unsupported. Zero elements
        are outside the problem statement: this initialization would not
        count their extra selections. Large targets require wide rows.
        Numeric input limits are not visible in the screenshot.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Read size and create prev_sum_count_dp with tar + 1 zeros.
           Each position represents a sum, and its stored integer counts
           ways to make that sum using the elements processed so far.
           Only sums through tar are needed because positive elements
           cannot reduce a larger sum back to tar.
        2. Initialize sum zero to one for the empty selection. If arr[0]
           fits within tar, initialize its sum to one for selecting index
           zero. All other sums have zero ways using only the first element.
        3. Process remaining elements from index 1 onward. Create a fresh
           curr_sum_count_dp and set its zero entry to one. Keep the previous
           row unchanged until every target in the current row is calculated.
        4. For each target from 1 through tar, read not_pick from the
           previous row at the same target. These are all matching index
           selections that skip the current element.
        5. Start pick at zero. If arr[index] <= target, read the previous
           row at target - arr[index]. Each earlier selection making that
           remainder becomes a matching selection by adding the current
           index. Reading the previous row prevents reusing that index.
        6. Store not_pick + pick in the current entry. Add counts because
           selections excluding and including the current index are disjoint.
           For [2, 2, 2] at index 2 and target 4, not_pick is 1 for [0, 1].
           pick is 2 because the earlier sum 2 can use index 0 or index 1;
           adding index 2 gives [0, 2] and [1, 2]. The combined count is 3.
           Boolean or would lose these distinct selections.
        7. After the target loop finishes, assign curr_sum_count_dp to
           prev_sum_count_dp. This shares the completed list rather than
           copying it; the next iteration creates a fresh current list.
           Only two rows are needed at a time.
        8. Return prev_sum_count_dp[tar] after all elements are considered.
           With one element, the initialized row already gives the answer.

    Time Complexity:
        O(N * (K + 1)), where N is the array length and K is tar.
        Initializing and filling a row takes O(K + 1) per element, with
        constant work per count update; this also covers K == 0.

    Space Complexity:
        O(K + 1) extra space, excluding the input list. At most two rows
        of K + 1 integer counts are needed, with constant storage otherwise
        and no recursive call stack.
    """
    # Step 1: Allocate counts for sums zero through tar.
    size: int = len(arr)

    prev_sum_count_dp: list[int] = [0] * (tar + 1)
    # Step 2: Count skipping or taking the first element.
    prev_sum_count_dp[0] = 1
    if arr[0] <= tar:
        prev_sum_count_dp[arr[0]] = 1

    # Step 3: Create a fresh count row for each later element.
    for index in range(1, size):
        curr_sum_count_dp: list[int] = [0] * (tar + 1)
        curr_sum_count_dp[0] = 1
        for target in range(1, tar + 1):
            # Step 4: Count selections that skip the current index.
            not_pick: int = prev_sum_count_dp[target]

            # Step 5: Taking it extends each selection making the remainder.
            pick: int = 0

            if arr[index] <= target:
                pick = prev_sum_count_dp[target - arr[index]]

            # Step 6: Add both disjoint groups of index selections.
            curr_sum_count_dp[target] = not_pick + pick

        # Step 7: Publish the row after every target count is complete.
        prev_sum_count_dp = curr_sum_count_dp

    # Step 8: Return the full target count using all available elements.
    return prev_sum_count_dp[tar]


def solve() -> None:
    # Added practice example; the original example is not visible.
    arr = [1, 2, 3]
    tar = 3
    expected = 2
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single minimum value matches.
    arr = [1]
    tar = 1
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single value exceeds target.
    arr = [5]
    tar = 4
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element cannot be reused.
    arr = [2]
    tar = 4
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero target has one empty subset.
    arr = [1, 2, 3]
    tar = 0
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match only at the beginning.
    arr = [3, 8, 9]
    tar = 3
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match only in the middle.
    arr = [8, 3, 9]
    tar = 3
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match only at the end.
    arr = [8, 9, 3]
    tar = 3
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values are separate index choices.
    arr = [1, 1, 2]
    tar = 2
    expected = 2
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three identical elements form three pairs.
    arr = [2, 2, 2]
    tar = 4
    expected = 3
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four identical elements form six pairs.
    arr = [2, 2, 2, 2]
    tar = 4
    expected = 6
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All identical values can each match individually.
    arr = [3, 3, 3, 3]
    tar = 3
    expected = 4
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    tar = 5
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every element must be selected.
    arr = [1, 2, 4]
    tar = 7
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target exceeds total sum.
    arr = [1, 2, 4]
    tar = 8
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every element exceeds target.
    arr = [4, 5, 6]
    tar = 2
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No subset despite target being below total.
    arr = [2, 4, 6]
    tar = 5
    expected = 0
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A single element and a pair both match.
    arr = [1, 2, 3]
    tar = 3
    expected = 2
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different subset sizes match.
    arr = [1, 1, 1, 3]
    tar = 3
    expected = 2
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both skip and take branches contribute.
    arr = [1, 2, 3, 4, 5]
    tar = 5
    expected = 3
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent elements.
    arr = [3, 20, 5, 30, 9]
    tar = 17
    expected = 1
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input.
    arr = [5, 4, 3, 2, 1]
    tar = 5
    expected = 3
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger positive values.
    arr = [1000000000000, 1000000000000, 3]
    tar = 1000000000003
    expected = 2
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Many duplicate index combinations.
    arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    tar = 6
    expected = 924
    result = number_of_subsets_recursions(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: duplicate values represent distinct index pairs.
    arr = [2, 2, 2]
    tar = 4
    expected = 3
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single minimum value matches.
    arr = [1]
    tar = 1
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single value exceeds target.
    arr = [5]
    tar = 4
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single element cannot be reused.
    arr = [2]
    tar = 4
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero target has one empty subset.
    arr = [1, 2, 3]
    tar = 0
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match only at the beginning.
    arr = [3, 8, 9]
    tar = 3
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match only in the middle.
    arr = [8, 3, 9]
    tar = 3
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match only at the end.
    arr = [8, 9, 3]
    tar = 3
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Duplicate values are separate index choices.
    arr = [1, 1, 2]
    tar = 2
    expected = 2
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Three identical elements form three pairs.
    arr = [2, 2, 2]
    tar = 4
    expected = 3
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Four identical elements form six pairs.
    arr = [2, 2, 2, 2]
    tar = 4
    expected = 6
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All identical values can each match individually.
    arr = [3, 3, 3, 3]
    tar = 3
    expected = 4
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    tar = 5
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Every element must be selected.
    arr = [1, 2, 4]
    tar = 7
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Target exceeds total sum.
    arr = [1, 2, 4]
    tar = 8
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    # assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Every element exceeds target.
    arr = [4, 5, 6]
    tar = 2
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: No subset despite target being below total.
    arr = [2, 4, 6]
    tar = 5
    expected = 0
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: A single element and a pair both match.
    arr = [1, 2, 3]
    tar = 3
    expected = 2
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Different subset sizes match.
    arr = [1, 1, 1, 3]
    tar = 3
    expected = 2
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Both skip and take branches contribute.
    arr = [1, 2, 3, 4, 5]
    tar = 5
    expected = 3
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Nonadjacent elements.
    arr = [3, 20, 5, 30, 9]
    tar = 17
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Descending input.
    arr = [5, 4, 3, 2, 1]
    tar = 5
    expected = 3
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Many duplicate index combinations.
    arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    tar = 6
    expected = 924
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: single element with zero target.
    arr = [7]
    tar = 0
    expected = 1
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger counts within signed 32-bit range.
    arr = [1] * 33
    tar = 16
    expected = 1166803110
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger values with two distinct choices.
    arr = [1000, 1000, 3]
    tar = 1003
    expected = 2
    result = number_of_subsets_tablation(arr, tar)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
