"""Minimum Coins (Minimum Elements)

Problem Statement:
    Given distinct positive integer denominations in nums and a target
    sum, return the fewest coins needed to make that sum exactly.
    Each denomination has an unlimited supply. Return -1 if it is
    impossible. A target of zero requires zero coins.

Constraints:
    1 <= len(nums) <= 15
    1 <= nums[i] <= 2**31 - 1
    All denominations are distinct.
    1 <= target <= 10000
    Time limit: 1 second.
    The source also includes target = 0 in its samples, despite the
    stated lower bound of 1; zero is supported by this question.

Sample:
    nums = [1, 2, 3]
    target = 7

    Output: 3

    Choose [3, 3, 1], whose sum is 7. Two coins cannot reach 7 because
    the largest denomination is 3, so three coins are necessary.

Additional Examples (added for practice):
    1. An impossible sum:
        nums = [2, 4]
        target = 7
        Output: -1
        Every combination has an even sum, so none makes 7.

    2. Reusing a denomination:
        nums = [5]
        target = 15
        Output: 3
        Choose [5, 5, 5]. The same denomination can be used repeatedly.

    3. The largest coin first is not always best:
        nums = [1, 3, 4]
        target = 6
        Output: 2
        Choose [3, 3]. Choosing 4 first would require [4, 1, 1],
        which uses three coins instead of two.

    4. An exact denomination match:
        nums = [2, 5, 7]
        target = 7
        Output: 1
        A single coin of denomination 7 makes the target.

    5. A zero target:
        nums = [2, 5]
        target = 0
        Output: 0
        Select no coins; the sum is already zero.

Sources:
    https://www.youtube.com/watch?v=myPeWb3Y68A
    https://www.naukri.com/code360/problems/minimum-elements_3843091
"""


def minimum_coins_recursion(nums: list[int], target: int) -> int:
    """Return the fewest coins making target exactly, or -1 if impossible.

    Args:
        nums: A nonempty list of distinct positive integer denominations.
            Each denomination has an unlimited supply; sorting is unnecessary.
        target: A nonnegative integer amount to make exactly.

    Returns:
        The minimum number of coins, zero for target zero, or -1 when
        no combination can form the target.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, positive denominations,
        and nonnegative target are assumed and are not validated. Empty input,
        zero denominations, and negative inputs are unsupported. The 10**9
        sentinel exceeds every valid answer under the target <= 10000
        constraint. Long take chains may exceed Python's recursion limit.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion.
        1. In find_min_coin, index identifies the last available denomination
           and remaining_amount is the sum still needed. At index zero,
           only nums[0] remains, but it can be reused. If the remaining
           amount is divisible by it, return the quotient as the coin count.
           Otherwise return 10**9 to mark this branch impossible. For coin
           5, amount 15 needs three coins; amount 14 is impossible.
           Amount zero is divisible by every positive coin and returns zero.
        2. Calculate not_take by moving to index - 1 without changing the
           amount. This excludes the current denomination entirely and
           searches for the best result using earlier denominations.
        3. Initialize take to 10**9. If the current coin fits, take one
           coin and add one to the result for the reduced amount. Keep
           the same index because more copies of this denomination remain
           available. The fit check prevents a negative remaining amount.
        4. Return min(not_take, take). Taking one coin per call allows
           every possible quantity: a later call may take another copy or
           skip the denomination. For [1, 3, 4] and amount 10, this can
           select one 4 followed by two 3s, using three coins. Taking the
           maximum number of 4s immediately would miss that choice.
           An impossible take must not start at zero, because min would
           incorrectly prefer it over a valid positive coin count.
        5. Start at the final index with the full target. The helper
           counts additional coins rather than constructing combinations.
           For target zero, skip calls eventually reach the first-denomination
           base case and return zero without selecting any coins.
        6. Convert a final coin_count of at least 10**9 to -1. Keeping
           impossible results large during the search lets min favor valid
           choices; -1 is used only for the final public result.

    Time Complexity:
        O(2**(N + T // m)) is a loose upper bound, where N is the number
        of denominations, T is target, and m is the smallest denomination.
        Calls branch into skip and take choices, with at most N skips and
        T // m takes along a path; this can exceed the one-second limit.

    Space Complexity:
        O(N + T // m) extra space, excluding the input list. The recursive
        stack grows through denomination skips and repeated takes, while
        each call stores constant local data and no combinations are saved.
    """

    def find_min_coin(index: int, remaining_amount: int) -> int:
        # Step 1: With one denomination left, use divisibility or mark failure.
        if index == 0:
            if remaining_amount % nums[index] == 0:
                return remaining_amount // nums[index]
            else:
                return 10**9

        # Step 2: Skip this denomination and keep the remaining amount.
        not_take: int = find_min_coin(
            index=index - 1, remaining_amount=remaining_amount
        )

        # Step 3: Take one fitting coin; keep its index for unlimited reuse.
        take: int = 10**9

        if nums[index] <= remaining_amount:
            take = 1 + find_min_coin(
                index=index, remaining_amount=remaining_amount - nums[index]
            )
        # Step 4: Choose the smaller valid coin count from the two alternatives.
        return min(not_take, take)

    # Step 5: Search all denominations for the full target amount.
    coin_count: int = find_min_coin(index=len(nums) - 1, remaining_amount=target)

    # Step 6: Translate the impossible sentinel to the required -1 result.
    return -1 if coin_count >= 10**9 else coin_count


