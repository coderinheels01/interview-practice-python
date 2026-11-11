"""Minimum Path Sum

Difficulty: Medium

Problem Statement:
    Ninjaland is a country in the shape of a two-dimensional grid, GRID,
    with N rows and M columns. Each point in the grid has some cost
    associated with it.

    Find a path from the top-left cell, (0, 0), to the bottom-right cell,
    (N - 1, M - 1), which minimizes the sum of the costs of all the numbers
    along the path. Return the minimum sum of that path.

Note:
    You can only move down or right at any point in time.

Source limitations:
    The screenshot cuts off the input format. The full input/output format,
    numeric constraints, and original sample cases are not visible.
    The function below accepts the grid directly.

Example (added for practice; not an original sample):
    Input: grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    Output: 7
    Explanation: The path Right, Right, Down, Down costs 1 + 3 + 1 + 1 + 1.

https://www.youtube.com/watch?v=_rgTlyky1uQ&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=11

"""


def minimum_path_sum_recursion(grid: list[list[int]]) -> int | float:
    """Return the smallest cost of a right/down path across the grid.

    Args:
        grid: A nonempty rectangular grid of integer cell costs, with at
            least one column. The function does not validate these assumptions.

    Returns:
        The minimum path sum, including the starting and ending cells.
        For valid input, the result is an integer. The float part of the
        annotation accommodates the helper's infinity sentinel.
        A single-cell grid returns that cell's cost.

    Mutation:
        The input grid is not modified.

    Approach:
        Recursive exhaustive search.
        1. Read the grid dimensions. The helper finds the cheapest cost from
           the starting cell to a particular (row, col), working backward
           toward the start. A forward right/down move becomes a backward
           left/up move.
        2. If a helper call goes above or left of the grid, return infinity.
           This marks that route as invalid so it cannot beat a valid route
           when choosing the smaller cost.
        3. At (0, 0), return the starting cell's cost. This ends that chain of
           calls and counts the starting cell exactly once.
        4. For every other cell, recursively find the cheapest cost to reach
           its left neighbor and its upper neighbor. Add the current cell's
           cost to each result because either route must enter this cell.
        5. Return the smaller of those two totals. For example, if the cell
           costs 4 and its neighbors can be reached for 3 and 8, choose 7
           instead of 12. On a grid boundary, the invalid route is infinity.
        6. Call the helper for the bottom-right cell and return its result.
           This compares all permitted routes to the requested destination.

    Time Complexity:
        O(2 ** (N + M)) upper bound, where N and M are the grid dimensions.
        Each call can make two more calls, with at most O(N + M) levels,
        and the same cells are calculated repeatedly.

    Space Complexity:
        O(N + M) extra space for the recursive call stack, excluding the input.
        Each active call stores only a few values; long paths may exceed
        Python's recursion-depth limit.
    """
    # Step 1: Read the dimensions and define the backward-looking helper.
    row_size: int = len(grid)
    col_size: int = len(grid[0])

    def find_min_path(row: int, col: int) -> int | float:
        # Step 2: Give an out-of-bounds route an infinitely large cost.
        if row < 0 or col < 0:
            return float("inf")

        # Step 3: The path to the starting cell costs just its own value.
        if row == 0 and col == 0:
            return grid[row][col]

        # Step 4: Include this cell's cost in each possible incoming route.
        left: int | float = grid[row][col] + find_min_path(row=row, col=col - 1)
        up: int | float = grid[row][col] + find_min_path(row=row - 1, col=col)

        # Step 5: Choose the cheaper incoming route.
        return min(left, up)

    # Step 6: Request the cheapest cost to reach the destination.
    return find_min_path(row=row_size - 1, col=col_size - 1)


