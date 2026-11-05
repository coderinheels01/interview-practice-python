"""70. Climbing Stairs

You are climbing a staircase with n steps to reach the top. Each move lets
you climb either 1 step or 2 steps. Return the number of distinct sequences
of moves that take you to the top. Different orders count as different ways.

Example 1:
    Input: n = 2
    Output: 2
    Explanation: The two ways are:
        1. 1 step + 1 step
        2. 2 steps

Example 2:
    Input: n = 3
    Output: 3
    Explanation: The three ways are:
        1. 1 step + 1 step + 1 step
        2. 1 step + 2 steps
        3. 2 steps + 1 step

Constraints:
    - 1 <= n <= 45

                             3 stairs left
                        /             \
                  take 1               take 2
                    /                     \
             2 stairs left            1 stair left
             /          \\              /         \
         take 1        take 2      take 1       take 2
           /              \\          /             \
     1 stair left       0 left     0 left         -1 left
       /      \\           ✅         ✅              ❌
   take 1    take 2
     /          \
   0 left     -1 left
     ✅          ❌
"""


def climbing_stairs_recursion(n: int) -> int:

    # n means the number of stairs still left to climb.
    # With 0 left, the moves taken reached the top exactly. Count this as
    # 1 successful way, even though no more moves are needed. For example,
    # starting with 3 stairs and taking 1 then 2 leaves 0 stairs.
    if n == 0:
        return 1
    # A negative number means the last move went past the top. This path
    # contributes 0 ways. For example, taking 2 with 1 left leaves -1.
    if n < 0:
        return 0

    return climbing_stairs_recursion(n - 1) + climbing_stairs_recursion(n - 2)


def climbing_stairs_memoization(n: int, dp: list[int]) -> int:
    # n means the number of stairs still left to climb.
    # With 0 left, the moves taken reached the top exactly. Count this as
    # 1 successful way, even though no more moves are needed. For example,
    # starting with 3 stairs and taking 1 then 2 leaves 0 stairs.
    if n == 0:
        return 1
    # A negative number means the last move went past the top. This path
    # contributes 0 ways. For example, taking 2 with 1 left leaves -1.
    if n < 0:
        return 0

    # Check the base cases before indexing dp: a negative Python index
    # would read from the end of the list instead of representing an overshoot.
    # -1 means not calculated yet; any other value is an answer we can reuse.
    if dp[n] != -1:
        return dp[n]

    dp[n] = climbing_stairs_memoization(n - 1, dp) + climbing_stairs_memoization(
        n - 2, dp
    )

    return dp[n]


