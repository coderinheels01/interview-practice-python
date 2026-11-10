"""Maze Obstacles

Given a maze with n rows and m columns, count the paths from the top-left
cell (0, 0) to the bottom-right cell (n - 1, m - 1).

Each cell contains:
    - -1: An obstacle that cannot be entered.
    - 0: An open cell.

From cell (row, col), you may move only down to (row + 1, col) or right
to (row, col + 1), remaining within the maze. Paths cannot pass through
obstacles. Return the number of valid paths modulo 1000000007 (10^9 + 7).

Example:
    Input: maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    Output: 2
    Explanation:
        The center cell is blocked. The two valid paths are:
        1. Right -> Right -> Down -> Down
        2. Down -> Down -> Right -> Right
        Both paths reach the bottom-right cell without entering the obstacle.

Assumptions:
    The maze is nonempty and rectangular, with at least one column.
    Cells contain only 0 or -1. A blocked start or destination has no paths.
    Numeric size constraints are not visible in the supplied screenshot.

https://www.youtube.com/watch?v=TmhpgXScLyY&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=10
"""


def maze_obstacles_recursion(maze: list[list[int]]) -> int:
    """Count right-and-down paths through open cells, modulo 1000000007.

    Approach: Naive Recursion
        1. Count the rows and columns. Define find_paths(row, col) as the
           number of paths from the start to that cell. Work backward from
           the destination by asking about the cells above and to the left.
        2. Return 0 if the cell is outside the grid or blocked. Neither can
           contribute a valid path. The negative-index checks run first,
           so Python never reads the maze with a negative index.
        3. At the open starting cell (0, 0), return 1: reaching it completes
           one path. Check obstacles first so a blocked start returns 0.
        4. Ask how many paths reach the cell above and the cell to the left.
           Each smaller call checks its own boundaries and obstacles.
        5. Add those counts because they describe different ways to enter
           this cell. Take the remainder modulo 1000000007, as required.
        6. Start at the bottom-right index and return its count.

        Example: maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]].
            The blocked center returns 0, stopping any route through it.
            One valid route goes along the top edge and then down.
            Another goes down the left edge and then right.
            Their counts add to 2 at the destination.

    Parameters:
        maze: A nonempty rectangular grid where 0 is open and -1 is blocked.

    Returns:
        Number of valid paths modulo 1000000007. Returns 0 for a blocked
        start or destination. A single open cell has one path.

    Mutation Behavior:
        Reads maze without modifying it or any other caller-owned data.

    Time Complexity: O(2^(r + c)) upper bound
        Here r and c are the row and column counts. Each call can split
        into two more calls, repeating earlier work. Obstacles stop some
        branches, but an open grid can still require exponential work.

    Space Complexity: O(r + c)
        One chain of paused calls can grow with the total rows and columns.
        Calls share the maze; the input grid is excluded from extra space.

    Assumptions:
        The grid has at least one row and column, and contains only 0 or -1.
        Numeric size limits were not provided. Python needs enough recursion
        depth for the longest chain. Arithmetic is treated as constant cost.
    """
    # Step 1: Count the grid dimensions.
    row_size: int = len(maze)
    col_size: int = len(maze[0])

    # Step 1: Count paths to a cell by looking backward.
    def find_paths(row: int, col: int) -> int:
        # Step 2: Outside cells and obstacles contribute zero paths.
        if row < 0 or col < 0 or maze[row][col] == -1:
            return 0
        # Step 3: Reaching the open starting cell completes one path.
        if row == 0 and col == 0:
            return 1

        # Step 4: Count paths arriving from above and from the left.
        up: int = find_paths(row - 1, col)
        left: int = find_paths(row, col - 1)

        # Step 5: Add the counts and apply the required modulo.
        return (left + up) % 1_000_000_007

    # Step 6: Begin at the destination's zero-based indexes.
    return find_paths(row=row_size - 1, col=col_size - 1)


