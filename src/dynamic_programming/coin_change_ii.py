"""Coin Change II

Difficulty: Medium

Problem Statement:
    Given distinct positive coin denominations in coins and a total amount,
    return the number of combinations that make that amount exactly.
    Each denomination has an unlimited supply. Return 0 if no combination
    can make the amount.

    Order does not distinguish combinations: [1, 2, 2] and [2, 1, 2]
    count once. Amount zero has one combination: choosing no coins.
    The answer is guaranteed to fit in a signed 32-bit integer.

Constraints (LeetCode 518 version):
    1 <= len(coins) <= 300
    1 <= coins[i] <= 5000
    All denominations are distinct.
    0 <= amount <= 5000

Sample:
    coins = [1, 2, 5]
    amount = 5
    Output: 4

    The combinations are [5], [2, 2, 1], [2, 1, 1, 1],
    and [1, 1, 1, 1, 1]. Different orders of these same coins
    do not create additional combinations.

Additional Examples (added for practice):
    1. Several combinations with three denominations:
        coins = [1, 3, 4]
        amount = 6
        Output: 4
        Choose [1, 1, 1, 1, 1, 1], [3, 1, 1, 1], [3, 3], or [4, 1, 1].

    2. An impossible amount:
        coins = [2, 4, 6]
        amount = 7
        Output: 0
        All denominations are even, so no combination makes an odd amount.

    3. Zero amount:
        coins = [2, 5, 7]
        amount = 0
        Output: 1
        Choosing no coins is the only combination.

    4. Unlimited reuse with unsorted denominations:
        coins = [5, 2, 3]
        amount = 7
        Output: 2
        Choose [5, 2] or [3, 2, 2]. Their rearrangements are not new ways.

    5. A single denomination:
        coins = [3]
        amount = 9
        Output: 1
        The only combination is [3, 3, 3].

Sources:
    https://www.youtube.com/watch?v=HgyouUi11zk
    https://leetcode.com/problems/coin-change-ii/
    The statement, constraints, and sample use the matching LeetCode 518
    version of the video's coin-combination counting problem.
"""


def coin_change_ii_recursion(coins: list[int], amount: int) -> int:
    """Count combinations of unlimited coins that make amount exactly.

    Parameters:
        coins: A nonempty list of distinct positive integer denominations.
        amount: A nonnegative integer amount to form.

    Returns:
        The number of combinations, ignoring coin order. Return 0 when
        impossible and 1 for amount zero (choosing no coins).
        The input list is not modified.

    Approach:
        Recursive Include/Exclude (Pick/Not Pick) Enumeration.

        1. Start with the last coin and the full amount. Each recursive call
           counts combinations using only coins from index 0 through index
           with a total equal to remaining_amount.
        2. When index is 0, only coins[0] is available. There is exactly one
           combination if it divides remaining_amount evenly, otherwise none.
           For coin 3 and amount 9, choose three copies. For amount 8, there
           is no combination. Amount zero counts once: choose no copies.
        3. Not taking the current denomination moves to index - 1 without
           changing the remaining amount. This counts every combination
           that uses no copies of the current coin.
        4. Taking the current coin subtracts its value from the remaining
           amount. Keep the same index because this denomination can be
           reused. Only take it when it fits, avoiding negative amounts.
        5. Add the two counts: combinations either use the current coin or
           do not. For coins [1, 2] and amount 4, not_take counts [1, 1, 1, 1];
           take counts [2, 1, 1] and [2, 2]. Their total is 3. Moving only
           toward earlier indexes prevents counting rearrangements again.

    Time Complexity:
        O(2 ** (n + amount // m)) is a loose upper bound, where n is the
        number of denominations and m is the smallest coin. Calls branch
        up to twice, and each branch reduces the index or remaining amount.

    Space Complexity:
        O(n + amount // m) for the recursive call stack, excluding the input.
        Large amounts can exceed Python's default recursion depth.
    """

    def count_ways(index: int, remaining_amount: int) -> int:
        # Step 2: Count the only possible selection using the first coin.
        if index == 0:
            return 1 if remaining_amount % coins[0] == 0 else 0

        # Step 3: Skip this denomination entirely.
        not_take: int = count_ways(index=index - 1, remaining_amount=remaining_amount)
        # Step 4: Take one coin if it fits, allowing this coin again.
        take: int = 0

        if coins[index] <= remaining_amount:
            take = count_ways(
                index=index, remaining_amount=remaining_amount - coins[index]
            )

        # Step 5: Add the counts from the two separate choices.
        return take + not_take

    # Step 1: Begin with every denomination available and the full amount.
    return count_ways(index=len(coins) - 1, remaining_amount=amount)


