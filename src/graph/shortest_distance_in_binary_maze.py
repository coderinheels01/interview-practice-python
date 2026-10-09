"""304. Shortest Distance in a Binary Maze

Given an n x m matrix grid where each cell contains either 0 or 1,
determine the shortest distance between a source cell and a destination
cell. You can move to an adjacent cell (up, down, left, or right) if that
adjacent cell has a value of 1. The path can only contain cells with value 1.

Return the minimum number of moves from source to destination. If the
destination is unreachable, return -1. Cell coordinates use [row, column].

Example 1:
    Input:
        grid = [[1, 1, 1, 1],
                [1, 1, 0, 1],
                [1, 1, 1, 1],
                [1, 1, 0, 0],
                [1, 0, 0, 1]]
        source = [0, 1]
        destination = [2, 2]
    Output: 3
    Explanation:
        Move down from (0, 1) to (1, 1), down to (2, 1), then right
        to (2, 2). The shortest distance is 3.

Example 2:
    Input:
        grid = [[1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 1, 0, 1]]
        source = [0, 0]
        destination = [3, 4]
    Output: -1
    Explanation:
        No path exists between the source and destination cells.

Now Your Turn:
    Input: grid = [[1, 0, 1], [1, 1, 0], [1, 1, 1]],
           source = [0, 0], destination = [2, 2]
    Pick the correct output:
        A. 3
        B. 2
        C. 5
        D. 4

Constraints:
    - 1 <= n, m <= 500.
    - grid[i][j] is either 0 or 1.
    - Source and destination are always inside the matrix.
    - Source and destination are always traversable:
      grid[source[0]][source[1]] = 1 and
      grid[destination[0]][destination[1]] = 1.

Discussion Questions:
    - Can we use Dijkstra's Algorithm instead of BFS?
    - What if multiple shortest paths exist?
    - What if obstacles could be removed at a cost?
    - What if multiple sources and multiple destinations existed?

https://www.youtube.com/watch?v=U5Mw4eyUmw4&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=36
"""

from collections import deque


def shortest_distance_in_binary_maze(
    grid: list[list[int]], source: list[int], destination: list[int]
) -> int:
    """Return the minimum number of moves between two traversable cells.

    Args:
        grid: A rectangular n x m matrix of zeros (blocked) and ones (open),
            with 1 <= n, m <= 500.
        source: Starting [row, column], within the grid.
        destination: Target [row, column], within the grid.
            Both endpoints are assumed open by the problem constraints.

    Returns:
        The shortest distance in moves, or -1 if no path exists. Returns 0
        when source equals destination. As a defensive check, a blocked
        source returns -1. The grid and coordinate lists are not modified.

    Approach:
        Breadth-First Search (BFS) on an implicit, unweighted graph: each
        open cell is a vertex, and each allowed move has cost 1.

        1. Read the grid dimensions and reject a blocked source.
        2. Initialize a FIFO queue with (0, source row, source column).
           Define the four orthogonal directions. Initialize a separate
           distance matrix to 10**9, marking the source with distance 0.
           This sentinel exceeds any possible shortest path under the
           constraints, since a shortest path needs at most n * m - 1 moves.
        3. Remove the next queued cell. FIFO order processes cells in
           nondecreasing distance, so the first time the destination is
           removed, its distance is the minimum. Return that distance.
        4. Inspect all four neighbors. A candidate must be inside the grid,
           open, and have a recorded distance greater than steps + 1.
           Record its distance before enqueueing it. Because all moves
           cost 1, the first discovery is already shortest; recording it
           immediately prevents later routes from enqueueing it again.
        5. If the queue becomes empty without reaching the destination,
           every reachable cell has been explored, so return -1.

    Time Complexity:
        O(n * m). Initializing the distance matrix visits all n * m cells.
        Each reachable cell is enqueued and dequeued at most once, and each
        examines four neighbors. deque append and popleft are O(1).
        The blocked-source check can return in O(1) before initialization.

    Space Complexity:
        O(n * m) extra space. The distance matrix contains n * m entries,
        and the queue can hold O(n * m) cells. The four direction tuples
        and loop variables use O(1) space. The input grid is not copied.
    """
    # 1. Read the dimensions and reject a blocked starting cell.
    row_size: int = len(grid)
    col_size: int = len(grid[0])

    if grid[source[0]][source[1]] != 1:
        return -1

    # 2. Start BFS at distance zero and mark all other cells as unreached.
    queue: deque[tuple[int, int, int]] = deque([(0, source[0], source[1])])

    delta: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    distances: list[list[int]] = [[10**9] * col_size for _ in range(row_size)]
    distances[source[0]][source[1]] = 0

    # 3. Process cells in increasing distance until the destination is found.
    while queue:
        steps, row, col = queue.popleft()

        if row == destination[0] and col == destination[1]:
            return steps

        # 4. Explore valid neighbors one move farther from the source.
        for row_delta, col_delta in delta:
            new_row = row + row_delta
            new_col = col + col_delta
            new_steps = steps + 1

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and grid[new_row][new_col] == 1
                and distances[new_row][new_col] > new_steps
            ):
                # Mark before enqueueing so another route cannot queue it again.
                distances[new_row][new_col] = new_steps
                queue.append((new_steps, new_row, new_col))

    # 5. Exhausting the queue means the destination is unreachable.
    return -1


