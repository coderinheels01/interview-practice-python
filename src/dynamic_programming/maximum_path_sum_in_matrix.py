"""Maximum Path Sum in a Matrix

Difficulty: Medium

Problem Statement:
    You are given an N x M matrix filled with integer numbers. Find the
    maximum sum obtainable along a path starting from any cell in the
    first row and ending at any cell in the last row.

    From a cell (row, col), you may move in three directions:
        Down:                 (row + 1, col)
        Down-left diagonal:   (row + 1, col - 1)
        Down-right diagonal:  (row + 1, col + 1)

    Each move must stay within the matrix. The path sum includes the
    values of all visited cells, including the first and last cells.

Input Format (visible portion):
    The first line contains an integer T, denoting the number of test
    cases or queries. The test cases follow.

Source Notes:
    The remaining input format, numeric constraints, and sample cases
    are not visible in the screenshot. This function accepts the matrix
    directly. The example below is added for practice, not an original
    sample from the question.

Practice Example:
    Input: matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]

        1   2   3
        9   8   7
        4   5   6

    Output: 17
    One maximum path is 3 -> 8 -> 6, with sum 17.
    Its coordinates are (0, 2) -> (1, 1) -> (2, 2).
    The sequence 2 -> 9 -> 6 is not a valid path because the
    move from (1, 0) to (2, 2) skips a column.

Additional Examples (added for practice):
    1. Single cell:
        Input: matrix = [[7]]

            7

        Output: 7
        The starting cell is already in the last row.

    2. Single row:
        Input: matrix = [[3, 9, 2, 5]]

            3   9   2   5

        Output: 9
        Choose 9 as both the start and the end. No moves are needed.

    3. Single column:
        Input: matrix = [[2], [5], [1], [4]]

            2
            5
            1
            4

        Output: 12
        The only path is 2 -> 5 -> 1 -> 4, moving straight down.

    4. Moving down-left:
        Input: matrix = [[1, 1, 9], [1, 8, 1], [7, 1, 1]]

            1   1   9
            1   8   1
            7   1   1

        Output: 24
        A maximum path is 9 -> 8 -> 7.
        Its column indexes are 2 -> 1 -> 0.

    5. Moving down-right:
        Input: matrix = [[9, 1, 1], [1, 8, 1], [1, 1, 7]]

            9   1   1
            1   8   1
            1   1   7

        Output: 24
        A maximum path is 9 -> 8 -> 7.
        Its column indexes are 0 -> 1 -> 2.

    6. Multiple maximum paths:
        Input: matrix = [[4, 4, 4], [4, 4, 4]]

            4   4   4
            4   4   4

        Output: 8
        Every valid path visits two cells of value 4.

    7. The largest starting value does not give the largest total:
        Input: matrix = [[9, 1, 8], [1, 1, 20], [1, 1, 20]]

             9    1    8
             1    1   20
             1    1   20

        Output: 48
        A maximum path is 8 -> 20 -> 20, staying in column 2.
        Starting at 9 cannot reach the first 20 in one move.

    8. Larger matrix with a path that changes direction:
        Input: matrix = [
            [1, 9, 1, 1],
            [1, 1, 8, 1],
            [1, 7, 1, 1],
            [1, 1, 6, 1],
            [1, 1, 5, 1],
        ]

            1   9   1   1
            1   1   8   1
            1   7   1   1
            1   1   6   1
            1   1   5   1

        Output: 35
        A maximum path is 9 -> 8 -> 7 -> 6 -> 5.
        Its column indexes are 1 -> 2 -> 1 -> 2 -> 2, using both
        diagonal directions and a final straight-down move.

    https://www.youtube.com/watch?v=N_aJ5qQbYA0&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=15
"""