def coin_change_ii_memoization(coins: list[int], amount: int) -> int:
    """Count combinations of unlimited coins that make amount exactly.

    Parameters:
        coins: A nonempty list of distinct positive integer denominations.
        amount: A nonnegative integer amount to form.

    Returns:
        The number of combinations, ignoring coin order. Return 0 if the
        amount is impossible and 1 for zero amount (choose no coins).
        The input list is not modified.

    Approach:
        Top-Down Dynamic Programming (Memoization).

        1. Create count_dp with one row per denomination and one column per
           amount from 0 through amount. A value of -1 means uncomputed;
           0 means computed but impossible. count_dp[index][remaining_amount]
           counts combinations using only coins[0:index + 1].
        2. Start the recursion at the last index with the full amount.
           Each call decides whether to use the current denomination.
        3. At index 0, only the first denomination remains. Return 1 if it
           divides remaining_amount evenly, otherwise 0. For coin 3, amount
           9 has one combination and amount 8 has none. Zero amount has one
           combination: choosing no coins. Store this answer in count_dp.
        4. For other indexes, return a stored answer when available. The
           same index and remaining amount always have the same answer,
           so this avoids repeating the recursive work.
        5. Calculate not_take by moving to index - 1 with the same amount.
           This counts combinations that exclude the current denomination.
        6. Calculate take only if the coin fits. Subtract its value but
           keep the same index, allowing unlimited copies of this coin.
           Do not add 1: the recursive result counts complete combinations,
           rather than the number of coins. For [1, 2] and amount 4, taking
           a 2 leaves amount 2, with combinations [1, 1] and [2]. Adding the
           chosen coin produces [2, 1, 1] and [2, 2]: still two combinations.
        7. Store and return take + not_take. These choices count separate
           groups of combinations. Only moving toward earlier indexes
           prevents counting different orders as different combinations.

    Time Complexity:
        O(n * (amount + 1)), where n is the number of denominations.
        The table is initialized once, and each state needs constant work
        apart from recursive calls whose results are saved.

    Space Complexity:
        O(n * (amount + 1) + n + amount // m), where m is the smallest coin.
        This includes the table and recursive stack, excluding the input.
        Large amounts can exceed Python's default recursion depth.
    """
    # Step 1: Allocate a table of uncomputed combination counts.
    size: int = len(coins)
    count_dp: list[list[int]] = [[-1] * (amount + 1) for _ in range(size)]

    def count_ways(index: int, remaining_amount: int) -> int:
        # Step 3: Count combinations using only the first denomination.
        if index == 0:
            count_dp[index][remaining_amount] = (
                1 if remaining_amount % coins[index] == 0 else 0
            )
            return count_dp[index][remaining_amount]

        # Step 4: Reuse an answer already computed for this state.
        if count_dp[index][remaining_amount] != -1:
            return count_dp[index][remaining_amount]

        # Step 5: Exclude the current denomination.
        not_take: int = count_ways(index=index - 1, remaining_amount=remaining_amount)

        # Step 6: Include one coin if it fits, keeping it available.
        take: int = 0

        if coins[index] <= remaining_amount:
            take = count_ways(
                index=index, remaining_amount=remaining_amount - coins[index]
            )

        # Step 7: Save and return the total from both choices.
        count_dp[index][remaining_amount] = take + not_take

        return count_dp[index][remaining_amount]

    # Step 2: Start with every denomination and the full amount.
    return count_ways(index=size - 1, remaining_amount=amount)


