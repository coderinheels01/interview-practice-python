"""
Fountain Flooding
=================
Problem:
    You are given:
    - An array `heights` of length n, where heights[i] is the height of position i.
    - A list `fountains` containing indices of fountains (sorted in ascending order).

    Each fountain at index f can flood position i only if heights[i] < heights[f].
    Water spreads left and right from each fountain until it hits a position whose
    height is >= the fountain's height (those positions act as walls/blockers).

    Return a bitmask array `flooded` of length n where:
        flooded[i] = 1 if position i is flooded
        flooded[i] = 0 otherwise

    Note: The fountain's own position is NOT flooded (water spreads to neighbors,
    not the source itself).

Example:
    heights  = [6, 2, 5, 3, 4, 1]
    fountains = [1, 4]

    Fountain at index 1 (height 2):
        - Left:  index 0 has height 6 >= 2 → blocked immediately, nothing flooded left
        - Right: index 2 has height 5 >= 2 → blocked immediately, nothing flooded right

    Fountain at index 4 (height 4):
        - Left:  index 3 has height 3 < 4 → flooded; index 2 has height 5 >= 4 → stop
        - Right: index 5 has height 1 < 4 → flooded; end of array → stop

    Output: [0, 0, 0, 1, 0, 1]
"""


def fountain_flooding_monotonic_stack_brute_force(
    walls: list[int], fountains: list[int]
) -> list[int]:
    """
    Brute Force Approach
    --------------------
    For each fountain, walk left and right from its position.
    Mark positions as flooded as long as they are shorter than the fountain.
    Stop as soon as a position with height >= fountain height is encountered.

    This directly simulates the flooding process for each fountain independently.

    Time Complexity:  O(k * n) — for each of the k fountains, we may scan up to n positions
    Space Complexity: O(n)     — for the result array
    """
    n: int = len(walls)
    k: int = len(fountains)
    result: list[int] = [0] * n

    for i in range(k):
        index: int = fountains[i]
        fountain: int = walls[index]

        # Flood leftward: stop when we hit a wall (height >= fountain)
        for j in range(index - 1, -1, -1):
            if walls[j] >= fountain:
                break
            result[j] = 1

        # Flood rightward: stop when we hit a wall (height >= fountain)
        for t in range(index + 1, n):
            if walls[t] >= fountain:
                break
            result[t] = 1

    return result


