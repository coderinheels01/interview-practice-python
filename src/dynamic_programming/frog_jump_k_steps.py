"""Frog Jump with K Steps

A frog starts at index 0 of a staircase with n stairs. The list heights
contains the height of each stair. The frog wants to reach index n - 1.

In one jump, the frog may move forward by any number of stairs from 1 to k,
as long as the destination is within the staircase. Jumping from index i
to index j costs abs(heights[i] - heights[j]) units of energy.

Return the minimum total energy required to reach the last stair.
For a single stair, no jumps are needed and the energy cost is 0.

Example:
    Input: n = 5, k = 3, heights = [10, 30, 40, 50, 20]
    Output: 30
    Explanation:
        Jump from index 0 to index 1, then from index 1 to index 4.
        The jumps move 1 and 3 stairs, both allowed when k = 3.
        Total energy is abs(30 - 10) + abs(20 - 30) = 20 + 10 = 30.
        This is the minimum possible energy.

Assumptions:
    - n == len(heights) and n >= 1.
    - k >= 1.
    - Numeric upper limits have not been specified.


    example with k = 4

                                         jump(4)
                       ┌────────────────┼──────────────┬─────────┐
                    jump(3)          jump(2)        jump(1)   jump(0)
             ┌─────────┼────────┐    ┌───┴────┐         │
          jump(2)   jump(1)  jump(0) jump(1) jump(0)   jump(0)
         ┌───┴───┐      │               │
      jump(1) jump(0) jump(0)         jump(0)
         │
      jump(0)
"""


