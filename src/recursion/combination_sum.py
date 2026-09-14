"""Combination Sum

Given an array of distinct integers nums and an integer target, return all
distinct combinations of numbers from nums whose sum equals target.
The combinations can be returned in any order.

Each number in nums may be selected an unlimited number of times. Two
combinations are distinct if the frequency of at least one selected number
differs. Different orderings of the same selected numbers are not distinct
combinations.

The test cases guarantee fewer than 150 combinations for each input.
Return an empty list if no combination sums to target.

Example 1:
    Input: nums = [2, 3, 5, 4], target = 7
    Output: [[2, 2, 3], [2, 5], [3, 4]]
    Explanation:
        2 + 2 + 3 = 7; the number 2 can be used multiple times.
        2 + 5 = 7.
        3 + 4 = 7.
        There are three distinct combinations.

Example 2:
    Input: nums = [2], target = 1
    Output: []
    Explanation: No selection of candidates sums to target.

Example 3:
    Input: nums = [3, 4, 5, 6], target = 10
    Output: [[3, 3, 4], [4, 6], [5, 5]]

Constraints:
    - 1 <= len(nums) <= 30
    - 2 <= nums[i] <= 40
    - All elements of nums are distinct.
    - 1 <= target <= 40
"""


def combination_sum(nums: list[int], target: int) -> list[list[int]]:
    """Return all distinct combinations that sum to target, allowing reuse.

    Args:
        nums: Distinct positive candidate integers under the module's
            constraints. Input order need not be sorted. nums is not modified.
        target: Positive required sum under the module's constraints.

    Returns:
        A list of independent combination lists, or [] if no solution exists.
        Each candidate can appear any number of times. Candidate indices within
        a combination never decrease, so different permutations of the same
        selection are not returned. Values need not be in numerical order
        when nums is unsorted. Result order is not part of the contract.

    Approach:
        Depth-First Search with Backtracking (include/exclude recursion).
        1. Initialize the output and start at index 0 with the full target
           remaining and an empty working combination.
        2. If remaining_target is zero, save a copy of the working combination
           and return immediately. All candidates are positive, so adding any
           further value cannot produce another match from this path. Copying
           prevents later append/pop operations from changing saved results.
        3. If index equals len(nums), return: every candidate has been
           considered. The index len(nums) - 1 is still valid and must be
           processed. This check prevents accessing nums beyond its last index.
        4. If nums[index] fits in the remaining target, append it and recurse
           at the SAME index with a reduced remaining target. Staying at this
           index allows unlimited reuse. The subtraction is passed directly
           to the child, leaving the parent's remaining target unchanged.
        5. Pop the included value after the child returns to restore the
           shared working list before exploring the alternative branch.
        6. Exclude this candidate by advancing to index + 1 with the original
           remaining target. This branch also runs when inclusion is too large.
           Once skipped, an index is never revisited on that path. With distinct
           candidates, each frequency combination therefore has one path,
           avoiding duplicate permutations without a set or sorting.
        7. Return the collected combinations after the search finishes.

        Example walkthrough:
            For nums=[2, 3, 5], target=7, include 2 twice to reach [2, 2]
            with remaining target 3. Skip further uses of 2 and include 3.
            The remaining target becomes zero, so save [2, 2, 3] immediately.
            Backtracking restores earlier paths and eventually also finds
            [2, 5]. No extra skips are needed after a match is found.

    Examples:
        >>> combination_sum([2, 3, 5, 4], 7)
        [[2, 2, 3], [2, 5], [3, 4]]
        >>> combination_sum([2], 1)
        []
        >>> combination_sum([2], 6)
        [[2, 2, 2]]
        >>> combination_sum([5, 2], 7)
        [[5, 2]]

    Time Complexity:
        O(2**(n + d) + L), a conservative worst-case upper bound.
        Here n = len(nums), d = target // min(nums), and L is the total
        number of elements in all returned combinations.
        Each recursion path has at most d selections and n skips. With at
        most two branches per call, this bounds the search by a binary tree
        of depth n + d. Copying successful combinations contributes L work.
        The fit check and early return can make the actual search much smaller.

        Example: O(2**(n + d) + L) is
                 nums=[2, 3, 5], target=7 gives n=3 and d=7 // 2=3.


    Space Complexity:
        O(n + d) auxiliary space: the recursion stack has depth O(n + d),
        and the shared working combination contains at most d elements.
        Here n is the number of candidates and d is target // min(nums).
        A single path can nest up to n skip calls and d include calls.
        Parent calls remain on the stack until their children return, so both
        kinds of calls use space. The working list adds O(d) space, which
        keeps the combined auxiliary bound at O(n + d).
        Saved copies take O(L) space, so total space is O(n + d + L).
        Since target is positive, every returned combination is nonempty;
        L also bounds the number of result-list references.

    https://www.youtube.com/watch?v=OyZFFqQtu98&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=10
    
    """
    # Step 1: Initialize the candidate count and output.
    size: int = len(nums)
    result: list[list[int]] = []

    def generate_combinations(
        index: int, remaining_target: int, combination_list: list[int]
    ) -> None:
        # Step 2: Save a snapshot as soon as the target is reached.
        if remaining_target == 0:
            result.append(combination_list.copy())
            return
        # Step 3: Stop after the last candidate, before indexing nums.
        if index == size:
            return
        # Step 4: Include a fitting candidate; keep its index to allow reuse.
        if nums[index] <= remaining_target:
            combination_list.append(nums[index])
            generate_combinations(
                index=index,
                remaining_target=remaining_target - nums[index],
                combination_list=combination_list,
            )
            # Step 5: Undo this inclusion before exploring exclusion.
            combination_list.pop()

        # Step 6: Skip this candidate permanently on the current path.
        generate_combinations(
            index=index + 1,
            remaining_target=remaining_target,
            combination_list=combination_list,
        )

    # Steps 1 and 7: Search from the empty combination and return all matches.
    generate_combinations(index=0, remaining_target=target, combination_list=[])
    return result


