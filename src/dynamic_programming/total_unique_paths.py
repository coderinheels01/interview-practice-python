"""Total Unique Paths

You start at point A, the top-left cell of a grid with m rows and n columns.
Your destination is point B, the bottom-right cell of the same grid.

Return the total number of unique paths from cell (0, 0) to cell
(m - 1, n - 1). At each step, you may move only right or down, remaining
within the grid:
    - Right: (row, col) -> (row, col + 1)
    - Down: (row, col) -> (row + 1, col)

The inputs are the grid dimensions; no matrix of cell values is needed.

Example (added for practice):
    Input: m = 2, n = 3
    Output: 3
    Explanation:
        The three paths are:
        1. Right -> Right -> Down
        2. Right -> Down -> Right
        3. Down -> Right -> Right

Example 2 (added for practice):
    Input: m = 1, n = 1
    Output: 1
    Explanation:
        The starting cell is also the destination. Taking no moves counts
        as one path.

Example 3 (added for practice):
    Input: m = 1, n = 4
    Output: 1
    Explanation:
        With only one row, the only path is Right -> Right -> Right.

Example 4 (added for practice):
    Input: m = 4, n = 1
    Output: 1
    Explanation:
        With only one column, the only path is Down -> Down -> Down.

Example 5 (added for practice):
    Input: m = 2, n = 2
    Output: 2
    Explanation:
        The paths are Right -> Down and Down -> Right.

Example 6 (added for practice):
    Input: m = 3, n = 3
    Output: 6
    Explanation:
        Each path contains two right moves and two down moves.
        The six orders are RRDD, RDRD, RDDR, DRRD, DRDR, and DDRR.
        Here R means Right and D means Down.

Example 7 (added for practice):
    Input: m = 3, n = 2
    Output: 3
    Explanation:
        The paths are Right -> Down -> Down, Down -> Right -> Down,
        and Down -> Down -> Right.

Input Format (original problem):
    The first line contains t, the number of test cases.
    Each test case contains two space-separated integers m and n,
    representing the number of rows and columns respectively.

Output Format:
    For each test case, output one integer: the number of unique paths
    from the top-left cell to the bottom-right cell.

Assumptions:
    m >= 1 and n >= 1.
    Numeric constraints and sample cases are not visible in the screenshot.

https://www.youtube.com/watch?v=sdE0A2Oxofw&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=9

"""


def total_unique_paths_recursion(m: int, n: int) -> int:
    """Count paths from the top-left cell to the bottom-right cell.

    Approach: Naive Recursion
        1. Define find_paths(row, col) to count ways to reach that cell
           from (0, 0). We work backward from the destination.
        2. At (0, 0), return 1. Reaching the starting cell completes one
           path; no more moves are needed. Returning 0 would lose that path.
        3. Start the counts from above and from the left at 0. A direction
           stays at 0 when that neighboring cell does not exist.
        4. If row > 0, ask how many paths reach the cell directly above.
           Each of those paths can take one down move into the current cell.
        5. If col > 0, ask how many paths reach the cell directly left.
           Each of those paths can take one right move into the current cell.
           These checks prevent calls outside the grid.
        6. Add the two counts. Every path arrives from above or from the
           left, and those groups are different, so both contribute.
        7. Start at (m - 1, n - 1). Dimensions are counts; indexes start at 0.

        Example: m = 2, n = 3.
            The destination is (1, 2).
            There is 1 path to the cell above it, (0, 2).
            There are 2 paths to the cell left of it, (1, 1).
            Add them: 1 + 2 = 3 paths to the destination.

    Parameters:
        m: Number of rows, at least 1.
        n: Number of columns, at least 1.

    Returns:
        Number of paths using only right and down moves. A single cell has
        one path: stay there. A single row or column also has one path.

    Mutation Behavior:
        Does not modify inputs or any external state. No grid is created.

    Time Complexity: O(2^(m + n)) upper bound
        Imagine each call asking up to two more questions. Those questions
        keep splitting for at most m + n - 2 moves, repeating work on the
        same cells. This can grow exponentially; a single row or column
        instead has only one chain and takes O(m + n) time.

    Space Complexity: O(m + n)
        Think of paused calls as a stack of plates. Only one branch runs
        at a time, with at most m + n - 1 helper calls stacked together.
        The input dimensions are excluded from extra space.

    Assumptions:
        m and n are positive integers. Python needs enough recursion depth
        for the longest chain. Arithmetic is treated as constant cost;
        numeric upper limits were not provided.
    """

    # Step 1: Count paths to a cell by looking backward at its neighbors.
    def find_paths(row: int, col: int) -> int:
        # Step 2: Reaching the starting cell completes one path.
        if row == 0 and col == 0:
            return 1

        # Step 3: A missing neighbor contributes zero paths.
        up: int = 0
        left: int = 0

        # Step 4: Count paths arriving from the cell above, if it exists.
        if row > 0:
            up = find_paths(row=row - 1, col=col)
        # Step 5: Count paths arriving from the cell to the left, if it exists.
        if col > 0:
            left = find_paths(row=row, col=col - 1)

        # Step 6: Add the two different groups of paths.
        return up + left

    # Step 7: Begin at the destination's indexes, not the dimension counts.
    return find_paths(row=m - 1, col=n - 1)


