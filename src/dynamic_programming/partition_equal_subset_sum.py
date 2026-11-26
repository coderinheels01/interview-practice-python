"""Partition Equal Subset Sum

Difficulty: Medium

Problem Statement:
    You are given an array ARR of N positive integers. Determine whether
    the array can be partitioned into two subsets such that the sum of
    elements in both subsets is equal.

Example:
    Input: ARR = [2, 3, 3, 3, 4, 5]
    Output: True    

    The array can be partitioned into [2, 3, 5] and [3, 3, 4],
    each with sum 10.

Additional Examples (added for practice):
    1. Two equal elements:
        Input: ARR = [1, 1]
        Output: True
        Partition into [1] and [1], each with sum 1.

    2. A single element:
        Input: ARR = [4]
        Output: False
        The element cannot be split between two equal-sum subsets.

    3. An odd total:
        Input: ARR = [1, 2, 4]
        Output: False
        The total is 7, which cannot be divided into equal integer sums.

    4. An even total with no valid partition:
        Input: ARR = [1, 2, 5]
        Output: False
        The possible subset sums are 0, 1, 2, 3, 5, 6, 7, and 8.
        None is 4, so two equal sums are impossible.

    5. Different subset sizes:
        Input: ARR = [1, 5, 11, 5]
        Output: True
        Partition into [11] and [1, 5, 5], each with sum 11.
        The subsets do not need the same number of elements.

    6. All-identical values:
        Input: ARR = [3, 3, 3, 3]
        Output: True
        Partition into [3, 3] and [3, 3], each with sum 6.

    7. An even total with identical values but no valid partition:
        Input: ARR = [2, 2, 2]
        Output: False
        Each subset sum is even, so neither subset can have sum 3.

    8. Nonadjacent elements in each subset:
        Input: ARR = [1, 2, 3, 4]
        Output: True
        Partition into [1, 4] and [2, 3], each with sum 5.
        Elements in a subset do not need to be adjacent in the array.

Follow Up:
    Can you solve this using no more than O(S) extra space, where S is
    the sum of all elements of the given array?

Source Notes:
    Numeric constraints and the input/output format are not visible in
    the screenshot. The function accepts ARR directly; its length gives N.

https://www.youtube.com/watch?v=7win3dcgo3k&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=16

"""


def partition_equal_subset_sum_recursion(arr: list[int]) -> bool:
    """Return whether arr can be partitioned into two equal-sum subsets.

    Args:
        arr: A list of positive integers. Each position belongs to exactly
            one of the two subsets; duplicate values are separate elements.
            The list does not need to be sorted.

    Returns:
        True if such a partition exists, otherwise False. The subsets can
        have different sizes and need not contain adjacent elements.
        A single positive element returns False. An empty list returns
        True in this implementation, although the prompt does not specify
        whether empty input is allowed.

    Mutation and assumptions:
        The input list is not modified. Positive integer values are assumed
        and are not validated; negative elements are unsupported by the
        pruning condition. Long inputs may exceed Python's recursion-depth
        limit. Numeric constraints are not visible in the screenshot.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. Calculate total_sum and target, its integer half. If the total
           is odd, return False: two equal integer sums cannot add to an
           odd number. For an even total, finding one subset with sum
           target is enough; all remaining elements also sum to target.
           For example, a total of 20 requires one subset with sum 10.
        2. In the helper, track index, the last available position, and
           k, the remaining sum needed. If k is zero, return True because
           the selected elements form the required half. If index is
           negative and k is not zero, return False: no elements remain.
           Checking k first recognizes a match completed at index zero.
        3. Explore not_take by skipping arr[index], decreasing index and
           leaving k unchanged. If that search succeeds, return True
           immediately without exploring the take branch.
        4. Otherwise, initialize take to False. Try selecting arr[index]
           only if its value is at most k. Subtract it from k and move
           to the previous index. Taking 3 when k is 7 leaves 4 to find.
           Positive values make skipping oversized elements safe, and
           decreasing index prevents selecting the same position twice.
        5. Return take. The skip branch has already failed, so whether
           this state succeeds depends on the take branch alone. Elements
           not selected for this subset belong to the other subset.
        6. Start at the final array index with k equal to target and
           return the result. The search passes indexes and sums rather
           than constructing either subset or changing the array.

    Time Complexity:
        O(2**N) in the worst case, where N is the number of elements.
        Each element can create a skip branch and a take branch; computing
        the total takes O(N), while early returns can reduce search work.

    Space Complexity:
        O(N) extra space, excluding the input list. The recursive stack
        holds at most one helper call per element plus its base call,
        with constant local storage per call. For positive integers,
        N <= S, so this also meets the follow-up's O(S) space bound.
    """
    # Step 1: Reduce an even total to finding a subset with half that sum.
    total_sum: int = sum(arr)
    target: int = total_sum // 2

    if total_sum % 2 != 0:
        return False

    def find_subset_sum_to_k(index: int, k: int) -> bool:
        # Step 2: Check for a completed half before checking exhausted input.
        if k == 0:
            return True
        if index < 0:
            return False

        # Step 3: Skip this element and return early if that finds a subset.
        not_take: bool = find_subset_sum_to_k(index=index - 1, k=k)

        if not_take:
            return True
        # Step 4: Try taking this element only when it fits the remaining sum.
        take: bool = False
        if arr[index] <= k:
            take = find_subset_sum_to_k(index=index - 1, k=k - arr[index])

        # Step 5: The skip branch failed, so return the take branch result.
        return take

    # Step 6: Search all positions for a subset totaling target.
    return find_subset_sum_to_k(index=len(arr) - 1, k=target)


