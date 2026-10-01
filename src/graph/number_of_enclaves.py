"""481. Number of enclaves

Given an N x M binary matrix grid, where 0 represents a sea cell and 1
represents a land cell, find the number of land cells from which we cannot
walk off the boundary of the grid in any number of moves.

A move consists of walking from one land cell to another adjacent land cell
in one of four directions (up, down, left, or right), or walking off the
boundary of the grid. Diagonal cells are not adjacent.

Example 1:
    Input: grid = [
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
    Output: 3
    Explanation: The land cells at (1, 2), (2, 1), and (2, 2) cannot
    reach the boundary. The land cell at (1, 0) can walk off the grid.

Example 2:
    Input: grid = [
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ]
    Output: 3
    Explanation: The land cells at (2, 1), (2, 2), and (3, 2) cannot
    reach the boundary. The two land cells in the last column can exit.

Practice example:
    Pick the correct output for grid = [
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]:
    A. 4
    B. 3
    C. 5
    D. 2

Constraints:
    - 1 <= N, M <= 500.
    - grid[i][j] == 0 or 1.

https://www.youtube.com/watch?v=rxKcepXQgU4&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=16

"""

from collections import deque


def number_of_enclaves_dfs(grid: list[list[int]]) -> int:
    """Count land cells that cannot reach any grid boundary.

    Args:
        grid: A nonempty rectangular binary matrix with N rows and M columns,
            where 1 <= N, M <= 500. Zero denotes sea and one denotes land.
            Only horizontal and vertical moves between land cells are allowed.

    Returns:
        The number of land cells in components disconnected from every boundary.
        Single-row and single-column grids return zero because all cells lie
        on the boundary. The input grid is not modified.

    Approach:
        Use Depth-First Search (DFS) to mark boundary-connected land.
        1. Read the dimensions, allocate a separate visited matrix, initialize
           the enclave count, and define the four possible movement directions.
        2. Define recursive DFS: mark the current land cell before exploring its
           neighbors. Recurse only into in-bounds, unvisited land cells. Marking
           before recursion prevents cycles and repeated visits.
        3. Scan the left and right columns. Start DFS from each unvisited land
           cell there, marking its entire component as able to escape.
        4. Scan the top and bottom rows in the same way. The shared visited
           matrix prevents reprocessing corners and components reached earlier.
           Any land cell can escape exactly when it connects to boundary land,
           so after these scans every escapable land cell has been marked.
        5. Scan only the interior rows and columns, excluding all four edges.
           Count each unvisited land cell: it cannot reach any boundary and
           is therefore an enclave cell. Return the total number of such cells,
           not the number of components. If either dimension is less than
           three, there are no interior cells and the count remains zero.

    Time Complexity:
        O(N * M). Allocating the visited matrix and scanning for enclaves each
        take O(N * M). Boundary scans take O(N + M), and DFS visits each reached
        land cell at most once, checking four neighbors per visit.

    Space Complexity:
        O(N * M) auxiliary space. The visited matrix stores N * M booleans,
        and the recursive DFS call stack can grow to O(N * M) in the worst
        case. The four direction pairs, dimensions, count, and other scalar
        variables use O(1) space outside the recursive calls.

    Limitation:
        A long boundary-connected land path can exceed Python's recursion
        limit and raise RecursionError, including on valid inputs within the
        stated constraints. Complexity bounds assume traversal completes.
    """
    # 1. Initialize dimensions, visited state, count, and movement directions.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    visited: list[list[bool]] = [[False] * col_size for _ in range(row_size)]
    count: int = 0

    delta_list: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 2. Mark each reached land cell and explore its four neighbors with DFS.
    def dfs(row_index: int, col_index: int) -> None:
        # Mark before recursion so neighboring cells cannot revisit this cell.
        visited[row_index][col_index] = True

        for row_delta, col_delta in delta_list:
            new_row: int = row_index + row_delta
            new_col: int = col_index + col_delta

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and grid[new_row][new_col] == 1
                and not visited[new_row][new_col]
            ):
                dfs(row_index=new_row, col_index=new_col)

    # 3. Mark land connected to the left or right boundary.
    for row_index in range(row_size):
        if grid[row_index][0] == 1 and not visited[row_index][0]:
            dfs(row_index=row_index, col_index=0)

        if grid[row_index][col_size - 1] == 1 and not visited[row_index][col_size - 1]:
            dfs(row_index=row_index, col_index=col_size - 1)

    # 4. Mark land connected to the top or bottom boundary.
    for col_index in range(col_size):
        if grid[0][col_index] == 1 and not visited[0][col_index]:
            dfs(row_index=0, col_index=col_index)

        if grid[row_size - 1][col_index] == 1 and not visited[row_size - 1][col_index]:
            dfs(row_index=row_size - 1, col_index=col_index)

    # 5. Count only interior land that no boundary DFS reached.
    for row_index in range(1, row_size - 1):
        for col_index in range(1, col_size - 1):
            if grid[row_index][col_index] == 1 and not visited[row_index][col_index]:
                count += 1

    return count


