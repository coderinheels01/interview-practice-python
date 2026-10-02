"""Number of Distinct Islands

Given a boolean 2D matrix grid of size n x m, find the number of distinct
island shapes. An island is a group of connected 1s, where cells connect
horizontally or vertically. Diagonal cells are not connected.

Two islands have the same shape if one can be translated to match the other
without rotation or reflection. Count each unique shape only once.

Example 1:
    Input: grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    Output: 1
    Explanation: The island in the top-left corner and the island in the
    bottom-right corner are both 2 x 2 squares, so there is one distinct shape.

Additional practice examples (not transcribed from the screenshot):

Example 2:
    Input: grid = [
        [1, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    Output: 2
    Explanation: There are three islands: two horizontal pairs and one single
    cell. The horizontal pairs share a shape, giving two distinct shapes.

Example 3:
    Input: grid = [
        [1, 1, 0, 1],
        [0, 0, 0, 1],
    ]
    Output: 2
    Explanation: A horizontal pair and a vertical pair are different shapes.
    Matching them would require rotation, which is not allowed.

Example 4:
    Input: grid = [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
    ]
    Output: 2
    Explanation: The two L-shaped islands are mirror images. Translation
    alone cannot match them, so they count as two distinct shapes.

Example 5:
    Input: grid = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    Output: 1
    Explanation: Diagonal contact does not connect cells. There are three
    separate single-cell islands, all with the same shape.

Example 6:
    Input: grid = [
        [0, 0, 0],
        [0, 0, 0],
    ]
    Output: 0
    Explanation: There are no land cells, so there are no island shapes.

https://www.youtube.com/watch?v=7zmgQSJghpo&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=16

"""


def number_of_distinct_islands(grid: list[list[int]]) -> int:
    """Count unique island shapes, treating translations as equivalent.

    Args:
        grid: A nonempty rectangular binary matrix with N rows and M columns.
            One represents land and zero represents water. Land cells connect
            horizontally or vertically, not diagonally. The input is assumed
            to satisfy these conditions; it is not validated or modified.

    Returns:
        The number of distinct island shapes. Translated copies count once;
        shapes that require rotation or reflection to match remain distinct.
        An all-water grid returns zero. A single land cell forms one shape.

    Approach:
        Use Depth-First Search (DFS) with relative-coordinate normalization.
        1. Read the dimensions, create a boolean visited matrix, define the
           four movement directions, and create a set of frozen shape sets.
        2. Define recursive DFS to collect one island. Record each cell as
           (row - start_row, col - start_col) relative to a fixed starting
           cell, then mark it visited. Explore only in-bounds, unvisited land
           neighbors, passing the same origin and mutable coordinate set to
           every recursive call. Marking before exploration prevents cycles.
        3. Scan the grid in row-major order. Each unvisited land cell starts
           a new island: create its coordinate set and run DFS from that cell.
           This consistently chooses the leftmost land cell in the island's
           topmost row as its origin. Translated copies therefore produce the
           same relative coordinates. Lower rows may have negative column
           offsets when they extend to the left of the origin.
        4. Convert the completed coordinate set to a frozenset and add it to
           the outer set. A frozenset is immutable and hashable, and its
           equality is independent of traversal order. The outer set ignores
           duplicate shapes automatically. Coordinates are only translated,
           so rotations and reflections are not treated as equivalent unless
           they already produce the same shape by translation alone.
        5. Return the size of the outer set: the number of unique shapes,
           rather than the total number of islands or land cells.

    Time Complexity:
        O(N * M) expected time, assuming average-case hash-set operations.
        Initializing visited and scanning the grid take O(N * M). DFS visits
        each land cell once and checks four neighbors. For an island with K
        cells, creating and initially hashing its frozenset take O(K); equal
        shape comparisons also take O(K) expected time. Summed over islands,
        these costs are O(N * M). Pathological hash collisions can worsen
        hash-set performance. These bounds assume traversal completes.

    Space Complexity:
        O(N * M) auxiliary space. The visited matrix uses O(N * M). The
        current island's coordinate set, its frozen copy, and the recursive
        call stack can each use O(K) for an island of K cells. Stored unique
        shapes contain at most O(N * M) coordinates in total. The four
        directions and other scalar variables use O(1) space outside calls.

    Limitation:
        A large connected island can exceed Python's recursion limit and
        raise RecursionError. Empty and ragged grids are unsupported.
    """
    # 1. Initialize dimensions, visited state, directions, and unique shapes.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    visited: list[list[bool]] = [[False] * col_size for _ in range(row_size)]
    delta_list: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    islands: set[frozenset[tuple[int, int]]] = set()

    # 2. Collect one island as offsets from a fixed starting cell using DFS.
    def dfs(
        row_index: int,
        col_index: int,
        start_row: int,
        start_col: int,
        island: set[tuple[int, int]],
    ) -> None:
        # Record the relative position and mark before exploring neighbors.
        island.add((row_index - start_row, col_index - start_col))
        visited[row_index][col_index] = True

        for row_delta, col_delta in delta_list:
            new_row: int = row_index + row_delta
            new_col: int = col_index + col_delta

            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and not visited[new_row][new_col]
                and grid[new_row][new_col] == 1
            ):
                dfs(
                    row_index=new_row,
                    col_index=new_col,
                    start_row=start_row,
                    start_col=start_col,
                    island=island,
                )

    # 3. Scan in row-major order and explore each previously unseen island.
    for row_index in range(row_size):
        for col_index in range(col_size):
            if grid[row_index][col_index] == 1 and not visited[row_index][col_index]:
                island: set[tuple[int, int]] = set()

                dfs(
                    row_index=row_index,
                    col_index=col_index,
                    start_row=row_index,
                    start_col=col_index,
                    island=island,
                )

                # 4. Freeze the shape so the outer set can deduplicate it.
                islands.add(frozenset(island))

    # 5. Return the number of distinct normalized shapes.
    return len(islands)