def maximum_path_sum_in_matrix_recursion(matrix: list[list[int]]) -> int:
    """Return the largest path sum from any first-row cell to the last row.

    Args:
        matrix: A nonempty rectangular matrix of integers with at least
            one column. Positive, zero, and negative values are supported.

    Returns:
        The maximum path sum, including the starting and ending cells.
        A single row returns its largest value; a single column returns
        the sum of its values. A single cell returns its own value.

    Mutation and assumptions:
        The input is not modified. Dimensions and row shapes are not
        validated; empty input is unsupported. Tall matrices may exceed
        Python's recursion-depth limit.

    Approach:
        Recursive exhaustive search.
        1. Read the row and column counts. The helper finds the largest
           sum ending at a selected cell, working backward toward the
           first row. Its possible predecessors are directly above,
           upper-left, and upper-right.
        2. At row 0, return that cell's value. Any first-row column is
           a valid start, and no earlier row is needed. This return
           prevents calls with a negative row index.
        3. If there is only one column, add the current value to the
           helper's result directly above. Handle this before the edge
           cases because a single column has no diagonal neighbors.
        4. At the left edge, compare the paths from above and upper-right,
           then add the current value. No upper-left call is made, so
           the column never becomes negative.
        5. At the right edge, compare the paths from above and upper-left,
           then add the current value. No upper-right call is made, so
           the column never exceeds the matrix width.
        6. At an interior cell, compare all three predecessor costs and
           add the current value to the largest. For example, if their
           costs are 5, 9, and 7 and this cell is 2, return 11.
           Only valid routes participate, so negative sums work without
           a zero fallback or an infinity sentinel. Columns may alternate
           between calls, but rows always decrease, preventing cycles.
        7. Call the helper for every last-row column and return the
           largest result. The generator inside max(...) produces one
           endpoint cost at a time, allowing the path to finish anywhere
           in the bottom row without storing a list of all results.

    Time Complexity:
        O(M * 3 ** N) upper bound, for N rows and M columns.
        Each of M endpoint searches can branch into up to three calls
        per level for N levels; the same cells are recalculated.

    Space Complexity:
        O(N) extra space for the recursive call stack, excluding the input.
        Only one branch and one endpoint search run at a time; the
        generator does not store all endpoint results.
    """
    # Step 1: Read dimensions for the backward path search.
    row_size: int = len(matrix)
    col_size: int = len(matrix[0])

    def find_max_path_sum(row: int, col: int) -> int:
        # Step 2: Any first-row cell can start the path.
        if row == 0:
            return matrix[row][col]

        # Step 3: A single column has only a straight-up predecessor.
        if col_size == 1:
            return matrix[row][col] + find_max_path_sum(row - 1, col)

        # Step 4: The left edge has no upper-left predecessor.
        if col == 0:
            return matrix[row][col] + max(
                find_max_path_sum(row=row - 1, col=col),
                find_max_path_sum(row=row - 1, col=col + 1),
            )

        # Step 5: The right edge has no upper-right predecessor.
        if col == (col_size - 1):
            return matrix[row][col] + max(
                find_max_path_sum(row=row - 1, col=col),
                find_max_path_sum(row=row - 1, col=col - 1),
            )

        # Step 6: Interior cells choose the best of all three predecessors.
        return matrix[row][col] + max(
            find_max_path_sum(row=row - 1, col=col),
            find_max_path_sum(row=row - 1, col=col + 1),
            find_max_path_sum(row=row - 1, col=col - 1),
        )

    # Step 7: Compare the best path to every bottom-row endpoint.
    return max(find_max_path_sum(row=row_size - 1, col=col) for col in range(col_size))