def fountain_flooding_monotonic_stack_optimized(
    walls: list[int], fountains: list[int]
) -> list[int]:
    """
    Optimized Approach: Monotonic Stack + Difference Array
    -------------------------------------------------------
    Key insight: Instead of scanning every position for each fountain, precompute
    for each index the nearest position to its left/right that has a STRICTLY GREATER
    OR EQUAL height (the "blocking wall"). Then use a difference array to mark entire
    flood ranges in O(1) per fountain.

    Step 1 — Precompute left_to_right_max[i]:
        For each index i, find the nearest index to the LEFT with walls[j] >= walls[i].
        This is computed using a monotonic (non-increasing) stack scanning left → right.
        left_to_right_max[i] = j means walls[j] is the first wall to the left of i
        that would block water coming from i.

    Step 2 — Precompute right_to_left_max[i]:
        For each index i, find the nearest index to the RIGHT with walls[j] >= walls[i].
        Computed using the same monotonic stack technique scanning right → left.

    Step 3 — For each fountain, determine the flooded range:
        Left boundary:  left_to_right_max[fountain] → the blocking wall on the left.
                        The flooded range on the left is (left_boundary+1, fountain-1).
        Right boundary: right_to_left_max[fountain] → the blocking wall on the right.
                        The flooded range on the right is (fountain+1, right_boundary-1).

        Also explicitly mark the boundary index itself if it is shorter than the fountain
        (the wall index is outside the flood range in the diff array, so handle separately).

    Step 4 — Apply the difference array:
        Use a prefix sum over the diff array to determine which positions have a
        non-zero flood contribution, and set result[i] = 1 for those positions.

    Time Complexity:  O(n + k) — O(n) to build the monotonic stacks and apply the diff
                                  array; O(k) to process each fountain
    Space Complexity: O(n)     — for the two precomputed arrays, diff array, and result
    """

    n: int = len(walls)
    k: int = len(fountains)

    stack: list[int] = []

    # left_to_right_max[i] = index of the nearest element to the LEFT of i
    # with walls[j] >= walls[i]. -1 if no such element exists.
    left_to_right_max: list[int] = [-1] * n

    # right_to_left_max[i] = index of the nearest element to the RIGHT of i
    # with walls[j] >= walls[i]. -1 if no such element exists.
    right_to_left_max: list[int] = [-1] * n

    result: list[int] = [0] * n

    # --- Step 1: Build left_to_right_max using a monotonic decreasing stack ---
    # We maintain a stack of indices whose wall heights are non-increasing.
    # For each position i, pop anything shorter than walls[i] (they can't block i).
    # Whatever remains on top is the first wall to the left that is >= walls[i].
    for i in range(n):
        while stack and walls[stack[-1]] < walls[i]:
            stack.pop()

        if stack:
            left_to_right_max[i] = stack[-1]

        stack.append(i)

    stack = []

    # --- Step 2: Build right_to_left_max using the same technique, right → left ---
    for i in range(n - 1, -1, -1):
        while stack and walls[stack[-1]] < walls[i]:
            stack.pop()

        if stack:
            right_to_left_max[i] = stack[-1]

        stack.append(i)

    # --- Step 3 & 4: For each fountain, mark flood boundaries and build diff array ---

    # Difference array: diff[i] += 1 means a flood range starts at i,
    # diff[j] -= 1 means a flood range ends before j.
    diff: list[int] = [0] * n

    for fountain_idx in fountains:
        fountain_h: int = walls[fountain_idx]

        # --- Left side ---
        # left_wall is the nearest index to the left with height >= fountain height.
        # If it exists and is STRICTLY lower than fountain, it gets flooded too.
        # The interior flooded range is (left_wall+1, fountain_idx-1).
        # If no left wall exists (left_wall == -1), the range extends to index 0.
        left_wall: int = left_to_right_max[fountain_idx]

        if left_wall != -1 and walls[left_wall] < fountain_h:
            # The blocking wall index itself is strictly below the fountain → flood it
            result[left_wall] = 1

        # Interior left range: from (left_wall+1) up to (fountain_idx-1)
        left_start: int = left_wall + 1   # = 0 when left_wall == -1
        if left_start < fountain_idx:     # at least one position in range
            diff[left_start] += 1
            diff[fountain_idx] -= 1       # fountain itself is not flooded

        # --- Right side ---
        # right_wall is the nearest index to the right with height >= fountain height.
        # If it exists and is STRICTLY lower than fountain, it gets flooded too.
        # The interior flooded range is (fountain_idx+1, right_wall-1).
        # If no right wall exists (right_wall == -1), the range extends to index n-1.
        right_wall: int = right_to_left_max[fountain_idx]

        if right_wall != -1 and walls[right_wall] < fountain_h:
            # The blocking wall index itself is strictly below the fountain → flood it
            result[right_wall] = 1

        # Interior right range: from (fountain_idx+1) up to (right_wall-1).
        # right_end is the exclusive upper bound for the diff array update:
        #   - if a blocking wall exists, the interior stops just before it → right_end = right_wall
        #   - if no blocking wall, the interior extends to n-1 → right_end = n (out-of-bounds safe
        #     because we only write diff[right_end] when right_end < n)
        right_end: int = right_wall if right_wall != -1 else n  # exclusive upper bound
        if fountain_idx + 1 < right_end:  # at least one position in range
            diff[fountain_idx + 1] += 1
            if right_end < n:             # no need to undo past the array end
                diff[right_end] -= 1

    # Apply prefix sum over diff to find all flooded interior positions
    running: int = 0
    for i in range(n):
        running += diff[i]
        if running >= 1:
            result[i] = 1

    return result


def solve():
    walls: list[int] = [6, 2, 5, 3, 4, 1]
    fountains: list[int] = [1, 4]

    print(
        f"brute force solution: {fountain_flooding_monotonic_stack_brute_force(walls=walls, fountains=fountains)}"
    )
    print(
        f"optimized solution: {fountain_flooding_monotonic_stack_optimized(walls=walls, fountains=fountains)}"
    )

    walls = [5, 2, 8, 1, 4, 9]
    fountains = [0, 4]
    print(
        f"brute force solution: {fountain_flooding_monotonic_stack_brute_force(walls=walls, fountains=fountains)}"
    )
    print(
        f"optimized solution: {fountain_flooding_monotonic_stack_optimized(walls=walls, fountains=fountains)}"
    )


solve()