def solve() -> None:
    grid: list[list[int]] = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single sea cell.
    grid: list[list[int]] = [
        [0],
    ]
    expected: int = 0
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single land cell.
    grid: list[list[int]] = [
        [1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All sea in a rectangular grid.
    grid: list[list[int]] = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    expected: int = 0
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All land forms one island.
    grid: list[list[int]] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row with repeated and differently sized islands.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    ]
    expected: int = 3
    result: int = number_of_distinct_islands(grid)

    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column with repeated and differently sized islands.
    grid: list[list[int]] = [
        [1],
        [1],
        [0],
        [1],
        [0],
        [1],
        [1],
        [0],
        [1],
        [1],
        [1],
    ]
    expected: int = 3
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated pairs and a singleton from Example 2.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Rotation produces a different shape.
    grid: list[list[int]] = [
        [1, 1, 0, 1],
        [0, 0, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reflection produces a different shape.
    grid: list[list[int]] = [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal singletons are separate but share one shape.
    grid: list[list[int]] = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same L shape translated in both dimensions.
    grid: list[list[int]] = [
        [1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same shape with cells left of its starting column.
    grid: list[list[int]] = [
        [0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal area does not imply equal shape.
    grid: list[list[int]] = [
        [1, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal bounding boxes do not imply equal shape.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A ring and a filled square are distinct.
    grid: list[list[int]] = [
        [1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal contact between different shapes does not merge them.
    grid: list[list[int]] = [
        [1, 1, 0],
        [0, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A one-cell bridge joins two blocks into one island.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching islands at the beginning middle and end.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 1, 0, 1, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Boundary and interior singletons have the same shape.
    grid: list[list[int]] = [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Checkerboard has many islands but only one shape.
    grid: list[list[int]] = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
    ]
    expected: int = 1
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide grid with a pair a singleton and an L shape.
    grid: list[list[int]] = [
        [1, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
    ]
    expected: int = 3
    result: int = number_of_distinct_islands(grid)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
