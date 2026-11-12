"""Triangle Minimum Path Sum

Difficulty: Medium

Problem Statement:
    You are given a triangular array/list TRIANGLE. Return the minimum
    path sum from the top to the bottom row.

    The triangle has N rows. Row i, where 0 <= i < N, contains i + 1
    elements.

    At each step, you may move only to an adjacent number in the row
    below. From column j in row i, you may move to column j or j + 1
    in row i + 1.

Example:
    Input: triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]

              1
            2   3
          3   6   7
        8   9   6   1

    Expected output (calculated from the shown array): 12
    A minimum path is 1 -> 3 -> 7 -> 1, with sum 12.

Additional Examples (added for practice):
    1. Single row:
        Input: triangle = [[5]]

            5

        Output: 5
        The top is already the bottom, so the path contains only 5.

    2. Two rows:
        Input: triangle = [[2], [3, 4]]

              2
            3   4

        Output: 5
        A minimum path is 2 -> 3.

    3. Minimum path along the left edge:
        Input: triangle = [[1], [2, 9], [3, 9, 9]]

                1
              2   9
            3   9   9

        Output: 6
        A minimum path is 1 -> 2 -> 3, staying at column 0.

    4. Minimum path along the right edge:
        Input: triangle = [[1], [9, 2], [9, 9, 3]]

                1
              9   2
            9   9   3

        Output: 6
        A minimum path is 1 -> 2 -> 3, increasing the column each step.

    5. Minimum path ends in the middle:
        Input: triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]

                  2
                3   4
              6   5   7
            4   1   8   3

        Output: 11
        A minimum path is 2 -> 3 -> 5 -> 1.

    6. Multiple paths have the same minimum sum:
        Input: triangle = [[2], [2, 2], [2, 2, 2]]

                2
              2   2
            2   2   2

        Output: 6
        Every valid path visits three cells of value 2.

    7. The smaller next number does not guarantee the smallest total:
        Input: triangle = [[1], [2, 3], [100, 100, 1]]

                   1
                2     3
            100   100     1

        Output: 5
        A minimum path is 1 -> 3 -> 1. Choosing 2 in the second row
        forces the path to visit 100 in the last row.

    8. Larger triangle with a minimum path that changes direction:
        Input: triangle = [
            [7],
            [6, 3],
            [8, 2, 9],
            [5, 9, 1, 6],
            [9, 4, 2, 8, 3],
            [6, 7, 9, 1, 5, 4],
        ]

                      7
                    6   3
                  8   2   9
                5   9   1   6
              9   4   2   8   3
            6   7   9   1   5   4

        Output: 16
        A minimum path is 7 -> 3 -> 2 -> 1 -> 2 -> 1.
        Its column indexes are 0 -> 1 -> 1 -> 2 -> 2 -> 3.
        Each step either keeps the column index or increases it by one.
        The total is 7 + 3 + 2 + 1 + 2 + 1 = 16.

Source Notes:
    The screenshot mixes row and column labels in its movement example;
    the adjacent-movement rule above uses consistent indexes.
    Its written array ends with 1, while the diagram ends with 10.
    This file uses the explicitly written array for the example and test.
    Numeric constraints and the full input/output format are not visible.


https://www.youtube.com/watch?v=SrP-PiLSYC0&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=12


"""