def maximum_path_sum_in_matrix_memoization(matrix: list[list[int]]) -> int:
    """Return the maximum first-to-last-row path sum using cached recursion.

    Args:
        matrix: A nonempty rectangular matrix of integers with at least
            one column. Positive, zero, and negative values are supported.

    Returns:
        The maximum path sum, including both endpoints. A single row
        returns its largest value; a single column returns its sum.

    Mutation and assumptions:
        The input is unchanged; a separate table stores computed costs.
        Shapes are not validated and empty input is unsupported.
        Tall matrices may exceed Python's recursion-depth limit.

    Approach:
        Top-down Dynamic Programming (Memoization).
        1. Read the dimensions and allocate a matching cache filled with
           None. None means uncomputed, so valid sums such as 0 and -1
           remain distinguishable from missing results.
        2. The helper finds the largest sum ending at a chosen cell by
           looking backward. At row 0, return the cell's value because
           any first-row cell can start the path. No earlier row is needed.
        3. Return a cached result when one exists. Different endpoints
           can depend on the same cell, so reusing its cost avoids
           exploring its predecessors repeatedly.
        4. For a single-column matrix, add the current value to the cost
           directly above, cache it, and return it. This special case
           prevents attempts to visit nonexistent diagonal neighbors.
        5. At the left edge, compare above and upper-right. Add the
           current value, cache the total, and return it.
        6. At the right edge, compare above and upper-left. Add the
           current value, cache the total, and return it.
        7. For interior cells, compare all three predecessor costs, add
           the current value, and cache the result before returning it.
           For example, predecessor costs 5, 9, and 7 with current value
           2 produce 11. Only valid predecessors participate, so negative
           sums work without a zero fallback or an infinity sentinel.
        8. Request the helper's result for every bottom-row column and
           return the largest. The generator inside max(...) evaluates
           one endpoint at a time, sharing the cache across all requests.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Each nonstarting cell is computed once and compares at most three
        predecessor costs; repeated requests reuse the cache.

    Space Complexity:
        O(N * M) extra space for the cache, excluding the input matrix.
        Recursion additionally uses O(N) stack space, while the endpoint
        generator avoids storing a separate list of results.
    """
    # Step 1: Allocate a separate cache with None for unknown costs.
    row_size: int = len(matrix)
    col_size: int = len(matrix[0])
    max_path_sum_dp: list[list[int | None]] = [
        [None] * col_size for _ in range(row_size)
    ]

    def find_max_path_sum(row: int, col: int) -> int:
        # Step 2: Any first-row cell is a valid starting point.
        if row == 0:
            return matrix[row][col]

        # Step 3: Reuse a saved cost, including zero or negative values.
        if max_path_sum_dp[row][col] != None:
            return max_path_sum_dp[row][col]

        # Step 4: A single column has only a straight-up predecessor.
        if col_size == 1:
            max_path_sum_dp[row][col] = matrix[row][col] + find_max_path_sum(
                row=row - 1, col=col
            )
            return max_path_sum_dp[row][col]

        # Step 5: The left edge has no upper-left predecessor.
        if col == 0:
            max_path_sum_dp[row][col] = matrix[row][col] + max(
                find_max_path_sum(row=row - 1, col=col),
                find_max_path_sum(row=row - 1, col=col + 1),
            )
            return max_path_sum_dp[row][col]

        # Step 6: The right edge has no upper-right predecessor.
        if col == col_size - 1:
            max_path_sum_dp[row][col] = matrix[row][col] + max(
                find_max_path_sum(row=row - 1, col=col),
                find_max_path_sum(row=row - 1, col=col - 1),
            )
            return max_path_sum_dp[row][col]

        # Step 7: Interior cells compare and cache all three routes.
        max_path_sum_dp[row][col] = matrix[row][col] + max(
            find_max_path_sum(row=row - 1, col=col),
            find_max_path_sum(row=row - 1, col=col + 1),
            find_max_path_sum(row=row - 1, col=col - 1),
        )
        return max_path_sum_dp[row][col]

    # Step 8: Compare all bottom-row endpoints using the shared cache.
    return max(find_max_path_sum(row=row_size - 1, col=col) for col in range(col_size))