def minimum_coins_memoization(nums: list[int], target: int) -> int:
    """Return the fewest coins making target exactly using cached recursion.

    Args:
        nums: A nonempty list of distinct positive integer denominations.
            Each denomination has unlimited supply; sorting is unnecessary.
        target: A nonnegative integer amount to make exactly.

    Returns:
        The minimum coin count, zero for target zero, or -1 if impossible.
        The helper uses 10**9 for impossible results; the outer function
        returns the final cache entry, converting that sentinel to -1.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, positive denominations,
        and nonnegative target are assumed and are not validated. Empty input,
        zero denominations, and negative inputs are unsupported. The 10**9
        sentinel exceeds all valid counts for target <= 10000. Large targets
        require wide cache rows, and long take chains may exceed Python's
        recursion-depth limit even with memoization.

    Approach:
        Top-down Dynamic Programming (Memoization), using Depth-First
        Search (DFS) with include/exclude recursion.
        1. Read size and create coin_sum_dp with size independent rows and
           target + 1 columns. An entry at index and remaining_amount stores
           the minimum coins needed using denominations 0 through index.
           Initialize entries to -1 for uncomputed states, distinct from
           the 10**9 impossible-result sentinel and a valid count of zero.
        2. At index zero, only the first denomination remains. If it divides
           remaining_amount exactly, store and return the quotient. Otherwise
           return 10**9 directly. A zero amount has quotient zero. This
           constant-time base case runs before the cache lookup; impossible
           base cases leave their cache entries at -1.
        3. For other indexes, return a cached entry whenever it is not -1.
           This reuses valid counts, zero counts, and impossible counts of
           10**9, so failed non-base states are not repeatedly explored.
        4. Calculate not_take by skipping this denomination and searching
           index - 1 with the same remaining amount.
        5. Initialize take to 10**9 for an unavailable choice. If the coin
           fits, add one to the result for the reduced amount at the same
           index. Keeping index allows unlimited reuse; subtracting the
           positive denomination ensures the amount decreases. Taking one
           coin at a time explores intermediate quantities, such as one 4
           and two 3s for [1, 3, 4] with target 10.
        6. Store min(take, not_take) in the cache and return it. Taking
           and skipping are alternative ways to make the same amount, so
           select the smaller count. Impossible values must stay large
           during the search so min does not prefer failure over success.
        7. Call the helper with the final index and full target to populate
           the final cache entry. For a single denomination, a divisible
           target is stored by the base case; an impossible target leaves
           -1 there, already matching the required public failure result.
        8. Read the final cache entry and convert 10**9 to -1. Other entries
           are returned unchanged. No coin combinations are constructed.

    Time Complexity:
        O(N * (T + 1)), where N is the denomination count and T is target.
        Cache initialization has this bound, and each non-base state is
        computed once with at most two constant-time transitions.

    Space Complexity:
        O(N * (T + 1)) extra space, excluding the input list. The cache
        holds N rows of T + 1 entries; the stack adds O(N + T // m), where
        m is the smallest denomination, which fits within the stated bound.
    """
    # Step 1: Allocate independent rows with -1 marking uncomputed states.
    size: int = len(nums)

    coin_sum_dp: list[list[int]] = [[-1] * (target + 1) for _ in range(size)]

    def find_min_coin(index: int, remaining_amount: int) -> int:
        # Step 2: Solve the one-denomination case directly using divisibility.
        if index == 0:
            if remaining_amount % nums[index] == 0:
                coin_sum_dp[index][remaining_amount] = remaining_amount // nums[index]
                return coin_sum_dp[index][remaining_amount]
            else:
                return 10**9

        # Step 3: Reuse computed counts, including zero and impossible results.
        if coin_sum_dp[index][remaining_amount] != -1:
            return coin_sum_dp[index][remaining_amount]

        # Step 4: Skip this denomination and keep the remaining amount.
        not_take: int = find_min_coin(
            index=index - 1, remaining_amount=remaining_amount
        )
        # Step 5: Take one fitting coin and retain its index for unlimited reuse.
        take: int = 10**9

        if nums[index] <= remaining_amount:
            take = 1 + find_min_coin(
                index=index, remaining_amount=remaining_amount - nums[index]
            )
        # Step 6: Cache and return the smaller of the two alternative counts.
        coin_sum_dp[index][remaining_amount] = min(take, not_take)

        return coin_sum_dp[index][remaining_amount]

    # Step 7: Populate the answer for the full target using all denominations.
    find_min_coin(index=size - 1, remaining_amount=target)

    # Step 8: Read the final cache entry and translate the impossible sentinel.
    return (
        -1 if coin_sum_dp[size - 1][target] == 10**9 else coin_sum_dp[size - 1][target]
    )


