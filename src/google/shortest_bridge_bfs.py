"""
Shortest Bridge (LeetCode #934)

You are given an n x n binary grid where exactly two islands exist (groups
of 1s connected horizontally/vertically). You may flip any 0 to a 1 to
bridge the two islands. Return the minimum number of 0s you must flip to
connect the two islands into one.

Example:
    grid = [
        [0, 1],
        [1, 0],
    ]
    Output: 1
"""

from collections import deque

"""
Approach: DFS to mark first island + multi-source BFS to reach second island
  Phase 1 — DFS: scan the grid until we find any 1-cell, then DFS to visit
  every cell in that island. Each visited cell is added to `visited` AND
  enqueued so it becomes a BFS source in phase 2.

  Phase 2 — BFS: expand outward from every cell of the first island
  simultaneously (multi-source), crossing 0-cells (water). The moment we
  step onto a 1-cell that belongs to the second island, the current BFS
  level (count) is the minimum bridge length — we return it immediately.

  The key insight: BFS expands level by level, so the first time we reach
  the second island is guaranteed to be via the shortest path.

Time Complexity:  O(n²) — DFS visits each cell at most once; BFS also
                  visits each cell at most once.
Space Complexity: O(n²) — visited set, queue, and DFS call stack can each
                  hold up to n² entries.

Reference: https://www.youtube.com/watch?v=gkINMhbbIbU
"""


def shortest_bridge_bfs(grid: list[list[int]]) -> int:
    queue: deque[tuple[int, int]] = deque()
    n: int = len(grid)
    visited: set[list[tuple[int, int]]] = set()
    directions: list[list[int, int]] = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    def dfs(x: int, y: int):
        # Step 2: Enqueue this cell as a BFS source (distance 0 from island 1)
        # and mark it visited so BFS won't cross back into island 1.
        queue.append((x, y, 0))
        visited.add((x, y))
        # Step 3: Recursively DFS to all connected 1-cells of the same island.
        for d1, d2 in directions:
            new_x, new_y = x + d1, y + d2
            if 0 <= new_x < n and 0 <= new_y < n:
                if grid[new_x][new_y] == 1 and (new_x, new_y) not in visited:
                    dfs(new_x, new_y)

    def bfs():
        # Step 4: Multi-source BFS from every cell of island 1 simultaneously.
        # We expand outward through water (0-cells), counting steps.
        while queue:
            x, y, count = queue.popleft()
            for d1, d2 in directions:
                new_x, new_y = x + d1, y + d2
                if 0 <= new_x < n and 0 <= new_y < n and (new_x, new_y) not in visited:
                    if grid[new_x][new_y] == 0:
                        # Step 5: Still water — keep expanding, incrementing the
                        # bridge length counter.
                        queue.append((new_x, new_y, count + 1))
                    else:
                        # Step 6: Hit a 1-cell that isn't in visited → it belongs
                        # to island 2. Return count as the minimum bridge length.
                        return count

            # Step 7: Mark processed water cells visited to avoid revisiting.
            visited.add((x, y))

    # Step 1: Scan until we find the first 1-cell, then DFS to mark the
    # entire first island and seed the BFS queue with all its cells.
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and (i, j) not in visited:
                dfs(i, j)
                return bfs()

    return 0


def solve():

    grid: list[list[int]] = [[0, 1], [1, 0]]
    # expected: 1
    print(f"shortest path to connect two islands - {shortest_bridge_bfs(grid)}")

    grid: list[list[int]] = [[0, 1, 0], [0, 0, 0], [0, 0, 1]]
    # expected: 2
    print(f"shortest path to connect two islands - {shortest_bridge_bfs(grid)}")

    grid: list[list[int]] = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    # expected: 1
    print(f"shortest path to connect two islands - {shortest_bridge_bfs(grid)}")

    grid: list[list[int]] = [[1, 0], [0, 1]]
    # expected: 1
    print(f"shortest path to connect two islands - {shortest_bridge_bfs(grid)}")

    grid: list[list[int]] = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 1],
    ]
    # expected: 1
    print(f"shortest path to connect two islands - {shortest_bridge_bfs(grid)}")


solve()