def maximum_path_sum_in_matrix_tabulation(matrix: list[list[int]]) -> int:
    """Return the maximum first-to-last-row path sum using a cost table.

    Args:
        matrix: A nonempty rectangular matrix of integers with at least
            one column. Positive, zero, and negative values are supported.

    Returns:
        The largest path sum, including both endpoints. A single row
        returns its largest value; a single column returns its sum.
        A single-cell matrix returns that cell's value.

    Mutation and assumptions:
        The input is unchanged; a separate table stores path costs.
        Shapes are not validated and empty input is unsupported.

    Approach:
        Bottom-Up Dynamic Programming (Tabulation).
        1. Read the dimensions and allocate a matching table of zeros.
           Each entry will store the largest sum of a path from any
           first-row cell to that entry's cell. Every needed entry is
           filled before it is read, so zeros are only initial placeholders.
        2. Visit cells row by row, from left to right. Finish the previous
           row before using its costs to calculate the current row.
        3. Copy the first row's values into the table. Any cell in this
           row can start a path, with no earlier cell contributing a cost.
        4. For a single-column matrix, add the current value to the cost
           directly above. Handle this before the edge cases because
           neither diagonal neighbor exists in a one-column matrix.
        5. At the left edge, add the current value to the larger cost
           from above or upper-right. There is no upper-left neighbor.
        6. At the right edge, compare above and upper-left, then add
           the current value. Both routes matter: a path may continue
           straight down the last column, such as 8 -> 20 -> 20 = 48.
        7. For interior cells, compare all three previous-row neighbors
           and add the current value to the largest cost. For example,
           predecessor costs 5, 9, and 7 with current value 2 give 11.
           Only existing neighbors participate, so negative path sums
           work without a zero fallback or infinity sentinel.
        8. Return max(max_path_sum_dp[-1]). The index -1 selects the
           entire last row, whose entries represent every possible
           endpoint. max(...) compares those values directly, so no
           explicit column index is needed for the final answer.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Each cell is filled once with constant work; the final scan of
        M endpoint costs does not change this bound.

    Space Complexity:
        O(N * M) extra space for the cost table, excluding the input.
        The loop indexes use constant space, and max(...) reads the
        last row directly without copying it.
    """
    # Step 1: Allocate a separate table for the best cost to each cell.
    row_size: int = len(matrix)
    col_size: int = len(matrix[0])
    max_path_sum_dp: list[list[int]] = [[0] * col_size for _ in range(row_size)]

    # Step 2: Complete each row before calculating the next one.
    for row in range(row_size):
        for col in range(col_size):
            # Step 3: Any first-row cell can be the starting point.
            if row == 0:
                max_path_sum_dp[row][col] = matrix[row][col]
            # Step 4: A single column has only a straight-up predecessor.
            elif col_size == 1:
                max_path_sum_dp[row][col] = (
                    matrix[row][col] + max_path_sum_dp[row - 1][col]
                )
            # Step 5: Compare above and upper-right at the left edge.
            elif col == 0:
                max_path_sum_dp[row][col] = matrix[row][col] + max(
                    max_path_sum_dp[row - 1][col], max_path_sum_dp[row - 1][col + 1]
                )
            # Step 6: Compare above and upper-left at the right edge.
            elif col == col_size - 1:
                max_path_sum_dp[row][col] = matrix[row][col] + max(
                    max_path_sum_dp[row - 1][col], max_path_sum_dp[row - 1][col - 1]
                )

            # Step 7: Interior cells compare all three valid predecessors.
            else:
                max_path_sum_dp[row][col] = matrix[row][col] + max(
                    max_path_sum_dp[row - 1][col],
                    max_path_sum_dp[row - 1][col + 1],
                    max_path_sum_dp[row - 1][col - 1],
                )

    # Step 8: Compare every last-row endpoint without an explicit col index.
    return max(max_path_sum_dp[-1])


