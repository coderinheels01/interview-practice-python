"""Print the Matrix in Spiral Manner

Given an ``m x n`` matrix, return its elements in clockwise spiral order.

Return an array containing the elements in the order in which they appear when
the matrix is traversed in a spiral manner.

Example 1:
    Input: matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

    Explanation: The spiral order is:
    1, 2, 3 -> 6, 9 -> 8, 7 -> 4, 5.

Example 2:
    Input: matrix = [[1, 2, 3, 4], [5, 6, 7, 8]]
    Output: [1, 2, 3, 4, 8, 7, 6, 5]

    Explanation: The spiral order is:
    1, 2, 3, 4 -> 8, 7, 6, 5.

Constraints:
    - m == matrix.length
    - n == matrix[i].length
    - 1 <= m, n <= 100
    - -100 <= matrix[i][j] <= 100

    https://www.youtube.com/watch?v=3Zv-s9UUrFM&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=16
"""


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """Return all matrix values in clockwise spiral order.

    Approach:
        Use four boundaries to describe the rectangular layer that has not yet
        been visited:

        - ``left`` is the first unvisited column.
        - ``right`` is one position after the last unvisited column.
        - ``top`` is the first unvisited row.
        - ``bottom`` is one position after the last unvisited row.

        1. Initialize the four boundaries around the entire matrix and create
           the result list.
        2. Traverse the current top row from left to right, then move ``top``
           down because that row has been visited.
        3. Traverse the current right column from top to bottom, then move
           ``right`` left because that column has been visited.
        4. Check whether any unvisited row and column remain. This check is
           needed in the middle of the loop because the top or right traversal
           may consume the final row or column. Without it, a single row or
           column could be visited twice.
        5. Traverse the current bottom row from right to left. Start at
           ``right - 1`` to skip the bottom-right corner already visited by the
           right-column traversal. Then move ``bottom`` up.
        6. Traverse the current left column from bottom to top. The bottom-left
           corner is included here because the bottom-row range intentionally
           excluded it. Then move ``left`` right.
        7. Repeat these steps while the boundaries contain an unvisited layer.

    Parameters:
        matrix: A non-empty, rectangular two-dimensional integer matrix.

    Returns:
        A new list containing every matrix element in clockwise spiral order.

    Mutation:
        The input matrix is not modified.

    Time Complexity:
        O(rows * cols), because every matrix element is appended exactly once.

    Space Complexity:
        O(rows * cols) for the returned result list. The four boundaries and
        loop variables use O(1) auxiliary space when the output is excluded.

    Assumptions:
        The matrix contains at least one row and one column, as guaranteed by
        the problem constraints.
    """
    # 1. Place exclusive boundaries around the entire unvisited matrix.
    rows: int = len(matrix)
    cols: int = len(matrix[0])

    left, right = 0, cols
    top, bottom = 0, rows

    result: list[int] = []

    # 7. Continue while at least one unvisited row and column remain.
    while left < right and top < bottom:
        # 2. Visit the top row from left to right, then remove that row.
        for index in range(left, right):
            result.append(matrix[top][index])

        top += 1

        # 3. Visit the right column from top to bottom, then remove it.
        for index in range(top, bottom):
            result.append(matrix[index][right - 1])

        right -= 1

        # 4. Stop if the last row or column was consumed above.
        if top >= bottom or left >= right:
            break

        # 5. Visit the bottom row from right to left, then remove it.
        for index in range(right - 1, left, -1):
            result.append(matrix[bottom - 1][index])

        bottom -= 1

        # 6. Visit the left column from bottom to top, then remove it.
        for index in range(bottom, top - 1, -1):
            result.append(matrix[index][left])

        left += 1

    return result


def solve() -> None:
    matrix: list[list[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    expected: list[int] = [1, 2, 3, 6, 9, 8, 7, 4, 5]
    result: list[int] = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[1, 2, 3, 4], [5, 6, 7, 8]]

    expected = [1, 2, 3, 4, 8, 7, 6, 5]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[1, 2], [3, 4], [5, 6], [7, 8]]

    expected = [1, 2, 4, 6, 8, 7, 5, 3]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[1]]

    expected = [1]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[1, 2, 3, 4]]

    expected = [1, 2, 3, 4]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[1], [2], [3], [4]]

    expected = [1, 2, 3, 4]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[-100, 0, 100], [4, -5, 6]]

    expected = [-100, 0, 100, 6, -5, 4]
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    matrix = [[100 for _ in range(100)] for _ in range(100)]

    expected = [100] * 10_000
    result = spiral_order(matrix)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
