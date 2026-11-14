"""Ninja And His Friends

Difficulty: Hard

Problem Statement:
    Ninja has a GRID of size R x C. Each cell contains some chocolates.
    Ninja has two friends, Alice and Bob, and wants to collect as many
    chocolates as possible with their help.

    Initially, Alice is at the top-left cell, (0, 0), and Bob is at the
    top-right cell, (0, C - 1). Each moves to the row immediately below.
    From (row, col), either friend can move to:
        Down:                 (row + 1, col)
        Down-left diagonal:   (row + 1, col - 1)
        Down-right diagonal:  (row + 1, col + 1)

    Both must always stay inside the grid. Whenever either friend visits
    a cell, they collect all its chocolates, leaving zero chocolates in
    that cell. If both occupy the same cell, its chocolates are collected
    only once, not once per friend.

    Find the maximum total number of chocolates collected by Alice and
    Bob as they travel from their starting positions to the bottom row.

Example:
    Input: R = 3, C = 4
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]

               Column
              0   1   2   3
    Row 0:    2   3   1   2
    Row 1:    3   4   2   2
    Row 2:    5   6   3   5

    Output: 21

    Alice starts at (0, 0) and can follow:
        (0, 0) -> (1, 1) -> (2, 1)
        Chocolates: 2 + 4 + 6 = 12

    Bob starts at (0, 3) and can follow:
        (0, 3) -> (1, 3) -> (2, 3)
        Chocolates: 2 + 2 + 5 = 9

    These paths visit different cells, so the total is 12 + 9 = 21.

Source Notes:
    Numeric constraints and the full input/output format are not visible
    in the screenshots. The function accepts the grid directly; its
    dimensions provide R and C.
"""


def ninja_and_his_friends_recursion(grid: list[list[int]]) -> int:
    """Return the most chocolates two friends can collect from top to bottom.

    Args:
        grid: A nonempty rectangular grid of nonnegative integer chocolate
            counts, with at least one column. Dimensions are not validated.

    Returns:
        The maximum total collected starting at the two top corners and
        moving down one row at a time, with column changes of -1, 0, or 1.
        A shared cell contributes only once. A single row collects only
        its endpoints; a single column collects every cell once.

    Mutation and assumptions:
        The grid is not modified. Chocolate counts represent nonnegative
        quantities; arbitrary negative values are outside this assumption.
        The fixed -10**9 sentinel marks invalid moves. Tall grids may exceed
        Python's recursion-depth limit. Numeric limits and a required time
        complexity are not provided in the problem statement.

    Approach:
        Depth-First Search (DFS), using recursive exhaustive search.
        1. Read the grid dimensions and define the three possible moves.
           Each move advances one row and changes the column by -1, 0,
           or 1. Track both friends together using one row and two columns.
        2. Reject a state if either column is outside the grid, before
           accessing any cell. Return -10**9 to discourage that move.
        3. At the bottom row, return the chocolates in the current cells.
           If both columns match, count that cell once: two friends on a
           cell containing 7 collect 7, rather than 14. No moves remain.
        4. Otherwise, initialize the best total and try all nine pairs of
           moves: each of Alice's three choices with each of Bob's three.
           Invalid combinations are rejected by step 2 in the next call.
        5. Count this row's chocolates once for a shared cell, or add both
           cells when the friends are apart. Recalculate this amount for
           each move pair so totals from separate choices do not mix.
        6. Recursively find the best remaining total for the next row and
           add it to the current amount. Keep the largest combined total
           across all move pairs, then return it. Looking to the bottom
           allows a smaller immediate reward to lead to a better total.
        7. Start the search at row 0, with Alice in column 0 and Bob in
           the last column. Return the best total for those fixed starts.

    Time Complexity:
        O(9 ** R) upper bound, where R is the number of rows. Each call
        before the last row tries nine move pairs, and repeated states
        are searched again; boundary checks can reduce the actual work.

    Space Complexity:
        O(R) extra space, excluding the input grid. The recursive call
        stack holds at most one call per row, with constant local storage.
    """
    # Step 1: Define the grid dimensions and the three moves per friend.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    directions: list[tuple[int, int]] = [(1, -1), (1, 0), (1, 1)]

    def collect_chocolates(row: int, alice_col: int, bob_col: int) -> int:
        # Step 2: Reject out-of-bounds columns before reading the grid.
        if alice_col < 0 or bob_col < 0 or alice_col >= col_size or bob_col >= col_size:
            return -(10**9)
        # Step 3: On the last row, count shared cells only once and stop.
        if row == (row_size - 1):
            if alice_col != bob_col:
                return grid[row][alice_col] + grid[row][bob_col]
            else:
                return grid[row][alice_col]
        # Step 4: Try every pair of moves and track the best total.
        max_chocolates: int = -(10**9)
        for row_delta_index, alice_delta_index in directions:
            for _, bob_delta_col_index in directions:
                # Step 5: Count this row's cells without double counting.
                current_chocolate: int = 0
                if alice_col == bob_col:
                    current_chocolate = grid[row][alice_col]
                else:
                    current_chocolate = grid[row][alice_col] + grid[row][bob_col]

                # Step 6: Add the best continuation and compare move pairs.
                current_chocolate += collect_chocolates(
                    row=row + row_delta_index,
                    alice_col=alice_col + alice_delta_index,
                    bob_col=bob_col + bob_delta_col_index,
                )
                max_chocolates = max(max_chocolates, current_chocolate)

        return max_chocolates

    # Step 7: Begin at the two top corners.
    return collect_chocolates(row=0, alice_col=0, bob_col=col_size - 1)