def coin_change_ii_tabulation(coins: list[int], amount: int) -> int:
    """Count combinations of unlimited coins that make amount exactly.

    Parameters:
        coins: A nonempty list of distinct positive integer denominations.
        amount: A nonnegative integer amount to form.

    Returns:
        The number of combinations, ignoring coin order. Return 0 when
        impossible and 1 for zero amount (choosing no coins).
        The input list is not modified.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation).

        1. Create coins_dp with one row per denomination and columns for
           amounts 0 through amount. coins_dp[index][remaining_amount]
           counts combinations using only coins[0:index + 1]. Initially,
           every count is 0 because no combinations have been calculated.
        2. Fill the first row using only coins[0]. If remaining_amount is
           divisible by this coin, there is exactly one combination.
           For coin 3, amounts 0, 3, and 6 each have one combination;
           amount 4 has none. Zero means choosing no coins.
        3. Process each later denomination and each amount in increasing
           order, including zero. Smaller amounts in the current row are
           ready before a larger amount needs them.
        4. Set not_take to the previous row at the same amount. This counts
           combinations that exclude the current denomination entirely.
        5. Set take to 0 when the coin does not fit. Otherwise, read the
           current row at remaining_amount - coins[index]. Using the same
           row permits unlimited reuse of this denomination. For [1, 2]
           and amount 4, the current row at amount 2 counts [1, 1] and [2].
           Adding the chosen 2 gives [2, 1, 1] and [2, 2]. The count stays
           2, so do not add 1 to take.
        6. Store not_take + take because the two choices count separate
           groups. Continuing with [1, 2] and amount 4, not_take contributes
           [1, 1, 1, 1], so the total is 3. Processing denominations in a
           fixed order avoids counting rearrangements as new combinations.
           At amount zero, not_take carries forward the one empty selection.
        7. Return the last row at amount: it includes every denomination
           and counts combinations for the requested amount exactly.

    Time Complexity:
        O(n * (amount + 1)), where n is the number of denominations.
        Initializing and filling the table takes constant work per cell.

    Space Complexity:
        O(n * (amount + 1)) for coins_dp, excluding the input.
        The remaining variables use constant extra space.
    """
    # Step 1: Allocate a count for each denomination prefix and amount.
    size: int = len(coins)
    coins_dp: list[list[int]] = [[0] * (amount + 1) for _ in range(size)]

    # Step 2: Initialize combinations using only the first denomination.
    for remaining_amount in range(amount + 1):
        if remaining_amount % coins[0] == 0:
            coins_dp[0][remaining_amount] = 1

    # Step 3: Build later rows from smaller amounts and the previous row.
    for index in range(1, size):
        for remaining_amount in range(amount + 1):
            # Step 4: Exclude this denomination using the previous row.
            not_take: int = coins_dp[index - 1][remaining_amount]
            # Step 5: Include one coin; the current row allows reuse.
            take: int = 0
            if coins[index] <= remaining_amount:
                take = coins_dp[index][remaining_amount - coins[index]]
            # Step 6: Add the counts from both choices.
            coins_dp[index][remaining_amount] = not_take + take
    # Step 7: Read the answer using all denominations.
    return coins_dp[size - 1][amount]


