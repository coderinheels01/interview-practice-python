# PROBLEM:
# You begin with an array filled with N zeros and you want to obtain an array A.
# In one move, you can choose an arbitrary interval and increase all the elements
# within that interval by 1.
#
# For example, you can transform [0, 0, 0, 0, 0] into [0, 1, 1, 1, 0] in a
# single move. However, you need three moves to obtain [1, 0, 1, 2, 2].
# One possible sequence:
#   [0,0,0,0,0] → [0,0,1,1,1] → [0,0,1,2,2] → [1,0,1,2,2]
#
# What is the minimum number of moves needed to obtain A from a zero-filled array?
#
# Write a function:
#   def solution(A) that, given an array A of length N, returns the minimum number
#   of moves needed to transform a zero-filled array into A.
#
# Examples:
#   A = [2, 1, 3]        → 4
#     [0,0,0] → [1,1,1] → [2,1,1] → [2,1,2] → [2,1,3]
#
#   A = [2, 2, 0, 0, 1]  → 3
#     [0,0,0,0,0] → [1,1,0,0,0] → [2,2,0,0,0] → [2,2,0,0,1]
#
#   A = [5, 4, 2, 4, 1]  → 7
#     [0,0,0,0,0] → [1,1,1,1,1] → [2,2,2,2,1] → [3,3,2,2,1]
#     → [4,4,2,2,1] → [5,4,2,2,1] → [5,4,2,3,1] → [5,4,2,4,1]
#
# Constraints:
#   N is an integer within the range [1..100,000]
#   each element of array A is an integer within the range [0..1,000,000,000]
#   the answer will not exceed 1,000,000,000
#
# Note: Write an efficient algorithm.


def minimum_moves_to_transform_array_brute_force(target: list[int]) -> int:
    """
    Brute-force DFS approach: exhaustively try every possible interval increment
    at each step, backtracking to find the minimum total number of moves.

    Key insight (used implicitly):
      The answer equals the sum of all "positive increases" when scanning left
      to right through the array — i.e., sum of max(0, A[i] - A[i-1]) for i >= 1,
      plus A[0]. The brute force confirms this by searching the full state space.

    Algorithm:
      - Maintain a `current` array (starts as all zeros).
      - At each DFS call, if current == target, return 0 (done).
      - Otherwise, try every valid interval [left, right]:
          * An interval is valid only if incrementing every element in it keeps
            current[i] + 1 <= target[i] (we never overshoot the target).
          * Apply the increment, recurse, then undo it (backtrack).
      - Return the minimum moves found across all choices.

    WARNING: This is exponential in complexity and only feasible for very small
    inputs (N <= ~5 with small values). It exists to validate correctness against
    the efficient O(N) solution.

    Time complexity: O(exponential) — not suitable for large inputs.
    Space complexity: O(N * depth) for the recursion stack.
    """
    n: int = len(target)
    # `current` tracks the state being built toward `target`; mutated in place
    # during DFS and restored on backtrack.
    current: list[int] = [0] * n

    def dfs() -> int:
        # Base case: we've reached the target array — no more moves needed.
        if current == target:
            return 0

        answer: float = float("inf")

        # Try every possible interval [left, right].
        for left in range(n):
            for right in range(left, n):
                # Validate: incrementing the entire interval must not push any
                # element past its target value.
                valid: bool = True
                for i in range(left, right + 1):
                    if current[i] + 1 > target[i]:
                        valid = False
                        break  # No need to check further — interval is invalid.

                if valid:
                    # Apply the move: increment all elements in [left, right].
                    for j in range(left, right + 1):
                        current[j] += 1

                    # Recurse: count this move plus the minimum moves from here.
                    moves = 1 + dfs()
                    answer = min(moves, answer)

                    # Backtrack: undo the increment to restore state for the
                    # next candidate interval.
                    for j in range(left, right + 1):
                        current[j] -= 1

        return answer

    return dfs()


