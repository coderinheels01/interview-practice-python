"""Frog Jump

A frog starts on the first stair of a staircase containing n stairs and
wants to reach the nth stair. The list heights contains the height of each
stair: heights[0] is the first stair's height.

From a stair, the frog can jump either one stair or two stairs forward,
provided the destination is within the staircase. A jump from index i to
index j costs abs(heights[i] - heights[j]) units of energy.

Return the minimum total energy needed to reach the last stair from the
first stair.

Example:
    Input: n = 4, heights = [10, 20, 30, 10]
    Output: 20
    Explanation:
        Jump from the first stair to the second stair: abs(20 - 10) = 10.
        Jump from the second stair to the fourth stair: abs(10 - 20) = 10.
        The minimum total energy is 10 + 10 = 20.

Example 2:
    Input: n = 3, heights = [10, 30, 20]
    Output: 10
    Explanation:
        Jump directly from the first stair to the third stair.
        The energy cost is abs(20 - 10) = 10.
        Using both one-stair jumps would cost 20 + 10 = 30.

Example 3:
    Input: n = 4, heights = [10, 20, 30, 40]
    Output: 30
    Explanation:
        Jump from the first stair to the second, then to the fourth.
        The total cost is abs(20 - 10) + abs(40 - 20) = 10 + 20 = 30.
        Other paths can also achieve the same minimum cost.

Example 4:
    Input: n = 4, heights = [7, 7, 7, 7]
    Output: 0
    Explanation:
        Every stair has the same height, so every jump costs 0 energy.

Example 5:
    Input: n = 6, heights = [30, 10, 60, 10, 60, 50]
    Output: 40
    Explanation:
        Jump from the first stair to the third, then fifth, then sixth.
        The total cost is abs(60 - 30) + abs(60 - 60) + abs(50 - 60)
        = 30 + 0 + 10 = 40.

Input Format (original problem):
    The first line contains t, the number of test cases.
    For each test case:
        The first line contains n, the number of stairs.
        The next line contains the n stair heights.

Output:
    For each test case, output the minimum total energy required.

Assumptions:
    There is at least one stair, and n == len(heights).
    Numeric constraints are not visible in the supplied screenshot.
"""