def minimum_path_sum_memoization(grid: list[list[int]]) -> int | float:
    """Return the minimum right/down path cost using cached recursive results.

    Args:
        grid: A nonempty rectangular grid of nonnegative integer costs,
            with at least one column. These assumptions are not validated.
            Nonnegative costs ensure -1 cannot be a computed path sum.

    Returns:
        The minimum cost from top-left to bottom-right, including both
        endpoints. A single-cell grid returns that cell's value.
        Valid input produces an integer; the float annotation accommodates
        the helper's infinity value for invalid routes.

    Mutation:
        The input grid is unchanged; cached costs use a separate table.

    Approach:
        Top-down Dynamic Programming (Memoization).
        1. Read the grid dimensions and create a table of the same shape.
           Fill it with -1 to mean that a cell's minimum cost is not yet
           known. The helper computes the cheapest cost to reach a cell
           from the start by looking backward toward its predecessors.
        2. Return infinity if the requested cell is above or left of the
           grid. This prevents an invalid route from winning a comparison.
        3. At (0, 0), store and return the starting cell's cost. No earlier
           cells are needed, and this includes its value in each path.
        4. If the table already contains a cost for the requested cell,
           return it immediately. For example, if two routes both need
           the cost to reach (1, 1), the second request reuses the first
           result instead of exploring its predecessors again.
        5. Otherwise, ask the helper for the cheapest costs to reach the
           upper and left neighbors. Add the current cell's value to each
           result, because either incoming route must enter this cell.
           These are the only predecessors for forward right/down moves.
        6. Store the smaller total in the table and return it. If the cell
           costs 4 and the neighbor costs are 3 and 8, store 7, not 12.
        7. Request the bottom-right cell's cost and return the helper's
           answer directly. Recursive calls fill the needed table entries.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Initializing the table visits every cell, and each cell's cost is
        computed once with constant-time work beyond its recursive calls.

    Space Complexity:
        O(N * M) extra space for the cache and O(N + M) for the call stack,
        or O(N * M) overall, excluding the input grid.
        Long paths can still exceed Python's recursion-depth limit.
    """
    # Step 1: Allocate a separate table of initially unknown path costs.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    path_cost_sum_dp: list[list[int | float]] = [
        [-1] * col_size for _ in range(row_size)
    ]

    def find_min_path(row: int, col: int) -> int | float:

        # Step 2: Exclude routes that leave the grid.
        if row < 0 or col < 0:
            return float("inf")

        # Step 3: Store and return the starting cell's own cost.
        if row == 0 and col == 0:
            path_cost_sum_dp[row][col] = grid[row][col]
            return path_cost_sum_dp[row][col]

        # Step 4: Reuse a previously computed cost for this cell.
        if path_cost_sum_dp[row][col] != -1:
            return path_cost_sum_dp[row][col]

        # Step 5: Calculate the totals for arriving from above or the left.
        up: int | float = grid[row][col] + find_min_path(row=row - 1, col=col)
        left: int | float = grid[row][col] + find_min_path(row=row, col=col - 1)

        # Step 6: Cache the cheaper total and return it.
        path_cost_sum_dp[row][col] = min(up, left)

        return path_cost_sum_dp[row][col]

    # Step 7: Return the minimum cost to reach the destination.
    return find_min_path(row=row_size - 1, col=col_size - 1)


