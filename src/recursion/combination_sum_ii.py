"""Combination Sum II

Given a list of candidate integers candidates and an integer target, return
all unique combinations whose sum equals target.

Each position in candidates may be used at most once in a combination.
Duplicate values are allowed in the input and may appear in a combination
only as many times as they occur in candidates. Different orderings of the
same values are not distinct combinations: [1, 1, 2] and [1, 2, 1] represent
the same combination.

Return each combination in nondecreasing order and the list of combinations
in lexicographic order. Return an empty list if no combination sums to target.

Example 1:
    Input: candidates = [2, 1, 2, 7, 6, 1, 5], target = 8
    Output: [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    Explanation:
        1 + 1 + 6 = 8.
        1 + 2 + 5 = 8.
        1 + 7 = 8.
        2 + 6 = 8.
        Each distinct combination is returned only once.

Example 2:
    Input: candidates = [2, 5, 2, 1, 2], target = 5
    Output: [[1, 2, 2], [5]]
    Explanation: 1 + 2 + 2 = 5 and 5 = 5.

Example 3:
    Input: candidates = [2, 1, 2], target = 5
    Output: [[1, 2, 2]]

Constraints:
    - 1 <= len(candidates) <= 100
    - 1 <= candidates[i] <= 50
    - 1 <= target <= 30

https://www.youtube.com/watch?v=G1fRTGRxXU8&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=11

"""


def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    """Return sorted unique combinations, using each candidate position once.

    Args:
        candidates: Positive integers under the module's constraints. Duplicate
            values are allowed. This function sorts the input list in place.
        target: Positive required sum under the module's constraints.

    Returns:
        Independent lists of values in nondecreasing order, with the outer
        list in lexicographic order. Each value can appear only as many times
        as it occurs in candidates. No matches produces an empty list.

    Approach:
        Depth-First Search with Backtracking, sorting, and duplicate skipping.
        1. Initialize the output and sort candidates in place. Sorting groups
           equal values and lets the search stop when a candidate is too large.
           Start with index 0, the full remaining target, and an empty sub_list.
        2. If remaining_target is zero, append a copy of sub_list and return.
           The copy preserves this result while the working list changes later.
           Positive candidates cannot extend a match without exceeding target.
        3. Loop over candidate positions from index to the end. If index equals
           the list length, the loop is empty and this call returns naturally.
        4. Skip a repeated value when next_element_index > index and it equals
           the previous value. This skips duplicate choices at the SAME depth.
           The first candidate in a new call is still allowed, so equal values
           from different positions can be selected together at deeper levels.
        5. Break when the candidate exceeds remaining_target. Every later
           value is at least as large because the input is sorted. This exits
           only this call's loop; its parent can still explore other choices.
        6. Append the candidate and recurse from next_element_index + 1 with
           its value subtracted from the remaining target. Advancing the index
           prevents reuse of the same position. After the call returns, pop
           the candidate to restore sub_list before trying the next choice.
        7. Return the collected results. Exploring sorted candidates in order
           produces sorted combinations and lexicographic result order without
           a final sort or a set.

        Duplicate example:
            For [1, 1, 2] and target=3, choosing the first 1 and then 2 saves
            [1, 2]. Back at the root, the second 1 is skipped because it would
            repeat the same choice. With target=2, however, the second 1 is
            allowed inside the first 1's child call, producing [1, 1].

        Early-stop example:
            For sorted candidates [1, 2, 5, 7] and remaining_target=3, the
            loop explores 1 and 2, then breaks at 5. It need not check 7,
            since every value after 5 also exceeds 3.

    Examples:
        >>> combination_sum_ii([2, 1, 2, 7, 6, 1, 5], 8)
        [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
        >>> combination_sum_ii([2, 5, 2, 1, 2], 5)
        [[1, 2, 2], [5]]
        >>> combination_sum_ii([1, 1, 2], 2)
        [[1, 1], [2]]
        >>> combination_sum_ii([2], 4)
        []

    Time Complexity:
        O(n * 2**n), a conservative worst-case upper bound, where n is the
        number of candidates. Each position can be selected or not, giving
        at most 2**n position subsets. A recursive call can scan up to n
        candidates, and copying a successful combination costs at most n.
        The initial O(n log n) sort is dominated by this bound. Duplicate
        skipping, early stopping, and the target limit reduce actual work.

        "Scanning" means the for loop over range(index, size), which checks
        up to n remaining candidates in one call. At a successful leaf,
        sub_list.copy() copies k elements, where k <= n; appending that copy
        to result costs only amortized O(1).
        Scanning and copying do not both happen in every call: a successful
        call copies and returns before the loop. Bounding either kind of call
        by O(n) work gives the n factor multiplying the 2**n call bound.
        Even if we conservatively add both allowances, n + n = 2n, and the
        constant 2 disappears in Big-O. These costs are added, not multiplied
        together, so they do not introduce an extra n factor.

    Space Complexity:
        O(n + L) total space, where L is the total number of elements in all
        saved combinations. Each recursive selection advances the index, so
        the stack has depth at most n and the shared working list sub_list
        holds at most n values. Python's in-place sort can also use O(n)
        temporary space. Output copies and their references use O(L) space;
        every saved combination is nonempty because target is positive.
    """
    # Step 1: Initialize the output and sort the caller's list.
    size: int = len(candidates)
    result: list[list[int]] = []
    candidates.sort()

    def generate_combination_sum_list(
        index: int, remaining_target: int, sub_list: list[int]
    ) -> None:
        # Step 2: Save an independent copy of a complete combination.
        if remaining_target == 0:
            result.append(sub_list.copy())
            return

        # Step 3: Try each remaining position as the next selection.
        for next_element_index in range(index, size):
            # Step 4: Skip equal choices at this depth, not at deeper levels.
            if (
                next_element_index > index
                and candidates[next_element_index] == candidates[next_element_index - 1]
            ):
                continue

            # Step 5: Sorted order guarantees all later values are too large.
            if candidates[next_element_index] > remaining_target:
                break
            # Step 6: Choose this position and recurse beyond it.
            sub_list.append(candidates[next_element_index])
            generate_combination_sum_list(
                index=next_element_index + 1,
                remaining_target=remaining_target - candidates[next_element_index],
                sub_list=sub_list,
            )
            # Step 6: Undo the choice before trying the next loop iteration.
            sub_list.pop()

    # Steps 1 and 7: Search from the empty working list and return the results.
    generate_combination_sum_list(index=0, remaining_target=target, sub_list=[])
    return result