def ninja_and_his_friends_memoization(grid: list[list[int]]) -> int:
    """Return the maximum chocolates collected by two friends using a cache.

    Args:
        grid: A nonempty rectangular grid of nonnegative integer chocolate
            counts, with at least one column.

    Returns:
        The largest total collected from the two top corners to the bottom
        row. Each friend moves down one row with a column change of -1, 0,
        or 1. A cell occupied by both friends contributes only once.
        A single row collects its endpoints; a single column is summed once.

    Mutation and assumptions:
        The input grid is not modified. Empty grids and uneven row lengths
        are unsupported and are not validated. The -10**9 sentinel marks
        invalid moves; arbitrary negative values are outside the assumed
        nonnegative chocolate counts. Tall grids may exceed Python's
        recursion-depth limit. The problem supplies no numeric limits or
        required time complexity.

    Approach:
        Top-down Dynamic Programming (Memoization), using Depth-First
        Search (DFS).
        1. Read the dimensions and define the three downward moves. Create
           chocolate_dp with R layers, each containing a C by C table.
           chocolate_dp[row][alice_col][bob_col] stores the best total
           from that shared row and those two positions to the bottom.
           None means the state has not been calculated; zero is a valid
           cached total. Each inner list is created independently.
        2. Reject a state if its row is negative or either column is out
           of bounds, returning -10**9 before accessing the grid. Rows
           increase by one, and the last-row case stops further descent.
        3. On the last row, return the current cells' chocolates directly.
           If both columns match, count the cell only once: a shared cell
           containing 7 contributes 7. These base cases are not cached.
        4. For other rows, check chocolate_dp before doing any further
           search. If the entry is not None, return it immediately instead
           of exploring the same state again.
        5. Initialize max_chocolates and calculate current_chocolates once
           before the loops. Count one cell when the friends meet, or add
           their two cells when they are apart. This amount stays the
           same for every pair of next moves.
        6. Try all nine move pairs: Alice has three choices and Bob has
           three choices. For each pair, recursively obtain the best
           remaining total and add current_chocolates. Keep the largest
           combined total; invalid moves are rejected by step 2.
        7. Store max_chocolates in the cache for the current row and both
           columns, then return it. Later calls to this state reuse it.
        8. Start at row 0, with Alice in column 0 and Bob in column C - 1.
           Return the total for these fixed starting positions.

    Time Complexity:
        O(R * C**2), where R is the row count and C is the column count.
        The cache is initialized at this size, and each computed non-base
        state tries nine move pairs; last-row calls take constant time.

    Space Complexity:
        O(R * C**2) extra space, excluding the input grid. The cache holds
        R * C**2 entries, and the recursive stack uses another O(R) space.
    """
    # Step 1: Set up the moves and the independent 3D cache lists.
    row_size: int = len(grid)
    col_size: int = len(grid[0])

    delta: list[tuple[int, int]] = [(1, 1), (1, 0), (1, -1)]

    chocolate_dp: list[list[list[int | None]]] = [
        [[None] * col_size for _ in range(col_size)] for _ in range(row_size)
    ]

    def collect_chocolates(row: int, alice_col: int, bob_col: int) -> int:
        # Step 2: Reject invalid positions before reading any cell.
        if (
            row < 0
            or alice_col < 0
            or bob_col < 0
            or alice_col >= col_size
            or bob_col >= col_size
        ):
            return -(10**9)
        # Step 3: Finish on the last row, counting a shared cell once.
        if row == row_size - 1:
            if alice_col == bob_col:
                return grid[row][alice_col]
            else:
                return grid[row][alice_col] + grid[row][bob_col]

        # Step 4: Reuse a previously calculated total, including zero.
        if chocolate_dp[row][alice_col][bob_col] is not None:
            return chocolate_dp[row][alice_col][bob_col]

        # Step 5: Calculate this row's chocolates once for all move pairs.
        max_chocolates: int = -(10**9)

        current_chocolates: int = 0
        if alice_col == bob_col:
            current_chocolates = grid[row][alice_col]
        else:
            current_chocolates = grid[row][alice_col] + grid[row][bob_col]

        # Step 6: Compare this row plus the best continuation for each pair.
        for row_delta_index, alice_col_delta in delta:
            for _, bob_col_delta in delta:
                max_chocolates = max(
                    max_chocolates,
                    current_chocolates
                    + collect_chocolates(
                        row=row + row_delta_index,
                        alice_col=alice_col + alice_col_delta,
                        bob_col=bob_col + bob_col_delta,
                    ),
                )

        # Step 7: Cache and return the best total for this state.
        chocolate_dp[row][alice_col][bob_col] = max_chocolates

        return chocolate_dp[row][alice_col][bob_col]

    # Step 8: Begin at the fixed top-left and top-right positions.
    return collect_chocolates(row=0, alice_col=0, bob_col=col_size - 1)