def maximum_path_sum_in_matrix_space_optimized(matrix: list[list[int]]) -> int:
    """Return the maximum first-to-last-row path sum using two cost rows.

    Args:
        matrix: A nonempty rectangular matrix of integers with at least
            one column. Positive, zero, and negative values are supported.

    Returns:
        The largest path sum, including both endpoints. A single row
        returns its largest value; a single column returns its sum.
        A single cell returns its own value.

    Mutation and assumptions:
        The input is unchanged; separate lists store path costs.
        Shapes are not validated and empty input is unsupported.

    Approach:
        Bottom-Up Dynamic Programming (Space-Optimized Tabulation).
        1. Read the dimensions and create a previous-row list of zeros.
           Only the previous row's costs are needed to calculate a new
           row, so a full matrix of saved costs is unnecessary.
        2. Visit rows from top to bottom. Allocate a fresh current-row
           list each time, then visit its columns from left to right.
           Keep previous-row costs separate while filling the new list.
        3. For row 0, copy each matrix value into the current list. Any
           first-row cell can start a path. The initial previous-row
           zeros are not used to calculate these starting costs.
        4. For a single-column matrix, add the current cell's value to
           the previous row's only cost. Neither diagonal exists, so
           handle this case before checking the left and right edges.
        5. At the left edge, add the current value to the larger cost
           from above or upper-right. There is no upper-left neighbor.
        6. At the right edge, add the current value to the larger cost
           from above or upper-left. Straight-down movement is still
           allowed at an edge; only the outward diagonal is missing.
        7. At an interior cell, compare all three previous-row neighbors
           and add the current value. For example, previous costs
           [5, 9, 7] and a middle-cell value of 2 produce a cost of 11.
           Only valid costs participate, so negative sums work without
           treating a missing route as zero or using infinity.
        8. After completing every column, assign the current list to the
           previous-row variable. Do this inside the row loop so the next
           row uses the newly computed costs. No copy is needed: the next
           iteration creates a fresh current list rather than modifying
           the completed list. Older rows are no longer needed.
        9. Return max(prev_max_path_sum_dp). This list now contains the
           best cost to every bottom-row endpoint. max(...) scans all
           those values directly, so no explicit column index is needed.

    Time Complexity:
        O(N * M), where N and M are the numbers of rows and columns.
        Each cell takes constant work; allocating row lists and scanning
        the final row do not change this bound.

    Space Complexity:
        O(M) extra space for the previous and current lists, excluding
        the input matrix. Each list holds M values, so keeping two rows
        still uses O(M) space instead of a full O(N * M) table.
    """
    # Step 1: Allocate one previous-row cost per column.
    row_size: int = len(matrix)

    col_size: int = len(matrix[0])
    prev_max_path_sum_dp: list[int] = [0] * col_size

    # Step 2: Build a fresh cost list for each row.
    for row in range(row_size):
        curr_max_path_sum_dp: list[int] = [0] * col_size

        for col in range(col_size):
            # Step 3: Any first-row value can start a path.
            if row == 0:
                curr_max_path_sum_dp[col] = matrix[row][col]
            # Step 4: A single column has only a straight-up predecessor.
            elif col_size == 1:
                curr_max_path_sum_dp[col] = matrix[row][col] + prev_max_path_sum_dp[col]
            # Step 5: Compare above and upper-right at the left edge.
            elif col == 0:
                curr_max_path_sum_dp[col] = matrix[row][col] + max(
                    prev_max_path_sum_dp[col],
                    prev_max_path_sum_dp[col + 1],
                )
            # Step 6: Compare above and upper-left at the right edge.
            elif col == col_size - 1:
                curr_max_path_sum_dp[col] = matrix[row][col] + max(
                    prev_max_path_sum_dp[col],
                    prev_max_path_sum_dp[col - 1],
                )

            # Step 7: Interior cells compare all three previous-row costs.
            else:
                curr_max_path_sum_dp[col] = matrix[row][col] + max(
                    prev_max_path_sum_dp[col],
                    prev_max_path_sum_dp[col + 1],
                    prev_max_path_sum_dp[col - 1],
                )
        # Step 8: Save the completed row before starting the next row.
        prev_max_path_sum_dp = curr_max_path_sum_dp

    # Step 9: Compare all final-row endpoint costs directly.
    return max(prev_max_path_sum_dp)


