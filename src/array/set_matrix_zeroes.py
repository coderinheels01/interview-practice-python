"""Set Matrix Zeroes

Given an ``m x n`` integer matrix ``matrix``, if an element is 0, set its entire
row and column to 0. You must modify the matrix in place.

Example 1:
    Input: matrix = [[1, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]]
    Output: [[1, 0, 1],
             [0, 0, 0],
             [1, 0, 1]]

    Explanation: The element at position (1, 1) is 0, so the entire row 1 and
    column 1 are set to 0.

Example 2:
    Input: matrix = [[0, 1, 2, 0],
                     [3, 4, 5, 2],
                     [1, 3, 1, 5]]
    Output: [[0, 0, 0, 0],
             [0, 4, 5, 0],
             [0, 3, 1, 0]]

    Explanation: There are two zeroes at positions (0, 0) and (0, 3). Row 0
    becomes all zeroes, and columns 0 and 3 become all zeroes.

Constraints:
    - m == matrix.length
    - n == matrix[0].length
    - 1 <= m, n <= 200
    - -2^31 <= matrix[i][j] <= 2^31 - 1

    https://www.youtube.com/watch?v=N0MgLvceX7M&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=14
"""


def set_matrix_zeroes_using_sets_time_optimized(matrix: list[list[int]]) -> None:
    """Set complete rows and columns to zero when they contain an original zero.

    Approach:
        1. Record the matrix dimensions and create sets for the indices of rows
           and columns that must become zero.
        2. Scan every cell in the original matrix. When a zero is found, add its
           row and column indices to the corresponding sets. No cells are
           changed during this scan, so newly written zeroes cannot influence
           the result.
        3. Scan the matrix again. Set a cell to zero when its row index or column
           index appears in one of the recorded sets.

    Parameters:
        matrix: A non-empty rectangular integer matrix to update.

    Returns:
        None. The result is stored directly in ``matrix``.

    Mutation Behavior:
        The function modifies ``matrix`` in place. It does not create a copy of
        the matrix, but it does allocate sets containing row and column indices.

    Assumptions:
        ``matrix`` has 1 to 200 rows and 1 to 200 columns. Every row has the same
        number of columns, and every value is a signed 32-bit integer.

    Time Complexity:
        O(m * n), where ``m`` is the number of rows and ``n`` is the number of
        columns. Both scans visit every matrix cell once.

    Space Complexity:
        O(m + n) additional space. In the worst case, ``zero_rows`` stores all
        ``m`` row indices and ``zero_cols`` stores all ``n`` column indices.
        The solution modifies the matrix in place but does not use constant
        additional space.
    """
    # Step 1: Store the dimensions and initialize the row and column markers.
    rows: int = len(matrix)
    cols: int = len(matrix[0])
    zero_rows: set[int] = set()
    zero_cols: set[int] = set()

    # Step 2: Record every row and column containing an original zero.
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 0:
                zero_rows.add(row)
                zero_cols.add(col)

    # Step 3: Zero each cell whose row or column was recorded.
    for row in range(rows):
        for col in range(cols):
            if row in zero_rows or col in zero_cols:
                matrix[row][col] = 0


def set_matrix_zeroes_recursive_brute_force(matrix: list[list[int]]) -> None:
    """Zero required rows and columns using directional recursive traversal.

    Approach:
        This uses Depth-First Search (DFS)-style directional recursion. Each
        recursive path travels as far as possible in one direction before it
        returns and another direction begins.

        1. Record the matrix dimensions, create storage for all original zero
           positions, and define the four horizontal and vertical directions.
        2. Scan the matrix before modifying it and store every original zero
           position. This prevents newly written zeroes from starting new
           traversals.
        3. Define ``dfs`` to check the matrix boundaries, set the current cell
           to zero, and recursively move one step farther in the same direction.
        4. Process every stored zero position. From each one, start a separate
           DFS path in each of the four directions, which zeroes its complete
           row and column.

    Parameters:
        matrix: A non-empty rectangular integer matrix to update.

    Returns:
        None. The result is stored directly in ``matrix``.

    Mutation Behavior:
        The function modifies ``matrix`` in place. It also allocates storage for
        the positions of all original zeroes.

    Assumptions:
        ``matrix`` has 1 to 200 rows and 1 to 200 columns. Every row has the same
        number of columns, and every value is a signed 32-bit integer.

    Time Complexity:
        O(m * n + z * (m + n)), where ``m`` and ``n`` are the matrix dimensions
        and ``z`` is the number of original zeroes. The initial scan costs
        O(m * n), and each zero launches traversals across one row and column.
        When every cell is zero, the worst case is O(m * n * (m + n)).

    Space Complexity:
        O(z + max(m, n)) additional space. ``zero_stack`` stores ``z`` original
        zero positions, and a recursive path can use up to ``max(m, n)`` call
        frames. In the worst case, this simplifies to O(m * n).
    """
    # Step 1: Store dimensions, original-zero positions, and four directions.

    rows: int = len(matrix)
    cols: int = len(matrix[0])

    zero_stack: list[tuple[int, int]] = []

    directions: tuple[tuple[int, int]] = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    # Step 2: Save every original zero before changing any matrix cells.
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == 0:
                zero_stack.append((row_index, col_index))

    # Step 3: Recursively travel to the boundary in one fixed direction.
    def dfs(
        row_index: int,
        col_index: int,
        row_direction: int,
        col_direction: int,
    ) -> None:

        if 0 <= row_index < rows and 0 <= col_index < cols:
            matrix[row_index][col_index] = 0
            dfs(
                row_index=row_index + row_direction,
                col_index=col_index + col_direction,
                row_direction=row_direction,
                col_direction=col_direction,
            )

    # Step 4: Launch four directional DFS paths from every original zero.
    while zero_stack:
        row_index, col_index = zero_stack.pop()

        for row_direction, col_direction in directions:
            dfs(
                row_index=row_index + row_direction,
                col_index=col_index + col_direction,
                row_direction=row_direction,
                col_direction=col_direction,
            )