def minimum_coins_tabulation(nums: list[int], target: int) -> int:
    """Return the fewest coins making target exactly using a 2D table.

    Args:
        nums: A nonempty list of distinct positive integer denominations.
            Each denomination has unlimited supply; sorting is unnecessary.
        target: A nonnegative integer amount to make exactly.

    Returns:
        The minimum coin count, zero for target zero, or -1 if no
        combination makes the amount exactly.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, positive denominations,
        and nonnegative target are assumed and are not validated. Empty input,
        zero denominations, and negative inputs are unsupported. The 10**9
        sentinel exceeds all valid counts under target <= 10000. Large
        targets require wide table rows. No recursive calls are used.

    Approach:
        Bottom-up Dynamic Programming (Tabulation).
        1. Read size and create coin_sum_dp with size independent rows
           and target + 1 columns, initially -1. The entry at index and
           amount is the minimum coins needed to form amount exactly using
           denominations 0 through index. Every cell is assigned before
           use, so -1 is only an initial placeholder, not a transition value.
        2. Initialize row zero for every amount, including zero. Only the
           first denomination is available, but it may be reused. If it
           divides amount, store amount // nums[0]; otherwise store 10**9
           for impossible. With first coin 3, amounts 0, 3, and 6 need
           0, 1, and 2 coins, while amounts 1 and 2 are impossible.
        3. Process later denominations starting at index 1, since row zero
           is already complete. Visit amounts from zero through target in
           ascending order. Including zero makes every row's zero entry
           become zero before larger amounts need it.
        4. Read not_take from the previous row at the same amount. This
           skips the current denomination and preserves the best result
           obtainable with earlier denominations.
        5. Initialize take to 10**9. If the current coin fits, add one
           to the current row's entry at amount - nums[index]. Unlike
           0/1 knapsack, read the current row because the denomination
           can be selected again. The smaller amount has already been
           calculated thanks to ascending order and positive coin values.
           For coin 3 and amount 6, this adds one to the current answer
           for amount 3, allowing two copies of coin 3.
        6. Store min(take, not_take). Taking and skipping are alternatives,
           so choose the smaller count. A large impossible value cannot
           beat a valid count, and the initialized take sentinel keeps
           impossible states at 10**9 even if a take continuation exceeds it.
        7. Read the final row at target and translate 10**9 to -1.
           With one denomination, row-zero initialization already gives
           the answer. For target zero, every processed row contains zero
           in that column, so the returned result is zero.

    Time Complexity:
        O(N * (T + 1)), where N is the denomination count and T is target.
        Initializing and filling the table take constant work per cell;
        the first-row initialization also takes O(T + 1) time.

    Space Complexity:
        O(N * (T + 1)) extra space, excluding the input list. coin_sum_dp
        holds N rows of T + 1 integers; other variables take constant space
        and no recursive call stack is needed.
    """
    # Step 1: Allocate independent table rows for exact-amount coin counts.
    size: int = len(nums)
    coin_sum_dp: list[list[int]] = [[-1] * (target + 1) for _ in range(size)]

    # Step 2: Initialize every amount using only the first denomination.
    for amount in range(target + 1):
        if amount % nums[0] == 0:
            coin_sum_dp[0][amount] = amount // nums[0]
        else:
            coin_sum_dp[0][amount] = 10**9

    # Step 3: Fill later rows in ascending amount order, including zero.
    for index in range(1, size):
        for amount in range(target + 1):
            # Step 4: Skip this denomination and read the previous row.
            not_take: int = coin_sum_dp[index - 1][amount]
            # Step 5: Taking one coin uses this row to allow unlimited reuse.
            take: int = 10**9

            if nums[index] <= amount:
                take = 1 + coin_sum_dp[index][amount - nums[index]]

            # Step 6: Keep the smaller count from taking or skipping.
            coin_sum_dp[index][amount] = min(take, not_take)

    # Step 7: Return the full-target answer, converting impossible to -1.
    return (
        -1 if coin_sum_dp[size - 1][target] == 10**9 else coin_sum_dp[size - 1][target]
    )