def solve() -> None:
    # Practice example; the screenshot does not show an original sample.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Numeric constraints are unavailable; maximum-bound coverage is unverified.
    # These tests use nonempty rectangular matrices with positive costs.

    # Single cell.
    matrix = [[7]]
    expected = 7
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row, maximum at the beginning.
    matrix = [[9, 3, 2]]
    expected = 9
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row, maximum in the middle.
    matrix = [[3, 9, 2, 5]]
    expected = 9
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row, maximum at the end.
    matrix = [[3, 2, 9]]
    expected = 9
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column.
    matrix = [[2], [5], [1], [4]]
    expected = 12
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two columns with alternating best cells.
    matrix = [[9, 1], [1, 8], [7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Down-left diagonal to the left endpoint.
    matrix = [[1, 1, 9], [1, 8, 1], [7, 1, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Down-right diagonal to the right endpoint.
    matrix = [[9, 1, 1], [1, 8, 1], [1, 1, 7]]
    expected = 24
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Straight-down maximum in the middle.
    matrix = [[1, 9, 1], [1, 8, 1], [1, 7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical costs and tied paths.
    matrix = [[4, 4, 4], [4, 4, 4]]
    expected = 8
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest starting value gives a smaller total.
    matrix = [[9, 1, 8], [1, 1, 20], [1, 1, 20]]
    expected = 48
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide matrix with nonadjacent row maxima.
    matrix = [[10, 1, 1, 1, 1], [1, 1, 1, 1, 10]]
    expected = 11
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger zigzag path.
    matrix = [[1, 9, 1, 1], [1, 1, 8, 1], [1, 7, 1, 1], [1, 1, 6, 1], [1, 1, 5, 1]]
    expected = 35
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed costs from the practice example.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Eight rows with tied paths.
    matrix = [[1] * 4 for _ in range(8)]
    expected = 8
    result = maximum_path_sum_in_matrix_recursion(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: mixed costs with multiple possible endpoints.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # These cases include zero and negative integers, which the visible
    # statement does not exclude. Exact numeric limits remain unavailable.

    # Memoization: Single positive cell.
    matrix = [[7]]
    expected = 7
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single zero cell.
    matrix = [[0]]
    expected = 0
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single negative cell.
    matrix = [[-5]]
    expected = -5
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row, maximum at the beginning.
    matrix = [[9, 3, 2]]
    expected = 9
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row, maximum in the middle.
    matrix = [[3, 9, 2, 5]]
    expected = 9
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row, maximum at the end.
    matrix = [[3, 2, 9]]
    expected = 9
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single column.
    matrix = [[2], [5], [1], [4]]
    expected = 12
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single negative column.
    matrix = [[-5], [-2]]
    expected = -7
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two columns with alternating best cells.
    matrix = [[9, 1], [1, 8], [7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Down-left diagonal to the left endpoint.
    matrix = [[1, 1, 9], [1, 8, 1], [7, 1, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Down-right diagonal to the right endpoint.
    matrix = [[9, 1, 1], [1, 8, 1], [1, 1, 7]]
    expected = 24
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Straight-down maximum in the middle.
    matrix = [[1, 9, 1], [1, 8, 1], [1, 7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical costs and tied paths.
    matrix = [[4, 4, 4], [4, 4, 4]]
    expected = 8
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All zeros.
    matrix = [[0, 0], [0, 0], [0, 0]]
    expected = 0
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All negative costs.
    matrix = [[-1, -8], [-4, -2], [-3, -9]]
    expected = -6
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Valid maximum sum equals minus one.
    matrix = [[-2, -3], [1, -4]]
    expected = -1
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Mixed signs with a zero maximum.
    matrix = [[-2, -5], [2, -3]]
    expected = 0
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Largest starting value gives a smaller total.
    matrix = [[9, 1, 8], [1, 1, 20], [1, 1, 20]]
    expected = 48
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Wide matrix with nonadjacent row maxima.
    matrix = [[10, 1, 1, 1, 1], [1, 1, 1, 1, 10]]
    expected = 11
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Larger zigzag path.
    matrix = [[1, 9, 1, 1], [1, 1, 8, 1], [1, 7, 1, 1], [1, 1, 6, 1], [1, 1, 5, 1]]
    expected = 35
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Mixed costs from the practice example.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Eight rows with tied paths.
    matrix = [[1] * 4 for _ in range(8)]
    expected = 8
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: maximum path ends in the middle column.
    matrix = [[1, 9, 1], [1, 8, 1], [1, 7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_memoization(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single positive cell.
    matrix = [[7]]
    expected = 7
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single zero cell.
    matrix = [[0]]
    expected = 0
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single negative cell.
    matrix = [[-5]]
    expected = -5
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row, maximum at the beginning.
    matrix = [[9, 3, 2]]
    expected = 9
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row, maximum in the middle.
    matrix = [[3, 9, 2, 5]]
    expected = 9
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row, maximum at the end.
    matrix = [[3, 2, 9]]
    expected = 9
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single column.
    matrix = [[2], [5], [1], [4]]
    expected = 12
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single negative column.
    matrix = [[-5], [-2]]
    expected = -7
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two columns with alternating best cells.
    matrix = [[9, 1], [1, 8], [7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Down-left diagonal to the left endpoint.
    matrix = [[1, 1, 9], [1, 8, 1], [7, 1, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Down-right diagonal to the right endpoint.
    matrix = [[9, 1, 1], [1, 8, 1], [1, 1, 7]]
    expected = 24
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Straight-down maximum in the middle.
    matrix = [[1, 9, 1], [1, 8, 1], [1, 7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical costs and tied paths.
    matrix = [[4, 4, 4], [4, 4, 4]]
    expected = 8
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All zeros.
    matrix = [[0, 0], [0, 0], [0, 0]]
    expected = 0
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All negative costs.
    matrix = [[-1, -8], [-4, -2], [-3, -9]]
    expected = -6
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Valid maximum sum equals minus one.
    matrix = [[-2, -3], [1, -4]]
    expected = -1
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Mixed signs with a zero maximum.
    matrix = [[-2, -5], [2, -3]]
    expected = 0
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Largest starting value gives a smaller total.
    matrix = [[9, 1, 8], [1, 1, 20], [1, 1, 20]]
    expected = 48
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Wide matrix with nonadjacent row maxima.
    matrix = [[10, 1, 1, 1, 1], [1, 1, 1, 1, 10]]
    expected = 11
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Larger zigzag path.
    matrix = [[1, 9, 1, 1], [1, 1, 8, 1], [1, 7, 1, 1], [1, 1, 6, 1], [1, 1, 5, 1]]
    expected = 35
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Mixed costs from the practice example.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Larger rectangular matrix with tied paths.
    matrix = [[1] * 20 for _ in range(30)]
    expected = 30
    result = maximum_path_sum_in_matrix_tabulation(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: mixed costs with multiple possible endpoints.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single positive cell.
    matrix = [[7]]
    expected = 7
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single zero cell.
    matrix = [[0]]
    expected = 0
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single negative cell.
    matrix = [[-5]]
    expected = -5
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single row, maximum at the beginning.
    matrix = [[9, 3, 2]]
    expected = 9
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single row, maximum in the middle.
    matrix = [[3, 9, 2, 5]]
    expected = 9
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single row, maximum at the end.
    matrix = [[3, 2, 9]]
    expected = 9
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single column.
    matrix = [[2], [5], [1], [4]]
    expected = 12
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Single negative column.
    matrix = [[-5], [-2]]
    expected = -7
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Two columns with alternating best cells.
    matrix = [[9, 1], [1, 8], [7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Down-left diagonal to the left endpoint.
    matrix = [[1, 1, 9], [1, 8, 1], [7, 1, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Down-right diagonal to the right endpoint.
    matrix = [[9, 1, 1], [1, 8, 1], [1, 1, 7]]
    expected = 24
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Straight-down maximum in the middle.
    matrix = [[1, 9, 1], [1, 8, 1], [1, 7, 1]]
    expected = 24
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Identical costs and tied paths.
    matrix = [[4, 4, 4], [4, 4, 4]]
    expected = 8
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: All zeros.
    matrix = [[0, 0], [0, 0], [0, 0]]
    expected = 0
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: All negative costs.
    matrix = [[-1, -8], [-4, -2], [-3, -9]]
    expected = -6
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Valid maximum sum equals minus one.
    matrix = [[-2, -3], [1, -4]]
    expected = -1
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Mixed signs with a zero maximum.
    matrix = [[-2, -5], [2, -3]]
    expected = 0
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Largest starting value gives a smaller total.
    matrix = [[9, 1, 8], [1, 1, 20], [1, 1, 20]]
    expected = 48
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Wide matrix with nonadjacent row maxima.
    matrix = [[10, 1, 1, 1, 1], [1, 1, 1, 1, 10]]
    expected = 11
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Larger zigzag path.
    matrix = [[1, 9, 1, 1], [1, 1, 8, 1], [1, 7, 1, 1], [1, 1, 6, 1], [1, 1, 5, 1]]
    expected = 35
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Mixed costs from the practice example.
    matrix = [[1, 2, 3], [9, 8, 7], [4, 5, 6]]
    expected = 17
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized: Larger rectangular matrix with tied paths.
    matrix = [[1] * 20 for _ in range(30)]
    expected = 30
    result = maximum_path_sum_in_matrix_space_optimized(matrix)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