def solve() -> None:
    # grid: list[list[int]] = [
    #     [1, 1, 1, 1],
    #     [1, 1, 0, 1],
    #     [1, 1, 1, 1],
    #     [1, 1, 0, 0],
    #     [1, 0, 0, 1],
    # ]
    # source: list[int] = [0, 1]
    # destination: list[int] = [2, 2]
    # expected: int = 3
    # result: int = shortest_distance_in_binary_maze(grid, source, destination)

    # # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum grid; source equals destination.
    grid: list[list[int]] = [[1]]
    source: list[int] = [0, 0]
    destination: list[int] = [0, 0]
    expected: int = 0
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same interior cell, surrounded by obstacles.
    grid: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    source: list[int] = [1, 1]
    destination: list[int] = [1, 1]
    expected: int = 0
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One move right.
    grid: list[list[int]] = [[1, 1]]
    source: list[int] = [0, 0]
    destination: list[int] = [0, 1]
    expected: int = 1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One move left.
    grid: list[list[int]] = [[1, 1]]
    source: list[int] = [0, 1]
    destination: list[int] = [0, 0]
    expected: int = 1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One move down.
    grid: list[list[int]] = [[1], [1]]
    source: list[int] = [0, 0]
    destination: list[int] = [1, 0]
    expected: int = 1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One move up.
    grid: list[list[int]] = [[1], [1]]
    source: list[int] = [1, 0]
    destination: list[int] = [0, 0]
    expected: int = 1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row blocked between endpoints.
    grid: list[list[int]] = [[1, 0, 1]]
    source: list[int] = [0, 0]
    destination: list[int] = [0, 2]
    expected: int = -1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column blocked between endpoints.
    grid: list[list[int]] = [[1], [0], [1]]
    source: list[int] = [2, 0]
    destination: list[int] = [0, 0]
    expected: int = -1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal movement is forbidden.
    grid: list[list[int]] = [[1, 0], [0, 1]]
    source: list[int] = [0, 0]
    destination: list[int] = [1, 1]
    expected: int = -1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: route along the boundary.
    grid: list[list[int]] = [[1, 0, 1], [1, 1, 0], [1, 1, 1]]
    source: list[int] = [0, 0]
    destination: list[int] = [2, 2]
    expected: int = 4
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal shortest routes in an open grid.
    grid: list[list[int]] = [[1] * 3 for _ in range(3)]
    source: list[int] = [0, 0]
    destination: list[int] = [2, 2]
    expected: int = 4
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Destination in the middle of a rectangular grid.
    grid: list[list[int]] = [[1] * 5 for _ in range(3)]
    source: list[int] = [2, 4]
    destination: list[int] = [1, 2]
    expected: int = 3
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Detour initially moves away from destination.
    grid: list[list[int]] = [[1, 0, 1], [1, 0, 1], [1, 1, 1]]
    source: list[int] = [0, 0]
    destination: list[int] = [0, 2]
    expected: int = 6
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second example: unreachable destination with a cyclic source component.
    grid: list[list[int]] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1],
    ]
    source: list[int] = [0, 0]
    destination: list[int] = [3, 4]
    expected: int = -1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width with minimum height.
    grid: list[list[int]] = [[1] * 500]
    source: list[int] = [0, 499]
    destination: list[int] = [0, 0]
    expected: int = 499
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height with minimum width.
    grid: list[list[int]] = [[1] for _ in range(500)]
    source: list[int] = [499, 0]
    destination: list[int] = [0, 0]
    expected: int = 499
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum open grid: opposite corners.
    grid: list[list[int]] = [[1] * 500 for _ in range(500)]
    source: list[int] = [0, 0]
    destination: list[int] = [499, 499]
    expected: int = 998
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid separated by a complete wall.
    grid: list[list[int]] = (
        [[1] * 500 for _ in range(250)] + [[0] * 500] + [[1] * 500 for _ in range(249)]
    )
    source: list[int] = [0, 0]
    destination: list[int] = [499, 499]
    expected: int = -1
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with a long winding corridor.
    grid: list[list[int]] = [
        [1] * 500
        if row % 2 == 0
        else [int(col == (499 if (row // 2) % 2 == 0 else 0)) for col in range(500)]
        for row in range(500)
    ]
    source: list[int] = [0, 0]
    destination: list[int] = [499, 0]
    expected: int = 125249
    result: int = shortest_distance_in_binary_maze(grid, source, destination)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