def partition_equal_subset_sum_memoization(arr: list[int]) -> bool:
    """Return whether two equal-sum subsets exist using cached recursion.

    Args:
        arr: A list of positive integers. Each position belongs to exactly
            one subset; duplicate values are separate elements. The list
            does not need to be sorted, and subset sizes may differ.

    Returns:
        True if the array can be partitioned into equal-sum subsets,
        otherwise False. A single positive element returns False. Empty
        input returns True in this implementation, although the prompt
        does not specify whether empty input is allowed.

    Mutation and assumptions:
        The input list is not modified. Positive integers are assumed
        and are not validated; negative elements are unsupported by the
        pruning and cache indexing. Large sums require a wide cache, and
        long arrays may exceed Python's recursion-depth limit. Numeric
        constraints are not visible in the screenshot.

    Approach:
        Top-down Dynamic Programming (Memoization), using Depth-First
        Search (DFS) with include/exclude recursion.
        1. Calculate size, total_sum, and target, the integer half of the
           total. Reject an odd total before allocating the cache: equal
           integer subset sums cannot add to an odd number. For an even
           total, finding one subset with sum target is sufficient because
           the remaining elements also sum to target.
        2. Create sum_dp with size independent rows and target + 1 columns.
           sum_dp[index][k] records whether positions 0 through index can
           form remaining sum k. None means uncomputed; True and False
           are both computed answers that can be reused.
        3. In the helper, return True when k is zero: a matching subset
           has been found. Otherwise, return False when index is negative
           because no elements remain. Checking k first recognizes a
           match completed by selecting the first array element.
        4. Check the current cache entry. If it is not None, return its
           actual boolean value, including False. Returning True merely
           because an entry exists would turn impossible states into
           successful ones.
        5. First skip arr[index], decreasing index while keeping k the
           same. Save the result in sum_dp[index][k]. If it is True,
           return immediately because a valid subset already exists.
        6. If skipping failed, take the element only when arr[index] <= k.
           Decrease index and subtract the element from k, saving the
           result in the same cache entry. Taking 3 toward a remaining
           sum of 7 leaves 4. Positive values make skipping oversized
           elements safe, and decreasing index prevents element reuse.
        7. Return the cached result. If taking was not allowed, it still
           holds False from the skip branch. The elements not chosen for
           this subset form the other equal-sum subset. Base cases return
           directly without needing cache entries.
        8. Start at the final index with the full target and return the
           result. The search tracks sums and indexes without constructing
           subsets or changing the input list.

    Time Complexity:
        O(N * (S + 1)), where N is the array length and S is its total sum.
        For an even total, initializing the half-sum cache and computing
        each state once take this time; odd totals return after O(N) work.

    Space Complexity:
        O(N * (S + 1)) extra space, excluding the input list. The cache has
        N rows of S // 2 + 1 entries, and the stack adds O(N) space. This
        implementation does not meet the follow-up's O(S) space requirement.
    """
    # Step 1: Reduce an even total to a subset search for half the sum.
    size: int = len(arr)
    total_sum: int = sum(arr)
    target = total_sum // 2

    if total_sum % 2 != 0:
        return False

    # Step 2: Cache both successful and unsuccessful states using None initially.
    sum_dp: list[list[bool | None]] = [[None] * (target + 1) for _ in range(size)]

    def find_subset_sum_to_k(index: int, k: int) -> bool:
        # Step 3: Check for a completed sum before checking exhausted input.
        if k == 0:
            return True
        if index < 0:
            return False

        # Step 4: Reuse the actual cached answer, including False.
        if sum_dp[index][k] is not None:
            return sum_dp[index][k]

        # Step 5: Cache the skip result and stop early when it succeeds.
        sum_dp[index][k] = find_subset_sum_to_k(index=index - 1, k=k)

        if sum_dp[index][k]:
            return True

        # Step 6: Try taking the element when it fits the remaining sum.
        if arr[index] <= k:
            sum_dp[index][k] = find_subset_sum_to_k(index=index - 1, k=k - arr[index])
        # Step 7: Return the take result or the failed skip if taking was invalid.
        return sum_dp[index][k]

    # Step 8: Search all positions for the full half-sum target.
    return find_subset_sum_to_k(index=size - 1, k=target)