def ninja_and_his_friends_tabulation(grid: list[list[int]]) -> int:
    """Return the maximum chocolates two friends can collect using a table.

    Args:
        grid: A nonempty rectangular grid of nonnegative integer chocolate
            counts, with at least one column.

    Returns:
        The largest total from the two top corners to the bottom row.
        Each friend moves down one row and changes columns by -1, 0, or 1.
        Shared cells count once. A single row collects only its endpoints;
        a single column collects each cell once.

    Mutation and assumptions:
        The grid is not modified. Empty grids and uneven row lengths are
        unsupported and are not validated. The -10**9 initial maximum is
        below every valid continuation for nonnegative chocolate counts;
        arbitrary negative values are outside this assumption. Numeric
        limits and a required time complexity are not given in the prompt.

    Approach:
        Bottom-up Dynamic Programming (Tabulation).
        1. Read the dimensions and create chocolate_dp with R independent
           layers of C by C entries. An entry indexed by row, alice_col,
           and bob_col represents the best total from those positions to
           the bottom. Define the three downward moves for each friend.
        2. Fill rows from the bottom upward, considering every pair of
           columns on each row. This order ensures the next row's totals
           are ready before the current row needs them.
        3. Put the current row's chocolates into the entry. When the two
           columns match, count that cell once; otherwise add both cells.
           For example, two friends sharing a cell with 7 collect 7.
        4. On the last row, continue to the next column pair immediately.
           There is no next row, so the amount from step 3 is already the
           complete total. This also handles a grid with only one row.
        5. For earlier rows, initialize max_chocolates and try all nine
           move pairs: three choices for Alice and three for Bob. Accept
           only pairs whose next columns are between 0 and C - 1,
           including both boundaries, so no invalid table index is read.
        6. Compare the valid next-row entries and keep the largest as
           max_chocolates. These entries already include the best paths
           through all remaining rows. Choose one continuation rather
           than adding totals from mutually exclusive move pairs.
        7. Add max_chocolates to this entry's current-row chocolates.
           For example, a current amount of 5 and a best continuation
           of 12 produce a total of 17 for this pair of positions.
        8. Return chocolate_dp[0][0][C - 1], the entry for Alice starting
           at the top-left and Bob starting at the top-right.

    Time Complexity:
        O(R * C**2), where R is the row count and C is the column count.
        Each of the R * C**2 entries takes constant work, including up to
        nine move pairs; initializing the table has the same bound.

    Space Complexity:
        O(R * C**2) extra space, excluding the input grid. The table holds
        R * C**2 entries; the moves and loop variables take constant space.
    """
    # Step 1: Set up the independent table layers and downward moves.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    chocolate_dp: list[list[list[int]]] = [
        [[0] * col_size for _ in range(col_size)] for _ in range(row_size)
    ]

    delta: list[tuple[int, int]] = [(1, 1), (1, 0), (1, -1)]

    # Step 2: Fill every column pair, working from the bottom row upward.
    for row in range(row_size - 1, -1, -1):
        for alice_col in range(col_size):
            for bob_col in range(col_size):
                # Step 3: Count the current cells, sharing a cell only once.
                if alice_col == bob_col:
                    chocolate_dp[row][alice_col][bob_col] = grid[row][alice_col]
                else:
                    chocolate_dp[row][alice_col][bob_col] = (
                        grid[row][alice_col] + grid[row][bob_col]
                    )
                # Step 4: Last-row entries need no continuation.
                if row == row_size - 1:
                    continue
                # Step 5: Try all move pairs and check both column bounds.
                max_chocolates: int = -(10**9)
                for row_delta, alice_col_delta in delta:
                    for _, bob_col_delta in delta:
                        if (
                            0 <= alice_col + alice_col_delta < col_size
                            and 0 <= bob_col + bob_col_delta < col_size
                        ):
                            # Step 6: Keep the best valid next-row total.
                            max_chocolates = max(
                                max_chocolates,
                                chocolate_dp[row + row_delta][
                                    alice_col + alice_col_delta
                                ][bob_col + bob_col_delta],
                            )
                # Step 7: Add that continuation to this row's chocolates.
                chocolate_dp[row][alice_col][bob_col] += max_chocolates
    # Step 8: Return the total for the fixed top-corner starting positions.
    return chocolate_dp[0][0][col_size - 1]


