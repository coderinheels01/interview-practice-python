"""
Rotting Oranges (LeetCode #994)

A different flavor of BFS: multi-source, grid-based, instead of word/graph-based like Word Ladder.

You're given a grid where each cell is one of:
  0 — empty
  1 — a fresh orange
  2 — a rotten orange

Every minute, any fresh orange adjacent (up/down/left/right, not diagonal) to a rotten orange
becomes rotten too. You need to find the minimum number of minutes until no cell has a fresh
orange left. If it's impossible for some fresh orange to ever rot, return -1.

Example 1:
  Grid:
    2 1 1
    1 1 0
    0 1 1
  Output: 4 (minutes until everything that can rot, does)

Example 2 (impossible):
  Grid:
    2 1 1
    0 1 1
    1 0 1
  Output: -1 (the bottom-left 1 is isolated by 0s — it can never be reached)

Reference: https://www.youtube.com/watch?v=y704fEOx0s0
"""

from collections import deque


def rotten_orange_bfs(
    grid: list[list[int]],
) -> int:
    # BFS queue stores (row, col, minute) tuples — minute tracks the depth/time elapsed
    queue: deque[tuple[int, int, int]] = deque()

    # Count all fresh oranges; we'll decrement this as oranges rot
    fresh: int = 0

    # Tracks the last minute we processed (i.e. the answer when all oranges are rotten)
    depth: int = 0

    # Seed the BFS with every initially rotten orange (multi-source BFS)
    # and count all fresh oranges so we can detect unreachable ones later
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 2:
                # Start BFS from every rotten orange simultaneously at minute 0
                queue.append((i, j, 0))
            elif grid[i][j] == 1:
                # Track how many fresh oranges exist before BFS starts
                fresh += 1

    # Process the BFS level by level (each level = one minute passing)
    while queue:
        # Dequeue the next rotten orange and unpack its position and the minute it rotted
        col, row, depth = queue.popleft()

        # Check the cell directly below (col + 1) — spread rot downward
        if 0 <= col + 1 < len(grid) and grid[col + 1][row] == 1:
            queue.append((col + 1, row, depth + 1))  # enqueue neighbor at next minute
            grid[col + 1][row] = 2  # mark it as rotten so it won't be revisited
            fresh -= 1  # one fewer fresh orange remaining

        # Check the cell directly to the right (row + 1) — spread rot rightward
        if 0 <= row + 1 < len(grid[col]) and grid[col][row + 1] == 1:
            queue.append((col, row + 1, depth + 1))
            grid[col][row + 1] = 2
            fresh -= 1

        # Check the cell directly above (col - 1) — spread rot upward
        if 0 <= col - 1 < len(grid) and grid[col - 1][row] == 1:
            queue.append((col - 1, row, depth + 1))
            grid[col - 1][row] = 2
            fresh -= 1

        # Check the cell directly to the left (row - 1) — spread rot leftward
        if 0 <= row - 1 < len(grid[col]) and grid[col][row - 1] == 1:
            queue.append((col, row - 1, depth + 1))
            grid[col][row - 1] = 2
            fresh -= 1

    # If fresh == 0, all oranges rotted; return the minute the last one rotted
    # If fresh > 0, some oranges were isolated and could never be reached → return -1
    return depth if fresh == 0 else -1


def solve():
    grid: list[list[int]] = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    print(
        f"numbers of times to rot all fresh oranges in grid {grid} is {rotten_orange_bfs(grid)}"
    )


solve()