def minimum_path_sum_tabulation(grid: list[list[int]]) -> int:
    """Return the minimum cost of a right/down path through the grid.

    Args:
        grid: A nonempty rectangular grid of integer cell costs with at
            least one column. These assumptions are not validated.

    Returns:
        The minimum path sum from top-left to bottom-right, including
        both endpoints. A single-cell grid returns that cell's value.
        Negative costs also work because moves cannot form a cycle.

    Mutation:
        The input is unchanged; costs are stored in a separate table.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation).
        1. Read the grid dimensions and create a table of zeros with the
           same shape. Each entry will hold the minimum total cost to
           reach that cell from the starting cell.
        2. Visit cells row by row, from left to right. This ensures the
           upper and left neighbors have already been calculated before
           their costs are needed.
        3. For (0, 0), store its own cost. This includes the starting cell
           in the path without needing an earlier neighbor.
        4. For every other cell, initialize both possible incoming costs
           to infinity. An absent neighbor must not be chosen as a free
           route: zero would incorrectly win a minimum comparison.
        5. If an upper neighbor exists, add its saved cost to the current
           cell's value. Do the same for the left neighbor when it exists.
           For example, on the first row of [1, 3, 1], the second cell
           has an incoming cost of 1 + 3 = 4 from the left, while the
           missing upper route stays infinity.
        6. Store the smaller incoming total. The first row therefore
           accumulates costs from the left, and the first column from
           above; interior cells compare both routes. Every nonstarting
           cell has at least one valid predecessor, so the minimum is
           an integer and int(...) safely expresses that for the table.
        7. Return the bottom-right entry after filling the table. It now
           contains the cheapest total cost to reach the destination.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Creating the table and visiting every cell each take O(N * M)
        time, with constant work per cell.

    Space Complexity:
        O(N * M) extra space for the cost table, excluding the input grid.
        The loop indexes and temporary costs use constant extra space.
    """
    # Step 1: Allocate a separate minimum-cost table.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    path_cost_sum_dp: list[list[int]] = [[0] * col_size for _ in range(row_size)]

    # Step 2: Process each cell after its upper and left neighbors.
    for row in range(row_size):
        for col in range(col_size):
            # Step 3: Count the starting cell's own cost.
            if row == 0 and col == 0:
                path_cost_sum_dp[row][col] = grid[row][col]
            else:
                # Step 4: Keep unavailable routes infinitely expensive.
                up: int | float = float("inf")
                left: int | float = float("inf")

                # Step 5: Calculate incoming totals for existing neighbors.
                if row > 0:
                    up = grid[row][col] + path_cost_sum_dp[row - 1][col]

                if col > 0:
                    left = grid[row][col] + path_cost_sum_dp[row][col - 1]

                # Step 6: Save the cheaper valid total as an integer.
                path_cost_sum_dp[row][col] = int(min(up, left))

    # Step 7: Read the completed destination cost.
    return path_cost_sum_dp[row_size - 1][col_size - 1]


def minimum_path_sum_tabulation_optimized(grid: list[list[int]]) -> int:
    """Return the minimum right/down path cost using one reusable row.

    Args:
        grid: A nonempty rectangular grid of integer cell costs with at
            least one column. These assumptions are not validated.

    Returns:
        The minimum cost from top-left to bottom-right, counting both
        endpoints. A single-cell grid returns that cell's value.
        Negative costs also work because permitted moves cannot form cycles.

    Mutation:
        The input grid is unchanged. Only a separate list of costs is updated.

    Approach:
        Bottom-Up Dynamic Programming (Space-Optimized Tabulation).
        1. Read the dimensions and create a list with one zero per column.
           Reuse this list for each row instead of storing a full table.
        2. Visit rows from top to bottom and columns from left to right.
           Before updating a column, its entry holds the previous row's
           cost, while entries to its left already hold current-row costs.
           This order preserves both values needed for the next calculation.
        3. At (0, 0), save the starting cell's own cost. This counts the
           starting value even when the grid contains only one cell.
        4. For other cells, start both incoming costs at infinity. A missing
           neighbor must not appear to provide a free route with cost zero.
        5. If a row exists above, add the current cell's value to
           path_cost_dp[col], which still holds the cost directly above.
           If a column exists to the left, add the current value to
           path_cost_dp[col - 1], which already holds this row's left cost.
           On the first row only the left route exists; on the first
           column only the upper route exists.
        6. Overwrite path_cost_dp[col] with the smaller incoming total.
           For example, if the upper cost is 6, the updated left cost is 4,
           and this cell costs 2, save min(8, 6) = 6. The old upper value
           is no longer needed after this update. At least one neighbor
           exists, so the chosen total is an integer; int(...) expresses
           that guarantee despite the float infinity sentinels.
        7. After all rows are processed, return the last list entry. It
           holds the cheapest cost to reach the bottom-right cell.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Each cell is visited once and requires constant work.

    Space Complexity:
        O(M) extra space for the reusable cost list, excluding the input.
        The indexes and temporary costs use constant extra space.
    """

    # Step 1: Allocate one cost entry per column.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    path_cost_dp: list[int] = [0] * col_size

    # Step 2: Update left to right so upper and left costs remain available.
    for row in range(row_size):
        for col in range(col_size):
            # Step 3: Include the starting cell's cost.
            if row == 0 and col == 0:
                path_cost_dp[col] = grid[row][col]

            else:
                # Step 4: Make missing neighbors ineligible for the minimum.
                up: int | float = float("inf")
                left: int | float = float("inf")

                # Step 5: This column still holds the previous row's cost.
                if row > 0:
                    up = grid[row][col] + path_cost_dp[col]

                # Step 5: The left entry already holds this row's cost.
                if col > 0:
                    left = grid[row][col] + path_cost_dp[col - 1]

                # Step 6: Replace the old upper cost with this cell's cost.
                path_cost_dp[col] = int(min(up, left))

    # Step 7: The last entry now represents the destination.
    return path_cost_dp[col_size - 1]