def partition_equal_subset_sum_tabulation(arr: list[int]) -> bool:
    """Return whether two equal-sum subsets exist using a table of sums.

    Args:
        arr: A nonempty list of positive integers. Each position belongs
            to exactly one subset; duplicate values are separate elements.
            The array need not be sorted, and subset sizes may differ.

    Returns:
        True if the array can be partitioned into two equal-sum subsets,
        otherwise False. A single positive element returns False.

    Mutation and assumptions:
        The input list is not modified. Nonempty input and positive values
        are assumed and are not validated. Empty input and negative elements
        are unsupported. Large totals require a wide table. Numeric limits
        are not visible in the screenshot.

    Approach:
        Bottom-up Dynamic Programming (Tabulation).
        1. Calculate size, total_sum, and target, the integer half of the
           total. Reject an odd total: equal integer sums cannot add to an
           odd number. For an even total, finding one subset with sum
           target is sufficient because the remaining elements also sum
           to target. A total of 20 therefore requires a subset summing to 10.
        2. Create sum_dp with size independent rows and target + 1 columns,
           initially False. sum_dp[index][k] means that a subset of positions
           0 through index can form sum k. Columns represent intermediate
           sums, not just the final target.
        3. Mark column zero True for every row. Any prefix forms sum zero
           by choosing no elements, so the transition loop starts at sum 1.
        4. Initialize the first element separately. If arr[0] <= target,
           mark sum_dp[0][arr[0]] True. With only the first element, zero
           and its own value are the reachable sums. All other entries
           in the first row remain False.
        5. Process indexes from 1 onward and sums k from 1 through target,
           including target itself. Row zero is already initialized, so
           each transition can read a completed previous row without
           accidentally accessing Python's last row with index -1.
        6. Read not_take from the previous row at the same k. Skipping
           the current element preserves any sum earlier elements can form.
        7. Initialize take to False. If arr[index] <= k, read the previous
           row at k - arr[index]. For example, taking 3 toward sum 10
           succeeds if earlier elements can form 7. Using the previous row
           prevents selecting the current position more than once.
        8. Store take or not_take in the current cell. Either choice is
           enough to make sum k reachable; no explicit subsets are stored.
        9. Return the last row's target entry, which considers every array
           element. If it is True, the chosen elements and all remaining
           elements form the two equal-sum subsets.

    Time Complexity:
        O(N * (S + 1)), where N is the array length and S is its total sum.
        For an even total, initializing and filling the half-sum table take
        constant work per cell; odd totals return after O(N) work.

    Space Complexity:
        O(N * (S + 1)) extra space, excluding the input list. sum_dp holds
        N rows of S // 2 + 1 entries, while other variables use constant
        space. This does not meet the follow-up's O(S) space requirement.
    """
    # Step 1: Reduce an even total to finding a subset with half the sum.
    size: int = len(arr)
    total_sum: int = sum(arr)
    target: int = total_sum // 2

    if total_sum % 2 != 0:
        return False

    # Step 2: Create independent rows of initially unreachable sums.
    sum_dp: list[list[bool]] = [[False] * (target + 1) for _ in range(size)]

    # Step 3: Every prefix can form zero by selecting nothing.
    for index in range(size):
        sum_dp[index][0] = True

    # Step 4: Initialize the sum reachable using just the first element.
    if arr[0] <= target:
        sum_dp[0][arr[0]] = True

    # Step 5: Fill later rows for every positive sum through target.
    for index in range(1, size):
        for k in range(1, target + 1):
            # Step 6: Skip the current element and preserve the same sum.
            not_take: bool = sum_dp[index - 1][k]

            # Step 7: Taking it requires a reachable remainder in the previous row.
            take: bool = False

            if arr[index] <= k:
                take = sum_dp[index - 1][k - arr[index]]

            # Step 8: Either choice can establish reachability of this sum.
            sum_dp[index][k] = take or not_take

    # Step 9: Check the half-sum using all available positions.
    return sum_dp[size - 1][target]


