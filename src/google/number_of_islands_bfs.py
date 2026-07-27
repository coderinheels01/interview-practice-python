"""
Number of Islands (LeetCode #200)

You're given a 2D grid of '1's (land) and '0's (water). An island is a group
of '1's connected horizontally or vertically (not diagonally). Count the
total number of islands.

Example:
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1
  Output: 3
  — the top-left 2×2 block of land is one island, the single 1 in the middle
    is a second island, and the two connected 1s in the bottom-right are a
    third island.

Approach — BFS flood fill:
Scan every cell. When we hit an unvisited '1', we've found a new island.
Increment the counter, then BFS outward from that cell to mark every
connected land cell as visited ("-1"). That way the outer scan never
double-counts cells that belong to the same island.

Complexity:
  Time:  O(R * C) — every cell is enqueued and dequeued at most once.
  Space: O(min(R, C)) — the BFS queue holds at most the cells on the current
         "frontier", which in the worst case (a fully filled grid) is bounded
         by the shorter dimension due to the BFS wavefront shape.
         The visited marker is stored in-place on the grid itself (no extra
         visited set needed), so no additional O(R*C) space is used.
"""

from collections import deque


def number_of_islands_bfs(grid: list[list[str]]) -> int:
    row_len: int = len(grid)
    col_len: int = len(grid[0])

    def bfs(start_row: int, start_col: int) -> None:
        # Step 1: Seed the queue with the land cell that triggered this BFS.
        # This cell has already been marked "-1" by the caller to prevent it
        # from being re-enqueued.
        queue: deque[tuple[int, int]] = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()

            # Step 2: Explore all 4 neighbours (up, down, left, right).
            # Diagonal connections are not considered — islands are only
            # horizontally/vertically connected.
            for i, j in [
                [row, col + 1],  # right
                [row, col - 1],  # left
                [row + 1, col],  # down
                [row - 1, col],  # up
            ]:
                # Step 3: Bounds check — skip cells outside the grid.
                if 0 <= i < row_len and 0 <= j < col_len:
                    if grid[i][j] == "1":
                        # Step 4: Mark the neighbour as visited in-place before
                        # enqueuing. Marking here (not after dequeue) is important:
                        # it prevents the same cell from being added to the queue
                        # multiple times by different neighbours.
                        queue.append((i, j))
                        grid[i][j] = "-1"

    # Step 5: Outer scan — iterate every cell in reading order.
    count: int = 0
    for row in range(row_len):
        for col in range(col_len):
            if grid[row][col] == "1":
                # Step 6: Found an unvisited land cell — it's the entry point of
                # a new island. Increment the counter, mark it visited, then BFS
                # to consume (mark) every other cell in this island.
                count += 1
                grid[row][col] = "-1"
                bfs(row, col)

    # Step 7: All cells processed — return the total island count.
    return count


def solve():
    grid: list[list[str]] = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")

    grid: list[list[str]] = [
        ["1", "1", "1"],
        ["1", "1", "1"],
        ["1", "1", "1"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")

    grid: list[list[str]] = [
        ["0", "0", "0"],
        ["0", "0", "0"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")

    grid: list[list[str]] = [
        ["1", "0", "1", "0", "1"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")

    grid: list[list[str]] = [
        ["1", "1", "0", "1"],
        ["1", "0", "0", "1"],
        ["0", "0", "1", "0"],
        ["1", "0", "0", "1"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")

    grid: list[list[str]] = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"],
    ]
    print(f"number of islands for the grid is {number_of_islands_bfs(grid)}")


solve()