def ninja_and_his_friends_tabulation_space_optimized(grid: list[list[int]]) -> int:
    """Return the maximum chocolates using two tables of column pairs.

    Args:
        grid: A nonempty rectangular grid of nonnegative integer chocolate
            counts, with at least one column.

    Returns:
        The largest total collected from the two top corners to the bottom
        row. Each friend moves down one row and changes columns by -1, 0,
        or 1. A shared cell counts once. A single row collects its endpoints;
        a single column collects each cell once.

    Mutation and assumptions:
        The input grid is not modified. Empty grids and uneven row lengths
        are unsupported and are not validated. The -10**9 initial maximum
        assumes nonnegative chocolate counts; arbitrary negative values
        are outside that assumption. No numeric limits or required time
        complexity are provided in the problem statement.

    Approach:
        Bottom-up Dynamic Programming (Tabulation) with rolling arrays.
        1. Read the dimensions and define delta as the three possible
           column changes. Create prev_chocolate_dp as a C by C table
           with independent inner lists. After each completed row, its
           entry for two columns holds the best total from that row's
           positions to the bottom.
        2. Visit rows from bottom to top. Create a fresh curr_chocolate_dp
           for each row and consider every Alice and Bob column pair.
           While filling this table, prev_chocolate_dp holds totals for
           the row immediately below; keep it unchanged during the search.
        3. Store the current cells' chocolates in curr_chocolate_dp. If
           the friends share a column, count that cell once; otherwise
           add both cells. A shared cell containing 7 contributes 7.
        4. On the bottom row, continue to the next column pair. No future
           rows remain, so the current cells already give the final total.
           The initial zero-filled previous table is not read for this row.
        5. On other rows, initialize max_chocolate and try all nine move
           pairs: three choices for Alice and three for Bob. Check both
           next columns against 0 and C - 1, including the boundaries,
           before accessing the previous table.
        6. Keep the largest valid continuation from prev_chocolate_dp,
           then add it to the current entry. For example, 5 chocolates
           on this row plus a best remaining total of 12 gives 17.
           Only one move pair is chosen, so alternative totals are not
           added together.
        7. After both column loops finish, assign curr_chocolate_dp to
           prev_chocolate_dp. This assignment shares the completed table
           rather than copying it. The next iteration creates a fresh
           current table, so its writes cannot alter the previous row.
           Only the current and previous tables are needed at a time.
        8. After all rows are processed, return the entry for Alice in
           column 0 and Bob in column C - 1 of the top row.

    Time Complexity:
        O(R * C**2), where R is the row count and C is the column count.
        Each row creates a C by C table and checks up to nine move pairs
        for each entry, which is constant work per entry.

    Space Complexity:
        O(C**2) extra space, excluding the input grid. At most two C by C
        tables are needed at once; the moves and loop variables use
        constant space, and there is no recursive call stack.
    """
    # Step 1: Set up dimensions, column changes, and the previous table.
    row_size: int = len(grid)
    col_size: int = len(grid[0])
    delta: list[int] = [1, 0, -1]

    prev_chocolate_dp: list[list[int]] = [[0] * col_size for _ in range(col_size)]

    # Step 2: Work upward, using a fresh current table for each row.
    for row in range(row_size - 1, -1, -1):
        curr_chocolate_dp: list[list[int]] = [[0] * col_size for _ in range(col_size)]
        for alice_col_index in range(col_size):
            for bob_col_index in range(col_size):
                # Step 3: Count the current cells, sharing a cell only once.
                if alice_col_index == bob_col_index:
                    curr_chocolate_dp[alice_col_index][bob_col_index] = grid[row][
                        alice_col_index
                    ]
                else:
                    curr_chocolate_dp[alice_col_index][bob_col_index] = (
                        grid[row][alice_col_index] + grid[row][bob_col_index]
                    )
                # Step 4: The bottom row needs no continuation.
                if row == (row_size - 1):
                    continue
                # Step 5: Try all move pairs and reject out-of-bounds columns.
                max_chocolate: int = -(10**9)

                for alice_col_delta in delta:
                    for bob_col_delta in delta:
                        if (
                            0 <= alice_col_index + alice_col_delta < col_size
                            and 0 <= bob_col_index + bob_col_delta < col_size
                        ):
                            # Step 6: Select the best continuation below.
                            max_chocolate = max(
                                max_chocolate,
                                prev_chocolate_dp[alice_col_index + alice_col_delta][
                                    bob_col_index + bob_col_delta
                                ],
                            )
                # Step 6: Add that continuation to the current cells.
                curr_chocolate_dp[alice_col_index][bob_col_index] += max_chocolate
        # Step 7: Publish the completed row after both column loops finish.
        prev_chocolate_dp = curr_chocolate_dp

    # Step 8: Return the total for the two fixed top-corner positions.
    return prev_chocolate_dp[0][col_size - 1]


