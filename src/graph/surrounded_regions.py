"""232. Surrounded Regions

You are given a matrix mat of size N x M where each cell contains either
'O' or 'X'. Replace all 'O' cells completely surrounded by 'X' with 'X'.

Rules:
    - An 'O' or a group of connected 'O' cells is surrounded if it is not
      connected to any border of the matrix.
    - Two 'O' cells are connected if they are adjacent horizontally or
      vertically, not diagonally.
    - A connected region of 'O' cells touching the first row, last row,
      first column, or last column is not surrounded and must not change.

Example 1:
    Input: mat = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    Output: [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],
    ]
    Explanation: The region containing (1, 1), (1, 2), and (2, 2) is not
    connected to a border, so those cells become 'X'. The 'O' at (3, 1)
    touches the bottom border and remains unchanged.

Example 2:
    Input: mat = [
        ["X", "X", "X"],
        ["X", "O", "X"],
        ["X", "X", "X"],
    ]
    Output: [
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]
    Explanation: The only 'O', at (1, 1), is completely surrounded by 'X'
    horizontally and vertically, so it is replaced with 'X'.

Practice example:
    Pick the correct output for mat = [
        ["X", "X", "X", "O"],
        ["X", "X", "X", "X"],
        ["O", "X", "X", "X"],
        ["X", "X", "X", "X"],
    ]:
    A. [["X", "X", "X", "X"], ["X", "X", "X", "X"],
        ["O", "X", "X", "X"], ["X", "X", "X", "X"]]
    B. [["X", "X", "X", "O"], ["X", "X", "X", "X"],
        ["O", "X", "X", "X"], ["X", "X", "X", "X"]]
    C. [["X", "X", "X", "O"], ["X", "X", "X", "X"],
        ["X", "X", "X", "X"], ["X", "X", "X", "X"]]
    D. [["X", "X", "X", "X"], ["X", "X", "X", "X"],
        ["X", "X", "X", "X"], ["X", "X", "X", "X"]]

Constraints:
    - N == len(mat).
    - M == len(mat[i]).
    - 1 <= N, M <= 300.
    - mat[i][j] is 'X' or 'O'.

https://takeuforward.org/practice/dsa/surrounded-regions

https://www.youtube.com/watch?v=BtdgAys4yMk&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=14


"""