def coin_change_ii_tabulation_space_optimized(coins: list[int], amount: int) -> int:
    """Count combinations of unlimited coins using two rows of storage.

    Parameters:
        coins: A nonempty list of distinct positive integer denominations.
        amount: A nonnegative integer amount to form.

    Returns:
        The number of combinations, ignoring coin order. Return 0 when
        impossible and 1 for zero amount (choosing no coins).
        The input list is not modified.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation) with Space Optimization.

        1. Create prev_coin_dp for amounts 0 through amount. Each position
           stores a combination count, rather than a coin value or coin
           count. Only the previous and current rows are needed, so there
           is no need to store a row for every denomination.
        2. Initialize prev_coin_dp using only coins[0]. An amount divisible
           by this denomination has exactly one combination; other amounts
           have none. For coin 3, amounts 0, 3, and 6 get 1, while amount 4
           gets 0. Amount zero represents choosing no coins.
        3. For each later denomination, create a fresh current_coin_dp.
           Process amounts in increasing order so smaller amounts in this
           row are ready before a larger amount needs them.
        4. Set not_take to prev_coin_dp[remaining_amount]. This counts
           combinations using only the earlier denominations, with no
           copies of the current coin.
        5. Start take at 0. If the coin fits, read current_coin_dp at the
           remaining amount after taking one coin. Reading the current
           row allows this denomination to be used again. For [1, 2] at
           amount 4, current_coin_dp[2] counts [1, 1] and [2]. Adding the
           chosen 2 gives [2, 1, 1] and [2, 2]: still two combinations,
           so no extra 1 is added to take.
        6. Store take + not_take in the current row. The choices count
           separate groups of combinations. In the same example, not_take
           adds [1, 1, 1, 1], giving 3 combinations for amount 4. Processing
           denominations in a fixed order avoids counting rearrangements.
           At amount zero, the one empty selection carries forward.
        7. After finishing the entire row, assign current_coin_dp to
           prev_coin_dp. The next denomination then uses these completed
           counts as its previous row; older rows are no longer needed.
        8. Return prev_coin_dp[amount], which includes every denomination.
           With one denomination, this returns the initialized first row.

    Time Complexity:
        O(n * (amount + 1)), where n is the number of denominations.
        Each row is initialized and filled with constant work per amount.

    Space Complexity:
        O(amount + 1) for the previous and current rows, excluding the input.
        At most two rows are needed regardless of the denomination count.
    """
    # Step 1: Store combination counts for one row of amounts.
    size: int = len(coins)
    prev_coin_dp: list[int] = [0] * (amount + 1)

    # Step 2: Count amounts formed using only the first denomination.
    for remaining_amount in range(amount + 1):
        if remaining_amount % coins[0] == 0:
            prev_coin_dp[remaining_amount] = 1

    # Step 3: Build a fresh row for each later denomination.
    for index in range(1, size):
        current_coin_dp: list[int] = [0] * (amount + 1)
        for remaining_amount in range(amount + 1):
            # Step 4: Exclude the current coin using the previous row.
            not_take: int = prev_coin_dp[remaining_amount]
            # Step 5: Include one coin; the current row allows reuse.
            take: int = 0

            if coins[index] <= remaining_amount:
                take = current_coin_dp[remaining_amount - coins[index]]

            # Step 6: Add counts from the two separate choices.
            current_coin_dp[remaining_amount] = take + not_take

        # Step 7: Keep the completed row for the next denomination.
        prev_coin_dp = current_coin_dp

    # Step 8: Read the requested amount after all denominations.
    return prev_coin_dp[amount]