def minimum_coins_tabulation_space_optimized(nums: list[int], target: int) -> int:
    """Return the minimum coins making target exactly using two DP rows.

    Args:
        nums: A nonempty list of distinct positive integer denominations.
            Each denomination has unlimited supply; sorting is unnecessary.
        target: A nonnegative integer amount to make exactly.

    Returns:
        The fewest coins needed, zero for target zero, or -1 if the target
        cannot be made exactly. With one denomination, the result is its
        required quantity when divisible, otherwise -1.

    Mutation and assumptions:
        The input list is not modified. Nonempty input, positive denominations,
        and nonnegative target are assumed and are not validated. Empty input,
        zero denominations, and negative inputs are unsupported. The 10**9
        sentinel exceeds every valid count under target <= 10000. Large
        targets require wide rows; no recursive calls are used.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Read size and create prev_coin_sum_dp with target + 1 entries,
           initially 10**9 for impossible amounts. Each amount entry stores
           the minimum coins needed using the denominations processed so far.
           Only the previous and current denomination rows are needed.
        2. Initialize the first denomination for every amount from zero
           through target. If divisible by nums[0], store the quotient;
           otherwise keep 10**9. With coin 3, amounts 0, 3, and 6 need
           0, 1, and 2 coins. This also initializes amount zero to zero.
        3. For each later denomination, create a fresh current_coin_sum_dp
           filled with 10**9. Visit amounts in ascending order, including
           zero. At zero the coin does not fit, so the skip choice copies
           zero from the previous row before larger amounts need it.
        4. Read not_take from the previous row at the same amount. This
           skips the current denomination and preserves the best count
           obtainable using earlier denominations.
        5. Start take at 10**9. When the coin fits, add one to the current
           row at amount - nums[index]. Read the current row, not the
           previous row, because this denomination can be reused. For coin
           3 at amount 6, the current answer for amount 3 already uses a 3,
           so adding another gives two coins. Ascending amounts ensure the
           smaller current-row entry is ready before it is read.
        6. Store min(take, not_take). These are alternative ways to make
           the same amount, so select the smaller count rather than adding
           them. The sentinel keeps an unavailable take from beating a valid
           result and caps impossible entries at 10**9.
        7. After every amount is calculated, assign current_coin_sum_dp
           to prev_coin_sum_dp. This shares the completed list rather than
           copying it; the next iteration creates a fresh current row.
           Skip reads stay in the previous row, while take reads can reuse
           the current denomination through smaller current-row amounts.
        8. Return the final target entry, converting 10**9 to -1. For a
           single denomination, the initialization already gives the answer
           and the outer loop does not run.

    Time Complexity:
        O(N * (T + 1)), where N is the denomination count and T is target.
        Each denomination creates and fills a row with constant work per
        amount; first-row initialization takes O(T + 1) time.

    Space Complexity:
        O(T + 1) extra space, excluding the input list. At most two rows
        of T + 1 integer counts are needed at once; other variables use
        constant space and there is no recursive call stack.
    """
    # Step 1: Allocate minimum counts with a large sentinel for impossible sums.
    size: int = len(nums)
    prev_coin_sum_dp: list[int] = [10**9] * (target + 1)

    # Step 2: Initialize every amount using only the first denomination.
    for amount in range(target + 1):
        if amount % nums[0] == 0:
            prev_coin_sum_dp[amount] = amount // nums[0]

    # Step 3: Build each later row in ascending amount order, including zero.
    for index in range(1, size):
        current_coin_sum_dp: list[int] = [10**9] * (target + 1)

        for amount in range(target + 1):
            # Step 4: Skip this denomination using the previous row.
            not_take: int = prev_coin_sum_dp[amount]
            # Step 5: Taking a coin uses this row to permit unlimited reuse.
            take: int = 10**9

            if nums[index] <= amount:
                take = 1 + current_coin_sum_dp[amount - nums[index]]

            # Step 6: Keep the smaller count from the two alternatives.
            current_coin_sum_dp[amount] = min(take, not_take)

        # Step 7: Publish the completed row after every amount has been filled.
        prev_coin_sum_dp = current_coin_sum_dp

    # Step 8: Return the target count, translating impossible to -1.
    return -1 if prev_coin_sum_dp[target] == 10**9 else prev_coin_sum_dp[target]


