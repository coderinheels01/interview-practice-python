"""
Shortest Path in a Grid with budget Elimination

Topic: Graph traversal, state management

You're given an m x n grid where each cell is either 0 (empty) or 1
(budget). You start at (0, 0) and want to reach (m - 1, n - 1), moving
up, down, left, or right.

You can eliminate at most k budgets. Walking through an budget cell uses
one elimination.

Return the minimum number of steps needed to reach the bottom-right corner,
or -1 if it is impossible.

Examples:

    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]
    k = 1
    Output: 6

    Eliminate the budget at (3, 1), or take a similar route. The path takes
    6 steps.

    grid = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 0, 0],
    ]
    k = 1
    Output: -1

    One elimination is not enough to reach the destination.

Constraints:
    - 1 <= m, n <= 40
    - 0 <= k <= m * n
    - grid[0][0] == 0
    - grid[m - 1][n - 1] == 0
"""

from collections import deque


# Approach: Breadth-First Search (BFS)
#
# Treat each BFS state as (row, column, steps, budgets_remaining). The same
# cell may be visited more than once when reached with a different number of
# eliminations remaining, because those states can lead to different outcomes.
# BFS explores states in increasing order of steps, so the first time the
# destination is removed from the queue, its step count is the shortest path.
#
# Steps:
#   1. Add the starting state (0, 0, 0, k) to the queue and visited set.
#   2. Remove the next state from the front of the queue.
#   3. For each valid neighbor, keep the same number of eliminations if it is
#      empty, or use one elimination if it is an budget.
#   4. Add the neighbor if its complete state has not been visited before.
#   5. Return the step count upon reaching the destination, or -1 if the queue
#      becomes empty.
#
# Complexity:
#   m = number of rows in the grid.
#   n = number of columns in the grid.
#   k = maximum number of budgets that may be eliminated.
#
#   Time:  O(m * n * k), because each cell can be visited with up to k + 1
#          different amounts of remaining budget eliminations.
#   Space: O(m * n * k) for the queue and visited states.
def shortest_path_with_budget_elimination_bfs(grid: list[list[int]], k: int) -> int:
    if grid == [[0]]:
        return 0
    queue: deque[tuple[int, int, int, int]] = deque([(0, 0, 0,k)])
    visited: set[tuple[int, int, int]] = set([(0, 0, k)])
    dist: list[int] = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    n: int = len(grid)
    m: int = len(grid[0])
    
    while queue:
        row, col, count, budget = queue.popleft()
        if row == (n - 1) and col == (m - 1):
            return count
        for d1, d2 in dist:
            new_row = row + d1
            new_col = col + d2
            if 0 <= new_row < n and 0 <= new_col < m:
                if grid[new_row][new_col] == 0 and (new_row, new_col, budget) not in visited:
                    queue.append((new_row, new_col, count +1, budget))
                    visited.add((new_row, new_col, budget))
                elif budget > 0 and (new_row, new_col, budget -1) not in visited:
                    queue.append((new_row, new_col, count +1, budget - 1))
                    visited.add((new_row, new_col, budget - 1))

    return -1


import math


# Approach: Depth-First Search (DFS) with Backtracking
#
# Explore every valid path from the top-left cell to the bottom-right cell.
# Each recursive call tracks the current position, number of steps taken, and
# remaining obstacle-elimination budget. A visited set prevents cycles on the
# current path. After exploring a cell's four neighbors, remove that cell from
# visited so it can be used by a different path. Return the minimum valid path
# length found among the four directions.
#
# Steps:
#   1. Start DFS at (0, 0) with k eliminations and 0 steps used.
#   2. Reject states that are outside the grid or revisit a cell on the current
#      path.
#   3. Subtract the current cell's value from the remaining budget and reject
#      the path if the budget becomes negative.
#   4. Return the current step count when the destination is reached.
#   5. Mark the current cell, recursively explore all four neighbors, and take
#      the minimum result returned by them.
#   6. Remove the current cell from visited to backtrack for other paths.
#   7. Return -1 if every possible path is invalid.
#
# Complexity:
#   m = number of rows in the grid.
#   n = number of columns in the grid.
#   k = maximum number of obstacles that may be eliminated.
#
#   Time:  O(4^(m * n)) in the worst case. A simple path can contain up to
#          m * n cells, and DFS may branch in as many as four directions at
#          each cell. The budget k can prune paths but does not improve the
#          worst case when the grid contains no obstacles.
#   Space: O(m * n) for the recursion stack and current-path visited set.
def shortest_path_with_budget_elimination_dfs(grid: list[list[int]], k: int) -> int:
    n:int = len(grid)
    m:int = len(grid[0])
    row, col = 0, 0
    min_count:int = math.inf
    visited: set[tuple[int, int]]= set()

    def dfs(row:int, col:int, budget:int, count:int) -> int:

        # The position is outside the grid.
        if row < 0 or row >= n or col < 0 or col >= m:
            return math.inf

        # Prevent cycles within the current path.
        if (row, col) in visited:
            return math.inf

        # Entering an obstacle uses one elimination.
        budget -= grid[row][col]

        # This path used too many eliminations.
        if budget < 0:
            return math.inf

        # The destination was reached.
        if row == n - 1 and col == m - 1:
            return count

        visited.add((row, col))

        up_result = dfs(row+1, col, budget, count +1)
        down_result = dfs(row-1, col, budget, count+1)
        right_result = dfs(row, col+1, budget, count+1)
        left_result = dfs(row, col-1, budget, count+1)

        visited.remove((row, col))

        return min(up_result, down_result, right_result, left_result)


    min_count = dfs(0, 0, k, 0)

    return -1 if min_count == math.inf else min_count



def solve() -> None:
    grid = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]
    k = 1
    print(f"shortest path for grid {grid} with {k} budgets is {shortest_path_with_budget_elimination_bfs(grid, k)}")  # Expected: -1
    print(f"shortest path for grid {grid} with {k} budgets is {shortest_path_with_budget_elimination_dfs(grid, k)}")  # Expected: -1

    grid = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 0, 0],
    ]
    k = 1
    print(f"shortest path for grid {grid} with {k} budgets is {shortest_path_with_budget_elimination_bfs(grid, k)}")  # Expected: -1
    print(f"shortest path for grid {grid} with {k} budgets is {shortest_path_with_budget_elimination_dfs(grid, k)}")  # Expected: -1


if __name__ == "__main__":
    solve()
