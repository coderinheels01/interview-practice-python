"""
Trapping Rain Water II (LeetCode 407)

You are given an m x n matrix of non-negative integers where each value
height_map[row][column] represents the terrain height at that grid cell.

After rain, water can become trapped in low areas enclosed by higher surrounding
terrain, including the cells along the matrix boundary.

Return the total volume of water trapped across the entire grid.

Example 1:
    Input:
        height_map = [
            [1, 4, 3, 1, 3, 2],
            [3, 2, 1, 3, 2, 4],
            [2, 3, 3, 2, 3, 1],
        ]

    Output:
        4

Constraints:
    - 1 <= m, n <= 200
    - 0 <= height_map[row][column] <= 2 * 10^4
"""

import heapq


def trapping_rain_water_ii(height_map: list[list[int]]) -> int:
    """
    Approach: Priority-Queue Flood Fill (Multi-Source BFS with a Min-Heap)
        1. Treat each grid cell as a node connected to its four orthogonal
           neighbors. Record the grid dimensions, create a visited matrix, and
           use a min-heap ordered by terrain height.
        2. Return 0 when the grid has fewer than three rows or columns because it
           has no interior cells in which water can be enclosed.
        3. Add every boundary cell to the heap and mark it visited. Boundary
           cells cannot trap water because water can escape directly outside the
           grid. Together, they form the initial wall for an inward flood fill.
        4. Remove the lowest-height cell from the heap. Processing the lowest
           exposed boundary first ensures the grid is entered through its
           weakest surrounding wall, similar to Dijkstra's algorithm.
        5. Update water_level to the greater of its current value and the popped
           cell's height. This level never decreases as the flood moves inward.
        6. Examine every unvisited neighbor. If its terrain is below water_level,
           the difference is trapped above that cell. Add the neighbor to the
           heap and mark it visited immediately so it cannot be processed twice.
        7. Continue until the heap is empty, then return the accumulated water.

    Why the Min-Heap Works:
        Water escapes through the lowest surrounding boundary. The min-heap
        always expands the lowest currently exposed boundary first, so when an
        interior cell is reached, the active water_level represents the boundary
        that constrains it. A lower cell behind that boundary holds the
        difference between the boundary level and its own terrain height.

    Time Complexity:
        O(m * n * log(m * n)), where m is the number of rows and n is the number
        of columns. There are m * n cells, and each is marked visited when added,
        so it enters and leaves the heap at most once. Each heap insertion and
        removal costs O(log(m * n)). Examining four neighbors is O(1) per cell,
        so the heap operations determine the overall complexity.

    Space Complexity:
        O(m * n). The visited matrix stores one Boolean per cell, and the heap
        can hold O(m * n) cell entries in the worst case. The four directions
        and remaining scalar variables require only O(1) additional space.

        https://www.youtube.com/watch?v=nmY-NN4p4eI
    """
    # Step 1: Record dimensions and prepare the grid traversal.
    m: int = len(height_map)
    n: int = len(height_map[0])

    # Step 2: Without an interior row and column, no water can be enclosed.
    if m < 3 or n < 3:
        return 0

    visited: list[list[bool]] = [[False] * n for _ in range(m)]
    min_heap: list[tuple[int, int, int]] = []
    directions: list[tuple[int, int]] = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ]
    water_level: int = 0
    body_of_water: int = 0

    # Step 3: Seed the heap with all boundary cells and mark them visited.
    for row in range(m):
        if row == 0 or row == m - 1:
            for col in range(n):
                heapq.heappush(min_heap, (height_map[row][col], row, col))
                visited[row][col] = True
        else:
            heapq.heappush(min_heap, (height_map[row][0], row, 0))
            heapq.heappush(min_heap, (height_map[row][n - 1], row, n - 1))
            visited[row][0] = True
            visited[row][n - 1] = True

    def bfs():
        # Step 7: Continue until every cell exposed by the boundary is processed.
        while min_heap:
            nonlocal water_level, body_of_water

            # Step 4: Expand from the lowest currently exposed boundary.
            current_level, current_row, current_col = heapq.heappop(min_heap)

            # Step 5: The active flood level can rise but never fall.
            water_level = max(water_level, current_level)

            # Step 6: Examine each unvisited orthogonal neighbor.
            for row_delta, col_delta in directions:
                new_row: int = current_row + row_delta
                new_col: int = current_col + col_delta
                if (
                    0 <= new_row < m
                    and 0 <= new_col < n
                    and not visited[new_row][new_col]
                ):
                    # A neighbor below the active level traps the difference.
                    if height_map[new_row][new_col] < water_level:
                        body_of_water += water_level - height_map[new_row][new_col]

                    # Mark when added so no other path can process it again.
                    heapq.heappush(
                        min_heap, (height_map[new_row][new_col], new_row, new_col)
                    )
                    visited[new_row][new_col] = True

    bfs()

    # Step 7: Return the total after the priority flood reaches every cell.
    return body_of_water


def solve() -> None:
    height_map: list[list[int]] = [
        [1, 4, 3, 1, 3, 2],
        [3, 2, 1, 3, 2, 4],
        [2, 3, 3, 2, 3, 1],
    ]
    expected: int = 4
    result: int = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [[5]]
    expected = 0
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [[1, 2, 1]]
    expected = 0
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [
        [2, 2, 2],
        [2, 2, 2],
        [2, 2, 2],
    ]
    expected = 0
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [
        [3, 3, 3],
        [3, 0, 3],
        [3, 3, 3],
    ]
    expected = 3
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [
        [5, 5, 5, 5],
        [5, 1, 2, 5],
        [5, 3, 0, 5],
        [5, 5, 5, 5],
    ]
    expected = 14
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [
        [3, 3, 3, 3],
        [3, 1, 2, 1],
        [3, 3, 3, 3],
    ]
    expected = 1
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    height_map = [
        [3, 3, 3, 3, 3],
        [3, 2, 2, 2, 3],
        [3, 2, 1, 2, 3],
        [3, 2, 2, 2, 3],
        [3, 3, 3, 3, 3],
    ]
    expected = 10
    result = trapping_rain_water_ii(height_map)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


if __name__ == "__main__":
    solve()
