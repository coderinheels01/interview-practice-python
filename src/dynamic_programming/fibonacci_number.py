"""509. Fibonacci Number

Return F(n), where F(0) = 0, F(1) = 1, and
F(n) = F(n - 1) + F(n - 2) for n > 1.

Examples:
    Input: n = 2
    Output: 1

    Input: n = 4
    Output: 3

Constraints:
    - 0 <= n <= 30

https://www.youtube.com/watch?v=tyB0ztf0DNY&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=5

"""


def fibonacci_number_recursive(n: int, dp: list[int]) -> int:
    """Return the Fibonacci number at index n and write results into dp.

    Approach: Naive Recursion with Result Storage
        1. If n is 0 or 1, return n. These two answers are already known.
        2. Otherwise, ask the same function to calculate the previous two
           Fibonacci numbers. Add their answers and store the sum at dp[n].
           For example, F(3) is F(2) + F(1), which is 1 + 1 = 2.
        3. Return the answer stored at dp[n].

        This implementation writes answers into dp but does not read saved
        answers before making recursive calls. It therefore repeats work;
        it is not memoization (reusing previously saved answers).

    Parameters:
        n: The requested index, with 0 <= n <= 30.
        dp: A writable list with at least n + 1 entries.

    Returns:
        F(n), with F(0) = 0 and F(1) = 1.

    Mutation Behavior:
        Updates entries in the caller's dp list for indexes from 2 through n.
        Base cases return directly without writing into dp.

    Time Complexity:
        Let n be the requested index. Each base case takes O(1), meaning
        constant time. Every other call makes two smaller calls and adds
        their answers. For n = 5, F(3) is calculated both inside F(4) and
        again separately. These repeated calculations grow exponentially.
        A call tree of depth at most n with up to two children per call has
        O(2^n) calls. Constant work per call gives O(2^n) time; the tighter
        bound is Theta(phi^n), where phi is approximately 1.618.
        Interview answer: exponential time because results are recalculated.

    Space Complexity:
        The input integer is excluded from auxiliary (extra) space. The
        caller supplies n + 1 list entries: for n = 5, that is 6 entries.
        The longest chain of unfinished calls has O(n) stack frames. Each
        frame holds a reference to the same list, not a copy of that list.
        Counting the supplied table, O(n) table space + O(n) stack space
        gives O(n) extra space. Beyond the supplied list, the function still
        needs O(n) stack space. The entire call tree is never stored at once.
        For n = 0 or 1, the function itself uses O(1) extra space.
        Interview answer: O(n) space for the table and recursion stack.

    Assumptions:
        Inputs satisfy the stated constraints and Python has enough recursion
        depth. Arithmetic on the bounded Fibonacci values takes constant time.
    """
    # Step 1: Return either of the two known starting values.
    if n < 2:
        return n

    # Step 2: Calculate the previous two numbers and store their sum.
    dp[n] = fibonacci_number_recursive(n - 1, dp) + fibonacci_number_recursive(
        n - 2, dp
    )

    # Step 3: Return the stored answer.
    return dp[n]


def fibonacci_number_tabulation(n: int) -> int:
    """Return the Fibonacci number at index n using a table.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. If n is 0 or 1, return n immediately. No table is needed.
        2. Make a list with n + 1 entries, so indexes 0 through n all exist.
           For n = 3, we need four slots: dp[0], dp[1], dp[2], and dp[3].
           The initial -1 values are placeholders to be replaced.
        3. Put the two known starting answers into the table: 0 and 1.
        4. Visit each index from 2 through n, including n. Add the previous
           two stored answers to get the answer for this index.
           For n = 3, the table becomes [0, 1, 1, 2]. Python's range stops
           before its ending value, so range(2, n + 1) includes index n.
        5. Return dp[n], the answer at the requested index.

    Parameters:
        n: The requested index, with 0 <= n <= 30.

    Returns:
        F(n), with F(0) = 0 and F(1) = 1.

    Mutation Behavior:
        Changes only its own local table; no caller-owned data is modified.

    Time Complexity:
        Let n be the requested index. For n = 5, creating the table fills
        6 entries, and the loop fills indexes 2, 3, 4, and 5: 4 iterations.
        Creating n + 1 entries takes O(n) time. Setting the first two values
        takes O(1) time. The loop runs n - 1 times, with two reads, one
        addition, and one write each time: constant work per iteration,
        giving O(n) loop time. Returning one value takes O(1) time.
        These phases happen one after another, so their costs add:
        O(n) + O(1) + O(n) + O(1) = O(n).
        For n = 0 or 1, the early return takes O(1) time.
        Interview answer: O(n) time because each table entry is filled once.

    Space Complexity:
        Excluding the input integer, the table holds exactly n + 1 entries
        when n >= 2. For n = 5, that is 6 entries. The index and other local
        bookkeeping need O(1) space. There are no recursive calls, so there
        is no growing recursion stack. O(n) table space + O(1) bookkeeping
        gives O(n) extra space. For n = 0 or 1, no table is created and
        extra space is O(1).
        Interview answer: O(n) extra space for the table.

    Assumptions:
        n satisfies the stated constraints. Arithmetic on the bounded
        Fibonacci values takes constant time.
    """
    # Step 1: Return either known starting value without making a table.
    if n < 2:
        return n

    # Step 2: Reserve a slot for every index from 0 through n.
    dp: list[int] = [-1] * (n + 1)
    # Step 3: Store the two known starting answers.
    dp[0] = 0
    dp[1] = 1

    # Step 4: Fill each remaining slot using the previous two answers.
    for index in range(2, n + 1):
        dp[index] = dp[index - 1] + dp[index - 2]

    # Step 5: Read the answer at the requested index.
    return dp[n]


