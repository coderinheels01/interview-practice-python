"""
Number of Distinct Islands (Medium - Graphs / DFS + Hashing)

You're given an m x n binary matrix grid. An island is a group of 1s connected
4-directionally. Two islands are considered the same if one can be translated
(shifted, with no rotation or reflection) to exactly overlap the other.

Return the number of distinct islands.

Example 1:
    Input:
        grid = [[1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1]]

    Output: 1

    Explanation: Both islands are the same 2x2 square.

Example 2:
    Input:
        grid = [[1, 1, 0, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 0, 1, 1]]

    Output: 3

Constraints:
    - 1 <= m, n <= 50
    - grid[i][j] is either 0 or 1

Approach - DFS with normalized coordinates:
    Scan every cell in the grid. When land is found, use DFS to visit the
    entire island. Record each island cell as an offset from the first cell of
    that island instead of using its absolute grid position. This normalizes
    translated copies of the same shape to the same set of coordinates.

    Convert the normalized coordinates to a frozenset so the shape is hashable
    and can be stored in a set. The number of entries in that set is the number
    of distinct island shapes. Rotation and reflection are not normalized, so
    they correctly remain different shapes.

Complexity (m = rows, n = columns):
    Time:  O(m * n) - each grid cell is scanned and each land cell is fully
           explored by DFS at most once.
    Space: O(m * n) - the visited cells, stored island shapes, and recursion
           stack can each contain up to m * n coordinates in the worst case.
"""


def number_of_distinct_island_coordiatess(grid: list[list[int]]) -> int:
    # Step 1: Handle an empty grid before accessing its first row.
    if not grid:
        return -1

    # Step 2: Track land cells already explored by a previous DFS.
    visited: set[tuple[int, int]] = set()

    # Step 3: Define the four allowed directions: right, left, down, and up.
    dists:list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Store hashable, normalized representations of all unique island shapes.
    distinct_island_coordiatess:set[frozenset[tuple[int, int]]] = set()

    # Save the grid dimensions for neighbor bounds checking during DFS.
    n:int = len(grid)
    k:int = len(grid[0])

    count: int = 0

    def dfs(row:int, col:int, start:int, end:int, island_coordiates: set[tuple[int, int]]):
        # Step 4: Record this cell's position relative to the island's origin.
        if (row, col) not in visited:
            island_coordiates.add((start, end))

        # Mark the cell visited so it is not explored again.
        visited.add((row, col))

        # Step 5: Explore every valid, connected, unvisited land neighbor.
        for d1, d2 in dists:
            new_row:int = row + d1
            new_col:int = col + d2

            # Apply the same movement to the normalized coordinates.
            new_start:int = start + d1
            new_end:int = end + d2

            if 0 <= new_row < n and 0 <= new_col < k and  grid[new_row][new_col] == 1 and (new_row, new_col) not in visited:
                dfs(new_row, new_col, new_start, new_end, island_coordiates)
        
                
    # Step 6: Scan the grid for the starting cell of every island.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                # Start each island at relative coordinate (0, 0).
                island_coordiates:set[tuple[int, int]] = set()
                dfs(i, j, 0, 0, island_coordiates)

                # Step 7: Freeze the coordinates so the shape can enter a set.
                shape: frozenset[tuple[int, int]] = frozenset(island_coordiates)

                # Count the shape only when it is nonempty and not seen before.
                if shape not in distinct_island_coordiatess and shape:
                    distinct_island_coordiatess.add(shape)
                    count += 1

    

    # Step 8: Return the number of unique normalized island shapes.
    return count




def solve():
    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    print(
        f"expected distinct island_coordiatess = 1, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

    grid = [
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
    ]
    print(
        f"expected distinct island_coordiatess = 3, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

    grid = [[0, 0], [0, 0]]
    print(
        f"expected distinct island_coordiatess = 0, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

    grid = [[1, 1, 1], [1, 1, 1]]
    print(
        f"expected distinct island_coordiatess = 1, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

    grid = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    print(
        f"expected distinct island_coordiatess = 1, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

    grid = [
        [1, 1, 0, 1, 0],
        [1, 0, 0, 1, 1],
    ]
    print(
        f"expected distinct island_coordiatess = 2, "
        f"result = {number_of_distinct_island_coordiatess(grid)}"
    )

solve()