def solve() -> None:
    # Sample from the question.
    coins = [1, 2, 5]
    amount = 5
    expected = 4
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest denomination and positive amount.
    coins = [1]
    amount = 1
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One denomination reused.
    coins = [3]
    amount = 9
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One denomination cannot make the amount.
    coins = [3]
    amount = 8
    expected = 0
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with one denomination.
    coins = [3]
    amount = 0
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with several denominations.
    coins = [2, 5, 7]
    amount = 0
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several different combinations.
    coins = [1, 3, 4]
    amount = 6
    expected = 4
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even denominations cannot make an odd amount.
    coins = [2, 4, 6]
    amount = 7
    expected = 0
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted denominations.
    coins = [5, 2, 3]
    amount = 7
    expected = 2
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Rearrangements count only once.
    coins = [1, 2]
    amount = 3
    expected = 2
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Combinations using three denominations.
    coins = [1, 2, 3]
    amount = 4
    expected = 4
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Combinations without a denomination of one.
    coins = [2, 3, 5]
    amount = 10
    expected = 4
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every denomination exceeds the amount.
    coins = [4, 7, 9]
    amount = 3
    expected = 0
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at the beginning.
    coins = [7, 4, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match in the middle.
    coins = [4, 7, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at the end.
    coins = [4, 6, 7]
    amount = 7
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination and amount.
    coins = [5000]
    amount = 5000
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount handled directly by the base case.
    coins = [1]
    amount = 5000
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination cannot make a smaller amount.
    coins = [5000]
    amount = 4999
    expected = 0
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of distinct denominations.
    coins = list(range(4701, 5001))
    amount = 1
    expected = 0
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of denominations with zero amount.
    coins = list(range(4701, 5001))
    amount = 0
    expected = 1
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger count with a modest recursion depth.
    coins = [1, 2, 5]
    amount = 10
    expected = 10
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated even coins.
    coins = [2, 4]
    amount = 8
    expected = 3
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending denominations give the same count.
    coins = [5, 2, 1]
    amount = 10
    expected = 10
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both branches contribute with two denominations.
    coins = [2, 3]
    amount = 6
    expected = 2
    result = coin_change_ii_recursion(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Count combinations using unlimited copies of each denomination.
    coins = [1, 2, 5]
    amount = 5
    expected = 4
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smallest positive amount.
    coins = [1]
    amount = 1
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with one coin.
    coins = [7]
    amount = 0
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with several coins.
    coins = [2, 5, 7]
    amount = 0
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination reused.
    coins = [3]
    amount = 9
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination cannot form amount.
    coins = [3]
    amount = 8
    expected = 0
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All denominations exceed amount.
    coins = [4, 7, 9]
    amount = 3
    expected = 0
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd amount with even denominations.
    coins = [2, 4, 6]
    amount = 7
    expected = 0
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several combinations.
    coins = [1, 3, 4]
    amount = 6
    expected = 4
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted denominations.
    coins = [5, 2, 3]
    amount = 7
    expected = 2
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Coin order does not create new combinations.
    coins = [1, 2]
    amount = 3
    expected = 2
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both taking and skipping contribute.
    coins = [2, 3]
    amount = 6
    expected = 2
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three denominations without coin one.
    coins = [2, 3, 5]
    amount = 10
    expected = 4
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple uses of even coins.
    coins = [2, 4]
    amount = 8
    expected = 3
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at beginning.
    coins = [7, 4, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match in middle.
    coins = [4, 7, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at end.
    coins = [4, 6, 7]
    amount = 7
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum coin and amount.
    coins = [5000]
    amount = 5000
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount with a direct base case.
    coins = [1]
    amount = 5000
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Amount just below maximum coin.
    coins = [5000]
    amount = 4999
    expected = 0
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of denominations.
    coins = list(range(4701, 5001))
    amount = 1
    expected = 0
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with maximum denomination count.
    coins = list(range(4701, 5001))
    amount = 0
    expected = 1
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and amount with a valid combination.
    coins = [1] + list(range(4702, 5001))
    amount = 5000
    expected = 300
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated subproblems with manageable recursion.
    coins = [1, 2, 5, 10, 20, 50]
    amount = 100
    expected = 4562
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending denominations.
    coins = [5, 2, 1]
    amount = 10
    expected = 10
    result = coin_change_ii_memoization(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: count combinations with unlimited coin reuse.
    coins = [1, 2, 5]
    amount = 5
    expected = 4
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum positive denomination and amount.
    coins = [1]
    amount = 1
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with one denomination.
    coins = [3]
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with several denominations.
    coins = [2, 5, 7]
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination reused.
    coins = [3]
    amount = 9
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination cannot form amount.
    coins = [3]
    amount = 8
    expected = 0
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All denominations exceed amount.
    coins = [4, 7, 9]
    amount = 3
    expected = 0
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd amount with even denominations.
    coins = [2, 4, 6]
    amount = 7
    expected = 0
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several combinations.
    coins = [1, 3, 4]
    amount = 6
    expected = 4
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted denominations.
    coins = [5, 2, 3]
    amount = 7
    expected = 2
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different orders count only once.
    coins = [1, 2]
    amount = 3
    expected = 2
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both taking and skipping contribute.
    coins = [2, 3]
    amount = 6
    expected = 2
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three denominations without coin one.
    coins = [2, 3, 5]
    amount = 10
    expected = 4
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated use within the current row.
    coins = [2, 4]
    amount = 8
    expected = 3
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at beginning.
    coins = [7, 4, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match in middle.
    coins = [4, 7, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at end.
    coins = [4, 6, 7]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum coin and amount.
    coins = [5000]
    amount = 5000
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount with smallest denomination.
    coins = [1]
    amount = 5000
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Amount just below maximum coin.
    coins = [5000]
    amount = 4999
    expected = 0
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount with repeated picks.
    coins = [4999, 1]
    amount = 5000
    expected = 2
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of distinct denominations.
    coins = list(range(4701, 5001))
    amount = 1
    expected = 0
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination count with zero amount.
    coins = list(range(4701, 5001))
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and amount.
    coins = [1] + list(range(4702, 5001))
    amount = 5000
    expected = 300
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger combination count.
    coins = [1, 2, 5, 10, 20, 50]
    amount = 100
    expected = 4562
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending denominations.
    coins = [5, 2, 1]
    amount = 10
    expected = 10
    result = coin_change_ii_tabulation(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimized tabulation: combinations with unlimited coin reuse.
    coins = [1, 2, 5]
    amount = 5
    expected = 4
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum positive denomination and amount.
    coins = [1]
    amount = 1
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with one denomination.
    coins = [3]
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero amount with several denominations.
    coins = [2, 5, 7]
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination reused.
    coins = [3]
    amount = 9
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single denomination cannot form amount.
    coins = [3]
    amount = 8
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All denominations exceed amount.
    coins = [4, 7, 9]
    amount = 3
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd amount with even denominations.
    coins = [2, 4, 6]
    amount = 7
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several combinations.
    coins = [1, 3, 4]
    amount = 6
    expected = 4
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted denominations.
    coins = [5, 2, 3]
    amount = 7
    expected = 2
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different orders count only once.
    coins = [1, 2]
    amount = 3
    expected = 2
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both taking and skipping contribute.
    coins = [2, 3]
    amount = 6
    expected = 2
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three denominations without coin one.
    coins = [2, 3, 5]
    amount = 10
    expected = 4
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated use within the current row.
    coins = [2, 4]
    amount = 8
    expected = 3
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First denomination cannot form every larger amount.
    coins = [3, 5]
    amount = 4
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at beginning.
    coins = [7, 4, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match in middle.
    coins = [4, 7, 6]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exact match at end.
    coins = [4, 6, 7]
    amount = 7
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum coin and amount.
    coins = [5000]
    amount = 5000
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount with smallest denomination.
    coins = [1]
    amount = 5000
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Amount just below maximum coin.
    coins = [5000]
    amount = 4999
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum amount with repeated picks.
    coins = [4999, 1]
    amount = 5000
    expected = 2
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum number of distinct denominations.
    coins = list(range(4701, 5001))
    amount = 1
    expected = 0
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum denomination count with zero amount.
    coins = list(range(4701, 5001))
    amount = 0
    expected = 1
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and amount.
    coins = [1] + list(range(4702, 5001))
    amount = 5000
    expected = 300
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger combination count.
    coins = [1, 2, 5, 10, 20, 50]
    amount = 100
    expected = 4562
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending denominations.
    coins = [5, 2, 1]
    amount = 10
    expected = 10
    result = coin_change_ii_tabulation_space_optimized(coins, amount)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