def set_matrix_zeroes_optimized(matrix: list[list[int]]) -> None:
    """Set matrix rows and columns to zero using constant additional space.

    Approach:
        This uses an in-place marker approach.

        1. Use an integer flag to remember whether the first column originally
           contains a zero. A separate flag is necessary because ``matrix[0][0]``
           cannot independently represent both the first row and first column.
        2. Scan every original cell. For each zero, mark the beginning of its
           row in the first column and the beginning of its column in the first
           row. A zero in column 0 updates the separate first-column flag.
        3. Visit the inner matrix, excluding its first row and first column. Set
           a cell to zero when either its row marker or column marker is zero.
        4. If ``matrix[0][0]`` is zero, set the complete first row to zero.
        5. If the separate first-column flag indicates an original zero, set
           the complete first column to zero.

    Parameters:
        matrix: A non-empty rectangular integer matrix to update.

    Returns:
        None. The result is stored directly in ``matrix``.

    Mutation Behavior:
        The function modifies ``matrix`` in place. Its first row and first
        column temporarily store markers before receiving their final values.

    Assumptions:
        ``matrix`` has 1 to 200 rows and 1 to 200 columns. Every row has the same
        number of columns, and every value is a signed 32-bit integer.

    Time Complexity:
        O(m * n), where ``m`` is the number of rows and ``n`` is the number of
        columns. The marker and inner-matrix passes each inspect at most every
        cell, while the final row and column passes cost O(n) and O(m).

    Space Complexity:
        O(1) additional space. The matrix itself stores all row and column
        markers, and only dimensions, indices, values, and one flag are stored
        separately.
    """
    # Step 1: Track whether the first column originally contains a zero.

    first_column_has_zero: int = 1

    # Step 2: Store row markers in column 0 and column markers in row 0.
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            if value == 0:
                matrix[row_index][0] = 0
                if col_index != 0:
                    matrix[0][col_index] = 0
                else:
                    first_column_has_zero = 0

    # Step 3: Use the markers to update every inner matrix cell.
    rows: int = len(matrix)
    cols: int = len(matrix[0])

    for row_index in range(1, rows):
        for col_index in range(1, cols):
            if matrix[row_index][0] == 0 or matrix[0][col_index] == 0:
                matrix[row_index][col_index] = 0

    # Step 4: Apply the marker representing the first row.
    if matrix[0][0] == 0:
        for col_index in range(cols):
            matrix[0][col_index] = 0

    # Step 5: Apply the separate marker representing the first column.
    if first_column_has_zero == 0:
        for row_index in range(rows):
            matrix[row_index][0] = 0