def solve() -> None:
    # nums: list[int] = [2, 3, 5, 4]
    # target: int = 7
    # expected: list[list[int]] = [[2, 2, 3], [2, 5], [3, 4]]
    # result: list[list[int]] = combination_sum(nums, target)

    # Ignore ordering within and between combinations, but preserve duplicates.
    # assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # Minimum length, candidate value, and target: no solution.
    nums = [2]
    target = 1
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single candidate exactly matches.
    nums = [2]
    target = 2
    expected = [[2]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single candidate must be reused.
    nums = [2]
    target = 6
    expected = [[2, 2, 2]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single candidate leaves an unreachable remainder.
    nums = [2]
    target = 7
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target and longest possible combination.
    nums = [2]
    target = 40
    expected = [[2] * 20]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum candidate equals maximum target.
    nums = [40]
    target = 40
    expected = [[40]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum candidate exceeds target.
    nums = [40]
    target = 39
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example with unsorted candidates.
    nums = [2, 3, 5, 4]
    target = 7
    expected = [[2, 2, 3], [2, 5], [3, 4]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple combinations and repeated candidates.
    nums = [3, 4, 5, 6]
    target = 10
    expected = [[3, 3, 4], [4, 6], [5, 5]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different frequencies count separately, permutations do not.
    nums = [2, 3, 5]
    target = 8
    expected = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only matching candidate is at the beginning.
    nums = [7, 8, 9]
    target = 7
    expected = [[7]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only matching candidate is in the middle.
    nums = [8, 7, 9]
    target = 7
    expected = [[7]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only matching candidate is at the end.
    nums = [8, 9, 7]
    target = 7
    expected = [[7]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Skip a large first candidate and reuse a later candidate.
    nums = [9, 2, 3]
    target = 7
    expected = [[2, 2, 3]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending candidates produce the same unique combinations.
    nums = [5, 3, 2]
    target = 8
    expected = [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every candidate is greater than target.
    nums = [4, 5, 6]
    target = 3
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Candidates smaller than target still cannot form it.
    nums = [4, 6]
    target = 7
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated use of a later candidate after skipping earlier ones.
    nums = [9, 4]
    target = 12
    expected = [[4, 4, 4]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with minimum target.
    nums = list(range(11, 41))
    target = 1
    expected = []
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with minimum candidate and a matching singleton.
    nums = list(range(2, 32))
    target = 2
    expected = [[2]]
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and target with many distinct solutions.
    nums = list(range(11, 41))
    target = 40
    expected = (
        [[40]]
        + [[value, 40 - value] for value in range(11, 21)]
        + [
            [11, 11, 18],
            [11, 12, 17],
            [11, 13, 16],
            [11, 14, 15],
            [12, 12, 16],
            [12, 13, 15],
            [12, 14, 14],
            [13, 13, 14],
        ]
    )
    result = combination_sum(nums, target)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(combination) for combination in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
