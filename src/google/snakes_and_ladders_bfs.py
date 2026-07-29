"""
Snakes and Ladders (LeetCode #909)

You have an n x n board, numbered 1 to n² in a "boustrophedon" (snaking)
pattern — starting at the bottom-left corner, the bottom row goes
left-to-right, the row above it goes right-to-left, alternating direction
each row as you go up.

Some squares have a snake or ladder: board[row][col] is either -1 (nothing
there) or another square number (a destination). If you land on a square
with a value other than -1, you're immediately moved to that destination
square instead.

You start on square 1. Each turn, you roll a die and can move forward 1 to
6 squares. Return the minimum number of dice rolls needed to reach square
n², or -1 if it's impossible.

Approach: BFS
  Treat each square as a node. BFS explores squares in order of dice rolls
  taken, so the first time we reach square n² is guaranteed to be the minimum.

Time Complexity:  O(n²)
  There are n² squares on the board. Each square is enqueued and processed
  at most once. For each square we try at most 6 die outcomes, so the total
  work is O(6 * n²) = O(n²).

Space Complexity: O(n²)
  The visited set and the BFS queue each hold at most n² entries.

Reference: https://www.youtube.com/watch?v=6lH4nO3JfLk
"""

from collections import deque


def snakes_and_ladders_bfs(board: list[list[int]]):
    n: int = len(board)

    # BFS queue holds (square_number, dice_rolls_so_far).
    # We start on square 1 with 0 rolls taken.
    queue: deque[tuple[int, int]] = deque([(1, 0)])

    # Track visited squares to avoid re-processing the same square
    # through a different path (BFS guarantees we reach it with the
    # fewest rolls the first time).
    visited: set[int] = set()

    # The board is given with row 0 at the top, but square 1 is at the
    # bottom-left. Reversing puts row 0 at the bottom so that square
    # numbering aligns with normal index arithmetic.
    board.reverse()

    def get_row_col_index(value: int) -> tuple[int, int]:
        # Convert a 1-based square number to (row, col) board indices.

        # Which row from the bottom (0-indexed) does this square fall on?
        row: int = (value - 1) // n

        # Position within that row, left-to-right on even rows.
        col: int = (value - 1) % n

        # Odd rows run right-to-left (boustrophedon pattern), so mirror
        # the column index for those rows.
        if row % 2:
            col = n - 1 - col

        return [row, col]

    while queue:
        value, count = queue.popleft()

        # Try all six possible die outcomes from the current square.
        for i in range(1, 7):
            next_value = value + i

            # Skip squares beyond the board boundary.
            if next_value > n * n:
                break

            # Look up the board cell for this landing square.
            row, col = get_row_col_index(value=next_value)

            # If the cell has a snake or ladder, teleport immediately.
            if board[row][col] != -1:
                next_value = board[row][col]

            # Reached the last square — return the roll count.
            if next_value == n * n:
                return count + 1

            # Only enqueue squares we haven't visited yet.
            if next_value not in visited:
                visited.add(next_value)
                queue.append((next_value, count + 1))

    # All reachable squares exhausted without reaching n² — impossible.
    return -1


def solve():
    board: list[list[int]] = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ]
    print(f"minimum moves {snakes_and_ladders_bfs(board)}")


solve()
