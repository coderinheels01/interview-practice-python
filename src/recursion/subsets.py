"""78. Subsets

Source: https://leetcode.com/problems/subsets/

Given an array of distinct integers named ``nums``, return every subset,
including the empty subset and the entire array. This collection is called
the power set. Include each subset exactly once; output order does not matter.

Practice context:
    Generate the subsets using recursion and print the returned collection
    in solve(). Keeping selected elements in their original array order
    also represents all subsequences for this distinct-element input.
    LeetCode asks for the collection to be returned, rather than only printed.

Example 1:
    Input: nums = [1, 2, 3]
    Output: [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

Example 2:
    Input: nums = [0]
    Output: [[], [0]]

Constraints:
    - 1 <= nums.length <= 10
    - -10 <= nums[i] <= 10
    - Every element in nums is distinct.
"""


def subsets(nums: list[int]) -> list[list[int]]:
    """Return every subset of an array of distinct integers.

    Approach: Backtracking (Include/Exclude, Depth-First Search)
        1. Create the result list and record the input length.
        2. Define a recursive helper with the next index to consider and
           a shared working list, sub_array. On entry, this list contains
           exactly the elements selected from earlier indexes.
        3. When all indexes have been considered, append a shallow copy
           of sub_array to result and return. The copy preserves this
           completed subset while later calls change the working list.
           Copying the list is sufficient because its integers are immutable.
        4. Include nums[index] by appending it, then recurse on index + 1
           to explore every subset containing this element for this prefix.
        5. Backtrack by popping the last element. This undoes the append
           and restores the working list to its state on helper entry.
        6. Exclude nums[index] by recursing on index + 1 with the restored
           working list. Together, the two branches cover both choices
           for every element, producing exactly 2^n completed subsets.
        7. Start the helper at index zero with an empty working list.
        8. Return the collected subsets. The include branch runs first,
           so the full input is recorded first and the empty subset last.

    Parameters:
        nums: A list of 1 to 10 distinct integers, each between -10 and 10.

    Returns:
        A list of all 2^n subsets, including the empty subset and the full
        input. Elements within each subset retain their input order.
        Each subset is a separate list; changing one does not change another.
        LeetCode accepts any ordering of the returned subsets.

    Mutation Behavior:
        nums is not modified. The helper mutates only its working list and
        the local result list. Stored subsets are copies, not references
        to the shared working list that becomes empty after backtracking.

    Time Complexity:
        O(n * 2^n), where n is len(nums). The recursion tree has 2^n
        leaves and O(2^n) total calls. Copying a subset of length k costs
        O(k); across all leaves, n * 2^(n - 1) element references are
        copied because each input element appears in half the subsets.
        List append and removal from the end with pop take amortized
        O(1) time each. Copying the output dominates the total cost.

    Space Complexity:
        O(n) auxiliary space excluding the returned output: the working
        list holds at most n elements and the recursion stack has at most
        n + 1 helper frames. Each frame holds an index, a reference to the
        shared list, and constant bookkeeping. The two branches execute
        sequentially and share the same working list.
        Including output, space is O(n * 2^n): result holds 2^n separate
        lists with n * 2^(n - 1) element references in total.

    Assumptions:
        Inputs satisfy the stated constraints; no validation is performed.
        Distinct input values ensure that distinct include/exclude choices
        produce distinct subsets. Duplicate input values are outside the
        constraints and are not deduplicated by this implementation.
    """
    # Step 1: Prepare the output collection and input length.
    result: list[list[int]] = []
    size: int = len(nums)

    # Step 2: Track the next index and the choices made so far.
    def generate_subsets(index: int, sub_array: list[int]):
        # Step 3: Save an independent snapshot after deciding every index.
        if index >= size:
            result.append(sub_array.copy())
            return

        # Step 4: Include the current element and explore that branch.
        sub_array.append(nums[index])
        generate_subsets(index=index + 1, sub_array=sub_array)
        # Step 5: Undo the inclusion to restore the previous working list.
        sub_array.pop()
        # Step 6: Explore the branch that excludes the current element.
        generate_subsets(index=index + 1, sub_array=sub_array)

    # Step 7: Begin with no elements selected.
    generate_subsets(index=0, sub_array=[])
    # Step 8: Return all completed subsets.
    return result


def solve() -> None:
    nums: list[int] = [1, 2, 3]
    expected: list[list[int]] = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    result: list[list[int]] = subsets(nums)

    # Compare without requiring a particular subset or element order.
    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length with zero (Example 2).
    nums = [0]
    expected = [[], [0]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [0]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum allowed element value.
    nums = [-10]
    expected = [[], [-10]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [-10]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum allowed element value.
    nums = [10]
    expected = [[], [10]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [10]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements exercise every include/exclude combination.
    nums = [10, -10]
    expected = [[], [10], [-10], [10, -10]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [10, -10]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All negative values in unsorted order.
    nums = [-1, -3, -2]
    expected = [[], [-1], [-3], [-2], [-1, -3], [-1, -2], [-3, -2], [-1, -3, -2]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [-1, -3, -2]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Mixed signs, zero, and both value boundaries.
    nums = [10, 0, -10]
    expected = [[], [10], [0], [-10], [10, 0], [10, -10], [0, -10], [10, 0, -10]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [10, 0, -10]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal positive input (Example 1).
    nums = [1, 2, 3]
    expected = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert nums == [1, 2, 3]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length: independently build all 1024 expected subsets by size.
    from itertools import combinations

    nums = [10, -10, 0, 7, -7, 3, -3, 1, -1, 5]
    expected = [
        list(combination)
        for length in range(len(nums) + 1)
        for combination in combinations(nums, length)
    ]
    result = subsets(nums)

    assert sorted(tuple(sorted(subset)) for subset in result) == sorted(
        tuple(sorted(subset)) for subset in expected
    )
    assert len(result) == 1024
    assert nums == [10, -10, 0, 7, -7, 3, -3, 1, -1, 5]
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
