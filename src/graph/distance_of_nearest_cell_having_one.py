"""317. Distance of nearest cell having one

Given a binary grid of N x M, find the distance of the nearest 1 in the grid
for each cell.

The distance is calculated as |i1 - i2| + |j1 - j2|, where i1, j1 are the
row and column indices of the current cell, and i2, j2 are the row and
column indices of the nearest cell having value 1.

Example 1:
    Input: grid = [
      [0, 1, 1, 0]
    , [1, 1, 0, 0],
      [0, 0, 1, 1]]
    Output: [
        [1, 0, 0, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0]]
    Explanation: Zeros at (0, 0), (0, 3), (1, 2), (1, 3), (2, 0),
    and (2, 1) are at a distance of 1 from ones at (0, 1), (0, 2),
    (0, 2), (2, 3), (1, 0), and (1, 1), respectively.

Example 2:
    Input: grid = [
    [1, 0, 1],
    [1, 1, 0],
    [1, 0, 0]]
    Output: [
    [0, 1, 0],
    [0, 0, 1],
    [0, 1, 2]]
    Explanation: Zeros at (0, 1), (1, 2), (2, 1), and (2, 2) are at
    distances of 1, 1, 1, and 2 from ones at (0, 0), (0, 2), (2, 0),
    and (1, 1), respectively.

Constraints:
    - 1 <= N, M <= 500.
    - grid[i][j] == 0 or 1.
    - There is at least one 1 in the grid.

https://www.youtube.com/watch?v=edXdVwkYHF8&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=13
"""

from collections import deque


def distance_of_nearest_cell_having_one(grid: list[list[int]]) -> list[list[int]]:
    """Return each cell's Manhattan distance to the nearest cell containing 1.

    Args:
        grid: A nonempty rectangular binary grid with 1 to 500 rows and
            columns and at least one cell containing 1. These input
            constraints are assumed rather than validated.

    Returns:
        A new matrix of the same shape containing the minimum distances.
        Cells containing 1 have distance 0. The input grid is not modified.

    Approach:
        Multi-source Breadth-First Search (BFS).
        1. Read the dimensions, initialize distances to -1, and create a
           FIFO queue. A distance of -1 also means the cell is undiscovered,
           so a separate visited matrix is unnecessary.
        2. Scan the entire grid. Enqueue every cell containing 1 and set its
           distance to 0 before traversal begins. All ones are simultaneous
           sources, so the search finds the nearest one, not merely the
           first one in scan order.
        3. Define the four horizontal and vertical moves. Each move costs
           one; without obstacles, the shortest such path has length
           |row1 - row2| + |col1 - col2|, the Manhattan distance.
        4. Remove the oldest coordinate pair and read its distance from the
           result matrix. FIFO processing explores cells in nondecreasing
           distance from the set of sources.
        5. Examine its four neighbors. Ignore coordinates outside the grid
           and cells whose distance is already assigned. This also excludes
           every source cell because its distance was initialized to 0.
        6. Enqueue each undiscovered neighbor and assign the current distance
           plus one in the same iteration, before another cell is processed.
           This prevents duplicate discovery. The first arrival is shortest:
           any shorter route would have reached it from an earlier BFS layer.
        7. Return the distance matrix when the queue is empty. Since there is
           at least one source and no blocked cells, every cell is reachable
           and no -1 entries remain. A single-cell grid [[1]] returns [[0]];
           an all-ones grid returns all zeros.

    Time Complexity:
        O(N * M), where N and M are the row and column counts. Initializing
        distances and scanning for sources each take O(N * M). Each cell is
        enqueued and dequeued once, using O(1) deque operations, and examines
        exactly four candidate neighbors. The total traversal is O(N * M).

    Space Complexity:
        O(N * M) for the returned distances matrix and up to N * M coordinate
        pairs in the queue. Even excluding the output, auxiliary space is
        O(N * M): an all-ones grid initially enqueues every cell. delta_list
        contains four fixed moves, and dimensions, coordinates, and distance
        variables use O(1) space. There is no recursive call stack or separate
        visited matrix.
    """
    # 1. Use -1 distances to track undiscovered cells and create the BFS queue.
    row_size: int = len(grid)
    col_size: int = len(grid[0])

    distances: list[list[int]] = [[-1] * col_size for _ in range(row_size)]
    queue: deque[tuple[int, int, int]] = deque()

    # 2. Initialize every one as a source at distance zero before running BFS.
    for row_index in range(row_size):
        for col_index in range(col_size):
            if grid[row_index][col_index] == 1:
                queue.append((row_index, col_index))
                distances[row_index][col_index] = 0

    # 3. Each horizontal or vertical move adds one to the distance.
    delta_list: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        # 4. Process the oldest cell and look up its assigned distance.
        row_index, col_index = queue.popleft()
        current_distance = distances[row_index][col_index]

        # 5. Consider only in-bounds neighbors that are still undiscovered.
        for row_delta, col_delta in delta_list:
            new_row: int = row_index + row_delta
            new_col: int = col_index + col_delta

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and distances[new_row][new_col] == -1
            ):
                # 6. Assign distance on enqueue so no later cell adds it again.
                queue.append((new_row, new_col))
                distances[new_row][new_col] = current_distance + 1

    # 7. All cells now contain their shortest distance to any source.
    return distances