def solve() -> None:
    # Sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum denomination and positive target.
    nums = [1]
    target = 1
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination reused.
    nums = [5]
    target = 15
    expected = 3
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination cannot make target.
    nums = [5]
    target = 14
    expected = -1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All denominations exceed target.
    nums = [5, 7]
    target = 3
    expected = -1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero target with one denomination.
    nums = [5]
    target = 0
    expected = 0
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero target with several denominations.
    nums = [2, 5, 7]
    target = 0
    expected = 0
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd target with only even denominations.
    nums = [2, 4]
    target = 7
    expected = -1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at the beginning.
    nums = [7, 2, 5]
    target = 7
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match in the middle.
    nums = [2, 7, 5]
    target = 7
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at the end.
    nums = [2, 5, 7]
    target = 7
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Taking the largest denomination first is suboptimal.
    nums = [1, 3, 4]
    target = 6
    expected = 2
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An intermediate number of largest coins is best.
    nums = [1, 3, 4]
    target = 10
    expected = 3
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted denominations.
    nums = [4, 1, 3]
    target = 6
    expected = 2
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending denominations.
    nums = [7, 5, 2]
    target = 9
    expected = 2
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated nonfirst denomination.
    nums = [3, 5]
    target = 10
    expected = 2
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Combination of denominations.
    nums = [4, 7]
    target = 11
    expected = 2
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unreachable sum despite coprime denominations.
    nums = [4, 7]
    target = 5
    expected = -1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination cannot fit.
    nums = [2147483647]
    target = 1
    expected = -1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination alongside a usable coin.
    nums = [1, 2147483647]
    target = 3
    expected = 3
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target using the first denomination.
    nums = [1]
    target = 10000
    expected = 10000
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target with an exact coin.
    nums = [10000]
    target = 10000
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of distinct denominations.
    nums = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    target = 34
    expected = 1
    result = minimum_coins_recursion(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum denomination and positive target.
    nums = [1]
    target = 1
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single denomination reused.
    nums = [5]
    target = 15
    expected = 3
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single denomination cannot make target.
    nums = [5]
    target = 14
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All denominations exceed target.
    nums = [5, 7]
    target = 3
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Zero target with one denomination.
    nums = [5]
    target = 0
    expected = 0
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Zero target with several denominations.
    nums = [2, 5, 7]
    target = 0
    expected = 0
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Odd target with only even denominations.
    nums = [2, 4]
    target = 7
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Exact match at the beginning.
    nums = [7, 2, 5]
    target = 7
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Exact match in the middle.
    nums = [2, 7, 5]
    target = 7
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Exact match at the end.
    nums = [2, 5, 7]
    target = 7
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Taking the largest denomination first is suboptimal.
    nums = [1, 3, 4]
    target = 6
    expected = 2
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: An intermediate number of largest coins is best.
    nums = [1, 3, 4]
    target = 10
    expected = 3
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Unsorted denominations.
    nums = [4, 1, 3]
    target = 6
    expected = 2
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Descending denominations.
    nums = [7, 5, 2]
    target = 9
    expected = 2
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Repeated nonfirst denomination.
    nums = [3, 5]
    target = 10
    expected = 2
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Combination of denominations.
    nums = [4, 7]
    target = 11
    expected = 2
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Unreachable sum despite coprime denominations.
    nums = [4, 7]
    target = 5
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum denomination cannot fit.
    nums = [2147483647]
    target = 1
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum denomination alongside a usable coin.
    nums = [1, 2147483647]
    target = 3
    expected = 3
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum target using the first denomination.
    nums = [1]
    target = 10000
    expected = 10000
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum target with an exact coin.
    nums = [10000]
    target = 10000
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum number of distinct denominations.
    nums = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    target = 34
    expected = 1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: repeated overlapping states with a reachable sum.
    nums = [1, 5, 7]
    target = 35
    expected = 5
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: repeated overlapping states with an unreachable sum.
    nums = [6, 10, 14]
    target = 31
    expected = -1
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: maximum target with short take paths.
    nums = [100, 250, 1000]
    target = 10000
    expected = 10
    result = minimum_coins_memoization(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum denomination and positive target.
    nums = [1]
    target = 1
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single denomination reused.
    nums = [5]
    target = 15
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single denomination cannot make target.
    nums = [5]
    target = 14
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All denominations exceed target.
    nums = [5, 7]
    target = 3
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero target with one denomination.
    nums = [5]
    target = 0
    expected = 0
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero target with several denominations.
    nums = [2, 5, 7]
    target = 0
    expected = 0
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Odd target with only even denominations.
    nums = [2, 4]
    target = 7
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Exact match at the beginning.
    nums = [7, 2, 5]
    target = 7
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Exact match in the middle.
    nums = [2, 7, 5]
    target = 7
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Exact match at the end.
    nums = [2, 5, 7]
    target = 7
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Taking the largest denomination first is suboptimal.
    nums = [1, 3, 4]
    target = 6
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: An intermediate number of largest coins is best.
    nums = [1, 3, 4]
    target = 10
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Unsorted denominations.
    nums = [4, 1, 3]
    target = 6
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Descending denominations.
    nums = [7, 5, 2]
    target = 9
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Repeated nonfirst denomination.
    nums = [3, 5]
    target = 10
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Combination of denominations.
    nums = [4, 7]
    target = 11
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Unreachable sum despite coprime denominations.
    nums = [4, 7]
    target = 5
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum denomination cannot fit.
    nums = [2147483647]
    target = 1
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum denomination alongside a usable coin.
    nums = [1, 2147483647]
    target = 3
    expected = 3
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum target using the first denomination.
    nums = [1]
    target = 10000
    expected = 10000
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum target with an exact coin.
    nums = [10000]
    target = 10000
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum number of distinct denominations.
    nums = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    target = 34
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: repeated overlapping states with a reachable sum.
    nums = [1, 5, 7]
    target = 35
    expected = 5
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: repeated overlapping states with an unreachable sum.
    nums = [6, 10, 14]
    target = 31
    expected = -1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximum target with short take paths.
    nums = [100, 250, 1000]
    target = 10000
    expected = 10
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximum denomination at the first position.
    nums = [2147483647, 2, 5]
    target = 7
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: maximum size and target with a usable exact coin.
    nums = [10000] + list(range(10001, 10015))
    target = 10000
    expected = 1
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: first denomination cannot make an amount that later coins can.
    nums = [4, 3]
    target = 6
    expected = 2
    result = minimum_coins_tabulation(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Sample from the question.
    nums = [1, 2, 3]
    target = 7
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum denomination and positive target.
    nums = [1]
    target = 1
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single denomination reused.
    nums = [5]
    target = 15
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single denomination cannot make target.
    nums = [5]
    target = 14
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: All denominations exceed target.
    nums = [5, 7]
    target = 3
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Zero target with one denomination.
    nums = [5]
    target = 0
    expected = 0
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Zero target with several denominations.
    nums = [2, 5, 7]
    target = 0
    expected = 0
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Odd target with only even denominations.
    nums = [2, 4]
    target = 7
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Exact match at the beginning.
    nums = [7, 2, 5]
    target = 7
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Exact match in the middle.
    nums = [2, 7, 5]
    target = 7
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Exact match at the end.
    nums = [2, 5, 7]
    target = 7
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Taking the largest denomination first is suboptimal.
    nums = [1, 3, 4]
    target = 6
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: An intermediate number of largest coins is best.
    nums = [1, 3, 4]
    target = 10
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Unsorted denominations.
    nums = [4, 1, 3]
    target = 6
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Descending denominations.
    nums = [7, 5, 2]
    target = 9
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Repeated nonfirst denomination.
    nums = [3, 5]
    target = 10
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Combination of denominations.
    nums = [4, 7]
    target = 11
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Unreachable sum despite coprime denominations.
    nums = [4, 7]
    target = 5
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum denomination cannot fit.
    nums = [2147483647]
    target = 1
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum denomination alongside a usable coin.
    nums = [1, 2147483647]
    target = 3
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum target using the first denomination.
    nums = [1]
    target = 10000
    expected = 10000
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum target with an exact coin.
    nums = [10000]
    target = 10000
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum number of distinct denominations.
    nums = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    target = 34
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: repeated overlapping states with a reachable sum.
    nums = [1, 5, 7]
    target = 35
    expected = 5
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: repeated overlapping states with an unreachable sum.
    nums = [6, 10, 14]
    target = 31
    expected = -1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: maximum target with short take paths.
    nums = [100, 250, 1000]
    target = 10000
    expected = 10
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: maximum denomination at the first position.
    nums = [2147483647, 2, 5]
    target = 7
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: maximum size and target with a usable exact coin.
    nums = [10000] + list(range(10001, 10015))
    target = 10000
    expected = 1
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: first denomination cannot make an amount that later coins can.
    nums = [4, 3]
    target = 6
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: later denomination must be reused three times.
    nums = [5, 3]
    target = 9
    expected = 3
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: zero remains reachable through multiple row replacements.
    nums = [9, 7, 4, 2]
    target = 0
    expected = 0
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: last denomination improves an already reachable amount.
    nums = [1, 4, 6]
    target = 12
    expected = 2
    result = minimum_coins_tabulation_space_optimized(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