def solve() -> None:
    # Example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single cell: collect it only once.
    grid = [[7]]
    expected = 7
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 7, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single row: only the starting endpoints are collected.
    grid = [[2, 100, 3]]
    expected = 5
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 5, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single column: both friends share every cell.
    grid = [[2], [5], [1], [4]]
    expected = 12
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero chocolates throughout the grid.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 0, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two columns: collect both cells on every row.
    grid = [[1, 2], [3, 4], [5, 6]]
    expected = 21
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 21, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Meet on the last row: count the middle cell once.
    grid = [[1, 0, 1], [0, 10, 0]]
    expected = 12
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Meet in the middle, then separate on the last row.
    grid = [[1, 0, 1], [0, 10, 0], [9, 0, 9]]
    expected = 30
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 30, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A valuable middle cell cannot be reached in one move.
    grid = [[1, 0, 0, 0, 1], [0, 0, 100, 0, 0]]
    expected = 2
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 2, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Choosing a smaller immediate reward gives the best total.
    grid = [[0, 0, 0, 0, 0], [10, 0, 0, 0, 10], [0, 0, 100, 0, 0]]
    expected = 110
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 110, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values allow multiple optimal paths.
    grid = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    expected = 24
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 24, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both friends change diagonal directions.
    grid = [[8, 0, 0, 0, 7], [0, 6, 0, 5, 0], [4, 0, 0, 0, 3], [0, 2, 0, 1, 0]]
    expected = 36
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 36, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The center reward first becomes reachable on the last row.
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 100, 0, 0, 0],
    ]
    expected = 100
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 100, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Large positive chocolate counts.
    grid = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    expected = 4000000000000
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 4000000000000, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Stay at the boundaries for the best path.
    grid = [[9, 0, 0, 8], [7, 0, 0, 6], [5, 0, 0, 4]]
    expected = 39
    result = ninja_and_his_friends_recursion(grid)
    assert result == expected, f"Expected 39, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single cell: collect it only once.
    grid = [[7]]
    expected = 7
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 7, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single row: only the starting endpoints are collected.
    grid = [[2, 100, 3]]
    expected = 5
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 5, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single column: both friends share every cell.
    grid = [[2], [5], [1], [4]]
    expected = 12
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Zero chocolates throughout the grid.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 0, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Two columns: collect both cells on every row.
    grid = [[1, 2], [3, 4], [5, 6]]
    expected = 21
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 21, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Meet on the last row: count the middle cell once.
    grid = [[1, 0, 1], [0, 10, 0]]
    expected = 12
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Meet in the middle, then separate on the last row.
    grid = [[1, 0, 1], [0, 10, 0], [9, 0, 9]]
    expected = 30
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 30, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: A valuable middle cell cannot be reached in one move.
    grid = [[1, 0, 0, 0, 1], [0, 0, 100, 0, 0]]
    expected = 2
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 2, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choosing a smaller immediate reward gives the best total.
    grid = [[0, 0, 0, 0, 0], [10, 0, 0, 0, 10], [0, 0, 100, 0, 0]]
    expected = 110
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 110, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Identical values allow multiple optimal paths.
    grid = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    expected = 24
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 24, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Both friends change diagonal directions.
    grid = [[8, 0, 0, 0, 7], [0, 6, 0, 5, 0], [4, 0, 0, 0, 3], [0, 2, 0, 1, 0]]
    expected = 36
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 36, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: The center reward first becomes reachable on the last row.
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 100, 0, 0, 0],
    ]
    expected = 100
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 100, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Large positive chocolate counts.
    grid = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    expected = 4000000000000
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 4000000000000, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Stay at the boundaries for the best path.
    grid = [[9, 0, 0, 8], [7, 0, 0, 6], [5, 0, 0, 4]]
    expected = 39
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected 39, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: single zero cell.
    grid = [[0]]
    expected = 0
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: single row with two starting cells.
    grid = [[4, 6]]
    expected = 10
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: wide single row with interior rewards.
    grid = [[3, 99, 99, 99, 2]]
    expected = 5
    result = ninja_and_his_friends_memoization(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single cell: collect it only once.
    grid = [[7]]
    expected = 7
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 7, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single row: only the starting endpoints are collected.
    grid = [[2, 100, 3]]
    expected = 5
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 5, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single column: both friends share every cell.
    grid = [[2], [5], [1], [4]]
    expected = 12
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Zero chocolates throughout the grid.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 0, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Two columns: collect both cells on every row.
    grid = [[1, 2], [3, 4], [5, 6]]
    expected = 21
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 21, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Meet on the last row: count the middle cell once.
    grid = [[1, 0, 1], [0, 10, 0]]
    expected = 12
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Meet in the middle, then separate on the last row.
    grid = [[1, 0, 1], [0, 10, 0], [9, 0, 9]]
    expected = 30
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 30, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: A valuable middle cell cannot be reached in one move.
    grid = [[1, 0, 0, 0, 1], [0, 0, 100, 0, 0]]
    expected = 2
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 2, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Choosing a smaller immediate reward gives the best total.
    grid = [[0, 0, 0, 0, 0], [10, 0, 0, 0, 10], [0, 0, 100, 0, 0]]
    expected = 110
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 110, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Identical values allow multiple optimal paths.
    grid = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    expected = 24
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 24, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Both friends change diagonal directions.
    grid = [[8, 0, 0, 0, 7], [0, 6, 0, 5, 0], [4, 0, 0, 0, 3], [0, 2, 0, 1, 0]]
    expected = 36
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 36, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: The center reward first becomes reachable on the last row.
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 100, 0, 0, 0],
    ]
    expected = 100
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 100, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Large positive chocolate counts.
    grid = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    expected = 4000000000000
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 4000000000000, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Stay at the boundaries for the best path.
    grid = [[9, 0, 0, 8], [7, 0, 0, 6], [5, 0, 0, 4]]
    expected = 39
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected 39, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: single zero cell.
    grid = [[0]]
    expected = 0
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: single row with two starting cells.
    grid = [[4, 6]]
    expected = 10
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: wide single row with interior rewards.
    grid = [[3, 99, 99, 99, 2]]
    expected = 5
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: larger rectangular grid with tied paths.
    grid = [[1] * 20 for _ in range(30)]
    expected = 60
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: tall single column.
    grid = [[2] for _ in range(40)]
    expected = 80
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: wide two-row grid with unreachable interior rewards.
    grid = [[1] + [0] * 18 + [2], [3] + [0] * 8 + [100] + [0] * 9 + [4]]
    expected = 10
    result = ninja_and_his_friends_tabulation(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: example from the question.
    grid = [[2, 3, 1, 2], [3, 4, 2, 2], [5, 6, 3, 5]]
    expected = 21
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single cell: collect it only once.
    grid = [[7]]
    expected = 7
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 7, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single row: only the starting endpoints are collected.
    grid = [[2, 100, 3]]
    expected = 5
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 5, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Single column: both friends share every cell.
    grid = [[2], [5], [1], [4]]
    expected = 12
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Zero chocolates throughout the grid.
    grid = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 0, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Two columns: collect both cells on every row.
    grid = [[1, 2], [3, 4], [5, 6]]
    expected = 21
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 21, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Meet on the last row: count the middle cell once.
    grid = [[1, 0, 1], [0, 10, 0]]
    expected = 12
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 12, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Meet in the middle, then separate on the last row.
    grid = [[1, 0, 1], [0, 10, 0], [9, 0, 9]]
    expected = 30
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 30, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: A valuable middle cell cannot be reached in one move.
    grid = [[1, 0, 0, 0, 1], [0, 0, 100, 0, 0]]
    expected = 2
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 2, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Choosing a smaller immediate reward gives the best total.
    grid = [[0, 0, 0, 0, 0], [10, 0, 0, 0, 10], [0, 0, 100, 0, 0]]
    expected = 110
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 110, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Identical values allow multiple optimal paths.
    grid = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    expected = 24
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 24, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Both friends change diagonal directions.
    grid = [[8, 0, 0, 0, 7], [0, 6, 0, 5, 0], [4, 0, 0, 0, 3], [0, 2, 0, 1, 0]]
    expected = 36
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 36, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: The center reward first becomes reachable on the last row.
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 100, 0, 0, 0],
    ]
    expected = 100
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 100, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Large positive chocolate counts.
    grid = [[1000000000000, 1000000000000], [1000000000000, 1000000000000]]
    expected = 4000000000000
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 4000000000000, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Stay at the boundaries for the best path.
    grid = [[9, 0, 0, 8], [7, 0, 0, 6], [5, 0, 0, 4]]
    expected = 39
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected 39, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: single zero cell.
    grid = [[0]]
    expected = 0
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: single row with two starting cells.
    grid = [[4, 6]]
    expected = 10
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: wide single row with interior rewards.
    grid = [[3, 99, 99, 99, 2]]
    expected = 5
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: larger rectangular grid with tied paths.
    grid = [[1] * 20 for _ in range(30)]
    expected = 60
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: tall single column.
    grid = [[2] for _ in range(40)]
    expected = 80
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: wide two-row grid with unreachable interior rewards.
    grid = [[1] + [0] * 18 + [2], [3] + [0] * 8 + [100] + [0] * 9 + [4]]
    expected = 10
    result = ninja_and_his_friends_tabulation_space_optimized(grid)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