def surrounded_regions(mat: list[list[str]]) -> list[list[str]]:
    """Replace surrounded O regions in a copy of the matrix.

    Args:
        mat: A nonempty rectangular N x M matrix containing only 'O' and
            'X', with 1 <= N, M <= 300. These constraints are assumed,
            not validated.

    Returns:
        A new matrix with every O region that has no horizontal or vertical
        connection to a border replaced by X. Border-connected O cells and
        all original X cells remain unchanged. Each output row is copied;
        the input matrix is not modified.

    Approach:
        Recursive Depth-First Search (DFS), using flood fill from the borders.
        1. Read the dimensions, copy each input row into result, and create
           a visited matrix initialized to False. Define the four horizontal
           and vertical moves; diagonal cells are not connected.
        2. Define DFS to mark its current O cell visited before exploring
           neighbors. Recurse only into in-bounds, unvisited O cells. Marking
           first prevents cycles and repeated exploration. Here visited means
           border-connected, because all searches begin at border O cells.
        3. Scan the left and right borders, starting DFS at each unvisited O.
           DFS marks the entire connected region safe from replacement.
           The visited checks avoid restarting searches in marked regions.
        4. Scan the top and bottom borders in the same way. Shared visited
           flags also avoid duplicate searches at corners or overlapping
           borders in single-row and single-column matrices.
        5. Scan only interior cells. Change an O to X in result if it is not
           visited. Any O connected to a border was reached by DFS, so the
           remaining O cells are exactly the surrounded regions. Border
           cells themselves cannot be surrounded and need no replacement.
        6. Return result. For one or two rows or columns there is no interior,
           so the matrix stays unchanged. All-X matrices also stay unchanged;
           all-O matrices should stay unchanged because every O connects to
           a border, provided traversal completes within the recursion limit.

        Example: In the first example, DFS marks only the border O at (3, 1).
        The interior O cells at (1, 1), (1, 2), and (2, 2) remain unvisited
        and become X in the output copy.

    Time Complexity:
        O(N * M). Copying the matrix and initializing visited each cost
        O(N * M). Border scans cost O(N + M). Every reached O is visited
        once and checks four neighbors, so all DFS searches together cost
        O(N * M), not that amount per border cell. The final interior scan
        costs at most O(N * M).

    Space Complexity:
        O(N * M). result stores N * M cells, visited stores N * M flags,
        and the recursive call stack can contain O(N * M) frames along a
        long connected path. Excluding the output, auxiliary space is still
        O(N * M). The four moves and scalar indices use O(1) space.

    Limitation:
        Python's recursion limit can be exceeded on valid large regions,
        including a 300 x 300 all-O matrix. Thus this recursive implementation
        does not reliably support the full input bounds under the default
        recursion limit, despite its O(N * M) time and space complexity.
    """
    # 1. Copy the matrix and prepare shared discovery flags and four moves.
    row_size: int = len(mat)
    col_size: int = len(mat[0])
    result: list[list[str]] = [row.copy() for row in mat]
    visited: list[list[bool]] = [[False] * col_size for _ in range(row_size)]
    delta_list: list[tuple[int, int]] = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def dfs(row_index: int, col_index: int) -> None:
        # 2. Mark this border-connected O before exploring unvisited O neighbors.
        visited[row_index][col_index] = True
        for row_delta, col_delta in delta_list:
            new_row: int = row_index + row_delta
            new_col: int = col_index + col_delta

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and not visited[new_row][new_col]
                and mat[new_row][new_col] == "O"
            ):
                dfs(row_index=new_row, col_index=new_col)

    # 3. Flood fill from unvisited O cells on the left and right borders.
    for row_index in range(row_size):
        if mat[row_index][0] == "O" and not visited[row_index][0]:
            dfs(row_index=row_index, col_index=0)
        if mat[row_index][col_size - 1] == "O" and not visited[row_index][col_size - 1]:
            dfs(row_index=row_index, col_index=col_size - 1)

    # 4. Complete border discovery from the top and bottom rows.
    for col_index in range(col_size):
        if mat[0][col_index] == "O" and not visited[0][col_index]:
            dfs(row_index=0, col_index=col_index)
        if mat[row_size - 1][col_index] == "O" and not visited[row_size - 1][col_index]:
            dfs(row_index=row_size - 1, col_index=col_index)

    # 5. Capture only interior Os with no connection to any border.
    for row_index in range(1, row_size - 1):
        for col_index in range(1, col_size - 1):
            if not visited[row_index][col_index] and mat[row_index][col_index] == "O":
                result[row_index][col_index] = "X"

    # 6. Return the modified copy, preserving the original matrix.
    return result