def total_unique_paths_memoization(m: int, n: int) -> int:
    """Count right-and-down paths while saving answers for previously seen cells.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Make an m-row, n-column cache. Start each entry at -1, meaning
           the number of paths to that cell has not been calculated yet.
        2. Define find_paths(row, col) to count ways to reach that cell
           from (0, 0). At (0, 0), return 1: reaching the start completes
           one path. No further moves are needed for that branch.
        3. If the cell's answer is saved, return it immediately. This avoids
           repeating the same question when another branch reaches the cell.
        4. Start the counts from above and from the left at 0. If row > 0,
           ask for the paths to the cell above. If col > 0, ask for the paths
           to the cell on the left. The checks prevent negative indexes;
           a missing neighbor contributes no paths.
        5. Add the two counts and save the result for this cell. Every path
           arrives from above or from the left, so both groups contribute.
        6. Return the saved total. Each caller uses it in its own calculation.
        7. Start at (m - 1, n - 1), the destination's zero-based indexes,
           and return its answer.

        Example: m = 2, n = 3.
            The destination is (1, 2). There is 1 path to (0, 2) and
            2 paths to (1, 1). Add them to get 3 paths to (1, 2).
            When both branches ask about the same cell, its saved answer
            is reused instead of calculating its earlier paths again.

    Parameters:
        m: Number of rows, at least 1.
        n: Number of columns, at least 1.

    Returns:
        Number of unique paths from top-left to bottom-right, moving only
        right or down. A single cell, row, or column has one path.

    Mutation Behavior:
        Updates only its local cache; inputs and external state are unchanged.

    Time Complexity: O(m * n)
        There are m * n cells. Each cell's answer is calculated once, and
        later calls reuse it, doing only a fixed amount of work per cell.

    Space Complexity: O(m * n + m + n), simplifying to O(m * n)
        The cache stores m * n answers. Paused calls also use a stack of
        O(m + n) depth. The input dimensions are excluded from extra space.

    Assumptions:
        m and n are positive integers. Python needs enough recursion depth
        for a chain of m + n - 1 helper calls. Numeric limits were not
        provided; arithmetic is treated as constant cost.
    """
    # Step 1: Reserve a cache entry for every cell.
    path_sum_dp: list[list[int]] = [[-1] * n for _ in range(m)]

    # Step 2: Count paths to a cell, stopping at the starting cell.
    def find_paths(row: int, col: int) -> int:
        if row == 0 and col == 0:
            return 1

        # Step 3: Reuse a saved answer before making more calls.
        if path_sum_dp[row][col] != -1:
            return path_sum_dp[row][col]

        # Step 4: Count paths from each neighbor only when it exists.
        up: int = 0
        left: int = 0
        if row > 0:
            up = find_paths(row=row - 1, col=col)

        if col > 0:
            left = find_paths(row=row, col=col - 1)

        # Step 5: Add and save the two different groups of paths.
        path_sum_dp[row][col] = up + left

        # Step 6: Return this cell's completed answer.
        return path_sum_dp[row][col]

    # Step 7: Start at the destination's indexes.
    return find_paths(row=m - 1, col=n - 1)