def partition_equal_subset_sum_tabulation_space_optimized(arr: list[int]) -> bool:
    """Return whether equal-sum subsets exist using two rows of sums.

    Args:
        arr: A nonempty list of positive integers. Each position belongs
            to exactly one subset; duplicate values are separate elements.
            The list need not be sorted, and subset sizes may differ.

    Returns:
        True if the array can be partitioned into two equal-sum subsets,
        otherwise False. A single positive element returns False.

    Mutation and assumptions:
        The input list is not modified. Nonempty input and positive values
        are assumed and are not validated. Empty input and negative values
        are unsupported. Large totals require wide rows. Numeric limits
        are not visible in the screenshot.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Calculate size, total_sum, and target, the integer half of the
           total. Reject an odd total because two equal integer sums cannot
           add to an odd number. For an even total, a subset summing to
           target leaves the same sum for all remaining elements.
        2. Create prev_sum_dp with target + 1 False entries. Initialize
           the first element's sum to True if it fits, and initialize sum
           zero to True. These represent taking the first element or
           skipping it. For a first value of 2, sums 0 and 2 are reachable.
        3. Process each remaining element, starting at index 1. Create a
           fresh curr_sum_dp and mark its zero entry True, since choosing
           nothing remains possible for every prefix. Keep prev_sum_dp
           unchanged while calculating the current row.
        4. Check every sum k from 1 through target. Read not_take from
           prev_sum_dp[k]: skipping the current element preserves whether
           earlier elements can form this same sum. Smaller sums are
           calculated because later elements may need them as remainders.
        5. Initialize take to False. If arr[index] <= k, read
           prev_sum_dp[k - arr[index]]. Taking 3 toward sum 10 succeeds
           if earlier elements can form 7. Reading the previous row
           prevents using the current element more than once.
        6. Store take or not_take at curr_sum_dp[k]. Either choice can
           establish reachability. Use the current sum k for both the
           remainder lookup and destination, rather than the final target.
        7. After every sum is calculated, assign curr_sum_dp to
           prev_sum_dp. This shares the completed list rather than copying
           it; the next iteration creates a fresh current row. Only two
           rows are needed because each transition uses the previous row.
        8. Return prev_sum_dp[target] after all elements are considered.
           If True, the chosen subset and its remaining elements give
           equal sums. For a single element, the initialized row already
           provides the answer and the outer loop does not run.

    Time Complexity:
        O(N * (S + 1)), where N is the array length and S is its total sum.
        For even totals, each element creates and fills a half-sum row with
        constant work per entry; odd totals return after O(N) work.

    Space Complexity:
        O(S + 1) extra space, excluding the input list. At most two rows
        of S // 2 + 1 booleans are needed, with constant storage otherwise.
        For nonempty positive input, this meets the O(S) space follow-up.
    """
    # Step 1: Reduce an even total to a subset search for half the sum.
    size: int = len(arr)
    total_sum: int = sum(arr)
    target: int = total_sum // 2

    if total_sum % 2 != 0:
        return False

    # Step 2: Initialize sums made by taking or skipping the first element.
    prev_sum_dp: list[bool] = [False] * (target + 1)

    if arr[0] <= target:
        prev_sum_dp[arr[0]] = True

    prev_sum_dp[0] = True

    # Step 3: Build a fresh row per later element, keeping zero reachable.
    for index in range(1, size):
        curr_sum_dp: list[bool] = [False] * (target + 1)
        curr_sum_dp[0] = True
        # Step 4: Check each positive sum and the option to skip this element.
        for k in range(1, target + 1):
            not_take: bool = prev_sum_dp[k]
            # Step 5: Taking it needs a reachable remainder in the previous row.
            take: bool = False
            if arr[index] <= k:
                take = prev_sum_dp[k - arr[index]]
            # Step 6: Save reachability for this sum using either choice.
            curr_sum_dp[k] = take or not_take
        # Step 7: Publish the completed row after all sums have been calculated.
        prev_sum_dp = curr_sum_dp

    # Step 8: Check whether all available elements can form the half-sum.
    return prev_sum_dp[target]