def number_of_enclaves_bfs(grid: list[list[int]]) -> int:
    """Count land cells that cannot reach the boundary using a queue.

    Args:
        grid: A nonempty rectangular binary matrix with N rows and M columns,
            where 1 <= N, M <= 500. Zero represents sea and one represents land.
            Movement is allowed only between horizontally or vertically
            adjacent land cells; diagonal contact does not permit escape.

    Returns:
        The number of land cells disconnected from every boundary, not the
        number of land components. The input grid is not modified. If either
        dimension is less than three, there are no interior cells and the
        result is zero.

    Approach:
        Use multi-source Breadth-First Search (BFS) from boundary land cells.
        1. Read the dimensions and initialize a deque, a count, four movement
           directions, and a separate boolean visited matrix.
        2. Scan the left and right columns. Enqueue each unvisited land cell
           and immediately mark it visited because it can walk off the grid.
        3. Scan the top and bottom rows in the same way. Checking visited before
           enqueueing prevents duplicates at corners and on overlapping edges
           in single-row or single-column grids. These boundary cells form
           the initial sources for one shared BFS.
        4. Repeatedly remove the oldest queued cell with popleft() and inspect
           its four neighbors. Enqueue only in-bounds, unvisited land cells,
           marking each visited immediately so it is queued at most once.
           Every reached cell connects to boundary land and can therefore
           escape. When the queue is empty, all escapable land is visited.
        5. Scan only the interior rows and columns. Count land cells that are
           still unvisited, since none can reach the boundary. Return the count.

    Time Complexity:
        O(N * M). Initializing visited takes O(N * M), boundary scans take
        O(N + M), and the final interior scan takes at most O(N * M). BFS
        enqueues and dequeues each reachable land cell at most once and checks
        four neighbors per cell. Deque append and popleft take O(1) each.

    Space Complexity:
        O(N * M) auxiliary space. The visited matrix stores N * M booleans,
        and the queue can hold O(N * M) coordinate pairs in the worst case.
        The four direction pairs and scalar variables use O(1) additional
        space. This implementation uses no recursive call stack.
    """
    # 1. Initialize dimensions, queue, count, directions, and visited state.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    queue: deque[tuple[int, int]] = deque()
    count: int = 0
    delta_list: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited: list[list[bool]] = [[False] * col_size for _ in range(row_size)]

    # 2. Enqueue and mark unvisited land on the left and right boundaries.
    for row_index in range(row_size):
        if grid[row_index][0] == 1 and not visited[row_index][0]:
            queue.append((row_index, 0))
            visited[row_index][0] = True

        if grid[row_index][col_size - 1] == 1 and not visited[row_index][col_size - 1]:
            queue.append((row_index, col_size - 1))
            visited[row_index][col_size - 1] = True

    # 3. Add top and bottom boundary land, skipping already queued cells.
    for col_index in range(col_size):
        if grid[0][col_index] == 1 and not visited[0][col_index]:
            queue.append((0, col_index))
            visited[0][col_index] = True
        if grid[row_size - 1][col_index] == 1 and not visited[row_size - 1][col_index]:
            queue.append((row_size - 1, col_index))
            visited[row_size - 1][col_index] = True

    # 4. Expand BFS from all boundary sources through adjacent land.
    while queue:
        current_row, current_col = queue.popleft()

        for row_delta, col_delta in delta_list:
            new_row: int = current_row + row_delta
            new_col: int = current_col + col_delta

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and grid[new_row][new_col] == 1
                and not visited[new_row][new_col]
            ):
                # Mark on enqueue so another neighbor cannot queue it again.
                queue.append((new_row, new_col))
                visited[new_row][new_col] = True

    # 5. Count interior land that the boundary BFS could not reach.
    for row_index in range(1, row_size - 1):
        for col_index in range(1, col_size - 1):
            if grid[row_index][col_index] == 1 and not visited[row_index][col_index]:
                count += 1

    return count