def climbing_stairs_tabulation(n: int) -> int:
    """Return the number of ways to climb n stairs using 1- or 2-step moves.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Make a table called dp with a slot for every stair count from
           0 through n. Each slot will store the number of ways to reach
           that stair. The initial -1 values are placeholders.
        2. Set dp[0] to 1. There is one way to reach the starting position:
           take no steps. This also lets a single 2-step move count as one
           way when we calculate dp[2].
        3. Visit stair counts 1 through n in order. For stair 1, copy dp[0]:
           there is only one way to get there, by taking one step.
        4. For each stair from 2 onward, add the ways to reach the previous
           two stairs. Every path ends with either a 1-step move from the
           previous stair or a 2-step move from two stairs back. These are
           different groups of paths, so adding them counts every way once.
           The checks avoid reading negative table indexes.
        5. Return dp[n], the number of ways to reach the requested stair.

        Example for n = 3:
            Start: dp = [1, -1, -1, -1].
            Stair 1: dp[1] = dp[0] = 1.
            Stair 2: dp[2] = dp[1] + dp[0] = 1 + 1 = 2.
            Stair 3: dp[3] = dp[2] + dp[1] = 2 + 1 = 3.
            Return 3. The three paths are 1+1+1, 1+2, and 2+1.

    Parameters:
        n: The total number of stairs, with 1 <= n <= 45.

    Returns:
        The number of distinct sequences of 1- and 2-step moves that reach
        the top exactly. Different move orders count as different ways.

    Mutation Behavior:
        Only changes its local table; no caller-owned data is modified.

    Time Complexity:
        Let n be the number of stairs. Creating n + 1 table entries takes
        O(n) time. For n = 3, this creates 4 entries. Setting dp[0] takes
        O(1), meaning constant time. The loop runs exactly n times: for
        n = 3, it visits 1, 2, and 3. Each visit performs two fixed checks
        and a fixed number of table reads, additions, and writes. This is
        O(1) work per visit, so n visits take O(n). Returning one entry
        takes O(1). These phases happen in sequence, so their costs add:
        O(n) + O(1) + O(n) + O(1) = O(n).
        Interview answer: O(n) time because each stair's answer is filled once.

    Space Complexity:
        Excluding the input integer, dp stores exactly n + 1 entries.
        For n = 3, that is 4 entries. The loop index and temporary values
        use O(1) space. Each loop visit replaces a table entry rather than
        creating another table. We count the largest storage in use at one
        time, not the sum of all assignments. There are no recursive calls
        and no growing call stack. O(n) table space + O(1) other space
        gives O(n) auxiliary (extra) space.
        Interview answer: O(n) extra space for the table of stair counts.

    Assumptions:
        n satisfies the problem constraints. Within this range, integer
        addition and storage are treated as constant cost.
    """
    # Step 1: Reserve slots for stair counts 0 through n.
    dp: list[int] = [-1] * (n + 1)
    # Step 2: Count taking no steps as one way to reach stair 0.
    dp[0] = 1

    # Step 3: Visit each stair in order and handle the single-stair case.
    for stairs in range(1, n + 1):
        if stairs == 1:
            dp[stairs] = dp[stairs - 1]

        # Step 4: Count paths arriving with a final move of 1 or 2 steps.
        if stairs >= 2:
            dp[stairs] = dp[stairs - 1] + dp[stairs - 2]

    # Step 5: Return the number of ways to reach the top.
    return dp[n]


def climbing_stairs_tabulation_space_optimized(n: int) -> int:
    """Count ways to climb n stairs while keeping only two earlier answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. If n is 0 or 1, return 1. With 0 stairs, taking no steps is one
           way to finish. With 1 stair, taking one step is the only way.
        2. Start with the answers for stair 0 and stair 1: both are 1.
           Keep them in two_steps_back and one_step_back. We only need
           these two answers to calculate the next one, so no list is needed.
        3. Visit stairs 2 through n. For each stair, add the two saved
           answers. Every path arrives with either a final 1-step move from
           one stair back or a final 2-step move from two stairs back.
        4. Move the saved answers forward. First, copy one_step_back into
           two_steps_back. Then put the new answer into one_step_back.
           This order preserves the older answer until it has been copied.
        5. Return the last number_of_ways calculated, which belongs to n.

        Example for n = 3:
            Start: two_steps_back = 1, one_step_back = 1.
            Stair 2: add 1 + 1 = 2. Move the saved pair to 1 and 2.
            Stair 3: add 1 + 2 = 3. Move the saved pair to 2 and 3.
            Return 3: the paths are 1+1+1, 1+2, and 2+1.

    Parameters:
        n: The total number of stairs. The problem requires 1 <= n <= 45;
           this function also supports n = 0.

    Returns:
        The number of sequences of 1- and 2-step moves reaching the top
        exactly. Different orders count separately. Returns 1 for n = 0.

    Mutation Behavior:
        Changes only local variables; no caller-owned data is modified.

    Time Complexity:
        Let n be the number of stairs. The initial check and setup take
        O(1), meaning constant time. For n >= 2, the loop visits stairs 2
        through n: exactly n - 1 iterations. For n = 3, that is 2 visits.
        Each visit does one addition and two updates, which is constant
        work. Thus (n - 1) * O(1) gives O(n) loop time. The final return
        takes O(1). These sequential costs add to O(1) + O(n) + O(1),
        which simplifies to O(n). For n = 0 or 1, time is O(1).
        Interview answer: O(n) time because each stair's answer is computed once.

    Space Complexity:
        Excluding the input n, there are four named integer locals:
        two_steps_back, one_step_back, number_of_ways, and stairs.
        For both n = 3 and n = 45, the same four variable slots are used.
        Temporary addition results and loop bookkeeping also use a fixed
        amount of storage. Each iteration replaces values rather than
        storing another answer in a growing list. We count the maximum
        storage used at once, not all assignments made during the loop.
        Four fixed slots plus fixed temporary storage gives O(1) extra
        space. There is no table and no growing recursion stack.
        Interview answer: O(1) auxiliary space because the number of saved
        values does not grow with n.

    Assumptions:
        n is a nonnegative integer no larger than 45. Negative inputs are
        unsupported. For n >= 2, the loop runs at least once, assigning
        number_of_ways before it is returned. Within the stated range,
        integer addition and storage are treated as constant cost.
    """
    # Step 1: Return the known answer for 0 or 1 stairs.
    if 0 <= n < 2:
        return 1
    # Step 2: Keep the answers for stair 0 and stair 1.
    two_steps_back: int = 1
    one_step_back: int = 1
    number_of_ways: int

    # Step 3: Add the previous two answers for each stair through n.
    for stairs in range(2, n + 1):
        number_of_ways = two_steps_back + one_step_back
        # Step 4: Move the pair forward to prepare for the next stair.
        two_steps_back = one_step_back
        one_step_back = number_of_ways

    # Step 5: Return the answer calculated for stair n.
    return number_of_ways