def minimum_moves_to_transform_array_optimized(target: list[int]) -> int:
    """
    Optimised O(N) greedy approach based on the "positive differences" insight.

    Key insight:
      Think of each move as painting a horizontal stripe across a contiguous
      interval. The total number of stripes needed equals the total "upward
      steps" when scanning the array left to right:
        - A[0] itself is an upward step from the implicit 0 to its left.
        - For each subsequent index i, if A[i] > A[i-1], we need
          (A[i] - A[i-1]) additional stripes that start at i.
        - Downward steps (A[i] < A[i-1]) require no extra stripes — existing
          stripes simply end before index i.

      Therefore:
        moves = A[0] + sum(max(0, A[i] - A[i-1]) for i in 1..N-1)

    Example — A = [2, 1, 3]:
      A[0] = 2  → +2
      A[1] - A[0] = 1-2 = -1 → no new stripes (downward step)
      A[2] - A[1] = 3-1 =  2 → +2
      Total = 4 ✓

    Time complexity:  O(N) — single pass through the array.
    Space complexity: O(1) — only a running counter.
    """
    n: int = len(target)

    # The first element contributes directly — we start from 0, so we need
    # A[0] stripes that all begin at or before index 0.
    moves: int = target[0]

    # For each subsequent position, count only upward steps — these are the
    # stripes that must start fresh at this index.
    for i in range(1, n):
        if target[i] > target[i - 1]:
            moves += target[i] - target[i - 1]

    return moves


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def run_tests():
    """
    Validate both solutions against the same set of known-good test cases.

    The expected values follow the O(N) insight:
      answer = A[0] + sum(max(0, A[i] - A[i-1]) for i in 1..N-1)
    which counts how much each position "rises" relative to its left neighbour.

    The brute force is only run on small inputs (it's exponential); the
    optimized solution handles all cases including larger ones.
    """
    # (target, expected, description, run_brute_force)
    # run_brute_force=False for inputs too large for the DFS to finish quickly.
    test_cases = [
        ([2, 1, 3], 4, "Example 1 from problem statement", True),
        ([2, 2, 0, 0, 1], 3, "Example 2 from problem statement", True),
        ([5, 4, 2, 4, 1], 7, "Example 3 from problem statement", False),
        ([0], 0, "Single zero — already at target, 0 moves", True),
        ([1], 1, "Single element 1 — one move covering index 0", True),
        ([3], 3, "Single element 3 — three individual moves", True),
        ([1, 1, 1], 1, "Flat array — one move covering the whole range", True),
        ([1, 2, 3], 3, "Strictly increasing — each step adds a layer", True),
        ([3, 2, 1], 3, "Strictly decreasing — A[0]=3 dominates", True),
        ([0, 0, 0], 0, "All zeros — already the target", True),
        ([2, 0, 2], 4, "Valley in the middle — two rising segments", True),
        ([1, 3, 1], 3, "Peak in the middle — rise of 2 at index 1", True),
        ([3, 3, 3], 3, "All equal — A[0] is the only contribution", True),
        # Optimized-only: inputs too large for the exponential brute force.
        ([0, 5], 5, "Jump from 0 to 5 — 5 new stripes start at i=1", False),
        ([10, 0, 10], 20, "High-valley-high — 10 + 0 + 10 positive rises", False),
        ([1, 2, 1, 2, 1], 3, "Alternating up-down — two upward steps of 1", False),
        ([5, 4, 2, 4, 1], 7, "Large example repeated for optimized only", False),
    ]

    print("Running tests...\n")
    all_passed = True

    for arr, expected, description, run_bf in test_cases:
        bf_result = (
            minimum_moves_to_transform_array_brute_force(arr) if run_bf else None
        )
        opt_result = minimum_moves_to_transform_array_optimized(arr)

        bf_ok = (bf_result == expected) if run_bf else None
        opt_ok = opt_result == expected

        overall_ok = opt_ok and (bf_ok if run_bf else True)
        status = "PASS" if overall_ok else "FAIL"
        if not overall_ok:
            all_passed = False

        bf_str = (
            f"brute_force={bf_result} ({'✓' if bf_ok else '✗'}), " if run_bf else ""
        )
        print(
            f"[{status}] {description}\n"
            f"        target={arr}, expected={expected}, "
            f"{bf_str}"
            f"optimized={opt_result} ({'✓' if opt_ok else '✗'})\n"
        )

    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests FAILED — see above for details.")


run_tests()
