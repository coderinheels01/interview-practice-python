"""
Equal Split
-----------
You are given two arrays of the same length:
  - votesPower[i] is the vote power of the ith state.
  - states[i]     is the name of the ith state.

There are two candidates, C1 and C2.
Return ALL ways to split the states between the two candidates such that
both candidates receive the same total vote power.

Example:
  votesPower = [1, 5, 7, 8, 9, 10, 20]
  states     = ["California", "Texas", "Florida", "Indiana", "Alaska", "Ohio", "Hawaii"]

  Output:
    ({"California", "Texas", "Florida", "Indiana", "Alaska"}, {"Ohio", "Hawaii"})
    ... (all other valid splits)

Approach: Backtracking (Include / Exclude)
------------------------------------------
For each state at index i we make a binary choice:
  - INCLUDE it in the left candidate's subset, or
  - EXCLUDE it (it will end up in the right candidate's subset).

We recurse through all indices 0..n-1, tracking the running sum of the left
subset.  When we reach the end (index == n) we check whether the left sum
equals half the total.  If so, the right subset is simply every index NOT
in the left subset.

Pruning:
  If left_sum already exceeds target, no further additions can help → prune.

Time Complexity:  O(2^n)
  - At each of the n states we branch into two choices (include / exclude).
  - In the worst case we explore all 2^n subsets.
  - With the early-exit pruning this is often much faster in practice,
    but the worst-case bound remains O(2^n).

Space Complexity: O(n)
  - The recursion call stack is at most n levels deep.
  - The left_subset set holds at most n indices at any point.
  - (The result list itself can hold O(2^n) entries in theory, but that is
    output space, not auxiliary space.)
"""


def find_all_equal_splits(
    votes_power: list[int],
    states: list[str],
) -> list[tuple[set[str], set[str]]]:
    n: int = len(votes_power)
    total: int = sum(votes_power)

    # Step 1: Early exit if total is odd — an equal split is impossible.
    if total % 2 != 0:
        return []

    target: int = total // 2          # each candidate must reach this sum
    index_set: set[int] = set(range(n))  # all indices; used to derive right subset
    result: list[tuple[set[str], set[str]]] = []

    def backtrack(index: int, left_subset: set[int], left_sum: int) -> None:
        """
        index       – the current state we are deciding on (0-indexed)
        left_subset – indices already assigned to the left candidate
        left_sum    – running vote-power total for the left candidate
        """
        # Step 2: Base case – we have made a decision for every state.
        if index == n:
            if left_sum == target:
                # Step 3: Valid split found.
                #   Right subset = all indices NOT in left_subset.
                right_subset: set[int] = index_set - left_subset

                left_states: set[str] = {states[i] for i in left_subset}
                right_states: set[str] = {states[i] for i in right_subset}
                result.append((left_states, right_states))
            return

        # Step 4: Pruning – left sum already exceeds target; no need to go deeper.
        if left_sum > target:
            return

        # Step 5a: INCLUDE states[index] in the left candidate's subset.
        left_subset.add(index)
        backtrack(
            index=index + 1,
            left_subset=left_subset,
            left_sum=left_sum + votes_power[index],
        )

        # Step 5b: EXCLUDE states[index] from the left subset (backtrack).
        left_subset.discard(index)
        backtrack(
            index=index + 1,
            left_subset=left_subset,
            left_sum=left_sum,
        )

    # Step 6: Kick off the recursion with an empty left subset and sum of 0.
    backtrack(index=0, left_subset=set(), left_sum=0)

    return result


def solve() -> None:
    # --- Test case 1 (from the problem statement) ---
    votes_power = [1, 5, 7, 8, 9, 10, 20]
    states = ["California", "Texas", "Florida", "Indiana", "Alaska", "Ohio", "Hawaii"]
    result = find_all_equal_splits(votes_power=votes_power, states=states)
    print("Test 1 results:")
    for left, right in result:
        print(f"  C1: {sorted(left)}")
        print(f"  C2: {sorted(right)}")
        print()

    # --- Test case 2 ---
    votes_power = [1, 2, 3, 4, 5, 5]
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado"]
    result = find_all_equal_splits(votes_power=votes_power, states=states)
    print("Test 2 results:")
    for left, right in result:
        print(f"  C1: {sorted(left)}")
        print(f"  C2: {sorted(right)}")
        print()


solve()
