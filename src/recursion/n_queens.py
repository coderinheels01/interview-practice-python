"""N Queen

Given an integer n, return every unique arrangement of n queens on an n x n
chessboard such that no two queens attack one another. The solutions may be
returned in any order.

Represent each solution as a list of n strings, each containing n characters.
'Q' represents a queen and '.' represents an empty square. Each solution must
describe a distinct board arrangement containing exactly n queens.

Attack rules:
    1. No two queens may share a row.
    2. No two queens may share a column.
    3. No two queens may share a diagonal with equal row - col values
       (top-left to bottom-right).
    4. No two queens may share an anti-diagonal with equal row + col values
       (top-right to bottom-left).

Example 1:
    Input: n = 4
    Output: [[".Q..", "...Q", "Q...", "..Q."],
             ["..Q.", "Q...", "...Q", ".Q.."]]
    Explanation: There are two valid arrangements of four queens.

Example 2:
    Input: n = 2
    Output: [[]]
    Explanation: No valid arrangement exists on a 2 x 2 board.
    Note: The supplied question represents no solutions as [[]].

Example 3:
    Input: n = 1
    Output: [["Q"]]

Constraints:
    - 1 <= n <= 9

    https://www.youtube.com/watch?v=i05Ju7AftcM&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=16
"""


def n_queens(n: int) -> list[list[str]]:
    row_filled: list[bool] = [False] * n
    upper_diagonal_filled: list[bool] = [False] * (2 * n - 1)
    lower_diagonal_filled: list[bool] = [False] * (2 * n - 1)

    board: list[list[str]] = [["." for _ in range(n)] for _ in range(n)]

    result: list[list[str]] = []

    def is_safe(row: int, col: int) -> bool:
        return (
            not row_filled[row]
            and not lower_diagonal_filled[row + col]
            and not upper_diagonal_filled[(n - 1) + col - row]
        )

    def fill_with_queen(col: int) -> None:
        if col == n:
            new_board: list[str] = ["".join(row) for row in board]
            result.append(new_board)
            return
        for row in range(n):
            if is_safe(row=row, col=col):
                board[row][col] = "Q"
                row_filled[row] = True
                lower_diagonal_filled[row + col] = True
                upper_diagonal_filled[(n - 1) + col - row] = True
                fill_with_queen(col=col + 1)
                board[row][col] = "."
                row_filled[row] = False
                # row + col identifies a top-right-to-bottom-left diagonal.
                # Moving down-left increases row by one and decreases col
                # by one, so their sum stays the same. For n = 4:
                #
                #         col 0   col 1   col 2   col 3
                # row 0      0       1       2       3
                # row 1      1       2       3       4
                # row 2      2       3       4       5
                # row 3      3       4       5       6
                #
                # Equal indices identify the same diagonal. Index 3 joins
                # (0,3), (1,2), (2,1), and (3,0). Index 0 has only (0,0),
                # and index 6 has only (3,3): extending either diagonal
                # up-right or down-left leaves the board.
                # The sum already ranges from 0 to 2*n - 2, so no offset
                # is needed. There are 2*n - 1 possible diagonal indices,
                # which explains the flag array's length.
                # Reset this flag when removing the queen during backtracking.
                lower_diagonal_filled[row + col] = False
                # col - row identifies a top-left-to-bottom-right diagonal.
                # Moving down-right increases both coordinates by one, so
                # their difference stays the same. For n = 4:
                #
                #         col 0   col 1   col 2   col 3
                # row 0      0       1       2       3
                # row 1     -1       0       1       2
                # row 2     -2      -1       0       1
                # row 3     -3      -2      -1       0
                #
                # Adding n - 1 shifts the labels from [-(n - 1), n - 1]
                # to nonnegative indices [0, 2*n - 2]. For n = 4, add 3:
                #
                #         col 0   col 1   col 2   col 3
                # row 0      3       4       5       6
                # row 1      2       3       4       5
                # row 2      1       2       3       4
                # row 3      0       1       2       3
                #
                # Equal indices identify the same diagonal. Index 3 joins
                # (0,0), (1,1), (2,2), and (3,3). Index 6 has only (0,3):
                # moving up-left or down-right leaves the board. A diagonal
                # can contain just one square. There are 2*n - 1 diagonals,
                # which explains the flag array's length. The opposite
                # diagonal direction is tracked separately using row + col.
                # Reset this flag when removing the queen during backtracking.
                upper_diagonal_filled[(n - 1) + col - row] = False

    fill_with_queen(col=0)

    return result if result else [[]]


def solve() -> None:
    from itertools import permutations as column_permutations

    n: int = 4
    expected: list[list[str]] = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."],
    ]
    result: list[list[str]] = n_queens(n)

    # Ignore solution order while preserving row order within each board.
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum size: one queen fills the board.
    n = 1
    expected = [["Q"]]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two queens have no solution; use the supplied empty-board sentinel.
    n = 2
    expected = [[]]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three queens also have no solution.
    n = 3
    expected = [[]]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example: both distinct arrangements.
    n = 4
    expected = [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All valid arrangements for size 5.
    n = 5
    # Independent oracle: each permutation selects one column per row.
    expected = [
        ["." * col + "Q" + "." * (n - col - 1) for col in columns]
        for columns in column_permutations(range(n))
        if len({row - col for row, col in enumerate(columns)}) == n
        and len({row + col for row, col in enumerate(columns)}) == n
    ]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All valid arrangements for size 6.
    n = 6
    # Independent oracle: each permutation selects one column per row.
    expected = [
        ["." * col + "Q" + "." * (n - col - 1) for col in columns]
        for columns in column_permutations(range(n))
        if len({row - col for row, col in enumerate(columns)}) == n
        and len({row + col for row, col in enumerate(columns)}) == n
    ]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All valid arrangements for size 7.
    n = 7
    # Independent oracle: each permutation selects one column per row.
    expected = [
        ["." * col + "Q" + "." * (n - col - 1) for col in columns]
        for columns in column_permutations(range(n))
        if len({row - col for row, col in enumerate(columns)}) == n
        and len({row + col for row, col in enumerate(columns)}) == n
    ]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All valid arrangements for size 8.
    n = 8
    # Independent oracle: each permutation selects one column per row.
    expected = [
        ["." * col + "Q" + "." * (n - col - 1) for col in columns]
        for columns in column_permutations(range(n))
        if len({row - col for row, col in enumerate(columns)}) == n
        and len({row + col for row, col in enumerate(columns)}) == n
    ]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed size: every valid arrangement.
    n = 9
    # Independent oracle: each permutation selects one column per row.
    expected = [
        ["." * col + "Q" + "." * (n - col - 1) for col in columns]
        for columns in column_permutations(range(n))
        if len({row - col for row, col in enumerate(columns)}) == n
        and len({row + col for row, col in enumerate(columns)}) == n
    ]
    result = n_queens(n)

    assert sorted(result) == sorted(expected)
    assert len({tuple(board) for board in result}) == len(result)
    assert len({id(board) for board in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