def triangle_minimum_path_sum_recursion(triangle: list[list[int]]) -> int:
    """Return the minimum sum of an adjacent path from top to bottom.

    Args:
        triangle: A nonempty triangle of integers. Row i must contain
            exactly i + 1 values. Zero and negative values also work.

    Returns:
        The smallest path sum, including the top and bottom values.
        A single-row triangle returns its only value.

    Mutation and assumptions:
        The input is not modified. Row shapes are not validated.
        Empty input currently raises IndexError; no empty-input guard
        is implemented. Deep triangles may exceed Python's recursion limit.

    Approach:
        Recursive exhaustive search.
        1. Read the number of rows and the number of bottom-row columns.
           The helper finds the cheapest path from the top to a chosen
           cell, working backward toward its possible predecessors.
        2. At (0, 0), return the top value. This ends the recursion and
           counts the starting value exactly once in each path.
        3. On the left edge (column 0), only the cell directly above can
           lead here. Add the current value to that predecessor's cost.
        4. On the right edge (the last column of this row), only the
           upper-left cell exists. Add the current value to its cost.
           For example, (2, 2) comes from (1, 1), never (1, 2).
        5. For an interior cell, compare the cheapest costs to reach the
           upper and upper-left cells, then add the current value.
           For example, (2, 1) can come from (1, 1) or (1, 0).
           The edge cases ensure all recursive calls use valid indexes,
           so no infinity sentinel is needed.
        6. Call the helper for every bottom-row cell and return the
           smallest result. The generator inside min(...) produces one
           endpoint cost at a time: column 0, then 1, and so on.
           This lets the path end anywhere in the bottom row.

    Time Complexity:
        O(2 ** N), where N is the number of rows.
        Exploring both predecessors repeatedly creates exponentially many
        calls overall across the bottom-row endpoints.

    Space Complexity:
        O(N) extra space for the recursive call stack, excluding the input.
        The endpoint generator evaluates one result at a time without
        storing a list of all results.
    """
    # Step 1: Identify the row count and all possible bottom endpoints.
    row_size: int = len(triangle)
    last_row_col_size: int = len(triangle[row_size - 1])

    def find_min_path_sum(row: int, col: int) -> int:
        # Step 2: The path to the top contains only the top value.
        if row == 0 and col == 0:
            return triangle[row][col]
        # Step 3: The left edge has only an upper predecessor.
        if col == 0:
            return triangle[row][col] + find_min_path_sum(row=row - 1, col=col)
        # Step 4: The right edge has only an upper-left predecessor.
        if col == (len(triangle[row]) - 1):
            return triangle[row][col] + find_min_path_sum(row=row - 1, col=col - 1)

        # Step 5: Interior cells choose the cheaper of both predecessors.
        return triangle[row][col] + min(
            find_min_path_sum(row=row - 1, col=col),
            find_min_path_sum(row=row - 1, col=col - 1),
        )

    # Step 6: Compare the minimum costs for every bottom-row endpoint.
    return min(
        find_min_path_sum(row=row_size - 1, col=col) for col in range(last_row_col_size)
    )


def triangle_minimum_path_sum_memoization(triangle: list[list[int]]) -> int:
    """Return the minimum top-to-bottom path sum using cached recursion.

    Args:
        triangle: A nonempty triangle of integers whose row i contains
            exactly i + 1 values. Zero and negative values are supported.

    Returns:
        The smallest adjacent-path sum, including the top and bottom
        values. A single-cell triangle returns its only value.

    Mutation and assumptions:
        The input is unchanged; results are stored in a separate cache.
        Row shapes are not validated. Empty input currently raises
        IndexError because no empty-input guard is implemented.
        Deep triangles may exceed Python's recursion-depth limit.

    Approach:
        Top-down Dynamic Programming (Memoization).
        1. Read the row count and bottom-row width. Allocate a cache with
           the same triangular shape, using None for uncomputed entries.
           None is distinct from every integer path sum, including 0 and -1.
        2. The helper finds the cheapest cost from the top to a selected
           cell by working backward. At (0, 0), return the top value;
           this base case needs no further recursive calls.
        3. If the cell already has a cached result, return it immediately.
           Multiple bottom endpoints can need the same earlier cell,
           so this avoids recalculating its predecessors.
        4. On the left edge, only the cell directly above is a valid
           predecessor. Add the current value to its minimum cost,
           store the result, and return it.
        5. On the right edge, only the upper-left cell exists. Add the
           current value to its minimum cost, store it, and return it.
           For example, (2, 2) comes from (1, 1), never (1, 2).
        6. For interior cells, compare the costs from above and upper-left,
           add the current value, and cache the total before returning it.
           If those costs are 8 and 5 and this cell is 3, store 8.
           The edge cases keep every recursive call within the triangle,
           so no infinity sentinel is needed.
        7. Request the cost for every bottom-row endpoint and return the
           smallest result. The generator inside min(...) evaluates the
           endpoints one at a time while sharing the same cache.

    Time Complexity:
        O(N ** 2), where N is the number of rows.
        The triangle has O(N ** 2) cells; each nonstarting cell is computed
        once, and later requests reuse its cached result.

    Space Complexity:
        O(N ** 2) extra space for the triangular cache, excluding the input.
        The recursion also uses O(N) stack space, and the endpoint generator
        does not store a list of all results.
    """
    # Step 1: Create a triangular cache with None for unknown costs.
    row_size: int = len(triangle)
    col_size: int = len(triangle[row_size - 1])
    path_sum_dp: list[list[int | None]] = [
        [None] * len(triangle[row_index]) for row_index in range(row_size)
    ]

    def find_min_path_sum(row: int, col: int) -> int:
        # Step 2: The cost to reach the top is its own value.
        if row == 0 and col == 0:
            return triangle[row][col]

        # Step 3: Reuse a saved result, including zero or negative sums.
        if path_sum_dp[row][col] != None:
            return path_sum_dp[row][col]

        # Step 4: The left edge can only be reached from directly above.
        if col == 0:
            path_sum_dp[row][col] = triangle[row][col] + find_min_path_sum(
                row=row - 1, col=col
            )
            return path_sum_dp[row][col]

        # Step 5: The right edge can only be reached from upper-left.
        if col == (len(triangle[row]) - 1):
            path_sum_dp[row][col] = triangle[row][col] + find_min_path_sum(
                row=row - 1, col=col - 1
            )
            return path_sum_dp[row][col]

        # Step 6: Cache the cheaper of the two interior incoming routes.
        path_sum_dp[row][col] = triangle[row][col] + min(
            find_min_path_sum(row=row - 1, col=col),
            find_min_path_sum(row=row - 1, col=col - 1),
        )
        return path_sum_dp[row][col]

    # Step 7: Choose the cheapest of all bottom-row endpoints.
    return min(find_min_path_sum(row=row_size - 1, col=col) for col in range(col_size))


