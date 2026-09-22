"""Rat in a Maze Problem - I

A rat starts at (0, 0) in an n x n square matrix maze and must reach
(n - 1, n - 1). Find all possible paths from the start to the destination.

The rat may move one cell at a time in four directions:
    - 'U': up
    - 'D': down
    - 'L': left
    - 'R': right

A cell containing 0 is blocked and cannot be entered. A cell containing 1
is open and can be traversed. Moves must remain within the matrix.
Within a single path, no cell may be visited more than once.

For this template, return a list of direction strings, one per valid path.
Return an empty list if no path exists. Output order is unrestricted.
The size n is derived from len(maze).

Example 1:
    Input: maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 1],
    ]
    Output: ["DDRDRR", "DRDDRR"]
    Explanation: Both paths lead from (0, 0) to (3, 3) through open cells
        without revisiting a cell.

Input requirements:
    - maze is a square matrix containing only 0 and 1.
    - Numeric size limits are not visible in the supplied screenshot.
"""


def rat_in_a_maze(maze: list[list[int]]) -> list[str]:
    """Return all non-revisiting paths from the top-left to bottom-right cell.

    Args:
        maze: A square matrix of 0 (blocked) and 1 (open) cells. The input
            is not modified. This implementation also returns [] for [].

    Returns:
        Direction strings using D, U, L, and R, one for each valid path.
        Output order is unrestricted. No route, a blocked endpoint, or an
        empty maze returns []. A single open cell returns [""]: the rat
        is already at its destination, so the path needs no moves.

    Approach:
        Depth-First Search with Backtracking and a visited matrix.
        1. Return immediately if the maze is empty or either endpoint is
           blocked. Initialize the direction offsets, an empty current_path,
           and a visited matrix. Mark (0, 0) visited before starting recursion.
           Otherwise a later move could revisit the starting cell.
        2. When the current cell is the destination, join current_path into
           a string, save it, and return. Strings preserve the completed path
           independently of later changes to the working list.
        3. Try each of the four directions. Check the NEXT cell's coordinates:
           it must be inside the board, open, and unvisited on this path.
           Bounds checks occur before indexing, preventing invalid accesses.
        4. Append the direction and mark the next cell visited before recursing
           into it. Each active path therefore contains distinct cells only.
        5. After the child returns, unmark that next cell and pop the direction.
           This restores the parent state and allows a different path to use
           that cell. Visited means used by the CURRENT path, not permanently
           explored. The starting cell stays marked throughout the search.
        6. Return all recorded paths after exploring every valid branch.

        Example walkthrough:
            In an open 2 x 2 maze, mark (0,0), choose D to reach (1,0), then
            R to reach (1,1), and save 'DR'. Moving U from (1,0) is rejected
            because the start is already visited. Undo those choices and
            explore R followed by D to save 'RD'. The result is ['DR', 'RD'].

    Examples:
        >>> rat_in_a_maze([[1, 1], [1, 1]])
        ['DR', 'RD']
        >>> rat_in_a_maze([[0, 1], [1, 1]])
        []
        >>> rat_in_a_maze([[1, 1], [1, 0]])
        []
        >>> rat_in_a_maze([[1]])
        ['']

    Time Complexity:
        O(4**(n*n) + L), a conservative worst-case upper bound, where n is
        the side length and L is the total length of returned path strings.
        A path visits at most n*n cells, and each call tries four directions.
        A full four-way tree of that depth bounds the search; walls, bounds,
        and visited checks eliminate many branches. Each attempted move uses
        constant-time checks and amortized constant-time append/pop operations.
        Joining a successful path costs its length, totaling O(L) across all
        results. The initial n*n visited-matrix allocation is dominated by
        this bound. The bound is deliberately loose, not an exact call count.

    Space Complexity:
        O(n*n + L + P) total space, where P is the number of returned paths.
        Auxiliary space is O(n*n): the visited matrix, active recursion path,
        and working direction list each have at most n*n entries. The output
        stores L characters and P string references, including the possible
        empty path for a single open cell. No maze copies are created.
    """
    size: int = len(maze)
    result: list[str] = []

    # Step 1: Reject empty input and blocked endpoints before searching.
    if size == 0 or maze[0][0] == 0 or maze[size - 1][size - 1] == 0:
        return result

    directions: dict[str, tuple[int, int]] = {
        "D": (1, 0),
        "U": (-1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }
    current_path: list[str] = []
    visited: list[list[bool]] = [[False] * size for _ in range(size)]

    def is_allowed(row: int, col: int) -> bool:
        allowed: bool = (
            0 <= row < size
            and 0 <= col < size
            and maze[row][col] == 1
            and not visited[row][col]
        )
        return allowed

    def find_directions(row: int, col: int) -> None:

        # Step 2: Save the completed path as an independent string.
        if row == size - 1 and col == size - 1:
            result.append("".join(current_path))
            return

        # Step 3: Check each neighboring cell before entering it.
        for direction, (row_diff, col_diff) in directions.items():
            if is_allowed(row=row + row_diff, col=col + col_diff):
                # Step 4: Record the move and mark its destination visited.
                current_path.append(direction)
                visited[row + row_diff][col + col_diff] = True
                find_directions(row=row + row_diff, col=col + col_diff)
                # Step 5: Undo this move so other branches can use the cell.
                visited[row + row_diff][col + col_diff] = False
                current_path.pop()

    # Steps 1 and 6: Protect the start from revisits and enumerate all paths.
    visited[0][0] = True
    find_directions(row=0, col=0)

    return result


def solve() -> None:
    maze: list[list[int]] = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 1],
    ]
    expected: list[str] = ["DDRDRR", "DRDDRR"]
    result: list[str] = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example with two paths.
    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 1],
    ]
    expected = ["DDRDRR", "DRDDRR"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked start with otherwise open cells.
    maze = [
        [0, 1],
        [1, 1],
    ]
    expected = []
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Blocked destination.
    maze = [
        [1, 1],
        [1, 0],
    ]
    expected = []
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Entire maze blocked.
    maze = [
        [0, 0],
        [0, 0],
    ]
    expected = []
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open endpoints with no connecting path.
    maze = [
        [1, 0],
        [0, 1],
    ]
    expected = []
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only down then right is possible.
    maze = [
        [1, 0],
        [1, 1],
    ]
    expected = ["DR"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only right then down is possible.
    maze = [
        [1, 1],
        [0, 1],
    ]
    expected = ["RD"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Open square gives two paths without revisiting the start.
    maze = [
        [1, 1],
        [1, 1],
    ]
    expected = ["DR", "RD"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All-open three-by-three maze exercises cycles and backtracking.
    maze = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
    expected = [
        "DDRR",
        "DDRURD",
        "DDRUURDD",
        "DRDR",
        "DRRD",
        "DRURDD",
        "RDDR",
        "RDLDRR",
        "RDRD",
        "RRDD",
        "RRDLDR",
        "RRDLLDRR",
    ]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Top and right boundary corridor.
    maze = [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ]
    expected = ["RRDD"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Left and bottom boundary corridor.
    maze = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
    ]
    expected = ["DDRR"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A dead end must not prevent exploring the successful branch.
    maze = [
        [1, 1, 0],
        [1, 0, 0],
        [1, 1, 1],
    ]
    expected = ["DDRR"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two routes around a blocked center.
    maze = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    expected = ["DDRR", "RRDD"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single open cell is already the destination.
    maze = [
        [1],
    ]
    expected = [""]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single blocked cell has no path.
    maze = [
        [0],
    ]
    expected = []
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Winding corridor requires upward moves.
    maze = [
        [1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
    ]
    expected = ["DDRRUURRDDDD"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Winding corridor requires leftward moves.
    maze = [
        [1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]
    expected = ["RRDDLLDDRRRR"]
    result = rat_in_a_maze(maze)

    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
