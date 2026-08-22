"""Rotate Matrix by 90 Degrees

Given an ``n x n`` 2D integer matrix, rotate the matrix by 90 degrees clockwise.

The rotation must be done in place, meaning the input 2D matrix must be modified
directly.

Example 1:
    Input: matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

Example 2:
    Input: matrix = [[0, 1, 1, 2], [2, 0, 3, 1], [4, 5, 0, 5],
                     [5, 6, 7, 0]]
    Output: [[5, 4, 2, 0], [6, 5, 0, 1], [7, 0, 3, 1],
             [0, 5, 1, 2]]

http://takeuforward.org/plus/dsa/problems/rotate-matrix-by-90-degrees
https://www.youtube.com/watch?v=Z0R2u6gd3GU&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=15

"""


def rotate_matrix_by_90_degrees_brute_force(matrix: list[list[int]]) -> None:
    """Rotate a square matrix 90 degrees clockwise using a separate matrix.

    Approach:
        1. Create an ``n x n`` matrix filled with zeroes to store the rotation.
        2. Visit every value at position ``(row, col)`` in the input matrix.
        3. Place that value at ``(col, n - 1 - row)`` in the new matrix. The old
           column becomes the new row, while the reversed old row becomes the
           new column.
        4. Replace all contents of the original outer list with the rows from
           the rotated matrix so callers observe the mutation.

    Parameters:
        matrix: A non-empty ``n x n`` integer matrix to rotate.

    Returns:
        None. The rotated result is stored directly in ``matrix``.

    Mutation Behavior:
        The function modifies the original outer ``matrix`` list using slice
        assignment. It creates new inner row lists and does not preserve the
        identities of the original rows.

    Assumptions:
        ``matrix`` is non-empty, square, and contains rows of equal length.

    Time Complexity:
        O(n^2), where ``n`` is the number of rows and columns. Initializing the
        rotated matrix and placing every value each process ``n^2`` cells. The
        final outer-list slice assignment takes O(n) time.

    Space Complexity:
        O(n^2) additional space for the separate ``rotated`` matrix. Therefore,
        this brute-force implementation does not satisfy the problem's intended
        constant-extra-space in-place requirement.
    """
    # Step 1: Create a separate zero-filled matrix for the rotated values.

    size: int = len(matrix)

    rotated: list[list[int]] = [[0] * size for _ in range(size)]

    # Step 2: Visit each original matrix position.
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            # Step 3: Map (row, col) to (col, n - 1 - row).
            new_row_index: int = col_index

            # ``size - 1`` is the last valid index. Subtracting ``row_index``
            # reverses the row position: the first row moves to the last column,
            # and the last row moves to the first column.
            new_col_index: int = size - row_index - 1
            rotated[new_row_index][new_col_index] = value

    # Step 4: Replace the original outer list's contents in place.
    matrix[:] = rotated


def rotate_matrix_by_90_degrees_optimized(matrix: list[list[int]]) -> None:
    size: int = len(matrix)

    for row_index in range(size - 1):
        for col_index in range(row_index + 1, size):
            matrix[row_index][col_index], matrix[col_index][row_index] = (
                matrix[col_index][row_index],
                matrix[row_index][col_index],
            )

    for row_index in range(size):
        matrix[row_index].reverse()


def solve() -> None:
    # matrix: list[list[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # expected: list[list[int]] = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result: list[list[int]] = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Provided 4 x 4 example.
    # matrix = [[0, 1, 1, 2], [2, 0, 3, 1], [4, 5, 0, 5], [5, 6, 7, 0]]

    # expected = [[5, 4, 2, 0], [6, 5, 0, 1], [7, 0, 3, 1], [0, 5, 1, 2]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum 1 x 1 matrix.
    # matrix = [[5]]

    # expected = [[5]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Even-sized 2 x 2 matrix.
    # matrix = [[1, 2], [3, 4]]

    # expected = [[3, 1], [4, 2]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Matrix containing negative values and zero.
    # matrix = [[-1, 0], [2, -3]]

    # expected = [[2, -1], [-3, 0]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Duplicate values remain in their correctly rotated positions.
    # matrix = [[7, 7, 7], [7, 7, 7], [7, 7, 7]]

    # expected = [[7, 7, 7], [7, 7, 7], [7, 7, 7]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Signed 32-bit boundary-style values.
    # matrix = [[-(2**31), 2**31 - 1], [0, 1]]

    # expected = [[0, -(2**31)], [1, 2**31 - 1]]
    # rotate_matrix_by_90_degrees_brute_force(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Optimized implementation with a 3 x 3 matrix.
    # matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # expected = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    # rotate_matrix_by_90_degrees_optimized(matrix)
    # result = matrix
    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Optimized implementation with the provided 4 x 4 matrix.
    matrix = [[0, 1, 1, 2], [2, 0, 3, 1], [4, 5, 0, 5], [5, 6, 7, 0]]

    expected = [[5, 4, 2, 0], [6, 5, 0, 1], [7, 0, 3, 1], [0, 5, 1, 2]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized implementation with an odd-sized 3 x 3 matrix.
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    expected = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum 1 x 1 matrix.
    matrix = [[5]]

    expected = [[5]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even-sized 2 x 2 matrix.
    matrix = [[1, 2], [3, 4]]

    expected = [[3, 1], [4, 2]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matrix containing negative values and zero.
    matrix = [[-1, 0], [2, -3]]

    expected = [[2, -1], [-3, 0]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values remain in their correctly rotated positions.
    matrix = [[7, 7, 7], [7, 7, 7], [7, 7, 7]]

    expected = [[7, 7, 7], [7, 7, 7], [7, 7, 7]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Signed 32-bit boundary-style values.
    matrix = [[-(2**31), 2**31 - 1], [0, 1]]

    expected = [[0, -(2**31)], [1, 2**31 - 1]]
    rotate_matrix_by_90_degrees_optimized(matrix)
    result = matrix
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
