"""Sudoku Solver

Fill the empty cells of a 9 x 9 Sudoku board to solve the puzzle.
Empty cells are represented by '.', and filled cells contain digit strings
from '1' through '9'. Preserve the digits already present in the input.

A completed board must satisfy all of these rules:
    1. Every row contains the digits 1 through 9 exactly once.
    2. Every column contains the digits 1 through 9 exactly once.
    3. Each of the nine 3 x 3 sub-boxes contains those digits exactly once.

For this practice template, modify board in place and return None.

Example 1:
    Input: board = [
        ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
        ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
        ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
        ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
        ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
        ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
        ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
        ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
        ['.', '.', '.', '.', '8', '.', '.', '7', '9'],
    ]
    Output: [
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'],
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
        ['3', '4', '5', '2', '8', '6', '1', '7', '9'],
    ]
    Explanation: The completed board fills every blank and satisfies all
        row, column, and 3 x 3 sub-box rules.

Example 2:
    Input: board = [
        ['.', '.', '.', '.', '.', '.', '7', '.', '.'],
        ['7', '.', '5', '.', '.', '.', '9', '.', '.'],
        ['.', '.', '.', '9', '7', '5', '4', '3', '1'],
        ['9', '.', '.', '.', '4', '1', '.', '.', '7'],
        ['.', '5', '.', '8', '.', '7', '6', '4', '.'],
        ['.', '7', '.', '.', '2', '.', '.', '.', '.'],
        ['.', '4', '.', '.', '.', '.', '.', '6', '9'],
        ['1', '6', '.', '4', '3', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '6', '2', '3', '.', '4'],
    ]
    Output: [
        ['4', '1', '9', '3', '8', '6', '7', '5', '2'],
        ['7', '3', '5', '2', '1', '4', '9', '8', '6'],
        ['8', '2', '6', '9', '7', '5', '4', '3', '1'],
        ['9', '8', '3', '6', '4', '1', '5', '2', '7'],
        ['2', '5', '1', '8', '9', '7', '6', '4', '3'],
        ['6', '7', '4', '5', '2', '3', '1', '9', '8'],
        ['3', '4', '7', '1', '5', '8', '2', '6', '9'],
        ['1', '6', '2', '4', '3', '9', '8', '7', '5'],
        ['5', '9', '8', '7', '6', '2', '3', '1', '4'],
    ]
    Explanation: The completed board fills every blank and satisfies all
        row, column, and 3 x 3 sub-box rules.

Constraints:
    - len(board) == 9
    - len(board[i]) == 9
    - Each cell is a digit string from '1' through '9', or '.'.
    - The input board is guaranteed to have exactly one solution.

    https://www.youtube.com/watch?v=FWAIf_EVUKE&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=17
"""