def total_unique_paths_tabulation(m: int, n: int) -> int:
    """Count right-and-down paths by filling a table from the starting cell.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Make a table with m rows and n columns, initially filled with 0.
           Each cell will store the number of paths from (0, 0) to that cell.
        2. Set the starting cell to 1. Staying there counts as one path,
           even though no moves are needed.
        3. Visit cells row by row, from left to right. Skip the starting
           cell so its saved 1 is not overwritten.
        4. Start up and left at 0. Read the cell above only if row > 0,
           and the cell to the left only if col > 0. Missing neighbors
           contribute no paths; these checks also avoid negative indexes.
        5. Add up and left and save the total. Every path into this cell
           comes from one of these two neighbors, so both groups count.
           On the first row, only left contributes. On the first column,
           only up contributes. This makes every edge cell's answer 1.
        6. Return the bottom-right cell, at indexes (m - 1, n - 1).

        Example: m = 2, n = 3.
            Start:              After filling the first row:
                [1, 0, 0]           [1, 1, 1]
                [0, 0, 0]           [0, 0, 0]
            Fill the second row:
                (1, 0): up 1 + left 0 = 1.
                (1, 1): up 1 + left 1 = 2.
                (1, 2): up 1 + left 2 = 3.
            Return 3.

    Parameters:
        m: Number of rows, at least 1.
        n: Number of columns, at least 1.

    Returns:
        Number of unique paths using only right and down moves. A single
        cell, single row, or single column has one path.

    Mutation Behavior:
        Updates only its local table; inputs and external state are unchanged.

    Time Complexity: O(m * n)
        The grid has m * n cells. Creating the table and visiting every
        cell each take linear time in that cell count.

    Space Complexity: O(m * n)
        The table stores one answer per cell. The input dimensions are
        excluded from extra space, and no recursion stack is needed.

    Assumptions:
        m and n are positive integers. Numeric upper limits were not
        provided; arithmetic is treated as constant cost.
    """
    # Step 1: Reserve a path-count entry for every cell.
    path_sum_dp: list[list[int]] = [[0] * n for _ in range(m)]
    # Step 2: Count the starting position as one path.
    path_sum_dp[0][0] = 1

    # Step 3: Fill cells in order, preserving the initialized starting cell.
    for row in range(m):
        for col in range(n):
            if row == 0 and col == 0:
                continue
            # Step 4: Missing neighbors count as zero; read only valid ones.
            up: int = 0
            left: int = 0
            if row > 0:
                up = path_sum_dp[row - 1][col]
            if col > 0:
                left = path_sum_dp[row][col - 1]

            # Step 5: Combine paths arriving from above and from the left.
            path_sum_dp[row][col] = up + left

    # Step 6: Return the number of paths to the destination.
    return path_sum_dp[m - 1][n - 1]


def total_unique_paths_tabulation_space_optimized(m: int, n: int) -> int:
    """Count right-and-down paths using a single reusable row of answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Create a list of n zeros, with one slot per column. This list
           replaces the full grid of saved answers.
        2. Visit cells row by row, from left to right. Set the starting
           cell's answer to 1: staying at the start counts as one path.
        3. For every other cell, start up and left at 0. Missing neighbors
           contribute no paths.
        4. If a row exists above, read paths[col]. Before this slot is
           updated, it still holds the answer for the cell in the previous row.
        5. If a column exists to the left, read paths[col - 1]. That slot
           has already been updated for the current row. This is why the
           loop must process columns from left to right.
        6. Add up and left, then replace paths[col] with this cell's answer.
           The old value is no longer needed: the next column reads its own
           old value from above and this newly saved value from the left.
        7. After the final row, return paths[n - 1], the destination's count.

        Example: m = 2, n = 3.
            Start: paths = [0, 0, 0].
            First row: [1, 1, 1].
            Second row, column 0: up 1 + left 0 -> [1, 1, 1].
            Second row, column 1: up 1 + left 1 -> [1, 2, 1].
            Second row, column 2: up 1 + left 2 -> [1, 2, 3].
            Return 3. Only one list was needed for both rows.

    Parameters:
        m: Number of rows, at least 1.
        n: Number of columns, at least 1.

    Returns:
        Number of paths from top-left to bottom-right using only right and
        down moves. A single cell, row, or column has one path.

    Mutation Behavior:
        Updates only its local paths list; inputs and external state are unchanged.

    Time Complexity: O(m * n)
        The loops visit all m * n cells once. Each visit does a fixed amount
        of work, such as reading two counts and adding them.

    Space Complexity: O(n)
        The reusable list holds n column answers, regardless of the number
        of rows. Input dimensions are excluded from extra space.

    Assumptions:
        m and n are positive integers. Numeric upper limits were not provided;
        arithmetic is treated as constant cost.
    """
    # Step 1: Reserve one reusable answer slot per column.
    paths: list[int] = [0] * n
    # Step 2: Process rows in order and columns from left to right.
    for row in range(m):
        for col in range(n):
            if row == 0 and col == 0:
                paths[col] = 1
            else:
                # Step 3: Missing neighbors contribute zero paths.
                up: int = 0
                left: int = 0
                # Step 4: This slot still holds the previous row's answer.
                if row > 0:
                    up = paths[col]
                # Step 5: The left slot already holds the current row's answer.
                if col > 0:
                    left = paths[col - 1]
                # Step 6: Replace the old answer with this cell's total.
                paths[col] = up + left

    # Step 7: Read the bottom-right answer after the final row is complete.
    return paths[n - 1]


