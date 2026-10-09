"""401. Path with Minimum Effort

A hiker is preparing for an upcoming hike. Given heights, a 2D array of
size rows x columns, heights[row][col] represents the height of that cell.
The hiker starts at the top-left cell (0, 0) and wants to reach the
bottom-right cell (rows - 1, columns - 1), using zero-based coordinates.
The hiker can move up, down, left, or right.

A route's effort is the maximum absolute difference in heights between
two consecutive cells along the route. Return the minimum effort required
to travel from the top-left cell to the bottom-right cell.

Example 1:
    Input: heights = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    Output: 2
    Explanation:
        The route with heights [1, 3, 5, 3, 5] has a maximum absolute
        difference of 2 between consecutive cells. This is better than
        the route [1, 2, 2, 2, 5], whose maximum difference is 3.

Example 2:
    Input: heights = [[1, 2, 3], [3, 8, 4], [5, 3, 5]]
    Output: 1
    Explanation:
        The route with heights [1, 2, 3, 4, 5] has a maximum absolute
        difference of 1 between consecutive cells. This is better than
        the route [1, 3, 5, 3, 5].

Now Your Turn:
    Input:
        heights = [[1, 2, 1, 1, 1],
                   [1, 2, 1, 2, 1],
                   [1, 2, 1, 2, 1],
                   [1, 2, 1, 2, 1],
                   [1, 1, 1, 2, 1]]
    Pick the correct output:
        A. 1
        B. 0
        C. 2
        D. 3

Constraints:
    - rows == len(heights).
    - columns == len(heights[i]).
    - 1 <= rows, columns <= 100.
    - 1 <= heights[i][j] <= 10**6.

https://www.youtube.com/watch?v=0ytpZyiZFhA&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=37

"""

import heapq


def path_with_minimum_effort(heights: list[list[int]]) -> int:
    """Return the minimum route effort from top-left to bottom-right.

    Args:
        heights: A nonempty rectangular grid with 1 <= rows, columns <= 100
            and integer heights between 1 and 10**6. Movement is allowed
            up, down, left, and right; every cell is traversable.

    Returns:
        The smallest possible maximum absolute height difference between
        consecutive cells on a route. A single-cell grid requires effort 0.
        The input grid is not modified.

    Approach:
        Dijkstra's Algorithm adapted to minimize the largest edge cost on
        a path. Each cell is a vertex; an edge's cost is the absolute height
        difference between adjacent cells. A path's cost combines edges
        using max instead of addition.

        1. Initialize the best-effort matrix to 10**9, a sentinel larger
           than any allowed height difference. Set the source effort to 0
           and seed a min heap with (0, 0, 0). Heap entries contain
           (route effort, row, column), so the lowest effort is popped first.
        2. Pop the lowest-effort entry. If its effort exceeds the cell's
           recorded best effort, skip it: a better route was discovered
           after this entry was pushed, and the old entry is now stale.
        3. If this cell is the destination, return its effort. Extending a
           route with max cannot decrease its effort. Therefore, processing
           the lowest available effort finalizes that cell's minimum effort,
           making it safe to return when the destination is popped.
        4. Inspect each in-bounds orthogonal neighbor. Calculate the absolute
           difference between the current and neighboring heights, then take
           max(current route effort, height difference). This preserves the
           largest jump along the entire candidate route.
        5. Compare the candidate effort with the neighbor's recorded best.
           Only if it is strictly smaller, update the matrix and push the
           candidate onto the heap. max measures one route; this comparison
           minimizes effort across competing routes. Equal-effort cycles
           do not create new entries.
        6. If the loop ends, return the destination's recorded effort as a
           fallback. Under the stated constraints, the rectangular grid is
           connected, so the destination is reached and returned in step 3.

    Time Complexity:
        O(V log V), where V = rows * columns (O(1) for a single cell).
        The grid has O(V) edges because each cell has at most four neighbors.
        Matrix initialization costs O(V). Each cell's neighbors are expanded
        once from its finalized entry; stale entries are skipped. There are
        O(V) heap pushes and pops, each costing at most O(log V).

    Space Complexity:
        O(V) extra space. The best-effort matrix stores V entries, and the
        heap can contain O(V) entries, including stale ones. The direction
        list and loop variables use O(1) space. The input is not copied.
    """
    # 1. Initialize best efforts and seed the heap with the starting cell.
    row_size: int = len(heights)
    col_size: int = len(heights[0])
    min_effort_heap: list[tuple[int, int, int]] = [(0, 0, 0)]
    min_effort_matrix: list[list[int]] = [[10**9] * col_size for _ in range(row_size)]
    min_effort_matrix[0][0] = 0
    delta: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while min_effort_heap:
        # 2. Pop the lowest effort and skip entries superseded by better routes.
        effort, row, col = heapq.heappop(min_effort_heap)

        if effort > min_effort_matrix[row][col]:
            continue
        # 3. A non-stale destination entry gives the minimum possible effort.
        if row == row_size - 1 and col == col_size - 1:
            return effort

        # 4. Extend the route to each valid neighbor, retaining its largest jump.
        for row_delta, col_delta in delta:
            new_row: int = row + row_delta
            new_col: int = col + col_delta

            if 0 <= new_row < row_size and 0 <= new_col < col_size:
                new_effort: int = max(
                    effort, abs(heights[new_row][new_col] - heights[row][col])
                )

                # 5. Queue only routes that improve the neighbor's best effort.
                if new_effort < min_effort_matrix[new_row][new_col]:
                    min_effort_matrix[new_row][new_col] = new_effort
                    heapq.heappush(
                        min_effort_heap,
                        (new_effort, new_row, new_col),
                    )

    # 6. Fallback; valid inputs reach the destination inside the loop.
    return min_effort_matrix[row_size - 1][col_size - 1]