def solve() -> None:
    # Example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum positive single element.
    arr = [1]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element with even total.
    arr = [4]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two minimum equal elements.
    arr = [1, 1]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two unequal elements with even total.
    arr = [1, 3]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd total despite a subset matching the rounded-down half.
    arr = [1, 2, 4]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even total with no equal partition.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different subset sizes.
    arr = [1, 5, 11, 5]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with a valid partition.
    arr = [3, 3, 3, 3]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values with unreachable half.
    arr = [2, 2, 2]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent elements form equal subsets.
    arr = [1, 2, 3, 4]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Half total equals the first element.
    arr = [6, 1, 2, 3]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Half total equals a middle element.
    arr = [1, 6, 2, 3]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Half total equals the last element.
    arr = [1, 2, 3, 6]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An element exceeds half the total.
    arr = [10, 1, 1, 2]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A duplicate cannot be invented or reused.
    arr = [2, 6]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted input requiring several elements per subset.
    arr = [7, 3, 2, 5, 1, 2]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input.
    arr = [4, 3, 2, 1]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several identical minimum values.
    arr = [1, 1, 1, 1, 1, 1]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd count of minimum values.
    arr = [1, 1, 1]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large positive counts with equal partition.
    arr = [1000000000000, 1000000000000]
    expected = True
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large even total without equal partition.
    arr = [1000000000000, 1000000000002]
    expected = False
    result = partition_equal_subset_sum_recursion(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum positive single element.
    arr = [1]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single element with even total.
    arr = [4]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two minimum equal elements.
    arr = [1, 1]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two unequal elements with even total.
    arr = [1, 3]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Odd total despite a subset matching the rounded-down half.
    arr = [1, 2, 4]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Even total with no equal partition.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Different subset sizes.
    arr = [1, 5, 11, 5]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values with a valid partition.
    arr = [3, 3, 3, 3]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values with unreachable half.
    arr = [2, 2, 2]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Nonadjacent elements form equal subsets.
    arr = [1, 2, 3, 4]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Half total equals the first element.
    arr = [6, 1, 2, 3]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Half total equals a middle element.
    arr = [1, 6, 2, 3]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Half total equals the last element.
    arr = [1, 2, 3, 6]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: An element exceeds half the total.
    arr = [10, 1, 1, 2]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: A duplicate cannot be invented or reused.
    arr = [2, 6]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Unsorted input requiring several elements per subset.
    arr = [7, 3, 2, 5, 1, 2]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Descending input.
    arr = [4, 3, 2, 1]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Several identical minimum values.
    arr = [1, 1, 1, 1, 1, 1]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Odd count of minimum values.
    arr = [1, 1, 1]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: repeated impossible states must stay False.
    arr = [2] * 15
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: many duplicates with a valid partition.
    arr = [2] * 30
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: larger values with an equal partition.
    arr = [1000, 1000]
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: larger even total without a partition.
    arr = [1000, 1002]
    expected = False
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: many distinct values.
    arr = list(range(1, 21))
    expected = True
    result = partition_equal_subset_sum_memoization(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum positive single element.
    arr = [1]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single element with even total.
    arr = [4]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two minimum equal elements.
    arr = [1, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two unequal elements with even total.
    arr = [1, 3]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Odd total despite a subset matching the rounded-down half.
    arr = [1, 2, 4]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Even total with no equal partition.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Different subset sizes.
    arr = [1, 5, 11, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values with a valid partition.
    arr = [3, 3, 3, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values with unreachable half.
    arr = [2, 2, 2]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Nonadjacent elements form equal subsets.
    arr = [1, 2, 3, 4]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Half total equals the first element.
    arr = [6, 1, 2, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Half total equals a middle element.
    arr = [1, 6, 2, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Half total equals the last element.
    arr = [1, 2, 3, 6]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: An element exceeds half the total.
    arr = [10, 1, 1, 2]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: A duplicate cannot be invented or reused.
    arr = [2, 6]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Unsorted input requiring several elements per subset.
    arr = [7, 3, 2, 5, 1, 2]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Descending input.
    arr = [4, 3, 2, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Several identical minimum values.
    arr = [1, 1, 1, 1, 1, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Odd count of minimum values.
    arr = [1, 1, 1]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: repeated impossible states must stay False.
    arr = [2] * 15
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: many duplicates with a valid partition.
    arr = [2] * 30
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger values with an equal partition.
    arr = [1000, 1000]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger even total without a partition.
    arr = [1000, 1002]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: many distinct values.
    arr = list(range(1, 21))
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: a later element must not be reused.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: half the total requires three nonadjacent values.
    arr = [1, 4, 2, 5, 3, 7]
    expected = True
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: two unequal odd values with an even total.
    arr = [3, 7]
    expected = False
    result = partition_equal_subset_sum_tabulation(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [2, 3, 3, 3, 4, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum positive single element.
    arr = [1]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single element with even total.
    arr = [4]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two minimum equal elements.
    arr = [1, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two unequal elements with even total.
    arr = [1, 3]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Odd total despite a subset matching the rounded-down half.
    arr = [1, 2, 4]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Even total with no equal partition.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Different subset sizes.
    arr = [1, 5, 11, 5]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values with a valid partition.
    arr = [3, 3, 3, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values with unreachable half.
    arr = [2, 2, 2]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Nonadjacent elements form equal subsets.
    arr = [1, 2, 3, 4]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Half total equals the first element.
    arr = [6, 1, 2, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Half total equals a middle element.
    arr = [1, 6, 2, 3]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Half total equals the last element.
    arr = [1, 2, 3, 6]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: An element exceeds half the total.
    arr = [10, 1, 1, 2]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: A duplicate cannot be invented or reused.
    arr = [2, 6]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Unsorted input requiring several elements per subset.
    arr = [7, 3, 2, 5, 1, 2]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Descending input.
    arr = [4, 3, 2, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Several identical minimum values.
    arr = [1, 1, 1, 1, 1, 1]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Odd count of minimum values.
    arr = [1, 1, 1]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: repeated impossible states must stay False.
    arr = [2] * 15
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: many duplicates with a valid partition.
    arr = [2] * 30
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: larger values with an equal partition.
    arr = [1000, 1000]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: larger even total without a partition.
    arr = [1000, 1002]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: many distinct values.
    arr = list(range(1, 21))
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: a later element must not be reused.
    arr = [1, 2, 5]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: half the total requires three nonadjacent values.
    arr = [1, 4, 2, 5, 3, 7]
    expected = True
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: two unequal odd values with an even total.
    arr = [3, 7]
    expected = False
    result = partition_equal_subset_sum_tabulation_space_optimized(arr)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
