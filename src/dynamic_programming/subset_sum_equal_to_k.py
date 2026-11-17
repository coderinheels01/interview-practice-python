"""Subset Sum Equal To K

Difficulty: Medium

Problem Statement:
    You are given an array/list ARR of N positive integers and an integer K.
    Check whether there exists a subset in ARR with a sum equal to K.

    Return True if such a subset exists. Otherwise, return False.

Example:
    Input: ARR = [1, 2, 3, 4], K = 4
    Output: True

    There are two subsets with sum 4: [1, 3] and [4].
    Hence, return True.

Input Format (visible portion):
    The first line contains a single integer T representing the number
    of test cases.

Source Notes:
    The remaining input format and numeric constraints are not visible
    in the screenshot. The function accepts ARR and K directly; the
    length of ARR provides N.

https://www.youtube.com/watch?v=fWX9xDmIzRI&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=15

"""


def subset_sum_equal_to_k_recursion(arr: list[int], k: int) -> bool:
    """Return whether a subset of arr sums exactly to k.

    Args:
        arr: A list of positive integers. Each position can be selected
            at most once; equal values at different positions are separate
            choices. The list does not need to be sorted.
        k: The integer target sum. Zero succeeds using the empty subset;
            a negative target returns False for positive input values.

    Returns:
        True if any subset has sum k, otherwise False. An empty list
        returns True only for k == 0.

    Mutation and assumptions:
        The input list is not modified. Values are assumed positive and
        are not validated; negative elements are unsupported by the
        pruning condition. Long inputs may exceed Python's recursion-depth
        limit. Numeric limits and a required time complexity are not
        visible in the problem statement.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. Track index, the last available position, and target, the sum
           still needed. If target is zero, return True immediately:
           the elements selected along this branch already form a match.
        2. If index is negative and target is not zero, return False.
           No elements remain to complete this branch. Checking target
           first allows a match that uses the element at index zero.
        3. First explore not_take: skip arr[index] and search earlier
           positions with the same target. If this returns True, return
           immediately without exploring the take branch.
        4. Otherwise, initialize take to False. Only consider taking the
           current element if arr[index] <= target, because all values
           are positive and an oversized element cannot help. Subtract
           its value from target and search earlier positions. For
           example, taking 3 when target is 7 leaves a target of 4.
           Decreasing index in both branches prevents reusing an element.
        5. Return take. The skip branch has already failed, so the result
           now depends entirely on whether taking this element succeeds.
           Separate recursive calls explore alternatives without changing
           the input list or storing a selected subset.
        6. Begin at the last index with the full target k, making every
           element available, and return the search result.

    Time Complexity:
        O(2**N) in the worst case, where N is the number of elements.
        Each element can lead to a skip branch and a take branch; early
        returns and skipping oversized values can reduce the actual work.

    Space Complexity:
        O(N) extra space, excluding the input list. The recursive stack
        holds at most N + 1 helper calls, with constant local storage per
        call; no list of subsets is created.
    """

    def find_subset_sum_equal_to_k_recursion(index: int, target: int) -> bool:
        # Step 1: A remaining target of zero means a subset was found.
        if target == 0:
            return True

        # Step 2: Without elements, a nonzero target cannot be reached.
        if index < 0:
            return False

        # Step 3: Skip this element and stop immediately if that succeeds.
        not_take: bool = find_subset_sum_equal_to_k_recursion(
            index=index - 1, target=target
        )

        if not_take:
            return True

        # Step 4: Try taking the element only when it fits the target.
        take: bool = False
        if arr[index] <= target:
            take = find_subset_sum_equal_to_k_recursion(
                index=index - 1, target=target - arr[index]
            )

        # Step 5: The skip branch failed, so return the take branch result.
        return take

    # Step 6: Start with all elements available and the full target.
    return find_subset_sum_equal_to_k_recursion(index=len(arr) - 1, target=k)