def solve() -> None:
    # candidates: list[int] = [2, 1, 2, 7, 6, 1, 5]
    # target: int = 8
    # expected: list[list[int]] = [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    # result: list[list[int]] = combination_sum_ii(candidates, target)

    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum length, value, and target match.
    candidates = [1]
    target = 1
    expected = [[1]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One position cannot be reused.
    candidates = [1]
    target = 2
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum candidate exceeds maximum target.
    candidates = [50]
    target = 30
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single candidate matches maximum target.
    candidates = [30]
    target = 30
    expected = [[30]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum target is unreachable.
    candidates = [2]
    target = 1
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example with duplicates in unsorted input.
    candidates = [2, 1, 2, 7, 6, 1, 5]
    target = 8
    expected = [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second example deduplicates repeated position selections.
    candidates = [2, 5, 2, 1, 2]
    target = 5
    expected = [[1, 2, 2], [5]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All positions are required.
    candidates = [2, 1, 2]
    target = 5
    expected = [[1, 2, 2]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal values may be selected at different recursion depths.
    candidates = [1, 1, 1, 2, 2]
    target = 4
    expected = [[1, 1, 2], [2, 2]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated singletons produce just one result.
    candidates = [1, 1, 1]
    target = 1
    expected = [[1]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All equal values give one pair combination.
    candidates = [2, 2, 2, 2]
    target = 4
    expected = [[2, 2]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Insufficient copies cannot be reused.
    candidates = [2, 2]
    target = 6
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All equal values cannot reach an odd target.
    candidates = [2, 2, 2, 2]
    target = 5
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match at the beginning of the original input.
    candidates = [3, 8, 9]
    target = 3
    expected = [[3]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match in the middle of the original input.
    candidates = [8, 3, 9]
    target = 3
    expected = [[3]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Match at the end of the original input.
    candidates = [8, 9, 3]
    target = 3
    expected = [[3]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Already sorted input returns lexicographically sorted combinations.
    candidates = [1, 2, 3, 4, 5]
    target = 6
    expected = [[1, 2, 3], [1, 5], [2, 4]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input returns the same sorted combinations.
    candidates = [5, 4, 3, 2, 1]
    target = 6
    expected = [[1, 2, 3], [1, 5], [2, 4]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All candidates exceed the target.
    candidates = [50, 40, 31]
    target = 30
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Total sum is less than target.
    candidates = [1, 2, 3]
    target = 7
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of minimum values and maximum target.
    candidates = [1] * 100
    target = 30
    expected = [[1] * 30]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of minimum values and minimum target.
    candidates = [1] * 100
    target = 1
    expected = [[1]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of maximum values yields no solution.
    candidates = [50] * 100
    target = 30
    expected = []
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with duplicate maximum-target matches.
    candidates = [30] * 100
    target = 30
    expected = [[30]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length mixing minimum and maximum values.
    candidates = [50, 1] * 50
    target = 30
    expected = [[1] * 30]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple combinations near the maximum target.
    candidates = [1, 1, 2, 28, 29, 30, 50]
    target = 30
    expected = [[1, 1, 28], [1, 29], [2, 28], [30]]
    result = combination_sum_ii(candidates, target)

    assert result == expected
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
