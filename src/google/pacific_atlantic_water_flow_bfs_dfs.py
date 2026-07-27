"""
417. Pacific Atlantic Water Flow

There's an m x n rectangular island bordering both the Pacific Ocean and the
Atlantic Ocean. The Pacific touches the island's left and top edges; the
Atlantic touches the island's right and bottom edges.

The island is divided into a grid of square cells. You're given an m x n
integer matrix heights, where heights[r][c] represents the height above sea
level at cell (r, c).

Rain falls on the island, and water can flow from a cell to a neighboring
cell to its north, south, east, or west, only if the neighboring cell's
height is less than or equal to the current cell's height. Water can flow
from any cell adjacent to an ocean directly into that ocean.

Return a 2D list result, where result[i] = [r_i, c_i] means rain water
starting at cell (r_i, c_i) can reach both the Pacific and Atlantic oceans.

References:
  https://www.youtube.com/watch?v=pDvvDvgHUKE
  https://www.youtube.com/watch?v=s-VkcjHqkGI
"""

from collections import deque


def pacific_atlantic_water_flow_bfs(grid: list[list[int]]) -> list[tuple[int, int]]:
    """
    Approach — reverse BFS from ocean borders:
    Instead of simulating water flowing downhill from every cell (expensive),
    we reverse the problem: start BFS from the ocean borders and flow uphill
    (to equal or higher cells). Any cell reachable from the Pacific border AND
    reachable from the Atlantic border is in the answer.

    Complexity:
      Time:  O(R * C) — every cell is visited at most twice (once per ocean BFS).
      Space: O(R * C) — the pacific and atlantic sets each hold at most R*C
             coordinates, and the queue holds at most R*C entries at peak.
    """
    rows: int = len(grid)
    cols: int = len(grid[0])
    queue: deque[list[int, int]] = deque([])

    pacific: set[tuple[int, int]] = set()
    atlantic: set[tuple[int, int]] = set()

    # Step 1: Seed the Pacific BFS from its two borders —
    # the entire top row (row 0) and the entire left column (col 0).
    for col in range(cols):
        if (0, col) not in pacific:
            queue.append((0, col))
            pacific.add((0, col))

    for row in range(rows):
        if (row, 0) not in pacific:
            queue.append((row, 0))
            pacific.add((row, 0))

    # Step 2: BFS uphill from Pacific borders.
    # A neighbour is reachable from the Pacific if its height >= current cell's
    # height (water can flow downhill from neighbour to current, so reverse:
    # we walk uphill to find all cells that can drain here).
    while queue:
        row, col = queue.popleft()
        for r, c in [[row, col + 1], [row, col - 1], [row + 1, col], [row - 1, col]]:
            if 0 <= r < rows and 0 <= c < cols:
                if (r, c) not in pacific:
                    if grid[r][c] >= grid[row][col]:
                        queue.append((r, c))
                        pacific.add((r, c))

    # Step 3: Seed the Atlantic BFS from its two borders —
    # the entire bottom row (row rows-1) and the entire right column (col cols-1).
    for col in range(cols):
        if (rows - 1, col) not in atlantic:
            queue.append((rows - 1, col))
            atlantic.add((rows - 1, col))

    for row in range(rows):
        if (row, cols - 1) not in atlantic:
            queue.append((row, cols - 1))
            atlantic.add((row, cols - 1))

    # Step 4: BFS uphill from Atlantic borders — same logic as Pacific.
    while queue:
        row, col = queue.popleft()

        for r, c in [[row, col + 1], [row, col - 1], [row + 1, col], [row - 1, col]]:
            if 0 <= r < rows and 0 <= c < cols:
                if (r, c) not in atlantic:
                    if grid[r][c] >= grid[row][col]:
                        queue.append((r, c))
                        atlantic.add((r, c))

    # Step 5: The answer is the intersection — cells reachable from both oceans.
    return list(pacific & atlantic)


def pacific_atlantic_water_flow_dfs(grid: list[list[int]]) -> list[tuple[int, int]]:
    """
    Approach — reverse DFS from ocean borders:
    Same idea as BFS: instead of flowing downhill from every cell, we reverse
    the problem and DFS uphill from each ocean's border cells. Any cell marked
    reachable from both the Pacific and Atlantic borders is in the answer.

    Complexity:
      Time:  O(R * C) — every cell is visited at most twice (once per ocean DFS).
      Space: O(R * C) — the pacific and atlantic sets each hold at most R*C
             coordinates, and the recursion stack is at most R*C frames deep
             in the worst case.
    """
    rows, cols = len(grid), len(grid[0])
    pacific: set[tuple[int, int]] = set()
    atlantic: set[tuple[int, int]] = set()

    def dfs(row: int, col: int, visited: set[tuple[int, int]], prev_height: int):
        # Base case: out of bounds, already visited, or water can't flow uphill
        # to this cell from the previous cell (prev_height > current height means
        # water would have to flow uphill in the forward direction, which is invalid).
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or prev_height > grid[row][col]
            or (row, col) in visited
        ):
            return

        # Mark this cell as reachable from the current ocean.
        visited.add((row, col))

        # Recurse uphill in all four directions, passing the current height
        # as the minimum height the next cell must meet.
        dfs(row + 1, col, visited, grid[row][col])
        dfs(row - 1, col, visited, grid[row][col])
        dfs(row, col + 1, visited, grid[row][col])
        dfs(row, col - 1, visited, grid[row][col])

    # Step 1: DFS uphill from Pacific borders —
    # left column (col 0) and top row (row 0).
    for row in range(rows):
        dfs(row, 0, pacific, grid[row][0])

    for col in range(cols):
        dfs(0, col, pacific, grid[0][col])

    # Step 2: DFS uphill from Atlantic borders —
    # right column (col cols-1) and bottom row (row rows-1).
    for row in range(rows):
        dfs(row, cols - 1, atlantic, grid[row][cols - 1])

    for col in range(cols):
        dfs(rows - 1, col, atlantic, grid[rows - 1][col])

    # Step 3: The answer is the intersection — cells reachable from both oceans.
    return list(pacific & atlantic)


def solve():
    grid: list[list[int]] = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    print(
        f"bfs: cells that can flow to both pacific and atlantic are {pacific_atlantic_water_flow_bfs(grid)}"
    )
    print(
        f"dfs: cells that can flow to both pacific and atlantic are {pacific_atlantic_water_flow_dfs(grid)}"
    )


solve()