def fibonacci_number_tabulation_space_optimized(n: int) -> int:
    """Return F(n) while keeping only the two most recent answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. If n is 0 or 1, return n. These answers are already known.
        2. Start with the first two Fibonacci numbers: previous = 0 and
           previous2 = 1. There is no need to keep a whole list because
           calculating the next number needs only these two numbers.
        3. Count from index 2 through n, including n. At each index, add
           the two saved numbers to calculate the current Fibonacci number.
        4. Move the saved numbers forward: put the old previous2 into
           previous, then put the new answer into previous2. This prepares
           the two numbers needed for the next round. The order matters:
           save the old previous2 before replacing it with the new answer.
        5. After the loop, return the last answer calculated.

        Example for n = 5:
            Start:   previous = 0, previous2 = 1
            Index 2: 0 + 1 = 1; saved numbers become 1 and 1.
            Index 3: 1 + 1 = 2; saved numbers become 1 and 2.
            Index 4: 1 + 2 = 3; saved numbers become 2 and 3.
            Index 5: 2 + 3 = 5; saved numbers become 3 and 5.
            Return 5.

    Parameters:
        n: The requested Fibonacci index, with 0 <= n <= 30.

    Returns:
        F(n), where F(0) = 0 and F(1) = 1.

    Mutation Behavior:
        Changes only local variables; no caller-owned data is modified.

    Time Complexity:
        Let n be the requested index. The starting check and variable setup
        take O(1), meaning constant time. The loop visits indexes 2 through
        n, so it runs n - 1 times when n >= 2. For n = 5, it runs 4 times.
        Each round does one addition and a fixed number of assignments,
        which is O(1) work. Thus the loop takes (n - 1) * O(1) = O(n).
        Returning the answer takes O(1). These phases happen sequentially,
        so O(1) + O(n) + O(1) = O(n) time overall.
        For n = 0 or 1, the early return takes O(1) time.
        Interview answer: O(n) time because each new number is computed once.

    Space Complexity:
        Excluding the input n, the function uses four named integer locals:
        previous, previous2, current_fibonacci_number, and index. For n = 5
        and n = 30, it still uses only these same four variables. The loop
        replaces their values instead of keeping every earlier answer.
        Temporary addition results and loop bookkeeping also require only
        a fixed amount of space. There is no list or growing recursion stack.
        Four fixed variable slots plus fixed temporary storage give O(1)
        auxiliary (extra) space. We count the maximum storage needed at
        one time, not all values assigned over the entire loop.
        Interview answer: O(1) extra space because only a fixed number of
        values are kept, regardless of n.

    Assumptions:
        n satisfies the stated constraints. Values fit within a bounded
        number of bits for this range, so integer storage and addition are
        treated as constant cost. For n >= 2, the loop runs at least once,
        assigning current_fibonacci_number before it is returned.
    """
    # Step 1: Return either known starting answer immediately.
    if n < 2:
        return n

    # Step 2: Keep the two starting numbers and a name for the next answer.
    previous: int = 0
    previous2: int = 1
    current_fibonacci_number: int

    # Step 3: Calculate each next number, up to and including index n.
    for index in range(2, n + 1):
        current_fibonacci_number = previous + previous2
        # Step 4: Move the saved pair forward for the next round.
        previous = previous2
        previous2 = current_fibonacci_number

    # Step 5: Return the final number calculated.
    return current_fibonacci_number


def solve() -> None:
    n: int = 2
    dp: list[int] = [-1] * (n + 1)
    expected: int = 1
    result: int = fibonacci_number_recursive(n, dp)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input and zero base case.
    n = 0
    dp = [-1] * (n + 1)
    expected = 0
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Upper boundary of the base case.
    n = 1
    dp = [-1] * (n + 1)
    expected = 1
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First input requiring the recurrence.
    n = 2
    dp = [-1] * (n + 1)
    expected = 1
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Recurrence combines a recursive result and a base case.
    n = 3
    dp = [-1] * (n + 1)
    expected = 2
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both preceding indexes are beyond the base cases.
    n = 4
    dp = [-1] * (n + 1)
    expected = 3
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Typical input.
    n = 10
    dp = [-1] * (n + 1)
    expected = 55
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Middle of the allowed range.
    n = 15
    dp = [-1] * (n + 1)
    expected = 610
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One below the maximum input.
    n = 29
    dp = [-1] * (n + 1)
    expected = 514229
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed input.
    n = 30
    dp = [-1] * (n + 1)
    expected = 832040
    result = fibonacci_number_recursive(n, dp)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 0.
    n = 0
    expected = 0
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 1.
    n = 1
    expected = 1
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 2.
    n = 2
    expected = 1
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 3.
    n = 3
    expected = 2
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 4.
    n = 4
    expected = 3
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 5.
    n = 5
    expected = 5
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 10.
    n = 10
    expected = 55
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 15.
    n = 15
    expected = 610
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 29.
    n = 29
    expected = 514229
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: n = 30.
    n = 30
    expected = 832040
    result = fibonacci_number_tabulation(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum input.
    n = 0
    expected = 0
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Second base case.
    n = 1
    expected = 1
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: First loop iteration.
    n = 2
    expected = 1
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two loop iterations.
    n = 3
    expected = 2
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Multiple updates.
    n = 4
    expected = 3
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Small example.
    n = 5
    expected = 5
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Typical input.
    n = 10
    expected = 55
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Middle of the range.
    n = 15
    expected = 610
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Below the maximum.
    n = 29
    expected = 514229
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum input.
    n = 30
    expected = 832040
    result = fibonacci_number_tabulation_space_optimized(n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