def frog_jump_recursion(n: int, heights: list[int]) -> int:
    """Return the minimum energy needed to reach the last stair.

    Approach: Naive Recursion
        1. Define jump(stair) to mean: "What is the minimum energy needed
           to reach this index from index 0?" Each call answers that question
           for its own stair. Indexes start at 0, so the last index is n - 1.
        2. At index 0, return 0 energy. The frog already starts there and
           does not need to make a jump.
        3. Calculate the option whose FINAL jump moves one stair. First ask
           jump(stair - 1) for the cheapest way to reach the previous stair.
           Then add the height difference for jumping from there to stair.
           abs() makes the cost nonnegative, even when jumping downhill.
        4. If stair >= 2, also calculate the option whose FINAL jump moves
           two stairs. Ask jump(stair - 2) for its minimum energy, then add
           the cost of jumping from that index to stair. The check prevents
           using an index before the start of the staircase.
        5. Return the cheaper of the two options. If stair is 1, return
           only the one-stair option because a two-stair arrival is impossible.
        6. Start the process at jump(n - 1) and return its answer.

        Each call finishes its one-stair option before its two-stair option.
        But the smaller call can explore BOTH of its own options while its
        parent waits. "One-stair option" describes only the final jump;
        earlier jumps in that path can have either size.

        Example: heights = [10, 20, 30, 10].
            jump(0) returns 0: the frog starts at index 0.
            jump(1) returns 0 + abs(20 - 10) = 10.
            jump(2) compares 10 + abs(30 - 20) with 0 + abs(30 - 10).
                Both options cost 20, so it returns 20.
            jump(3) compares 20 + abs(10 - 30) with 10 + abs(10 - 20).
                It returns min(40, 20) = 20.
            The cheaper path is 0 -> 1 -> 3, using jumps of 1 then 2 stairs.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        heights: The height of each stair, in staircase order.

    Returns:
        The minimum total absolute height difference along a valid path
        from index 0 to index n - 1. A single stair needs 0 energy.

    Mutation Behavior:
        Reads heights without modifying it or any other caller-owned data.

    Time Complexity: O(2^n)
        Each call can make two smaller calls. The same stairs are calculated
        repeatedly, so the amount of work grows exponentially.

    Space Complexity: O(n)
        Up to n recursive calls can be waiting at once. The input list
        is excluded from extra space.

    Assumptions:
        n == len(heights) and n >= 1. Python must have enough recursion
        depth for the call chain. Complexity counts integer arithmetic as
        constant cost; exact numeric constraints were not provided.

                           jump(3)
                    min(20+20, 10+10)
                         = 20
                       /      \
                      /        \
                jump(2)       jump(1)
             min(10+10, 0+20)   0+10
                   = 20          = 10
                 /     \\           |
                /       \\          |
           jump(1)    jump(0)    jump(0)
             0+10        = 0       = 0
             = 10
               |
           jump(0)
              = 0
    """

    # Step 1: Define the question each smaller recursive call answers.
    def jump(stair: int) -> int:
        # Step 2: Reaching the starting stair requires no energy.
        if stair == 0:
            return 0

        # Step 3: Reach the previous stair, then take a one-stair jump.
        jump_one: int = jump(stair=stair - 1) + abs(heights[stair] - heights[stair - 1])
        # Step 4: Consider a two-stair final jump only when it is possible.
        if stair >= 2:
            jump_two: int = jump(stair=stair - 2) + abs(
                heights[stair] - heights[stair - 2]
            )
            # Step 5: Choose the cheaper complete route.
            return min(jump_one, jump_two)

        # Step 5: At index 1, only a one-stair final jump is possible.
        return jump_one

    # Step 6: Ask for the minimum energy to reach the last index.
    return jump(stair=n - 1)