def solve() -> None:
    heights: list[list[int]] = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
    expected: int = 2
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum grid and minimum height.
    heights: list[list[int]] = [[1]]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single cell at maximum height still needs no effort.
    heights: list[list[int]] = [[10**6]]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One horizontal ascending move at the maximum difference.
    heights: list[list[int]] = [[1, 10**6]]
    expected: int = 999999
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One horizontal descending move uses the absolute difference.
    heights: list[list[int]] = [[10**6, 1]]
    expected: int = 999999
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One vertical ascending move.
    heights: list[list[int]] = [[1], [7]]
    expected: int = 6
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One vertical descending move.
    heights: list[list[int]] = [[7], [1]]
    expected: int = 6
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest jump at the beginning of a single row.
    heights: list[list[int]] = [[1, 10, 11, 12]]
    expected: int = 9
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest jump in the middle of a single row.
    heights: list[list[int]] = [[1, 2, 12, 13]]
    expected: int = 10
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Largest jump at the end of a single row.
    heights: list[list[int]] = [[1, 2, 3, 20]]
    expected: int = 17
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Route effort is a maximum, not a sum.
    heights: list[list[int]] = [[1, 3, 5, 7]]
    expected: int = 2
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal heights and multiple equal-effort routes.
    heights: list[list[int]] = [[7, 7, 7], [7, 7, 7]]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    heights: list[list[int]] = [[1, 2, 3], [3, 8, 4], [5, 3, 5]]
    expected: int = 1
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: a winding zero-effort route requires upward moves.
    heights: list[list[int]] = [
        [1, 2, 1, 1, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 1, 1, 2, 1],
    ]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A later route improves a previously discovered cell.
    heights: list[list[int]] = [[1, 10, 6], [3, 5, 6]]
    expected: int = 2
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First discovery of the destination is not necessarily optimal.
    heights: list[list[int]] = [[1, 2], [5, 10]]
    expected: int = 5
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # High interior peak can be avoided.
    heights: list[list[int]] = [[1, 1, 1], [1, 10**6, 1], [1, 1, 1]]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal endpoint heights do not allow diagonal shortcuts.
    heights: list[list[int]] = [[1, 100], [100, 1]]
    expected: int = 99
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A winding low route requires a leftward move.
    heights: list[list[int]] = [
        [1, 1, 1, 9, 9],
        [9, 9, 1, 9, 9],
        [1, 1, 1, 9, 9],
        [1, 9, 9, 9, 9],
        [1, 1, 1, 1, 1],
    ]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width and minimum height.
    heights: list[list[int]] = [list(range(1, 101))]
    expected: int = 1
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height and minimum width.
    heights: list[list[int]] = [[height] for height in range(100, 0, -1)]
    expected: int = 1
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid, all minimum heights.
    heights: list[list[int]] = [[1] * 100 for _ in range(100)]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid, all maximum heights.
    heights: list[list[int]] = [[10**6] * 100 for _ in range(100)]
    expected: int = 0
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with a gradual slope in both directions.
    heights: list[list[int]] = [
        [1 + row + col for col in range(100)] for row in range(100)
    ]
    expected: int = 1
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with alternating extreme heights.
    heights: list[list[int]] = [
        [1 if (row + col) % 2 == 0 else 10**6 for col in range(100)]
        for row in range(100)
    ]
    expected: int = 999999
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum grid with an unavoidable high barrier.
    heights: list[list[int]] = [[10**6 if row == 50 else 1] * 100 for row in range(100)]
    expected: int = 999999
    result: int = path_with_minimum_effort(heights)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