def frog_jump_k_steps_recursion(n: int, k: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair.

    Approach: Naive Recursion
        1. Define jump(stair) as the minimum energy to reach that index.
           Return 0 at the starting stair: the frog is already there.
           Negative indexes also return 0, but the bounds check below
           prevents any valid recursive call from reaching them.
        2. Give each call its own minimum, starting at infinity. Answers
           for different destination stairs must not share one minimum.
        3. Try final jump sizes 1 through k. Skip any size that would
           start before index 0.
        4. For each valid size, ask for the cheapest route to the earlier
           stair, then add the absolute height difference of the final jump.
           abs() makes downhill costs nonnegative too.
        5. Keep the smallest total. After checking every size, return it.
           These routes are alternatives, so compare them rather than add them.
        6. Start at index n - 1 and return its answer.

        Example: heights = [10, 30, 20], k = 2.
            Reaching index 1 costs 20.
            Reaching index 2 via index 1 costs 20 + abs(20 - 30) = 30.
            Reaching index 2 directly costs 0 + abs(20 - 10) = 10.
            Return 10, the cheaper route.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        k: Maximum jump size, at least 1.
        heights: Stair heights in order, starting at index 0.

    Returns:
        Minimum total energy for one- through k-stair jumps to index n - 1.
        Returns 0 for one stair because no jump is needed.

    Mutation Behavior:
        Does not modify heights or other caller-owned data.

    Time Complexity:
        O(k * 2^n) is a general upper bound: exponentially many calls can
        occur, each checking k sizes. Without caching, earlier answers are
        recalculated; for k = 1, the time is only O(n).

    Space Complexity: O(n)
        Up to n recursive calls can be waiting at once. Branches run one
        at a time, and the input heights list is excluded from extra space.

    Assumptions:
        n == len(heights), n >= 1, and k >= 1. Python needs enough recursion
        depth. Arithmetic is treated as constant cost; numeric limits were
        not specified.
    """

    # Step 1: Define the question for each smaller stair index.
    def jump(stair: int) -> int:

        # Step 1: Starting at index 0 costs no energy.
        if stair <= 0:
            return 0

        # Step 2: Start a separate minimum for this call.
        min_energy: float = float("inf")
        # Step 3: Try each final jump size, checking that its start exists.
        for step in range(1, k + 1):
            if stair - step >= 0:
                # Step 4: Add the earlier route cost and this jump cost.
                current_energy: int = jump(stair=stair - step) + abs(
                    heights[stair] - heights[stair - step]
                )
                # Step 5: Keep the cheapest route found so far.
                min_energy = min(min_energy, current_energy)
        # Step 5: Return the minimum after checking all sizes.
        return min_energy

    # Step 6: Find the answer for the last stair index.
    return jump(stair=n - 1)


def frog_jump_k_steps_memoization(n: int, k: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair with jumps up to k.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Make a table with one slot per stair. Start each slot at -1,
           meaning no answer has been saved yet.
        2. Define jump(stair) as the minimum energy to reach that index.
           At index 0, return 0 because the frog already starts there.
        3. Check whether an answer is saved for this stair. If it is,
           return it immediately instead of repeating the smaller calls.
        4. Start a fresh minimum at infinity for this call. Try jump sizes
           1 through k, skipping any that would start before index 0.
        5. For each valid jump, calculate the cheapest route to the earlier
           stair, then add the absolute height difference for the final jump.
           abs() makes downhill jumps cost energy too.
        6. Keep the smallest total. After trying all jump sizes, save and
           return the minimum energy for this stair.
        7. Start at index n - 1 and return the helper's answer directly.
           For one stair, the base case returns 0 without needing a cache entry.

        Example: heights = [10, 30, 20], k = 2.
            Reaching index 1 costs 0 + abs(30 - 10) = 20.
            For index 2, arriving from index 1 costs 20 + 10 = 30.
            Arriving directly from index 0 costs 0 + 10 = 10.
            Save and return 10.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        k: Maximum jump size, at least 1.
        heights: Stair heights in order, starting at index 0.

    Returns:
        Minimum energy to reach index n - 1 using jumps of 1 through k
        stairs. Returns 0 for a single stair.

    Mutation Behavior:
        Updates only its local energy table; heights is not modified.

    Time Complexity: O(n * k)
        Each stair's answer is calculated once, checking k jump sizes.
        Later calls reuse the saved answer instead of repeating that work.

    Space Complexity: O(n)
        The table holds n entries, and up to n recursive calls can wait
        at once. The input heights list is excluded from extra space.

    Assumptions:
        n == len(heights), n >= 1, and k >= 1. Python needs enough recursion
        depth. Arithmetic is treated as constant cost; numeric upper limits
        have not been specified.
    """
    # Step 1: Reserve one slot per stair for saved answers.
    energy_dp: list[int] = [-1] * n

    # Step 2: Find the minimum energy to reach a stair index.
    def jump(stair: int) -> int:
        # Step 2: No jump is needed to reach the starting stair.
        if stair == 0:
            return 0

        # Step 3: Return the saved answer immediately to avoid repeated work.
        if energy_dp[stair] != -1:
            return energy_dp[stair]

        # Step 4: Start a fresh minimum and try each valid jump size.
        min_energy: float = float("inf")
        for step in range(1, k + 1):
            if stair - step >= 0:
                # Step 5: Add the earlier route cost and the final jump cost.
                current_energy: int = jump(stair=stair - step) + abs(
                    heights[stair] - heights[stair - step]
                )
                # Step 6: Keep the cheapest complete route.
                min_energy = min(min_energy, current_energy)

        # Step 6: Save and return the minimum for this stair.
        energy_dp[stair] = min_energy
        return energy_dp[stair]

    # Step 7: Return the answer for the last valid index.
    return jump(stair=n - 1)


def frog_jump_k_steps_tabulation(n: int, k: int, heights: list[int]) -> int:
    """Return the minimum energy to reach the last stair with jumps up to k.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Create energy_dp with one slot per stair. Each slot will store
           the minimum energy to reach that index. Initially, -1 means the
           answer has not been filled in yet.
        2. Set energy_dp[0] to 0. The frog already starts there, so no jump
           or energy is needed.
        3. Visit each remaining stair in order. Start its minimum at infinity
           so the first valid route can replace it. Each stair needs a fresh
           minimum because we are finding an answer for a new destination.
        4. Try final jump sizes 1 through k. Only consider a jump when
           stair - step is at least 0, so its starting index exists.
        5. Read the saved minimum energy for that earlier index. Add the
           absolute height difference for the final jump to the current stair.
           abs() makes downhill jumps cost energy too.
        6. Keep the smallest total found. After checking every jump size,
           save that minimum in the current stair's table entry. Compare
           routes instead of adding them: the frog only needs one route.
        7. Return the last table entry, at index n - 1. For one stair,
           the loop is skipped and this returns the starting cost of 0.

        Example: heights = [10, 30, 40, 20], k = 3.
            Index 0: save 0.
            Index 1: from index 0, cost 0 + 20 = 20. Save 20.
            Index 2: compare 20 + 10 with 0 + 30. Save 30.
            Index 3: compare 30 + 20, 20 + 10, and 0 + 10. Save 10.
            Final table: [0, 20, 30, 10]. Return 10.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        k: Maximum jump size, at least 1.
        heights: Stair heights in order, starting at index 0.

    Returns:
        Minimum total energy to reach index n - 1. Each jump moves 1 through
        k stairs and costs the absolute difference in endpoint heights.

    Mutation Behavior:
        Updates only its local table; heights is not modified.

    Time Complexity: O(n * k)
        Each of the n - 1 remaining stairs checks k jump sizes, even when
        some sizes are invalid. Creating the table also takes O(n) time.

    Space Complexity: O(n)
        The energy table stores n answers. The input heights list is excluded
        from extra space; no recursion stack is needed.

    Assumptions:
        n == len(heights), n >= 1, and k >= 1. Arithmetic is treated as
        constant cost; numeric upper limits have not been specified.
        Infinity is only a starting placeholder: every non-starting stair
        has a valid one-stair option, so its saved minimum is an integer.
    """
    # Step 1: Reserve a slot for the answer at every stair index.
    energy_dp: list[int] = [-1] * n
    # Step 2: Reaching the starting stair costs no energy.
    energy_dp[0] = 0

    # Step 3: Calculate each stair's answer with a fresh minimum.
    for stair in range(1, n):
        min_energy: float = float("inf")

        # Step 4: Try each allowed final jump size and check its start exists.
        for step in range(1, k + 1):
            if stair - step >= 0:
                # Step 5: Add the saved earlier answer to the final jump cost.
                current_energy: int = energy_dp[stair - step] + abs(
                    heights[stair] - heights[stair - step]
                )
                # Step 6: Keep the cheapest route found so far.
                min_energy = min(min_energy, current_energy)
        # Step 6: Save the answer after all jump sizes have been checked.
        energy_dp[stair] = min_energy

    # Step 7: Return the minimum energy for the last index.
    return energy_dp[n - 1]


def frog_jump_k_steps_tabulation_space_optimized(
    n: int, k: int, heights: list[int]
) -> int:
    """Return the minimum jump energy using a circular buffer of k answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Create k slots for saved answers. Save 0 in slot 0 because the
           frog starts at stair index 0 without spending energy. The other
           slots start at -1 and are filled before valid jumps read them.
        2. Visit stair indexes 1 through n - 1 in order. Start a fresh
           minimum at infinity for each stair.
        3. Try final jump sizes 1 through k. Skip any jump whose starting
           index, stair - step, would be negative.
        4. Read the saved energy for that starting index using
           (stair - step) % k. The remainder selects its buffer slot.
           Add the absolute height difference for the final jump.
        5. Keep the smallest total among all valid jump options.
        6. After checking ALL options, save that minimum in slot stair % k.
           This replaces the oldest answer, which is no longer needed for
           future stairs. Do not replace it earlier: the jump of size k
           still needs that old answer while this stair is being calculated.
        7. Return slot (n - 1) % k, which holds the last stair's answer.
           For a single stair, this returns the starting answer of 0.

        Example: n = 5, k = 3, heights = [10, 30, 40, 50, 20].
            Start: [0, -1, -1].
            Stair 1 costs 20: save in slot 1 -> [0, 20, -1].
            Stair 2 costs 30: save in slot 2 -> [0, 20, 30].
            Stair 3 costs 40: save in slot 0 -> [40, 20, 30].
            Stair 4 reads stair 3 from slot 0, stair 2 from slot 2,
                and stair 1 from slot 1. Its minimum is 30.
            Save in slot 1 -> [40, 30, 30]. Return slot 1's answer: 30.

    Parameters:
        n: Number of stairs, at least 1, equal to len(heights).
        k: Maximum jump size, at least 1; also the buffer size.
        heights: Stair heights in order, starting at index 0.

    Returns:
        Minimum total energy to reach index n - 1 using jumps of 1 through
        k stairs. Each jump costs the absolute difference in endpoint heights.

    Mutation Behavior:
        Updates only its local buffer; heights is not modified.

    Time Complexity: O(k + n * k)
        Creating the buffer takes O(k). Each remaining stair checks k jump
        sizes, giving O(n * k) work. For n >= 2, this simplifies to O(n * k).

    Space Complexity: O(k)
        The buffer holds k answers and is reused throughout the loop.
        The input heights list is excluded from extra space.

    Assumptions:
        n == len(heights), n >= 1, and k >= 1. Arithmetic is treated as
        constant cost; numeric upper limits have not been specified.
        Each non-starting stair has a finite one-stair route, so its saved
        minimum is an integer even though infinity starts as a float.
    """
    # Step 1: Reserve k reusable slots and save the starting energy.
    previous_energy_dp: list[int] = [-1] * k
    previous_energy_dp[0] = 0

    # Step 2: Calculate each remaining stair with a fresh minimum.
    for stair in range(1, n):
        min_energy: float = float("inf")
        # Step 3: Try each jump size, checking that its starting stair exists.
        for step in range(1, k + 1):
            if stair - step >= 0:
                # Step 4: Read the earlier saved answer and add this jump cost.
                current_energy: int = previous_energy_dp[(stair - step) % k] + abs(
                    heights[stair] - heights[stair - step]
                )
                # Step 5: Keep the cheapest complete route.
                min_energy = min(min_energy, current_energy)

        # Step 6: Replace the oldest answer only after all reads are finished.
        previous_energy_dp[stair % k] = min_energy

    # Step 7: Read the slot holding the last stair's answer.
    return previous_energy_dp[(n - 1) % k]


def solve() -> None:
    n: int = 5
    k: int = 3
    heights: list[int] = [10, 30, 40, 50, 20]
    expected: int = 30
    result: int = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single stair and minimum k.
    n = 1
    k = 1
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single stair with k larger than n.
    n = 1
    k = 5
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stairs uphill.
    n = 2
    k = 1
    heights = [10, 30]
    expected = 20
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stairs downhill with oversized k.
    n = 2
    k = 3
    heights = [30, 10]
    expected = 20
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal heights.
    n = 2
    k = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k = 1 requires every stair.
    n = 3
    k = 1
    heights = [10, 30, 20]
    expected = 30
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-stair jump is cheaper.
    n = 3
    k = 2
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer jump unavailable.
    n = 4
    k = 2
    heights = [10, 100, 100, 20]
    expected = 170
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimal jump uses exactly k stairs.
    n = 4
    k = 3
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k equals n.
    n = 4
    k = 4
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k exceeds n.
    n = 4
    k = 6
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All equal heights.
    n = 4
    k = 3
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing heights and tied routes.
    n = 4
    k = 2
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing heights.
    n = 4
    k = 2
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Skip expensive intermediate stairs.
    n = 5
    k = 2
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed heights.
    n = 6
    k = 2
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example with an active assertion.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_recursion(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: the example from the question.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single stair and minimum k.
    n = 1
    k = 1
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single stair with oversized k.
    n = 1
    k = 5
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two stairs uphill.
    n = 2
    k = 1
    heights = [10, 30]
    expected = 20
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Downhill with oversized k.
    n = 2
    k = 3
    heights = [30, 10]
    expected = 20
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal heights.
    n = 2
    k = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k = 1 visits every stair.
    n = 3
    k = 1
    heights = [10, 30, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-stair jump is cheaper.
    n = 3
    k = 2
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Long jump unavailable.
    n = 4
    k = 2
    heights = [10, 100, 100, 20]
    expected = 170
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimal jump uses exactly k stairs.
    n = 4
    k = 3
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k equals n.
    n = 4
    k = 4
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # k exceeds n.
    n = 4
    k = 6
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All heights equal.
    n = 4
    k = 3
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing heights and tied routes.
    n = 4
    k = 2
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing heights.
    n = 4
    k = 2
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Skip expensive stairs.
    n = 5
    k = 2
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed heights and jump sizes.
    n = 6
    k = 2
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: the example from the question.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single stair and minimum k.
    n = 1
    k = 1
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single stair with oversized k.
    n = 1
    k = 5
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two stairs uphill.
    n = 2
    k = 1
    heights = [10, 30]
    expected = 20
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Downhill with oversized k.
    n = 2
    k = 3
    heights = [30, 10]
    expected = 20
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Equal heights.
    n = 2
    k = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: k = 1 visits every stair.
    n = 3
    k = 1
    heights = [10, 30, 20]
    expected = 30
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two-stair jump is cheaper.
    n = 3
    k = 2
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Long jump unavailable.
    n = 4
    k = 2
    heights = [10, 100, 100, 20]
    expected = 170
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Optimal jump uses exactly k stairs.
    n = 4
    k = 3
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: k equals n.
    n = 4
    k = 4
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: k exceeds n.
    n = 4
    k = 6
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All heights equal.
    n = 4
    k = 3
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Increasing heights and tied routes.
    n = 4
    k = 2
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Decreasing heights.
    n = 4
    k = 2
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Skip expensive stairs.
    n = 5
    k = 2
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Mixed heights and jump sizes.
    n = 6
    k = 2
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Original example.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_memoization(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: wrap around the circular buffer.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum n and k.
    n = 1
    k = 1
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single stair with oversized k.
    n = 1
    k = 5
    heights = [10]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two stairs uphill.
    n = 2
    k = 1
    heights = [10, 30]
    expected = 20
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Downhill with oversized k.
    n = 2
    k = 3
    heights = [30, 10]
    expected = 20
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Equal heights.
    n = 2
    k = 2
    heights = [7, 7]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single-slot buffer reused.
    n = 3
    k = 1
    heights = [10, 30, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Read oldest slot before replacing it.
    n = 3
    k = 2
    heights = [10, 30, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Long jump unavailable.
    n = 4
    k = 2
    heights = [10, 100, 100, 20]
    expected = 170
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Optimal jump uses exactly k.
    n = 4
    k = 3
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: k equals n.
    n = 4
    k = 4
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: k exceeds n.
    n = 4
    k = 6
    heights = [10, 100, 100, 20]
    expected = 10
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: All heights equal.
    n = 4
    k = 3
    heights = [7, 7, 7, 7]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Increasing heights and tied routes.
    n = 4
    k = 2
    heights = [10, 20, 30, 40]
    expected = 30
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Decreasing heights.
    n = 4
    k = 2
    heights = [40, 30, 20, 10]
    expected = 30
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Multiple buffer wraps and skipped stairs.
    n = 5
    k = 2
    heights = [10, 100, 10, 100, 10]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Mixed heights.
    n = 6
    k = 2
    heights = [30, 10, 60, 10, 60, 50]
    expected = 40
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Original example.
    n = 5
    k = 3
    heights = [10, 30, 40, 50, 20]
    expected = 30
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Repeated oldest-slot reuse with k-sized jumps.
    n = 10
    k = 3
    heights = [10, 100, 100, 10, 100, 100, 10, 100, 100, 10]
    expected = 0
    result = frog_jump_k_steps_tabulation_space_optimized(n, k, heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