def frog_jump_memoization(n: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair using saved answers.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Create energy_dp with one slot per stair. Start every slot at -1,
           meaning "not calculated yet." Valid energy costs are nonnegative,
           so -1 cannot be confused with a real answer, including zero.
        2. Define jump(stair) as the minimum energy to reach that index from
           index 0. At index 0, return 0: the frog already starts there.
        3. Check whether this stair's answer is saved. If its slot is not -1,
           return it immediately. This skips repeating the smaller calls.
        4. Calculate the route whose FINAL jump moves one stair. Ask for the
           cheapest way to reach stair - 1, then add the cost to jump from
           there to stair. abs() makes both uphill and downhill costs positive
           or zero. Earlier jumps in this route can have either size.
        5. If stair >= 2, also calculate the route whose final jump moves two
           stairs. Add the cheapest cost to reach stair - 2 to the cost of
           that final jump. Save the smaller of the two totals and return it.
           This check prevents accessing an index before the starting stair.
        6. At stair 1, only the one-stair option is possible. Save that answer
           and return it. The starting stair's answer is returned directly
           by step 2 and does not need a cache entry.
        7. Ask jump(n - 1) for the last stair's answer and return it directly.
           For one stair, jump(0) returns 0 even though its slot remains -1.

        Example: heights = [10, 20, 30, 10].
            jump(1) saves 10: the cost of jumping from index 0 to index 1.
            jump(2) compares 10 + 10 with 0 + 20, and saves 20.
            jump(3) compares 20 + 20 with 10 + 10, and saves 20.
            Its call to jump(1) reuses the saved 10 instead of recalculating.
            Return 20, for the path 0 -> 1 -> 3.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        heights: Stair heights in order, starting at index 0.

    Returns:
        Minimum total energy to reach index n - 1 using jumps of one or two
        stairs. A jump costs the absolute difference in endpoint heights.
        Returns 0 when there is only one stair.

    Mutation Behavior:
        Updates only its own local cache. Does not modify heights or other
        caller-owned data.

    Time Complexity: O(n)
        Each stair's answer is calculated once and saved. Later calls
        reuse that answer instead of repeating the work.

    Space Complexity: O(n)
        The cache holds n answers, and the recursion stack can grow to n
        calls. The input list is excluded from extra space.

    Assumptions:
        n == len(heights) and n >= 1. Python must have enough recursion depth
        for the call chain; memoization does not remove that stack-depth
        limit. Arithmetic is treated as constant cost; numeric limits were
        not provided in the screenshot.
    """
    # Step 1: Reserve one slot per stair; -1 means no answer is saved yet.
    energy_dp: list[int] = [-1] * n

    # Step 2: Find the minimum energy to reach a given stair index.
    def jump(stair: int) -> int:

        # Step 2: Starting at index 0 requires no energy.
        if stair == 0:
            return 0
        # Step 3: Reuse a saved answer before making more recursive calls.
        if energy_dp[stair] != -1:
            return energy_dp[stair]

        # Step 4: Reach the previous stair, then take a one-stair final jump.
        jump_one: int = jump(stair=stair - 1) + abs(heights[stair] - heights[stair - 1])
        # Step 5: If possible, also try arriving with a two-stair final jump.
        if stair >= 2:
            jump_two: int = jump(stair=stair - 2) + abs(
                heights[stair] - heights[stair - 2]
            )
            # Step 5: Save and return the cheaper total.
            energy_dp[stair] = min(jump_one, jump_two)
            return energy_dp[stair]

        # Step 6: At index 1, save and return the only possible option.
        energy_dp[stair] = jump_one
        return energy_dp[stair]

    # Step 7: Return the helper's answer for the last index, including n = 1.
    return jump(stair=n - 1)


def frog_jump_tabulation(n: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair using a table.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Create energy_dp with one slot per stair. Each slot will hold the
           minimum energy needed to reach that index. The -1 values are
           placeholders that will be replaced as we move through the table.
        2. Set energy_dp[0] to 0. The frog starts at index 0, so reaching
           that stair costs nothing.
        3. Visit indexes 1 through n - 1 in order. Calculate the cost of
           arriving with a one-stair final jump: take the saved minimum
           energy for the previous index and add the absolute difference
           between its height and the current height.
        4. Start the two-stair option at infinity. This means "unavailable"
           until we know the jump is valid. At index 1, there is no stair
           two positions back, so infinity prevents choosing this option.
        5. At index 2 or higher, replace infinity with the real two-stair
           cost: the saved energy two indexes back plus the height difference
           for that final jump. abs() ensures downhill jumps also cost energy.
        6. Save the cheaper of these two total costs in energy_dp[index].
           These are alternative routes, so choose the minimum rather than
           adding them together. Earlier jumps in either route can be of
           either size. Their minimum costs are already saved in the table.
        7. Return the entry at n - 1, the last valid index. With one stair,
           the loop is skipped and this returns the starting cost of 0.

        Example: heights = [10, 20, 30, 10].
            Start: energy_dp = [0, -1, -1, -1].
            Index 1: one-step cost = 0 + abs(20 - 10) = 10.
                Two-step cost is infinity. Save 10.
            Index 2: compare 10 + abs(30 - 20) with 0 + abs(30 - 10).
                Both cost 20. Save 20.
            Index 3: compare 20 + abs(10 - 30) with 10 + abs(10 - 20).
                Choose min(40, 20) = 20.
            Final table: [0, 10, 20, 20]. Return 20.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        heights: Heights of the stairs in order, starting at index 0.

    Returns:
        The minimum total energy to reach index n - 1 with one- or two-stair
        jumps. Each jump costs the absolute difference in endpoint heights.

    Mutation Behavior:
        Changes only its local table; heights is not modified.

    Time Complexity: O(n)
        Creating the table and visiting each stair both take linear time.
        Each loop visit does a fixed amount of work.

    Space Complexity: O(n)
        The energy table has n entries. The input list is excluded from
        extra space.

    Assumptions:
        n == len(heights) and n >= 1. Integer arithmetic is treated as constant
        cost; numeric limits were not provided. Infinity is a float sentinel,
        but the one-stair option is always a finite integer, so the minimum
        saved in the table is an integer. A float annotation on two_step_cost
        allows integer assignments without converting those integers to floats.
    """
    # Step 1: Reserve one energy slot for each stair.
    energy_dp: list[int] = [-1] * n
    # Step 2: Reaching the starting stair costs no energy.
    energy_dp[0] = 0

    # Step 3: Calculate the one-stair arrival cost for each remaining index.
    for index in range(1, n):
        one_step_cost: int = energy_dp[index - 1] + abs(
            heights[index] - heights[index - 1]
        )
        # Step 4: Treat the two-stair option as unavailable initially.
        two_step_cost: float = float("inf")

        # Step 5: Calculate that option only when two stairs back exists.
        if index >= 2:
            two_step_cost = energy_dp[index - 2] + abs(
                heights[index] - heights[index - 2]
            )

        # Step 6: Save the cheaper complete route to this stair.
        energy_dp[index] = min(one_step_cost, two_step_cost)

    # Step 7: Return the minimum energy for the last stair.
    return energy_dp[n - 1]


def frog_jump_tabulation_space_optimized(n: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair without a DP list.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Start with zero saved energy. The frog starts at index 0, so
           reaching it costs 0. one_step_back holds that starting answer.
           two_step_back is initially a placeholder: it is not used until
           index 2. Initialize current_cost to 0 for the single-stair case.
        2. Visit indexes 1 through n - 1 in order. Calculate the cost of
           arriving with a one-stair final jump: add one_step_back to the
           absolute height difference from index - 1 to index.
        3. Start the two-stair option at infinity, meaning unavailable.
           When index >= 2, calculate its real cost: add two_step_back to
           the absolute height difference from index - 2 to index.
           abs() makes downhill jumps cost energy too. Infinity prevents
           choosing a two-stair jump at index 1, where it is not possible.
        4. Choose the smaller option as current_cost. This is the minimum
           energy to reach this index. Each option includes the cheapest
           earlier route plus its final jump, so do not add the options.
        5. Move the saved answers forward for the next iteration. First copy
           the old one_step_back into two_step_back. Then replace
           one_step_back with current_cost. The order preserves the earlier
           answer before it is overwritten. Save earlier ANSWERS here, not
           the one-step or two-step option costs.
        6. Return current_cost after the last index. For one stair, the loop
           never runs and current_cost stays 0: the frog is already there.

        Example: heights = [10, 20, 30, 10].
            Start: one_step_back = 0, two_step_back = 0.
            Index 1: one-step cost = 0 + abs(20 - 10) = 10.
                Two-step option is unavailable. Choose 10.
                Saved answers become two_step_back = 0, one_step_back = 10.
            Index 2: compare 10 + abs(30 - 20) with 0 + abs(30 - 10).
                Choose 20. Saved answers become 10 and 20.
            Index 3: compare 20 + abs(10 - 30) with 10 + abs(10 - 20).
                Choose 20. Saved answers become 20 and 20.
            Return 20, for the path 0 -> 1 -> 3.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        heights: Heights of the stairs in order, starting at index 0.

    Returns:
        Minimum total energy to reach index n - 1 with one- or two-stair
        jumps. A jump costs the absolute difference in endpoint heights.
        Returns 0 for a single stair.

    Mutation Behavior:
        Reads heights without changing it. Only local variables are updated.

    Time Complexity: O(n)
        The loop visits each stair once. Each visit does a fixed amount
        of work: calculate two costs, choose the smaller, and update values.

    Space Complexity: O(1)
        Only a few variables are used, no matter how many stairs there are.
        No extra list or recursion stack is needed. The input list is excluded.

    Assumptions:
        n == len(heights) and n >= 1. Arithmetic and integer storage are
        treated as constant cost; numeric limits were not provided.
        Infinity is a float sentinel. The one-stair option is always a
        finite integer, so the selected minimum is an integer. A float
        annotation permits integer assignments without converting them.
    """
    # Step 1: Start with zero energy and prepare the single-stair answer.
    one_step_back: int = 0
    two_step_back: int = 0
    current_cost: int = 0

    # Step 2: Visit each remaining stair and calculate its one-stair option.
    for index in range(1, n):
        one_step_cost: int = one_step_back + abs(heights[index] - heights[index - 1])

        # Step 3: Use infinity unless a two-stair final jump is possible.
        two_step_cost: float = float("inf")
        if index >= 2:
            two_step_cost = two_step_back + abs(heights[index] - heights[index - 2])

        # Step 4: Choose the cheaper complete route to this index.
        current_cost = min(one_step_cost, two_step_cost)
        # Step 5: Preserve the old answer first, then save the new answer.
        two_step_back = one_step_back
        one_step_back = current_cost

    # Step 6: Return the last calculated cost, or 0 if there was no jump.
    return current_cost


def solve() -> None:
    n: int = 4
    heights: list[int] = [10, 20, 30, 10]
    expected: int = 20
    result: int = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single stair; already at the destination.
    n = 1
    heights = [10]
    expected = 0
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stairs; uphill jump.
    n = 2
    heights = [10, 30]
    expected = 20
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stairs; downhill jump.
    n = 2
    heights = [30, 10]
    expected = 20
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal heights.
    n = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-stair jump is cheaper.
    n = 3
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One- and two-stair routes tie.
    n = 3
    heights = [10, 20, 30]
    expected = 20
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing heights.
    n = 4
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing heights.
    n = 4
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All heights equal.
    n = 4
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Skip high stairs.
    n = 5
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed heights and longer route.
    n = 6
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_recursion(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: mixed heights with one- and two-stair jumps.
    n = 6
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_memoization(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: the example from the question.
    n = 4
    heights = [10, 20, 30, 10]
    expected = 20
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single stair; no loop iterations.
    n = 1
    heights = [10]
    expected = 0
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two stairs; only the one-stair option is available.
    n = 2
    heights = [10, 30]
    expected = 20
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Downhill jump still costs energy.
    n = 2
    heights = [30, 10]
    expected = 20
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two equal heights.
    n = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: First two-stair option is cheaper.
    n = 3
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Both options tie.
    n = 3
    heights = [10, 20, 30]
    expected = 20
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Increasing heights.
    n = 4
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Decreasing heights.
    n = 4
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All heights equal.
    n = 4
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Skip expensive intermediate stairs.
    n = 5
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Mixed heights and jump sizes.
    n = 6
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_tabulation(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: the example from the question.
    n = 4
    heights = [10, 20, 30, 10]
    expected = 20
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single stair; no loop iterations.
    n = 1
    heights = [10]
    expected = 0
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two stairs; uphill.
    n = 2
    heights = [10, 30]
    expected = 20
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two stairs; downhill.
    n = 2
    heights = [30, 10]
    expected = 20
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Equal endpoints.
    n = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two-stair route is cheaper.
    n = 3
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Routes have equal cost.
    n = 3
    heights = [10, 20, 30]
    expected = 20
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Increasing heights.
    n = 4
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Decreasing heights.
    n = 4
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: All heights equal.
    n = 4
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Skip expensive stairs.
    n = 5
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Mixed jump sizes.
    n = 6
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_tabulation_space_optimized(n, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