def solve() -> None:
    # matrix: list[list[int]] = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    # expected: list[list[int]] = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result: list[list[int]] = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Provided example with two zeroes in the first row.
    # matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]

    # expected = [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Provided multiple-choice example.
    # matrix = [[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 11, 12]]

    # expected = [[1, 2, 0, 4], [0, 0, 0, 0], [9, 10, 0, 12]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A matrix without zeroes remains unchanged.
    # matrix = [[1, 2], [3, 4]]

    # expected = [[1, 2], [3, 4]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A matrix containing only zeroes remains all zeroes.
    # matrix = [[0, 0], [0, 0]]

    # expected = [[0, 0], [0, 0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum dimensions containing a zero.
    # matrix = [[0]]

    # expected = [[0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum dimensions without a zero.
    # matrix = [[1]]

    # expected = [[1]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A single-row matrix.
    # matrix = [[1, 2, 0, 4]]

    # expected = [[0, 0, 0, 0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A single-column matrix.
    # matrix = [[1], [0], [3]]

    # expected = [[0], [0], [0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum and maximum allowed integer values surrounding a zero.
    # matrix = [[-(2**31), 0], [2**31 - 1, 1]]

    # expected = [[0, 0], [2**31 - 1, 0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Zeroes in opposite corners affect every row and column.
    # matrix = [[0, 2, 3], [4, 5, 6], [7, 8, 0]]

    # expected = [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Maximum row and column dimensions with one zero in the final position.
    # matrix = [[1] * 200 for _ in range(200)]
    # matrix[199][199] = 0

    # expected = [[1] * 200 for _ in range(200)]
    # for index in range(200):
    # expected[199][index] = 0
    # expected[index][199] = 0
    # set_matrix_zeroes_using_sets_time_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Second implementation with a zero in the center.
    # matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    # expected = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Second implementation with two zeroes in the first row.
    # matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]

    # expected = [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Second implementation for the provided multiple-choice example.
    # matrix = [[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 11, 12]]

    #  [[1, 2, 0, 4],
    #  [5, 0, 0, 0],
    #  [9, 10, 0, 12]]

    # expected = [[1, 2, 0, 4], [0, 0, 0, 0], [9, 10, 0, 12]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A matrix without zeroes remains unchanged.
    # matrix = [[1, 2], [3, 4]]

    # expected = [[1, 2], [3, 4]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A matrix containing only zeroes remains all zeroes.
    # matrix = [[0, 0], [0, 0]]

    # expected = [[0, 0], [0, 0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum dimensions containing a zero.
    # matrix = [[0]]

    # expected = [[0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum dimensions without a zero.
    # matrix = [[1]]

    # expected = [[1]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A single-row matrix must zero the entire row.
    # matrix = [[1, 2, 0, 4]]

    # expected = [[0, 0, 0, 0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # A single-column matrix must zero the entire column.
    # matrix = [[1], [0], [3]]

    # expected = [[0], [0], [0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum and maximum allowed integer values surrounding a zero.
    # matrix = [[-(2**31), 0], [2**31 - 1, 1]]

    # expected = [[0, 0], [2**31 - 1, 0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Zeroes in opposite corners affect every corresponding row and column.
    # matrix = [[0, 2, 3], [4, 5, 6], [7, 8, 0]]

    # expected = [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Maximum row and column dimensions with one zero in the final position.
    # matrix = [[1] * 200 for _ in range(200)]
    # matrix[199][199] = 0

    # expected = [[1] * 200 for _ in range(200)]
    # for index in range(200):
    # expected[199][index] = 0
    # expected[index][199] = 0
    # set_matrix_zeroes_recursive_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Constant-space optimized implementation with a zero in the center.
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

    expected = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    # after marking
    # [[1, 0, 1],
    # [0, 0, 1],
    # [1, 1, 1]]

    # after flipping inner matrix
    # [[1, 0, 1],
    # [0, 0, 1],
    # [1, 0, 0]]

    # expected
    # [[1, 0, 1],
    # [0, 0, 0],
    # [1, 0, 1]]

    # result
    #  [[1, 0, 1],
    #  [0, 0, 1],
    #  [1, 0, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Constant-space implementation with two zeroes in the first row.
    matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]

    expected = [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Constant-space implementation for the multiple-choice example.
    matrix = [[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 11, 12]]

    expected = [[1, 2, 0, 4], [0, 0, 0, 0], [9, 10, 0, 12]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A matrix without zeroes remains unchanged.
    matrix = [[1, 2], [3, 4]]

    expected = [[1, 2], [3, 4]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A matrix containing only zeroes remains all zeroes.
    matrix = [[0, 0], [0, 0]]

    expected = [[0, 0], [0, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum dimensions containing a zero.
    matrix = [[0]]

    expected = [[0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum dimensions without a zero.
    matrix = [[1]]

    expected = [[1]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A single-row matrix must zero the entire row.
    matrix = [[1, 2, 0, 4]]

    expected = [[0, 0, 0, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A single-column matrix must zero the entire column.
    matrix = [[1], [0], [3]]

    expected = [[0], [0], [0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum and maximum allowed integer values surrounding a zero.
    matrix = [[-(2**31), 0], [2**31 - 1, 1]]

    expected = [[0, 0], [2**31 - 1, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zeroes in opposite corners affect every corresponding row and column.
    matrix = [[0, 2, 3], [4, 5, 6], [7, 8, 0]]

    expected = [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum row and column dimensions with one zero in the final position.
    matrix = [[1] * 200 for _ in range(200)]
    matrix[199][199] = 0

    expected = [[1] * 200 for _ in range(200)]
    for index in range(200):
        expected[199][index] = 0
        expected[index][199] = 0
    set_matrix_zeroes_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