def solve() -> None:
    grid: list[list[int]] = [
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
    expected: int = 3
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid: sea.
    grid: list[list[int]] = [[0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid: land.
    grid: list[list[int]] = [[1]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row with mixed cells.
    grid: list[list[int]] = [[1, 0, 1, 1, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column with mixed cells.
    grid: list[list[int]] = [[1], [0], [1], [1], [0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two rows: every cell is on the boundary.
    grid: list[list[int]] = [[1, 1, 1, 1], [1, 1, 1, 1]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two columns: every cell is on the boundary.
    grid: list[list[int]] = [[1, 1], [1, 1], [1, 1], [1, 1]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All sea.
    grid: list[list[int]] = [[0] * 5 for _ in range(5)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All land.
    grid: list[list[int]] = [[1] * 5 for _ in range(5)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One enclosed land cell.
    grid: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal contact does not allow escape.
    grid: list[list[int]] = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land connected only to the top boundary.
    grid: list[list[int]] = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land connected only to the bottom boundary.
    grid: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 1, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land connected only to the left boundary.
    grid: list[list[int]] = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Land connected only to the right boundary.
    grid: list[list[int]] = [[0, 0, 0], [0, 1, 1], [0, 0, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple disconnected enclaves alongside escaping land.
    grid: list[list[int]] = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    expected: int = 8
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid with an enclosed component.
    grid: list[list[int]] = [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]]
    expected: int = 2
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid with a right-boundary exit.
    grid: list[list[int]] = [[0, 0, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 0]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall grid from the second example.
    grid: list[list[int]] = [
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ]
    expected: int = 3
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width and minimum height.
    grid: list[list[int]] = [[1] * 500]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height and minimum width.
    grid: list[list[int]] = [[1] for _ in range(500)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions with all sea.
    grid: list[list[int]] = [[0] * 500 for _ in range(500)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum possible enclave count.
    grid: list[list[int]] = (
        [[0] * 500] + [[0] + [1] * 498 + [0] for _ in range(498)] + [[0] * 500]
    )
    expected: int = 248004
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: enclosed block beside a boundary corner.
    grid: list[list[int]] = [
        [0, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
    expected: int = 4
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Closed land ring encloses a sea cell.
    grid: list[list[int]] = [
        [0] * 5,
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0] * 5,
    ]
    expected: int = 8
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One bridge connects the entire ring to the top boundary.
    grid: list[list[int]] = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0] * 5,
    ]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Boundary ring with an isolated central island.
    grid: list[list[int]] = (
        [[1] * 7] + [[1] + [0] * 5 + [1] for _ in range(5)] + [[1] * 7]
    )
    grid[3][3] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Checkerboard land touches only diagonally.
    grid: list[list[int]] = [
        [int((row + col) % 2 == 0) for col in range(7)] for row in range(7)
    ]
    expected: int = 13
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One land component reaches all four boundaries.
    grid: list[list[int]] = [
        [int(row == 3 or col == 3) for col in range(7)] for row in range(7)
    ]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated land at the top-left interior.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[1][1] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated land at the center.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated land at the bottom-right interior.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[5][5] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Escape through the top edge leaves another island enclosed.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    grid[0][2] = 1
    grid[1][2] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Escape through the bottom edge leaves another island enclosed.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    grid[6][2] = 1
    grid[5][2] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Escape through the left edge leaves another island enclosed.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    grid[2][0] = 1
    grid[2][1] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Escape through the right edge leaves another island enclosed.
    grid: list[list[int]] = [[0] * 7 for _ in range(7)]
    grid[3][3] = 1
    grid[2][6] = 1
    grid[2][5] = 1
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Winding escape path with a separate enclave.
    grid: list[list[int]] = [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid with enclosed land next to right-edge escaping land.
    grid: list[list[int]] = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    expected: int = 3
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall grid with a fully enclosed vertical component.
    grid: list[list[int]] = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    expected: int = 5
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-by-two grid has no interior.
    grid: list[list[int]] = [
        [1, 0],
        [0, 1],
    ]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum dimensions with no land.
    grid: list[list[int]] = [
        [0],
    ]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum dimensions with boundary land.
    grid: list[list[int]] = [
        [1],
    ]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum height and maximum width with alternating land.
    grid: list[list[int]] = [[col % 2 for col in range(500)]]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height and minimum width with alternating land.
    grid: list[list[int]] = [[row % 2] for row in range(500)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width with one enclosed horizontal strip.
    grid: list[list[int]] = [[0] * 500, [0] + [1] * 498 + [0], [0] * 500]
    expected: int = 498
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height with one enclosed vertical strip.
    grid: list[list[int]] = [[0, 0, 0]] + [[0, 1, 0] for _ in range(498)] + [[0, 0, 0]]
    expected: int = 498
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid filled with sea.
    grid: list[list[int]] = [[0] * 500 for _ in range(500)]
    expected: int = 0
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid of isolated checkerboard land cells.
    grid: list[list[int]] = [
        [(row + col) % 2 for col in range(500)] for row in range(500)
    ]
    expected: int = 124002
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum count with a sea border.
    grid: list[list[int]] = (
        [[0] * 500] + [[0] + [1] * 498 + [0] for _ in range(498)] + [[0] * 500]
    )
    expected: int = 248004
    result: int = number_of_enclaves_bfs(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # BFS: top-boundary-connected land escapes; a separate island is enclosed.
    grid: list[list[int]] = [
        [0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    expected: int = 1
    result: int = number_of_enclaves_bfs(grid)

    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