def maze_obstacles_memoization(maze: list[list[int]]) -> int:
    """Count obstacle-free paths using saved cell answers, modulo 1000000007.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Create a cache with one slot per maze cell. Start slots at -1,
           meaning not calculated. A saved 0 is a real answer: no paths.
        2. Define find_paths(row, col) as the number of paths from the start
           to that cell. Return 0 if the cell is outside the maze or blocked.
           Check negative indexes first so they are never used to read maze.
        3. At the open starting cell (0, 0), return 1. Reaching it completes
           one path. The obstacle check comes first, so a blocked start
           correctly returns 0. Other edge cells do not automatically return
           1, because an obstacle earlier along the edge may block them.
        4. If this cell's answer is saved, return it immediately. Another
           branch can reuse that count without repeating earlier calls.
        5. Count paths to the cell above and the cell to the left. Their
           calls handle their own obstacles and boundaries.
        6. Add those two groups of paths, take the remainder modulo
           1000000007, and save the result for this cell. Return that answer.
        7. Start at the bottom-right indexes and return the helper's count.

        Example: maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]].
            The blocked center contributes 0 paths.
            One path reaches the destination from above, along the top edge.
            Another arrives from the left, along the left and bottom edges.
            Add them to get 2. Repeated questions about open cells use the cache.

    Parameters:
        maze: A nonempty rectangular grid, with 0 for open cells and -1
            for obstacles. At least one column is required.

    Returns:
        Number of right-and-down paths modulo 1000000007. A blocked start
        or destination has 0 paths; a single open cell has 1 path.

    Mutation Behavior:
        Updates only its local cache; maze is not modified.

    Time Complexity: O(r * c)
        Here r and c are the row and column counts. Each open cell's answer
        is calculated at most once and reused; creating the cache also visits
        r * c entries.

    Space Complexity: O(r * c)
        The cache stores r * c entries, plus a recursion stack of O(r + c).
        The cache dominates overall; the input maze is excluded from extra space.

    Assumptions:
        The maze contains only 0 and -1. Numeric size limits were not provided.
        Python needs enough recursion depth for the longest call chain.
        Arithmetic is treated as constant cost; saved counts use the modulus.
    """
    # Step 1: Reserve one cache slot per maze cell.
    row_size: int = len(maze)
    col_size: int = len(maze[0])
    paths_dp: list[list[int]] = [[-1] * col_size for _ in range(row_size)]

    # Step 2: Count paths to this cell, rejecting invalid or blocked cells.
    def find_paths(row: int, col: int) -> int:
        if row < 0 or col < 0 or maze[row][col] == -1:
            return 0
        # Step 3: Reaching the open starting cell completes one path.
        if row == 0 and col == 0:
            return 1

        # Step 4: Reuse the answer, including a saved zero.
        if paths_dp[row][col] != -1:
            return paths_dp[row][col]

        # Step 5: Count paths arriving from above and from the left.
        up: int = find_paths(row=row - 1, col=col)
        left: int = find_paths(row=row, col=col - 1)

        # Step 6: Combine, apply the modulus, save, and return.
        paths_dp[row][col] = (left + up) % 1_000_000_007
        return paths_dp[row][col]

    # Step 7: Begin at the bottom-right destination.
    return find_paths(row=row_size - 1, col=col_size - 1)