def solve() -> None:
    m: int = 2
    n: int = 3
    expected: int = 3
    result: int = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single cell; start equals destination.
    m = 1
    n = 1
    expected = 1
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row; only right moves.
    m = 1
    n = 5
    expected = 1
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column; only down moves.
    m = 5
    n = 1
    expected = 1
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First grid requiring both directions.
    m = 2
    n = 2
    expected = 2
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Transposed example.
    m = 3
    n = 2
    expected = 3
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Small square.
    m = 3
    n = 3
    expected = 6
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide rectangle.
    m = 2
    n = 5
    expected = 5
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall rectangle.
    m = 5
    n = 2
    expected = 5
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Rectangle with multiple branching paths.
    m = 3
    n = 4
    expected = 10
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Transposed rectangle.
    m = 4
    n = 3
    expected = 10
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger square.
    m = 4
    n = 4
    expected = 20
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several recursive levels.
    m = 5
    n = 5
    expected = 70
    result = total_unique_paths_recursion(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: a two-row, three-column grid.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single cell.
    m = 1
    n = 1
    expected = 1
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row.
    m = 1
    n = 10
    expected = 1
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single column.
    m = 10
    n = 1
    expected = 1
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Both movement directions.
    m = 2
    n = 2
    expected = 2
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Original example.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Transposed example.
    m = 3
    n = 2
    expected = 3
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Small square.
    m = 3
    n = 3
    expected = 6
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Wide rectangle.
    m = 2
    n = 5
    expected = 5
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tall rectangle.
    m = 5
    n = 2
    expected = 5
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Overlapping subproblems.
    m = 3
    n = 4
    expected = 10
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Transposed rectangle.
    m = 4
    n = 3
    expected = 10
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Larger square.
    m = 5
    n = 5
    expected = 70
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Many cached states.
    m = 10
    n = 10
    expected = 48620
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Large integer path count.
    m = 20
    n = 20
    expected = 35345263800
    result = total_unique_paths_memoization(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: a two-row, three-column grid.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single cell.
    m = 1
    n = 1
    expected = 1
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row; no upper neighbor.
    m = 1
    n = 10
    expected = 1
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single column; no left neighbor.
    m = 10
    n = 1
    expected = 1
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Both movement directions.
    m = 2
    n = 2
    expected = 2
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Original example.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Transposed example.
    m = 3
    n = 2
    expected = 3
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Small square.
    m = 3
    n = 3
    expected = 6
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Wide rectangle.
    m = 2
    n = 5
    expected = 5
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Tall rectangle.
    m = 5
    n = 2
    expected = 5
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Multiple paths per interior cell.
    m = 3
    n = 4
    expected = 10
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Transposed rectangle.
    m = 4
    n = 3
    expected = 10
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Larger square.
    m = 5
    n = 5
    expected = 70
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Many table entries.
    m = 10
    n = 10
    expected = 48620
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Large integer path count.
    m = 20
    n = 20
    expected = 35345263800
    result = total_unique_paths_tabulation(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: a two-row, three-column grid.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single cell.
    m = 1
    n = 1
    expected = 1
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single row.
    m = 1
    n = 10
    expected = 1
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single column.
    m = 10
    n = 1
    expected = 1
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Both movement directions.
    m = 2
    n = 2
    expected = 2
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Original example.
    m = 2
    n = 3
    expected = 3
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Transposed example.
    m = 3
    n = 2
    expected = 3
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Small square.
    m = 3
    n = 3
    expected = 6
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Wide rectangle.
    m = 2
    n = 5
    expected = 5
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Tall rectangle.
    m = 5
    n = 2
    expected = 5
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Multiple row updates.
    m = 3
    n = 4
    expected = 10
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Transposed rectangle.
    m = 4
    n = 3
    expected = 10
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Larger square.
    m = 5
    n = 5
    expected = 70
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Many row updates.
    m = 10
    n = 10
    expected = 48620
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Large integer path count.
    m = 20
    n = 20
    expected = 35345263800
    result = total_unique_paths_tabulation_space_optimized(m, n)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
