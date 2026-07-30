"""
01 Matrix (LeetCode #542)

Given an m x n binary matrix mat of 0s and 1s, return a matrix of the same
size where each cell contains the distance to the nearest 0. Distance is
measured in steps moving only up, down, left, or right.

Example:
    mat = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 1],
    ]
    Output:
    [
        [0, 0, 0],
        [0, 1, 0],
        [1, 2, 1],
    ]

"""

import math
from collections import deque

"""
Approach: Multi-source BFS
  Like Rotting Oranges, we seed the BFS queue with ALL 0-cells at once,
  then expand outward. Each time we reach a 1-cell for the first time,
  its distance is the current cell's distance + 1. Because BFS explores
  level by level, the first time we reach any cell is guaranteed to be
  via the shortest path.

Time Complexity:  O(m * n) — every cell is enqueued and processed at most once.
Space Complexity: O(m * n) — the queue and visited set can hold all cells.
"""


def zero_one_matrix_bfs(mat: list[list[int]]) -> list[list[int]]:
    n: int = len(mat)
    m: int = len(mat[0])
    queue: deque[list[tuple[int, int, int]]] = deque()
    visited: set[tuple[int, int]] = set([])

    # Step 1: Seed the queue with every 0-cell.
    # These are our "sources" — distance 0 by definition.
    # We start BFS from all of them simultaneously (multi-source BFS).
    for i in range(n):
        for j in range(m):
            if mat[i][j] == 0:
                queue.append((i, j))

    # Step 2: BFS outward from all 0-cells at the same time.
    # Each wave front represents one additional step away from the nearest 0.
    while queue:
        row, col = queue.popleft()

        # Step 3: Explore all four neighbors (up, down, left, right).
        for r, c in [
            [row + 1, col],
            [row - 1, col],
            [row, col + 1],
            [row, col - 1],
        ]:
            # Step 4: Only process neighbors that are:
            #   - within bounds
            #   - not a 0-cell (0-cells are already at distance 0)
            #   - not yet visited (first visit = shortest distance)
            if 0 <= r < n and 0 <= c < m and mat[r][c] != 0 and (r, c) not in visited:
                # Step 5: Distance to this neighbor = parent's distance + 1.
                # We reuse mat in-place to store the result.
                mat[r][c] = mat[row][col] + 1
                queue.append((r, c))
                # Step 6: Mark visited so we never overwrite with a longer path.
                visited.add((r, c))

    # Step 7: mat is now fully updated with shortest distances — return it.
    return mat


"""
Approach: Dijkstra-style relaxation (multi-source, distance-based)
  Instead of a visited set, we initialise every 1-cell to infinity and
  every 0-cell to 0, then relax distances as we expand. A neighbor is
  only re-enqueued when we find a strictly shorter path to it
  (mat[neighbor] > mat[current] + 1). This mirrors Dijkstra's edge-
  relaxation logic: we only update and re-visit a node when we discover
  a better route.

  Note: using a plain deque (FIFO) here rather than a min-heap means this
  is technically BFS-with-relaxation (similar to Bellman-Ford in spirit).
  A true Dijkstra would use heapq to always pop the minimum-distance cell
  first — but because all edge weights are 1, the two approaches produce
  identical results. The visited-set BFS is generally preferred for this
  problem; this variant is shown as a contrast.

Time Complexity:  O(m * n) — each cell can be re-enqueued, but only when
                  a shorter path is found, which happens at most once per cell.
Space Complexity: O(m * n) — for the queue and the in-place distance matrix.

Reference: https://www.youtube.com/watch?v=CTqBOiciqc4
"""


def zero_one_matrix_bfs_with_relaxation(mat: list[list[int]]) -> list[list[int]]:
    queue: deque(tuple[int, int, int]) = deque()
    n: int = len(mat)
    m: int = len(mat[0])

    directions: list[list[int, int]] = [[0, -1], [0, 1], [1, 0], [-1, 0]]

    # Step 1: Initialise distances.
    # 0-cells are sources — distance 0, enqueue them immediately.
    # 1-cells start at infinity so any real path will be shorter.
    for i in range(n):
        for j in range(m):
            if mat[i][j] == 0:
                queue.append((i, j, 0))
            elif mat[i][j] == 1:
                mat[i][j] = math.inf

    # Step 2: Process cells in FIFO order (BFS-with-relaxation).
    # Unlike the visited-set BFS, a cell can be re-enqueued if we later
    # find a shorter path to it.
    while queue:
        row, col, count = queue.popleft()

        # Step 3: Try all four neighbors.
        for x, y in directions:
            if (
                0 <= (row + x) < n
                and 0 <= (col + y) < m
                # Step 4: Relax — only update if the path through (row, col)
                # is strictly shorter than the neighbor's current best distance.
                # We use `count` (carried in the queue tuple) rather than
                # re-reading mat[row][col], which is the standard Dijkstra
                # pattern — the distance is owned by the queue entry, not the cell.
                and mat[row + x][col + y] > count + 1
            ):
                # Step 5: Update the neighbor's distance to the shorter value.
                mat[row + x][col + y] = count + 1
                # Step 6: Re-enqueue the neighbor so its own neighbors can be
                # relaxed with the new, better distance.
                queue.append((row + x, col + y, mat[row + x][col + y]))

    # Step 7: All distances have been relaxed to their minimum — return mat.
    return mat


def solve():
    mat: list[list[int]] = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")
    mat: list[list[int]] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")
    mat: list[list[int]] = [[1, 1, 1], [1, 1, 1], [1, 1, 0]]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")
    mat: list[list[int]] = [[0]]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")
    mat: list[list[int]] = [[0, 1], [1, 1]]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")
    mat: list[list[int]] = [
        [1, 0, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1],
    ]
    print(f"mat with moves {zero_one_matrix_bfs(mat)}")
    print(f"mat with moves {zero_one_matrix_bfs_with_relaxation(mat)}")


solve()