def maze_obstacles_tabulation(maze: list[list[int]]) -> int:
    """Count obstacle-free paths by filling a table from top-left to bottom-right.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Create a table of zeros with the same dimensions as the maze.
           Each entry will hold the number of valid paths to that cell.
        2. Visit cells row by row, from left to right. For the starting
           cell, save 1 only if it is open. Staying there counts as one path;
           a blocked starting cell must have zero paths.
        3. For every other case, start up and left at 0. If the cell is
           blocked, leave both at 0 so no path can enter or pass through it.
        4. If the cell is open, read the answer above when row > 0 and
           the answer to the left when col > 0. Missing neighbors contribute
           0. These checks prevent negative indexes from reading other cells.
        5. Add up and left, take the remainder modulo 1000000007, and save
           it. These counts represent different ways to arrive at this cell.
           Edge cells can have zero paths if an earlier obstacle blocks them.
        6. Return the bottom-right table entry. A blocked destination stays
           at 0, and a single open cell returns 1.

        Example: maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]].
            First row of path counts: [1, 1, 1].
            Second row: [1, 0, 1], because the center is blocked.
            Third row: [1, 1, 2].
            The destination receives 1 path from above and 1 from the left.
            Return 2.

    Parameters:
        maze: A nonempty rectangular grid where 0 is open and -1 is blocked.

    Returns:
        Number of right-and-down paths modulo 1000000007. Returns 0 when
        the start or destination is blocked, or no valid route exists.

    Mutation Behavior:
        Updates only its local table; maze is not modified.

    Time Complexity: O(r * c)
        Here r and c are the row and column counts. Creating the table and
        visiting every cell take linear time in the number of cells.

    Space Complexity: O(r * c)
        The table stores one answer per cell. The input maze is excluded
        from extra space, and no recursion stack is needed.

    Assumptions:
        The maze has at least one row and column and contains only 0 or -1.
        Numeric size limits were not provided. Arithmetic is treated as
        constant cost; saved counts use the required modulus.
    """
    # Step 1: Reserve a zero-initialized path count for every cell.
    row_size: int = len(maze)
    col_size: int = len(maze[0])
    paths_dp: list[list[int]] = [[0] * col_size for _ in range(row_size)]

    # Step 2: Process cells in order and initialize the start only if open.
    for row in range(row_size):
        for col in range(col_size):
            if row == 0 and col == 0 and maze[row][col] != -1:
                paths_dp[row][col] = 1
            else:
                # Step 3: Start with zero paths, keeping obstacles at zero.
                up: int = 0
                left: int = 0
                # Step 4: For an open cell, read only existing neighbors.
                if maze[row][col] != -1:
                    if row > 0:
                        up = paths_dp[row - 1][col]
                    if col > 0:
                        left = paths_dp[row][col - 1]
                # Step 5: Combine the path counts and apply the modulus.
                paths_dp[row][col] = (left + up) % 1_000_000_007

    # Step 6: Return the number of paths to the destination.
    return paths_dp[row_size - 1][col_size - 1]


def maze_obstacles_tabulation_space_optimized(maze: list[list[int]]) -> int:
    """Count obstacle-free paths using one reusable row, modulo 1000000007.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Create one zero-filled list with a slot per column. Before a cell
           is updated, its slot holds the previous row's path count.
        2. Visit cells row by row, from left to right. If a cell is blocked,
           reset its slot to 0 and skip it. Simply skipping would leave an
           old count from above, incorrectly allowing paths through the obstacle.
        3. For the open starting cell, save 1: staying there counts as one
           path. The obstacle check happens first, so a blocked start stays 0.
        4. For any other open cell, start up and left at 0. If row > 0,
           read paths_dp[col]: it still holds the answer from above.
           If col > 0, read paths_dp[col - 1]: that slot has already been
           updated for this row and holds the answer from the left.
        5. Add these two counts, apply modulo 1000000007, and replace the
           current slot. Reading before replacing preserves the old answer
           until it is used. Processing left to right supplies the new left
           answer while keeping the not-yet-updated answers from above.
        6. Return the final column's answer after the last row. A blocked
           destination returns 0; a single open cell returns 1.

        Example: maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]].
            Start with [0, 0, 0].
            After the first row: [1, 1, 1].
            On the second row, reset the center slot because it is blocked.
                The row ends as [1, 0, 1].
            On the third row, combine above and left to get [1, 1, 2].
            Return 2. The same list stores every row in turn.

    Parameters:
        maze: A nonempty rectangular grid where 0 is open and -1 is blocked.

    Returns:
        Number of right-and-down paths modulo 1000000007. Returns 0 when
        no valid route exists, including a blocked start or destination.

    Mutation Behavior:
        Updates only its local paths list; maze is not modified.

    Time Complexity: O(r * c)
        Here r and c are the row and column counts. Each cell is visited
        once, with a fixed amount of work per visit.

    Space Complexity: O(c)
        One reusable list holds c column answers, regardless of row count.
        The input maze is excluded from extra space.

    Assumptions:
        The maze has at least one row and column and contains only 0 or -1.
        Numeric size limits were not provided. Arithmetic is treated as
        constant cost; saved counts use the required modulus.
    """
    # Step 1: Reserve one reusable path-count slot per column.
    row_size: int = len(maze)
    col_size: int = len(maze[0])
    paths_dp: list[int] = [0] * col_size

    # Step 2: Process cells in order, clearing saved counts at obstacles.
    for row in range(row_size):
        for col in range(col_size):
            if maze[row][col] == -1:
                paths_dp[col] = 0
                continue
            # Step 3: Initialize the starting cell only after checking it is open.
            if row == 0 and col == 0:
                paths_dp[col] = 1
            else:
                # Step 4: Read valid neighbors; missing ones contribute zero.
                up: int = 0
                left: int = 0

                if row > 0:
                    up = paths_dp[col]
                if col > 0:
                    left = paths_dp[col - 1]
                # Step 5: Save this cell's combined count using the modulus.
                paths_dp[col] = (up + left) % 1_000_000_007

    # Step 6: Return the destination's count after processing all rows.
    return paths_dp[col_size - 1]


