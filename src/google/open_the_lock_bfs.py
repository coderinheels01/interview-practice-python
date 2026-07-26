"""
Open the Lock (LeetCode #752)

It's another implicit state-space BFS, similar in spirit to Word Ladder, but
with a new wrinkle: some states are explicitly forbidden ("dead ends"), and
the "graph" is a 4-digit combination lock instead of words.

The problem, in my own words:
You have a lock with 4 circular wheels, each showing a digit 0-9. Each wheel
can rotate one step at a time (either direction), wrapping around (9 → 0 and
0 → 9 are both valid single moves). The lock starts at "0000".

You're given a list deadends — combinations that, if the lock ever displays
them, permanently lock it (you can never move away from a dead end, so you
must never step into one). You're also given a target combination.

Return the minimum number of turns required to reach target from "0000", or
-1 if it's impossible (e.g., "0000" itself is a dead end, or every path to
target is blocked).

Example:
  deadends = ["0201","0101","0102","1212","2002"]
  target   = "0202"
  Output: 6

Why this is BFS:
- Each 4-digit combination is a node; turning any single wheel one step (up
  or down) creates an edge to a neighboring combination — 8 possible moves
  per node (4 wheels × 2 directions).
- You want the minimum number of turns — that's the "shortest path in an
  unweighted graph" signal again, exactly like Word Ladder.
- The graph is implicit — you generate each state's 8 neighbors on the fly,
  the same way Word Ladder generated neighbors by mutating one letter at a
  time.

Complexity:
  Time:  O(10^4 * 8 + D) where 10^4 = total possible lock states (0000–9999),
         8 = neighbors per state, and D = len(deadends) for building the set.
         In practice this is O(10_000) — a fixed upper bound.
  Space: O(10^4 + D) for the visited set and the deadends set.
"""

from collections import deque


def generate_neighbors(state: str) -> list[str]:
    # For each of the 4 wheel positions, spin it one step up and one step down.
    # % 10 handles the wraparound: (9+1)%10 = 0, (0-1)%10 = 9.
    neighbors: list[str] = []

    for i in range(4):
        digit: int = int(state[i])

        for new_digit in [(digit + 1) % 10, (digit - 1) % 10]:
            # Rebuild the string with only position i changed.
            new_state: str = state[:i] + str(new_digit) + state[i + 1 :]
            neighbors.append(new_state)

    return neighbors


def open_the_lock_bfs(deadends: list[str], target: str) -> int:
    start: str = "0000"

    # Step 1: Edge case — if the start itself is a dead end, we're stuck
    # immediately and can never make a single move.
    if start in deadends:
        return -1

    # Step 2: BFS initialisation.
    # Each queue entry is (current_combination, turns_taken_so_far).
    # Seed with the start state at turn 0.
    queue: deque[tuple[str, int]] = deque([(start, 0)])

    # Track visited states so we never revisit a combination (avoids cycles
    # and redundant work — BFS already guarantees the first visit is shortest).
    visited: set[int] = set(start)

    # Step 3: BFS loop — explore level by level (each level = one more turn).
    while queue:
        state, count = queue.popleft()

        # Step 4: Goal check — return the turn count as soon as we reach target.
        if state == target:
            return count

        # Step 5: Expand neighbors — try all 8 single-wheel moves.
        for neighbor in generate_neighbors(state):
            # Skip if already visited or if this combination is a dead end.
            if neighbor not in visited and neighbor not in deadends:
                queue.append((neighbor, count + 1))
                visited.add(neighbor)

    # Step 6: Queue exhausted with no path found — target is unreachable.
    return -1


def solve():
    deadends: list[str] = ["0201", "0101", "0102", "1212", "2002"]
    target: str = "0202"

    print(
        f"number of steps to get to target - {target} from 0000 is {open_the_lock_bfs(deadends=deadends, target=target)}"
    )

    deadends: list[str] = ["8888"]
    target: str = "0009"

    print(
        f"number of steps to get to target - {target} from 0000 is {open_the_lock_bfs(deadends=deadends, target=target)}"
    )

    deadends: list[str] = [
        "8887",
        "8889",
        "8878",
        "8898",
        "8788",
        "8988",
        "7888",
        "9888",
    ]
    target: str = "8888"

    print(
        f"number of steps to get to target - {target} from 0000 is {open_the_lock_bfs(deadends=deadends, target=target)}"
    )

    deadends: list[str] = []
    target: str = "0001"
    print(
        f"number of steps to get to target - {target} from 0000 is {open_the_lock_bfs(deadends=deadends, target=target)}"
    )

    deadends: list[str] = []
    target: str = "9999"
    print(
        f"number of steps to get to target - {target} from 0000 is {open_the_lock_bfs(deadends=deadends, target=target)}"
    )


solve()