def solve() -> None:
    n: int = 2
    expected: int = 2
    result: int = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum allowed input.
    n = 1
    expected = 1
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First input with two possible step sizes.
    n = 2
    expected = 2
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Question example with mixed step orders.
    n = 3
    expected = 3
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple recursive levels.
    n = 4
    expected = 5
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Small typical input.
    n = 5
    expected = 8
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Typical input.
    n = 10
    expected = 89
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Middle of the allowed range.
    n = 23
    expected = 46368
    result = climbing_stairs_recursion(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")



    # Memoization: Minimum input; reaches both recursive base cases.
    n = 1
    dp = [-1] * (n + 1)
    expected = 1
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: First input allowing a two-step move.
    n = 2
    dp = [-1] * (n + 1)
    expected = 2
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Repeated subproblem and question example.
    n = 3
    dp = [-1] * (n + 1)
    expected = 3
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Multiple recursive levels.
    n = 4
    dp = [-1] * (n + 1)
    expected = 5
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Small typical input.
    n = 5
    dp = [-1] * (n + 1)
    expected = 8
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Typical input.
    n = 10
    dp = [-1] * (n + 1)
    expected = 89
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Middle of the allowed range.
    n = 23
    dp = [-1] * (n + 1)
    expected = 46368
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: One below the maximum.
    n = 44
    dp = [-1] * (n + 1)
    expected = 1134903170
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum allowed input.
    n = 45
    dp = [-1] * (n + 1)
    expected = 1836311903
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Reuse an answer already stored in the table.
    n = 3
    dp = [-1, 1, 2, 3]
    expected = 3
    result = climbing_stairs_memoization(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum input and index == 1 branch.
    n = 1
    expected = 1
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: First index >= 2 iteration.
    n = 2
    expected = 2
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Question example.
    n = 3
    expected = 3
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Repeated table updates.
    n = 4
    expected = 5
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Small typical input.
    n = 5
    expected = 8
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Typical input.
    n = 10
    expected = 89
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Middle of the allowed range.
    n = 23
    expected = 46368
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: One below the maximum.
    n = 44
    expected = 1134903170
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum allowed input.
    n = 45
    expected = 1836311903
    result = climbing_stairs_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum input; loop does not run.
    n = 1
    expected = 1
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: First loop iteration.
    n = 2
    expected = 2
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two loop iterations.
    n = 3
    expected = 3
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Multiple updates.
    n = 4
    expected = 5
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Small typical input.
    n = 5
    expected = 8
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Typical input.
    n = 10
    expected = 89
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Middle of the allowed range.
    n = 23
    expected = 46368
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: One below the maximum.
    n = 44
    expected = 1134903170
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum allowed input.
    n = 45
    expected = 1836311903
    result = climbing_stairs_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