def solve() -> None:
    maze: list[list[int]] = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected: int = 2
    result: int = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single open cell.
    maze = [[0]]
    expected = 1
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single blocked cell.
    maze = [[-1]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open single row.
    maze = [[0, 0, 0, 0]]
    expected = 1
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked single row.
    maze = [[0, -1, 0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open single column.
    maze = [[0], [0], [0]]
    expected = 1
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked single column.
    maze = [[0], [-1], [0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked start.
    maze = [[-1, 0], [0, 0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked destination.
    maze = [[0, 0], [0, -1]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open two-by-two grid.
    maze = [[0, 0], [0, 0]]
    expected = 2
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only downward route remains.
    maze = [[0, -1], [0, 0]]
    expected = 1
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only rightward route remains.
    maze = [[0, 0], [-1, 0]]
    expected = 1
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Start has no exit.
    maze = [[0, -1], [-1, 0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open square.
    maze = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected = 6
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete blocking row.
    maze = [[0, 0, 0], [-1, -1, -1], [0, 0, 0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete blocking column.
    maze = [[0, -1, 0], [0, -1, 0], [0, -1, 0]]
    expected = 0
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Obstacle on first row.
    maze = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Obstacle on first column.
    maze = [[0, 0, 0], [-1, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open rectangle.
    maze = [[0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall rectangle.
    maze = [[0, 0], [0, 0], [0, 0]]
    expected = 3
    result = maze_obstacles_recursion(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: the question's example with a center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single open cell.
    maze = [[0]]
    expected = 1
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single blocked cell.
    maze = [[-1]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Open single row.
    maze = [[0, 0, 0, 0]]
    expected = 1
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Obstacle interrupts single row.
    maze = [[0, -1, 0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Open single column.
    maze = [[0], [0], [0]]
    expected = 1
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Obstacle interrupts single column.
    maze = [[0], [-1], [0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Blocked start.
    maze = [[-1, 0], [0, 0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Blocked destination.
    maze = [[0, 0], [0, -1]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Open small square.
    maze = [[0, 0], [0, 0]]
    expected = 2
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Only downward first move.
    maze = [[0, -1], [0, 0]]
    expected = 1
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Only rightward first move.
    maze = [[0, 0], [-1, 0]]
    expected = 1
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Start has no exit.
    maze = [[0, -1], [-1, 0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Open square.
    maze = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected = 6
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Blocking row.
    maze = [[0, 0, 0], [-1, -1, -1], [0, 0, 0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Blocking column.
    maze = [[0, -1, 0], [0, -1, 0], [0, -1, 0]]
    expected = 0
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: First-row obstacle.
    maze = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: First-column obstacle.
    maze = [[0, 0, 0], [-1, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Wide rectangle.
    maze = [[0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tall rectangle.
    maze = [[0, 0], [0, 0], [0, 0]]
    expected = 3
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Path count requires modulo.
    maze = [[0] * 20 for _ in range(20)]
    expected = 345263555
    result = maze_obstacles_memoization(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: the question's example with a center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single open cell.
    maze = [[0]]
    expected = 1
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single blocked cell.
    maze = [[-1]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Open single row.
    maze = [[0, 0, 0, 0]]
    expected = 1
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Obstacle interrupts single row.
    maze = [[0, -1, 0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Open single column.
    maze = [[0], [0], [0]]
    expected = 1
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Obstacle interrupts single column.
    maze = [[0], [-1], [0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Blocked start.
    maze = [[-1, 0], [0, 0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Blocked destination.
    maze = [[0, 0], [0, -1]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Open small square.
    maze = [[0, 0], [0, 0]]
    expected = 2
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Only downward first move.
    maze = [[0, -1], [0, 0]]
    expected = 1
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Only rightward first move.
    maze = [[0, 0], [-1, 0]]
    expected = 1
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Start has no exit.
    maze = [[0, -1], [-1, 0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Open square.
    maze = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected = 6
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Blocking row.
    maze = [[0, 0, 0], [-1, -1, -1], [0, 0, 0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Blocking column.
    maze = [[0, -1, 0], [0, -1, 0], [0, -1, 0]]
    expected = 0
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: First-row obstacle.
    maze = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: First-column obstacle.
    maze = [[0, 0, 0], [-1, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Wide rectangle.
    maze = [[0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Tall rectangle.
    maze = [[0, 0], [0, 0], [0, 0]]
    expected = 3
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Path count requires modulo.
    maze = [[0] * 20 for _ in range(20)]
    expected = 345263555
    result = maze_obstacles_tabulation(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: the question's center-obstacle example.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single open cell.
    maze = [[0]]
    expected = 1
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single blocked cell.
    maze = [[-1]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Open single row.
    maze = [[0, 0, 0, 0]]
    expected = 1
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Obstacle interrupts single row.
    maze = [[0, -1, 0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Open single column.
    maze = [[0], [0], [0]]
    expected = 1
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Obstacle must clear a saved column count.
    maze = [[0], [-1], [0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Blocked start.
    maze = [[-1, 0], [0, 0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Blocked destination.
    maze = [[0, 0], [0, -1]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Open small square.
    maze = [[0, 0], [0, 0]]
    expected = 2
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Only downward first move.
    maze = [[0, -1], [0, 0]]
    expected = 1
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Only rightward first move.
    maze = [[0, 0], [-1, 0]]
    expected = 1
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Start has no exit.
    maze = [[0, -1], [-1, 0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Center obstacle.
    maze = [[0, 0, 0], [0, -1, 0], [0, 0, 0]]
    expected = 2
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Open square.
    maze = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    expected = 6
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Blocking row clears all saved counts.
    maze = [[0, 0, 0], [-1, -1, -1], [0, 0, 0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Blocking column.
    maze = [[0, -1, 0], [0, -1, 0], [0, -1, 0]]
    expected = 0
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: First-row obstacle.
    maze = [[0, -1, 0], [0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: First-column obstacle.
    maze = [[0, 0, 0], [-1, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Wide rectangle.
    maze = [[0, 0, 0], [0, 0, 0]]
    expected = 3
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Tall rectangle.
    maze = [[0, 0], [0, 0], [0, 0]]
    expected = 3
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Path count requires modulo.
    maze = [[0] * 20 for _ in range(20)]
    expected = 345263555
    result = maze_obstacles_tabulation_space_optimized(maze)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