def subset_sum_equal_to_k_memoization(arr: list[int], k: int) -> bool:
    """Return whether a subset sums to k, caching recursive results.

    Args:
        arr: A list of positive integers. Each position can be used at
            most once; duplicate values at different positions are separate
            choices. The list does not need to be sorted.
        k: A nonnegative integer target sum.

    Returns:
        True if a subset sums exactly to k, otherwise False. A zero target
        succeeds with the empty subset. An empty list returns True only
        when k is zero.

    Mutation and assumptions:
        The input list is not modified. Positive elements and nonnegative
        k are assumed and are not validated. Negative targets and negative
        elements are unsupported. Large targets require a wide cache, and
        long arrays may exceed Python's recursion-depth limit. Numeric
        limits and a required time complexity are not visible in the prompt.

    Approach:
        Top-down Dynamic Programming (Memoization), using Depth-First
        Search (DFS) with include/exclude recursion.
        1. Read the array length and create sum_dp with one independent
           row per element and k + 1 columns. sum_dp[index][target] records
           whether elements from position 0 through index can form target.
           None means uncomputed; both True and False are cached answers.
        2. In the helper, return True if target is zero: the selected
           elements already form a match. Otherwise, return False when
           index is negative because no elements remain. Checking zero
           first allows a match completed by the first array element.
        3. Check the cache after the base cases. If the entry is not None,
           return it immediately, including a cached False. This avoids
           repeating a search for the same index and remaining target.
        4. Explore skipping arr[index], keeping target unchanged and
           decreasing index. Store that result in the current cache entry.
           If it is True, return immediately: a valid subset already exists,
           so trying to take the current element is unnecessary.
        5. If skipping failed, try taking arr[index] only when its value
           is at most target. Subtract the value and decrease index, then
           store this result in the same cache entry. For example, taking
           3 toward a target of 7 leaves 4. Positive values make skipping
           an oversized element safe, and decreasing index prevents reuse.
        6. Return the cached result. If taking was not allowed, the entry
           still holds False from the skip branch; otherwise it holds the
           result of taking the element. Base cases return directly and
           do not need cache entries.
        7. Start at the last index with the full target k and return the
           result, making all array positions initially available.

    Time Complexity:
        O(N * (K + 1)), where N is the array length and K is the target.
        Initializing the cache takes this time, and each non-base state
        is computed once with at most two recursive choices.

    Space Complexity:
        O(N * (K + 1)) extra space, excluding the input list. The cache
        stores N * (K + 1) entries, and the recursive stack adds O(N) space.
    """
    # Step 1: Create an independent cache row for each array position.
    size: int = len(arr)
    sum_dp: list[list[bool | None]] = [[None] * (k + 1) for _ in range(size)]

    def find_subset_sum_equal_to_k(index: int, target: int) -> bool:
        # Step 2: Check for a completed sum before checking exhausted input.
        if target == 0:
            return True
        if index < 0:
            return False

        # Step 3: Reuse either a True or a False answer already computed.
        if sum_dp[index][target] is not None:
            return sum_dp[index][target]

        # Step 4: Cache the skip result and return early when it succeeds.
        sum_dp[index][target] = find_subset_sum_equal_to_k(
            index=index - 1, target=target
        )

        if sum_dp[index][target]:
            return True

        # Step 5: If it fits, try taking this element and cache that result.
        if arr[index] <= target:
            sum_dp[index][target] = find_subset_sum_equal_to_k(
                index=index - 1, target=target - arr[index]
            )

        # Step 6: Return the take result, or the failed skip if taking was invalid.
        return sum_dp[index][target]

    # Step 7: Begin with every element available and the full target.
    return find_subset_sum_equal_to_k(index=size - 1, target=k)