def solve() -> None:
    mat: list[list[str]] = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: isolated interior O.
    mat: list[list[str]] = [["X", "X", "X"], ["X", "O", "X"], ["X", "X", "X"]]
    expected: list[list[str]] = [["X", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid containing X.
    mat: list[list[str]] = [["X"]]
    expected: list[list[str]] = [["X"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid containing O.
    mat: list[list[str]] = [["O"]]
    expected: list[list[str]] = [["O"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row: every cell is on the border.
    mat: list[list[str]] = [["O", "X", "O", "X", "O"]]
    expected: list[list[str]] = [["O", "X", "O", "X", "O"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column: every cell is on the border.
    mat: list[list[str]] = [["O"], ["X"], ["O"], ["X"], ["O"]]
    expected: list[list[str]] = [["O"], ["X"], ["O"], ["X"], ["O"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two rows: no interior cells.
    mat: list[list[str]] = [["X", "O", "O", "O", "X"], ["O", "X", "O", "X", "O"]]
    expected: list[list[str]] = [["X", "O", "O", "O", "X"], ["O", "X", "O", "X", "O"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two columns: no interior cells.
    mat: list[list[str]] = [["X", "O"], ["O", "O"], ["O", "X"], ["X", "X"]]
    expected: list[list[str]] = [["X", "O"], ["O", "O"], ["O", "X"], ["X", "X"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Top-border connection protects an interior chain.
    mat: list[list[str]] = [
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bottom-border connection protects an interior chain.
    mat: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "O", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Left-border connection protects an interior chain.
    mat: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["O", "O", "O", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["O", "O", "O", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide rectangle: only the right border connects the region.
    mat: list[list[str]] = [
        ["X", "X", "X", "X", "X", "X"],
        ["X", "X", "O", "O", "O", "O"],
        ["X", "X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X", "X", "X"],
        ["X", "X", "O", "O", "O", "O"],
        ["X", "X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide rectangle: an interior O must not seed DFS at a border X.
    mat: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "O", "X", "X", "X"],
        ["X", "X", "O", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall rectangle: enclosed region.
    mat: list[list[str]] = [
        ["X", "X", "X"],
        ["X", "O", "X"],
        ["X", "O", "X"],
        ["X", "O", "X"],
        ["X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal contact with a corner does not protect the center.
    mat: list[list[str]] = [["O", "X", "X"], ["X", "O", "X"], ["X", "X", "X"]]
    expected: list[list[str]] = [["O", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate regions: preserve border-connected cells, capture the rest.
    mat: list[list[str]] = [
        ["X", "O", "X", "X", "X", "X", "X"],
        ["X", "O", "O", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "O", "O", "X"],
        ["X", "X", "X", "X", "O", "O", "X"],
        ["X", "X", "X", "X", "X", "X", "X"],
        ["X", "O", "X", "X", "X", "X", "X"],
        ["X", "O", "X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "O", "X", "X", "X", "X", "X"],
        ["X", "O", "O", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X"],
        ["X", "O", "X", "X", "X", "X", "X"],
        ["X", "O", "X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Closed O ring inside an X border.
    mat: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "O", "O", "O", "X"],
        ["X", "O", "X", "O", "X"],
        ["X", "O", "O", "O", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: isolated border Os stay unchanged.
    mat: list[list[str]] = [
        ["X", "X", "X", "O"],
        ["X", "X", "X", "X"],
        ["O", "X", "X", "X"],
        ["X", "X", "X", "X"],
    ]
    expected: list[list[str]] = [
        ["X", "X", "X", "O"],
        ["X", "X", "X", "X"],
        ["O", "X", "X", "X"],
        ["X", "X", "X", "X"],
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All Os in a small grid remain unchanged.
    mat: list[list[str]] = [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
    expected: list[list[str]] = [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width and minimum height.
    mat: list[list[str]] = [["O"] * 300]
    expected: list[list[str]] = [["O"] * 300]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height and minimum width.
    mat: list[list[str]] = [["O"] for _ in range(300)]
    expected: list[list[str]] = [["O"] for _ in range(300)]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: all Xs.
    mat: list[list[str]] = [["X"] * 300 for _ in range(300)]
    expected: list[list[str]] = [["X"] * 300 for _ in range(300)]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: enclosed interior Os.
    mat: list[list[str]] = (
        [["X"] * 300]
        + [["X"] + ["O"] * 298 + ["X"] for _ in range(298)]
        + [["X"] * 300]
    )
    expected: list[list[str]] = [["X"] * 300 for _ in range(300)]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: checkerboard has no diagonal connectivity.
    mat: list[list[str]] = [
        ["O" if (r + c) % 2 == 0 else "X" for c in range(300)] for r in range(300)
    ]
    expected: list[list[str]] = [
        [
            "O" if (r in (0, 299) or c in (0, 299)) and (r + c) % 2 == 0 else "X"
            for c in range(300)
        ]
        for r in range(300)
    ]
    result: list[list[str]] = surrounded_regions(mat)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