def solve_sudoku(board: list[list[str]]) -> None:
    """Solve the Sudoku board in place, preserving its original clues.

    Args:
        board: A 9 x 9 list of character lists. Digits '1' through '9' are
            clues and '.' marks an empty cell. The input is assumed to have
            exactly one valid solution, as guaranteed by the problem.

    Returns:
        None. The supplied board is updated with the completed solution.
        The helper returns a boolean internally to signal success or failure;
        the public function does not return that boolean or a new board.

    Approach:
        Depth-First Search with Backtracking and precomputed empty positions.
        1. Scan the board once and collect the coordinates of initially empty
           cells in row-major order. Original clues are never selected for
           replacement. Begin recursion with empty_slot_index=0.
        2. If empty_slot_index equals len(empty_slots), all collected cells
           have been filled successfully. Return True before accessing that
           list. An already solved board reaches this condition immediately.
        3. Read the next cell directly from empty_slots[empty_slot_index].
           Try digit strings '1' through '9'. Using the index avoids scanning
           previously filled cells again at every recursive call.
        4. Check whether the digit already appears in the row, column, or
           containing 3 x 3 box. Reject it on any conflict. For index 0..8,
           the box coordinates are:
               square_row = 3 * (row // 3) + index // 3
               square_col = 3 * (col // 3) + index % 3
           The first terms identify the box's top-left corner. The offsets
           visit (0,0), (0,1), (0,2), (1,0), ... , (2,2), covering all nine
           cells. Division advances the box row; remainder cycles its columns.
        5. Place a valid digit and recurse with empty_slot_index + 1. If the
           child returns True, return True immediately to preserve the solved
           board and stop searching.
        6. If the child fails, restore this cell to '.' and try the next digit.
           If all digits fail, return False so the parent can undo its choice.
           A digit can fit locally yet lead to a dead end in a later cell.
        7. After the search succeeds, leave its assignments on the original
           board. No board copies or collection of solutions are needed.

        Empty-slot example:
            If empty_slots is [(0, 2), (4, 5)], a successful branch fills
            board[0][2] at slot index 0, then board[4][5] at slot index 1.
            The next call has slot index 2, equal to the list length, and
            returns True without attempting to read empty_slots[2].

    Time Complexity:
        O(9**E) worst-case search bound, where E is the number of initially
        empty cells. There are at most nine candidate digits per cell and E
        levels of choices. Each validity check performs at most nine loop
        iterations, checking a row, column, and box in parallel, so its cost
        is constant for this fixed 9 x 9 board. The initial 81-cell scan is
        also constant. Constraint checks prune invalid branches and the first
        complete solution stops the search; actual work is often much smaller.
        This bound describes growth with E within the fixed board's limits.

    Space Complexity:
        O(E + 1) auxiliary space: empty_slots stores E coordinate pairs, and
        the recursion stack holds at most E + 1 active filling calls. The
        validity helper uses constant additional space. All calls share the
        input board, and the solution is written in place without copying it.

    https://www.youtube.com/watch?v=FWAIf_EVUKE&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=17

    """

    def is_valid(row: int, col: int, num_to_fill: str) -> bool:

        # Step 4: Reject any row, column, or box conflict.
        for index in range(9):
            if board[row][index] == num_to_fill:
                return False
            if board[index][col] == num_to_fill:
                return False

            # Step 4: Visit all nine cells relative to the box's top-left corner.
            square_row: int = 3 * (row // 3) + (index // 3)
            square_col: int = 3 * (col // 3) + (index % 3)

            if board[square_row][square_col] == num_to_fill:
                return False

        return True

    # Step 1: Collect empty coordinates once; preserve all original clues.
    empty_slots: list[tuple[int, int]] = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == ".":
                empty_slots.append((row, col))

    def fill_sudoku_board(empty_slot_index: int) -> bool:
        # Step 2: All collected cells are filled; no further lookup is needed.
        if empty_slot_index == len(empty_slots):
            return True
        # Step 3: Access the next empty position directly and try each digit.
        row, col = empty_slots[empty_slot_index]
        for num_to_fill in "123456789":
            if is_valid(row=row, col=col, num_to_fill=num_to_fill):
                # Step 5: Place this digit and keep it if the remaining board solves.
                board[row][col] = num_to_fill
                if fill_sudoku_board(empty_slot_index=empty_slot_index + 1):
                    return True
                # Step 6: Undo a failed choice before trying another digit.
                board[row][col] = "."
        # Step 6: No candidate worked; ask the parent to try another choice.
        return False

    # Steps 1 and 7: Start at the first empty slot and leave the solution in place.
    fill_sudoku_board(empty_slot_index=0)


def solve() -> None:
    board: list[list[str]] = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected: list[list[str]] = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    solve_sudoku(board)
    result: list[list[str]] = board

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original puzzle exercises backtracking.
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second supplied puzzle.
    board = [
        [".", ".", ".", ".", ".", ".", "7", ".", "."],
        ["7", ".", "5", ".", ".", ".", "9", ".", "."],
        [".", ".", ".", "9", "7", "5", "4", "3", "1"],
        ["9", ".", ".", ".", "4", "1", ".", ".", "7"],
        [".", "5", ".", "8", ".", "7", "6", "4", "."],
        [".", "7", ".", ".", "2", ".", ".", ".", "."],
        [".", "4", ".", ".", ".", ".", ".", "6", "9"],
        ["1", "6", ".", "4", "3", ".", ".", ".", "."],
        [".", ".", ".", ".", "6", "2", "3", ".", "4"],
    ]
    expected = [
        ["4", "1", "9", "3", "8", "6", "7", "5", "2"],
        ["7", "3", "5", "2", "1", "4", "9", "8", "6"],
        ["8", "2", "6", "9", "7", "5", "4", "3", "1"],
        ["9", "8", "3", "6", "4", "1", "5", "2", "7"],
        ["2", "5", "1", "8", "9", "7", "6", "4", "3"],
        ["6", "7", "4", "5", "2", "3", "1", "9", "8"],
        ["3", "4", "7", "1", "5", "8", "2", "6", "9"],
        ["1", "6", "2", "4", "3", "9", "8", "7", "5"],
        ["5", "9", "8", "7", "6", "2", "3", "1", "4"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Already solved board: no empty slots.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the first cell is empty.
    board = [
        [".", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the last cell is empty; it must become 9.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "."],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the center cell is empty.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", ".", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single missing digit 1.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", ".", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One entire row is empty.
    board = [
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One entire column is empty.
    board = [
        [".", "3", "4", "6", "7", "8", "9", "1", "2"],
        [".", "7", "2", "1", "9", "5", "3", "4", "8"],
        [".", "9", "8", "3", "4", "2", "5", "6", "7"],
        [".", "5", "9", "7", "6", "1", "4", "2", "3"],
        [".", "2", "6", "8", "5", "3", "7", "9", "1"],
        [".", "1", "3", "9", "2", "4", "8", "5", "6"],
        [".", "6", "1", "5", "3", "7", "2", "8", "4"],
        [".", "8", "7", "4", "1", "9", "6", "3", "5"],
        [".", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Top-left box is empty.
    board = [
        [".", ".", ".", "6", "7", "8", "9", "1", "2"],
        [".", ".", ".", "1", "9", "5", "3", "4", "8"],
        [".", ".", ".", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Center box is empty.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", ".", ".", ".", "4", "2", "3"],
        ["4", "2", "6", ".", ".", ".", "7", "9", "1"],
        ["7", "1", "3", ".", ".", ".", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Bottom-right box is empty.
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", ".", ".", "."],
        ["2", "8", "7", "4", "1", "9", ".", ".", "."],
        ["3", "4", "5", "2", "8", "6", ".", ".", "."],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One empty cell in every row and column.
    board = [
        [".", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", ".", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", ".", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", ".", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", ".", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", ".", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", ".", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", ".", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "."],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All occurrences of digit 9 are missing.
    board = [
        ["5", "3", "4", "6", "7", "8", ".", "1", "2"],
        ["6", "7", "2", "1", ".", "5", "3", "4", "8"],
        ["1", ".", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", ".", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", ".", "1"],
        ["7", "1", "3", ".", "2", "4", "8", "5", "6"],
        [".", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", ".", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "."],
    ]
    expected = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    returned = solve_sudoku(board)
    result = board

    assert result == expected
    assert returned is None
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