def triangle_minimum_path_sum_tabulation(triangle: list[list[int]]) -> int:
    """Return the minimum adjacent-path sum from the top to the bottom.

    Args:
        triangle: A nonempty triangle of integers. Row i must contain
            exactly i + 1 values. Zero and negative values are supported.

    Returns:
        The smallest path sum, including the starting and ending values.
        A single-cell triangle returns its only value.

    Mutation and assumptions:
        The input is unchanged; a separate table stores minimum costs.
        Row shapes are not validated. Empty input raises IndexError because
        there is no final row to read; no empty-input guard is implemented.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation).
        1. Create a table with the same triangular shape, initially filled
           with zeros. Each entry will store the minimum cost to reach
           that cell from the top. Every entry is assigned before another
           cell reads it, so no None or infinity marker is needed.
        2. Visit rows from top to bottom and each row's columns from left
           to right. Use that row's length because rows grow by one cell.
           The previous row is complete before the current row needs it.
        3. At (0, 0), store the top value. This counts the starting cell
           without needing a predecessor.
        4. On the left edge, add the current value to the saved cost
           directly above. That is the only valid incoming route.
        5. On the right edge, add the current value to the upper-left
           cost. The shorter previous row has no cell directly above.
        6. At an interior cell, choose the smaller cost from above and
           upper-left, then add the current value. For example, if those
           costs are 8 and 5 and the current value is 3, store 8.
        7. Return min(path_sum_dp[-1]) after finishing every row.
           In Python, [-1] selects the entire last row, not its last cell.
           Each value in that row is the cheapest cost to one possible
           endpoint. For the screenshot example, the row is
           [14, 15, 15, 12], and min(...) returns 12.
           No col variable is needed here: min(...) iterates over all
           values in the supplied row itself. We need the smallest sum,
           not the column index where it occurs. Reading [-1][col] instead
           would select just one endpoint rather than compare all of them.

    Time Complexity:
        O(N ** 2), where N is the number of rows.
        The table contains O(N ** 2) cells, each filled once with constant
        work; scanning the final N values does not change this bound.

    Space Complexity:
        O(N ** 2) extra space for the triangular table, excluding the input.
        The indexes use constant space, and min(...) reads the final row
        directly without copying it.
    """
    # Step 1: Allocate a separate cost table matching each row's length.
    row_size: int = len(triangle)
    path_sum_dp: list[list[int]] = [[0] * len(triangle[row]) for row in range(row_size)]

    # Step 2: Complete each row before processing the row below it.
    for row in range(row_size):
        for col in range(len(triangle[row])):
            # Step 3: The top cell's cost is its own value.
            if row == 0 and col == 0:
                path_sum_dp[row][col] = triangle[row][col]
            # Step 4: The left edge has only an upper predecessor.
            elif col == 0:
                path_sum_dp[row][col] = triangle[row][col] + path_sum_dp[row - 1][col]
            # Step 5: The right edge has only an upper-left predecessor.
            elif col == (len(triangle[row]) - 1):
                path_sum_dp[row][col] = (
                    triangle[row][col] + path_sum_dp[row - 1][col - 1]
                )
            # Step 6: Interior cells compare both incoming routes.
            else:
                path_sum_dp[row][col] = triangle[row][col] + min(
                    path_sum_dp[row - 1][col], path_sum_dp[row - 1][col - 1]
                )

    # Step 7: [-1] gives the entire bottom row; min checks every endpoint
    # value for us, so no explicit column index or column loop is needed.
    return min(path_sum_dp[-1])