def solve() -> None:
    grid: list[list[int]] = [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]]
    expected: list[list[int]] = [[1, 0, 0, 1], [0, 0, 1, 1], [1, 1, 0, 0]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2.
    grid: list[list[int]] = [[1, 0, 1], [1, 1, 0], [1, 0, 0]]
    expected: list[list[int]] = [[0, 1, 0], [0, 0, 1], [0, 1, 2]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum dimensions: the only cell is one.
    grid: list[list[int]] = [[1]]
    expected: list[list[int]] = [[0]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-by-two grid with equally near sources.
    grid: list[list[int]] = [[0, 1], [1, 0]]
    expected: list[list[int]] = [[1, 0], [0, 1]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row: source at the beginning.
    grid: list[list[int]] = [[1, 0, 0, 0, 0]]
    expected: list[list[int]] = [[0, 1, 2, 3, 4]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row: source in the middle.
    grid: list[list[int]] = [[0, 0, 1, 0, 0]]
    expected: list[list[int]] = [[2, 1, 0, 1, 2]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row: source at the end.
    grid: list[list[int]] = [[0, 0, 0, 0, 1]]
    expected: list[list[int]] = [[4, 3, 2, 1, 0]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column: source at the top.
    grid: list[list[int]] = [[1], [0], [0], [0], [0]]
    expected: list[list[int]] = [[0], [1], [2], [3], [4]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column: source in the middle.
    grid: list[list[int]] = [[0], [0], [1], [0], [0]]
    expected: list[list[int]] = [[2], [1], [0], [1], [2]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column: source at the bottom.
    grid: list[list[int]] = [[0], [0], [0], [0], [1]]
    expected: list[list[int]] = [[4], [3], [2], [1], [0]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide rectangle: source at the top-right corner.
    grid: list[list[int]] = [[0, 0, 0, 1], [0, 0, 0, 0]]
    expected: list[list[int]] = [[3, 2, 1, 0], [4, 3, 2, 1]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall rectangle: source at the bottom-left corner.
    grid: list[list[int]] = [[0, 0], [0, 0], [0, 0], [1, 0]]
    expected: list[list[int]] = [[3, 4], [2, 3], [1, 2], [0, 1]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Interior source: diagonals require two moves.
    grid: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    expected: list[list[int]] = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Competing sources: the later source is closer to some cells.
    grid: list[list[int]] = [[1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
    expected: list[list[int]] = [[0, 1, 2, 2, 1], [1, 2, 2, 1, 0], [2, 3, 3, 2, 1]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One zero surrounded by ones.
    grid: list[list[int]] = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    expected: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Checkerboard: multiple sources and equal-distance arrivals.
    grid: list[list[int]] = [[(r + c) % 2 for c in range(6)] for r in range(4)]
    expected: list[list[int]] = [[1 - (r + c) % 2 for c in range(6)] for r in range(4)]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width with minimum height.
    grid: list[list[int]] = [[1] + [0] * 499]
    expected: list[list[int]] = [list(range(500))]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height with minimum width.
    grid: list[list[int]] = [[0] for _ in range(499)] + [[1]]
    expected: list[list[int]] = [[499 - r] for r in range(500)]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: all cells are ones.
    grid: list[list[int]] = [[1] * 500 for _ in range(500)]
    expected: list[list[int]] = [[0] * 500 for _ in range(500)]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: one top-left source; maximum distance is 998.
    grid: list[list[int]] = [[1] + [0] * 499] + [[0] * 500 for _ in range(499)]
    expected: list[list[int]] = [[r + c for c in range(500)] for r in range(500)]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum dimensions: one bottom-right source.
    grid: list[list[int]] = [[0] * 500 for _ in range(499)] + [[0] * 499 + [1]]
    expected: list[list[int]] = [[998 - r - c for c in range(500)] for r in range(500)]
    result: list[list[int]] = distance_of_nearest_cell_having_one(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