def solve() -> None:
    # Practice example; replace with an original sample when available.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Numeric limits are unavailable; maximum-bound coverage is unverified.
    # These cases assume nonempty grids with nonnegative integer costs.

    # Single cell.
    grid = [[7]]
    expected = 7
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero cell.
    grid = [[0]]
    expected = 0
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row.
    grid = [[2, 0, 4, 1]]
    expected = 7
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column.
    grid = [[2], [0], [4], [1]]
    expected = 7
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zero costs.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical costs and tied paths.
    grid = [[3, 3, 3], [3, 3, 3]]
    expected = 12
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheapest path starts right.
    grid = [[1, 2], [9, 1]]
    expected = 4
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheapest path starts down.
    grid = [[1, 9], [2, 1]]
    expected = 4
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid.
    grid = [[1, 2, 3, 4], [9, 9, 1, 1]]
    expected = 8
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall grid.
    grid = [[1, 9], [2, 9], [3, 1], [4, 1]]
    expected = 8
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheapest path turns through the middle.
    grid = [[1, 1, 50], [50, 1, 50], [50, 1, 1]]
    expected = 5
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smaller immediate neighbor does not give the cheapest total.
    grid = [[1, 1, 100], [2, 100, 100], [2, 2, 1]]
    expected = 8
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Starting and ending costs both count.
    grid = [[8, 0, 0], [0, 0, 9]]
    expected = 17
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-cost route around expensive cells.
    grid = [[0, 0, 0], [5, 5, 0], [5, 5, 0]]
    expected = 0
    result = minimum_path_sum_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: single-cell grid.
    grid = [[7]]
    expected = 7
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single positive cell.
    grid = [[7]]
    expected = 7
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single zero cell.
    grid = [[0]]
    expected = 0
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row.
    grid = [[2, 0, 4, 1]]
    expected = 7
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single column.
    grid = [[2], [0], [4], [1]]
    expected = 7
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All zeros.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical costs with tied paths.
    grid = [[3, 3, 3], [3, 3, 3]]
    expected = 12
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Cheapest route starts right.
    grid = [[1, 2], [9, 1]]
    expected = 4
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Cheapest route starts down.
    grid = [[1, 9], [2, 1]]
    expected = 4
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Wide grid.
    grid = [[1, 2, 3, 4], [9, 9, 1, 1]]
    expected = 8
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tall grid.
    grid = [[1, 9], [2, 9], [3, 1], [4, 1]]
    expected = 8
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Route through the middle.
    grid = [[1, 1, 50], [50, 1, 50], [50, 1, 1]]
    expected = 5
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Cheaper immediate step leads to a more expensive total.
    grid = [[1, 1, 100], [2, 100, 100], [2, 2, 1]]
    expected = 8
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Starting and ending costs count.
    grid = [[8, 0, 0], [0, 0, 9]]
    expected = 17
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Zero-cost route around expensive cells.
    grid = [[0, 0, 0], [5, 5, 0], [5, 5, 0]]
    expected = 0
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Mixed costs with repeated subproblems.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Larger grid with many equal-cost routes.
    grid = [[1] * 20 for _ in range(20)]
    expected = 39
    result = minimum_path_sum_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: mixed costs with multiple possible routes.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single positive cell.
    grid = [[7]]
    expected = 7
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single zero cell.
    grid = [[0]]
    expected = 0
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row with zero.
    grid = [[2, 0, 4, 1]]
    expected = 7
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single column with zero.
    grid = [[2], [0], [4], [1]]
    expected = 7
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All zeros.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical costs and tied routes.
    grid = [[3, 3, 3], [3, 3, 3]]
    expected = 12
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Cheapest route starts right.
    grid = [[1, 2], [9, 1]]
    expected = 4
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Cheapest route starts down.
    grid = [[1, 9], [2, 1]]
    expected = 4
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Wide grid.
    grid = [[1, 2, 3, 4], [9, 9, 1, 1]]
    expected = 8
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Tall grid.
    grid = [[1, 9], [2, 9], [3, 1], [4, 1]]
    expected = 8
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Cheapest route through the middle.
    grid = [[1, 1, 50], [50, 1, 50], [50, 1, 1]]
    expected = 5
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Smaller immediate neighbor gives a more expensive route.
    grid = [[1, 1, 100], [2, 100, 100], [2, 2, 1]]
    expected = 8
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Both endpoint costs count.
    grid = [[8, 0, 0], [0, 0, 9]]
    expected = 17
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero-cost route around expensive cells.
    grid = [[0, 0, 0], [5, 5, 0], [5, 5, 0]]
    expected = 0
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Mixed costs.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Larger grid with tied routes.
    grid = [[1] * 20 for _ in range(20)]
    expected = 39
    result = minimum_path_sum_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: mixed costs with multiple possible routes.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Single positive cell.
    grid = [[7]]
    expected = 7
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Single zero cell.
    grid = [[0]]
    expected = 0
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Single row with zero.
    grid = [[2, 0, 4, 1]]
    expected = 7
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Single column with zero.
    grid = [[2], [0], [4], [1]]
    expected = 7
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: All zeros.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Identical costs and tied routes.
    grid = [[3, 3, 3], [3, 3, 3]]
    expected = 12
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Cheapest route starts right.
    grid = [[1, 2], [9, 1]]
    expected = 4
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Cheapest route starts down.
    grid = [[1, 9], [2, 1]]
    expected = 4
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Wide grid.
    grid = [[1, 2, 3, 4], [9, 9, 1, 1]]
    expected = 8
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Tall grid.
    grid = [[1, 9], [2, 9], [3, 1], [4, 1]]
    expected = 8
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Cheapest route through the middle.
    grid = [[1, 1, 50], [50, 1, 50], [50, 1, 1]]
    expected = 5
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Smaller immediate neighbor gives a more expensive route.
    grid = [[1, 1, 100], [2, 100, 100], [2, 2, 1]]
    expected = 8
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Both endpoint costs count.
    grid = [[8, 0, 0], [0, 0, 9]]
    expected = 17
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Zero-cost route around expensive cells.
    grid = [[0, 0, 0], [5, 5, 0], [5, 5, 0]]
    expected = 0
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Mixed costs across successive row updates.
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    expected = 7
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized tabulation: Larger grid with tied routes.
    grid = [[1] * 20 for _ in range(20)]
    expected = 39
    result = minimum_path_sum_tabulation_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