def triangle_minimum_path_sum_tabulation_space_optimized(
    triangle: list[list[int]],
) -> int:
    """Return the minimum adjacent-path sum while storing only two rows.

    Args:
        triangle: A nonempty triangle of integers. Row i must have exactly
            i + 1 values. Zero and negative values are supported.

    Returns:
        The smallest top-to-bottom path sum, including both endpoints.
        A single-cell triangle returns its only value without entering
        the row loop.

    Mutation and assumptions:
        The input is unchanged; separate lists store the path costs.
        Row shapes are not validated. Empty input raises IndexError
        because the function reads triangle[0][0] without an empty guard.

    Approach:
        Bottom-Up Dynamic Programming (Space-Optimized Tabulation).
        1. Initialize the previous-row list with the top cell's value.
           That is the only cost needed before processing the second row.
        2. Visit the remaining rows from top to bottom. For each row,
           create a fresh current-row list matching its length. Each
           entry will store the cheapest cost to reach that cell.
        3. At the left edge, add the cell's value to the previous row's
           first cost. There is no upper-left predecessor for column 0.
        4. At the right edge, add the cell's value to the upper-left cost.
           The shorter previous row has no cell directly above this edge.
        5. For interior cells, add the current value to the smaller cost
           from above and upper-left. For example, previous costs [4, 5]
           and current values [6, 1, 8] produce costs [10, 5, 13].
           Read only from the previous list while building the current
           list, so earlier writes cannot change later predecessor costs.
        6. After completing the row, assign the current list to the
           previous-row variable. No copy is needed: the next iteration
           creates a fresh current list, leaving these saved costs intact.
           Older rows are no longer needed because each cell depends
           only on the row immediately above it.
        7. Return min(prev_path_sum_dp_one_d). The list now holds the
           cheapest costs for every bottom-row endpoint. min(...) checks
           all those values directly, so no column index is required.

    Time Complexity:
        O(N ** 2), where N is the number of rows.
        Every cell is processed once with constant work; allocating the
        row lists and scanning the final row do not change this bound.

    Space Complexity:
        O(N) extra space for the previous and current rows, excluding
        the input triangle. Each list holds at most N values, so keeping
        two rows still uses O(N) space instead of a full O(N ** 2) table.
    """
    # Step 1: Start with the minimum cost to reach the top cell.
    prev_path_sum_dp_one_d: list[int] = [triangle[0][0]]

    # Step 2: Create a fresh cost list for each remaining row.
    for row in range(1, len(triangle)):
        current_col_len: int = len(triangle[row])
        curr_path_sum_dp_one_d = [0] * current_col_len
        for col in range(current_col_len):
            # Step 3: The left edge can only come from directly above.
            if col == 0:
                curr_path_sum_dp_one_d[col] = (
                    triangle[row][col] + prev_path_sum_dp_one_d[col]
                )
            # Step 4: The right edge can only come from upper-left.
            elif col == (current_col_len - 1):
                curr_path_sum_dp_one_d[col] = (
                    triangle[row][col] + prev_path_sum_dp_one_d[col - 1]
                )
            # Step 5: Interior cells compare both previous-row costs.
            else:
                curr_path_sum_dp_one_d[col] = triangle[row][col] + min(
                    prev_path_sum_dp_one_d[col], prev_path_sum_dp_one_d[col - 1]
                )

        # Step 6: Reuse the completed row as the next iteration's previous row.
        # The next current-row list is newly allocated, so no copy is needed.
        prev_path_sum_dp_one_d = curr_path_sum_dp_one_d

    # Step 7: Compare every bottom-row endpoint without an explicit col index.
    return min(prev_path_sum_dp_one_d)