def subset_sum_equal_to_k_tabulation(arr: list[int], k: int) -> bool:
    """Return whether a subset sums to k using a table of reachable sums.

    Args:
        arr: A nonempty list of positive integers. Each position can be
            used at most once; duplicate values are separate choices.
            The list does not need to be sorted.
        k: A nonnegative integer target sum.

    Returns:
        True if a subset sums exactly to k, otherwise False. A target
        of zero returns True because choosing no elements makes zero.

    Mutation and assumptions:
        The input list is not modified. A nonempty list, positive elements,
        and nonnegative k are assumed and are not validated. Empty input
        and negative targets or elements are unsupported. Large targets
        require a wide table. Numeric limits and a required time complexity
        are not visible in the problem statement.

    Approach:
        Bottom-up Dynamic Programming (Tabulation).
        1. Create sum_dp with one independent row per array element and
           k + 1 columns, all initially False. sum_dp[index][target] means
           a subset of positions 0 through index can form target. False
           marks sums that are impossible until shown otherwise.
        2. Mark column zero True in every row. Any prefix can form sum
           zero by choosing nothing, so the transition loops do not need
           to calculate this column again.
        3. Initialize the first row separately. With only arr[0], the
           possible sums are zero and arr[0]. If arr[0] <= k, mark its
           column True; otherwise it lies outside the table's targets.
           For arr[0] == 3 and k == 8, this marks sum 3, not sum 8.
        4. Process indexes from 1 onward and targets from 1 through k,
           including k. Row zero is already initialized, so every new
           row can read the completed row immediately before it without
           accidentally treating Python's index -1 as a previous row.
        5. Read not_take from the previous row at the same target. This
           represents skipping arr[index]: any previously reachable sum
           remains reachable without selecting the current element.
        6. Start take as False. If arr[index] <= target, read the previous
           row at target - arr[index]. For example, taking 5 toward sum
           8 succeeds if earlier elements can form 3. Reading the previous
           row ensures the current element cannot be reused.
        7. Store take or not_take in the current entry. Either choosing
           or skipping the element is enough to make the sum possible.
           All reads come from the previous row, so no selected subset
           or changes to the input list are needed.
        8. Return the last row's column k. This entry considers every
           array element and answers whether the requested sum is possible.

    Time Complexity:
        O(N * (K + 1)), where N is the array length and K is the target.
        Initializing the table and filling its entries take constant work
        per cell; this bound includes the case K == 0.

    Space Complexity:
        O(N * (K + 1)) extra space, excluding the input list. sum_dp holds
        N rows of K + 1 boolean entries, and loop variables use constant
        space; no recursive call stack is needed.
    """
    # Step 1: Create independent table rows, initially marking sums impossible.
    size: int = len(arr)
    sum_dp: list[list[bool]] = [[False] * (k + 1) for _ in range(size)]

    # Step 2: Every prefix can form zero using the empty subset.
    for index in range(size):
        sum_dp[index][0] = True

    # Step 3: With only the first element, its own value is also reachable.
    if arr[0] <= k:
        sum_dp[0][arr[0]] = True

    # Step 4: Build subsequent rows for each positive target through k.
    for index in range(1, size):
        for target in range(1, k + 1):
            # Step 5: Skip the current element and reuse the same target.
            not_take: bool = sum_dp[index - 1][target]

            # Step 6: Take it only if earlier elements can form the remainder.
            take: bool = False

            if arr[index] <= target:
                take = sum_dp[index - 1][target - arr[index]]

            # Step 7: Either choice can establish that the target is reachable.
            sum_dp[index][target] = take or not_take

    # Step 8: Check the full target using all available array positions.
    return sum_dp[size - 1][k]


def subset_sum_equal_to_k_tabulation_space_optimized(arr: list[int], k: int) -> bool:
    """Return whether a subset sums to k using two rows of reachable sums.

    Args:
        arr: A nonempty list of positive integers. Each position can be
            selected at most once; duplicate values are separate choices.
            The list does not need to be sorted.
        k: A nonnegative integer target sum.

    Returns:
        True if some subset sums exactly to k, otherwise False. Zero is
        reachable using the empty subset. For a single element, the answer
        is True only when k is zero or equals that element.

    Mutation and assumptions:
        The input list is not modified. A nonempty list, positive values,
        and nonnegative k are assumed and are not validated. Empty input
        and negative targets or elements are unsupported. Large targets
        require wide rows. Numeric limits and a required time complexity
        are not visible in the problem statement.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Read the array length and create prev_sum_dp with k + 1 False
           entries. Its target position records whether the elements
           processed so far can form that sum. Mark zero True because
           choosing nothing always makes zero.
        2. Initialize the first element separately: if arr[0] <= k, mark
           prev_sum_dp[arr[0]] True. With only this element, zero and its
           own value are the only reachable sums. For a first value of 3
           and k == 7, this marks sum 3, not the final target 7.
        3. Process the remaining elements from index 1 onward. Create a
           fresh curr_sum_dp for each element and set its zero entry True.
           The previous row must remain unchanged until this row is done.
        4. Visit each positive target from 1 through k. These smaller
           sums provide answers that later elements may need. Read
           not_take from prev_sum_dp[target]: skipping the current element
           preserves any sum reachable using earlier elements.
        5. Initialize take to False. If arr[index] <= target, read
           prev_sum_dp[target - arr[index]]. For example, taking 2 toward
           7 works if earlier elements can form 5. Reading the previous
           row ensures the current element cannot be selected repeatedly.
        6. Store take or not_take in curr_sum_dp[target]. Either choice
           can establish that the sum is reachable. Every positive target
           is assigned, while zero remains True from initialization.
        7. After all targets are processed, assign curr_sum_dp to
           prev_sum_dp. This shares the completed list rather than copying
           it. The next iteration creates a fresh current list, so future
           writes do not change the previous row. Only two rows are needed.
        8. Return prev_sum_dp[k] after all elements have been considered.
           If the list has one element, the initialized row already gives
           the answer and the outer loop does not run.

    Time Complexity:
        O(N * (K + 1)), where N is the array length and K is the target.
        Each element requires a row of K + 1 entries and constant work
        per target; the bound also covers K == 0.

    Space Complexity:
        O(K + 1) extra space, excluding the input list. At most two rows
        of K + 1 boolean entries are needed at once; other variables use
        constant space and there is no recursive call stack.
    """
    # Step 1: Create the previous row and mark the empty subset sum.
    size: int = len(arr)
    prev_sum_dp: list[bool] = [False] * (k + 1)
    prev_sum_dp[0] = True
    # Step 2: Initialize the sum made by selecting the first element.
    if arr[0] <= k:
        prev_sum_dp[arr[0]] = True

    # Step 3: Build a fresh row for each remaining element, keeping zero True.
    for index in range(1, size):
        curr_sum_dp: list[bool] = [False] * (k + 1)
        curr_sum_dp[0] = True
        # Step 4: Check each positive target, starting with the skip choice.
        for target in range(1, k + 1):
            not_take: bool = prev_sum_dp[target]
            # Step 5: Taking this element needs a reachable previous remainder.
            take: bool = False
            if arr[index] <= target:
                take = prev_sum_dp[target - arr[index]]

            # Step 6: Either taking or skipping can make the sum reachable.
            curr_sum_dp[target] = take or not_take

        # Step 7: Publish this row only after every target has been calculated.
        prev_sum_dp = curr_sum_dp

    # Step 8: Return reachability of k after considering all elements.
    return prev_sum_dp[k]