def solve() -> None:
    # Example array from the screenshot.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Numeric bounds are unavailable; maximum-bound coverage is unverified.
    # These tests use nonempty triangles with positive integer values.

    # Single cell.
    triangle = [[5]]
    expected = 5
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two rows, cheaper left endpoint.
    triangle = [[2], [3, 4]]
    expected = 5
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two rows, cheaper right endpoint.
    triangle = [[2], [4, 3]]
    expected = 5
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum along the left edge.
    triangle = [[1], [2, 9], [3, 9, 9]]
    expected = 6
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum along the right edge.
    triangle = [[1], [9, 2], [9, 9, 3]]
    expected = 6
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum ends in the middle.
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    expected = 11
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values and tied paths.
    triangle = [[2], [2, 2], [2, 2, 2]]
    expected = 6
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Smaller immediate value leads to a larger total.
    triangle = [[1], [2, 3], [100, 100, 1]]
    expected = 5
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum changes direction across six rows.
    triangle = [
        [7],
        [6, 3],
        [8, 2, 9],
        [5, 9, 1, 6],
        [9, 4, 2, 8, 3],
        [6, 7, 9, 1, 5, 4],
    ]
    expected = 16
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Small values in nonadjacent positions cannot form a path.
    triangle = [[1], [1, 9], [9, 9, 1]]
    expected = 11
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed values from the screenshot.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Ten rows with many tied paths.
    triangle = [[1] * (row + 1) for row in range(10)]
    expected = 10
    result = triangle_minimum_path_sum_recursion(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: mixed costs with shared predecessor cells.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single cell.
    triangle = [[5]]
    expected = 5
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two rows, cheaper left endpoint.
    triangle = [[2], [3, 4]]
    expected = 5
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two rows, cheaper right endpoint.
    triangle = [[2], [4, 3]]
    expected = 5
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum along the left edge.
    triangle = [[1], [2, 9], [3, 9, 9]]
    expected = 6
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum along the right edge.
    triangle = [[1], [9, 2], [9, 9, 3]]
    expected = 6
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum ends in the middle.
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    expected = 11
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values and tied paths.
    triangle = [[2], [2, 2], [2, 2, 2]]
    expected = 6
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Smaller immediate value leads to a larger total.
    triangle = [[1], [2, 3], [100, 100, 1]]
    expected = 5
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum changes direction across six rows.
    triangle = [
        [7],
        [6, 3],
        [8, 2, 9],
        [5, 9, 1, 6],
        [9, 4, 2, 8, 3],
        [6, 7, 9, 1, 5, 4],
    ]
    expected = 16
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Small values in nonadjacent positions cannot form a path.
    triangle = [[1], [1, 9], [9, 9, 1]]
    expected = 11
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Mixed costs with shared predecessor cells.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Thirty rows with many shared subproblems.
    triangle = [[1] * (row + 1) for row in range(30)]
    expected = 30
    result = triangle_minimum_path_sum_memoization(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: mixed costs with multiple bottom-row endpoints.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single cell.
    triangle = [[5]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two rows, cheaper left endpoint.
    triangle = [[2], [3, 4]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two rows, cheaper right endpoint.
    triangle = [[2], [4, 3]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum along the left edge.
    triangle = [[1], [2, 9], [3, 9, 9]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum along the right edge.
    triangle = [[1], [9, 2], [9, 9, 3]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum ends in the middle.
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    expected = 11
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values and tied paths.
    triangle = [[2], [2, 2], [2, 2, 2]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Smaller immediate value leads to a larger total.
    triangle = [[1], [2, 3], [100, 100, 1]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum changes direction across six rows.
    triangle = [
        [7],
        [6, 3],
        [8, 2, 9],
        [5, 9, 1, 6],
        [9, 4, 2, 8, 3],
        [6, 7, 9, 1, 5, 4],
    ]
    expected = 16
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Nonadjacent small values cannot form a path.
    triangle = [[1], [1, 9], [9, 9, 1]]
    expected = 11
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Mixed costs from the screenshot.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Thirty rows with tied paths.
    triangle = [[1] * (row + 1) for row in range(30)]
    expected = 30
    result = triangle_minimum_path_sum_tabulation(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: mixed costs with multiple endpoints.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single cell.
    triangle = [[5]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two rows, cheaper left endpoint.
    triangle = [[2], [3, 4]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two rows, cheaper right endpoint.
    triangle = [[2], [4, 3]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum along the left edge.
    triangle = [[1], [2, 9], [3, 9, 9]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum along the right edge.
    triangle = [[1], [9, 2], [9, 9, 3]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum ends in the middle.
    triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    expected = 11
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values and tied paths.
    triangle = [[2], [2, 2], [2, 2, 2]]
    expected = 6
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Smaller immediate value leads to a larger total.
    triangle = [[1], [2, 3], [100, 100, 1]]
    expected = 5
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum changes direction across six rows.
    triangle = [
        [7],
        [6, 3],
        [8, 2, 9],
        [5, 9, 1, 6],
        [9, 4, 2, 8, 3],
        [6, 7, 9, 1, 5, 4],
    ]
    expected = 16
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Nonadjacent small values cannot form a path.
    triangle = [[1], [1, 9], [9, 9, 1]]
    expected = 11
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Mixed costs from the screenshot.
    triangle = [[1], [2, 3], [3, 6, 7], [8, 9, 6, 1]]
    expected = 12
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Thirty rows with tied paths.
    triangle = [[1] * (row + 1) for row in range(30)]
    expected = 30
    result = triangle_minimum_path_sum_tabulation_space_optimized(triangle)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