def solve() -> None:
    # Example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single minimum positive value matches.
    arr = [1]
    k = 1
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single value exceeds target.
    arr = [5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single value cannot be reused.
    arr = [3]
    k = 6
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero target uses the empty subset.
    arr = [2, 3, 7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match at the beginning.
    arr = [7, 10, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match in the middle.
    arr = [10, 7, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match at the end.
    arr = [10, 12, 7]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All elements are required.
    arr = [2, 3, 7]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target exceeds the entire array sum.
    arr = [2, 3, 7]
    k = 13
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every element exceeds the target.
    arr = [5, 8, 11]
    k = 3
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No subset matches although target is below total.
    arr = [2, 4, 8]
    k = 7
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent elements form the subset.
    arr = [3, 20, 5, 30, 9]
    k = 17
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only a later pair matches.
    arr = [20, 30, 4, 7]
    k = 11
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values represent separate elements.
    arr = [3, 3, 8]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values can form the target.
    arr = [2, 2, 2, 2]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    k = 5
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Too few copies of a value.
    arr = [2, 5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input.
    arr = [9, 7, 5, 3, 1]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A smaller choice succeeds where the largest cannot.
    arr = [4, 5, 6]
    k = 9
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large positive values.
    arr = [1000000000000, 1000000000001, 3]
    k = 2000000000001
    expected = True
    result = subset_sum_equal_to_k_recursion(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single minimum positive value matches.
    arr = [1]
    k = 1
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single value exceeds target.
    arr = [5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single value cannot be reused.
    arr = [3]
    k = 6
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Zero target uses the empty subset.
    arr = [2, 3, 7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Match at the beginning.
    arr = [7, 10, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Match in the middle.
    arr = [10, 7, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Match at the end.
    arr = [10, 12, 7]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All elements are required.
    arr = [2, 3, 7]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Target exceeds the entire array sum.
    arr = [2, 3, 7]
    k = 13
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Every element exceeds the target.
    arr = [5, 8, 11]
    k = 3
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: No subset matches although target is below total.
    arr = [2, 4, 8]
    k = 7
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Nonadjacent elements form the subset.
    arr = [3, 20, 5, 30, 9]
    k = 17
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Only a later pair matches.
    arr = [20, 30, 4, 7]
    k = 11
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Duplicate values represent separate elements.
    arr = [3, 3, 8]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values can form the target.
    arr = [2, 2, 2, 2]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    k = 5
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Too few copies of a value.
    arr = [2, 5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Descending input.
    arr = [9, 7, 5, 3, 1]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: A smaller choice succeeds where the largest cannot.
    arr = [4, 5, 6]
    k = 9
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: larger target with an exact pair.
    arr = [1000, 1001, 3]
    k = 2001
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: many repeated states with an unreachable odd target.
    arr = [2] * 30
    k = 31
    expected = False
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: many repeated values with a reachable target.
    arr = [2] * 30
    k = 32
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: all elements needed in a longer array.
    arr = list(range(1, 21))
    k = 210
    expected = True
    result = subset_sum_equal_to_k_memoization(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single minimum positive value matches.
    arr = [1]
    k = 1
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single value exceeds target.
    arr = [5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single value cannot be reused.
    arr = [3]
    k = 6
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero target uses the empty subset.
    arr = [2, 3, 7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match at the beginning.
    arr = [7, 10, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match in the middle.
    arr = [10, 7, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Match at the end.
    arr = [10, 12, 7]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All elements are required.
    arr = [2, 3, 7]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Target exceeds the entire array sum.
    arr = [2, 3, 7]
    k = 13
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Every element exceeds the target.
    arr = [5, 8, 11]
    k = 3
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: No subset matches although target is below total.
    arr = [2, 4, 8]
    k = 7
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Nonadjacent elements form the subset.
    arr = [3, 20, 5, 30, 9]
    k = 17
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Only a later pair matches.
    arr = [20, 30, 4, 7]
    k = 11
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Duplicate values represent separate elements.
    arr = [3, 3, 8]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values can form the target.
    arr = [2, 2, 2, 2]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    k = 5
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Too few copies of a value.
    arr = [2, 5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Descending input.
    arr = [9, 7, 5, 3, 1]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: A smaller choice succeeds where the largest cannot.
    arr = [4, 5, 6]
    k = 9
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger target with an exact pair.
    arr = [1000, 1001, 3]
    k = 2001
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: many repeated states with an unreachable odd target.
    arr = [2] * 30
    k = 31
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: many repeated values with a reachable target.
    arr = [2] * 30
    k = 32
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: all elements needed in a longer array.
    arr = list(range(1, 21))
    k = 210
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: single element with zero target.
    arr = [7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: first element must be combined with a later element.
    arr = [3, 10, 5]
    k = 8
    expected = True
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: later element cannot be reused.
    arr = [3, 5]
    k = 10
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: minimum positive target is unreachable.
    arr = [2, 3]
    k = 1
    expected = False
    result = subset_sum_equal_to_k_tabulation(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    arr = [1, 2, 3, 4]
    k = 4
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single minimum positive value matches.
    arr = [1]
    k = 1
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single value exceeds target.
    arr = [5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single value cannot be reused.
    arr = [3]
    k = 6
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Zero target uses the empty subset.
    arr = [2, 3, 7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Match at the beginning.
    arr = [7, 10, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Match in the middle.
    arr = [10, 7, 12]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Match at the end.
    arr = [10, 12, 7]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: All elements are required.
    arr = [2, 3, 7]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Target exceeds the entire array sum.
    arr = [2, 3, 7]
    k = 13
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Every element exceeds the target.
    arr = [5, 8, 11]
    k = 3
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: No subset matches although target is below total.
    arr = [2, 4, 8]
    k = 7
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Nonadjacent elements form the subset.
    arr = [3, 20, 5, 30, 9]
    k = 17
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Only a later pair matches.
    arr = [20, 30, 4, 7]
    k = 11
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Duplicate values represent separate elements.
    arr = [3, 3, 8]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values can form the target.
    arr = [2, 2, 2, 2]
    k = 6
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values cannot form an odd target.
    arr = [2, 2, 2, 2]
    k = 5
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Too few copies of a value.
    arr = [2, 5]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Descending input.
    arr = [9, 7, 5, 3, 1]
    k = 12
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: A smaller choice succeeds where the largest cannot.
    arr = [4, 5, 6]
    k = 9
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: larger target with an exact pair.
    arr = [1000, 1001, 3]
    k = 2001
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: many repeated states with an unreachable odd target.
    arr = [2] * 30
    k = 31
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: many repeated values with a reachable target.
    arr = [2] * 30
    k = 32
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: all elements needed in a longer array.
    arr = list(range(1, 21))
    k = 210
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: single element with zero target.
    arr = [7]
    k = 0
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: first element must be combined with a later element.
    arr = [3, 10, 5]
    k = 8
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: later element cannot be reused.
    arr = [3, 5]
    k = 10
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: minimum positive target is unreachable.
    arr = [2, 3]
    k = 1
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: preserve an early match across later rows.
    arr = [3, 10, 20, 30]
    k = 3
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: skip the first element and combine later elements.
    arr = [3, 5, 2]
    k = 7
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: fresh row must not reuse the current element.
    arr = [10, 2]
    k = 4
    expected = False
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: many elements with zero target.
    arr = [7] * 40
    k = 0
    expected = True
    result = subset_sum_equal_to_k_tabulation_space_optimized(arr, k)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
