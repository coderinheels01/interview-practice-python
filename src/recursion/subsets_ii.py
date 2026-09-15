"""Subsets II

Given an integer array nums that may contain duplicate values, return all
unique subsets (the power set). The answer may be returned in any order.

Include the empty subset. Each input position may be selected at most once,
so a value can appear in a subset only as many times as it appears in nums.
Different orderings of the same values represent the same subset and must
not be returned as separate results.

Example 1:
    Input: nums = [1, 2, 2]
    Output: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

Example 2:
    Input: nums = [1, 2]
    Output: [[], [1], [2], [1, 2]]

Example 3:
    Input: nums = [1, 3, 3]
    Output: [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]

Constraints:
    - 1 <= len(nums) <= 10
    - -10 <= nums[i] <= 10

https://www.youtube.com/watch?v=RIn3gOkbhQE&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=13
"""


def subsets_ii(nums: list[int]) -> list[list[int]]:
    """Return every unique subset, including the empty subset.

    Args:
        nums: Integers under the module's constraints, including negative
            values, zeros, and duplicates. The input is sorted in place.

    Returns:
        Independent lists representing unique subsets. Each position is used
        at most once, so repeated values can appear only as often as in nums.
        Subsets contain values in nondecreasing order. The problem permits
        any output order; this implementation explores sorted choices depth-first.

    Approach:
        Depth-First Search with Backtracking and duplicate skipping.
        1. Sort nums to place equal values together, initialize the result,
           and start at index zero with an empty working list named subset.
        2. Save subset.copy() at the start of every call. Every partial choice
           is a valid subset, including the initial empty list. A copy is
           necessary because append/pop later modify the same working list;
           storing its reference would let those changes affect saved results.
        3. Loop over the remaining positions starting at index. If index equals
           len(nums), the loop is empty, so the call returns naturally.
        4. Skip a value equal to its predecessor only when subset_index > index.
           This avoids duplicate choices at the same recursion depth. The first
           position of a child call is still eligible, allowing equal values
           from different positions to appear together in a subset.
        5. Append the chosen value and recurse from subset_index + 1. Advancing
           the index prevents reusing a position. The current loop waits for
           this child to finish, so traversal is depth-first, not breadth-first.
        6. Pop the chosen value after recursion returns, restoring the working
           list before the loop tries another choice.
        7. Return all saved subsets after the search completes. No set is
           needed because duplicate branches are skipped before exploration.

        Example walkthrough:
            For [1, 2, 2], first save []. Choose 1 and save [1], then choose
            the first 2 and save [1, 2]. Its child may choose the second 2,
            saving [1, 2, 2]. After backtracking to [1], skip choosing the
            second 2 at that same depth because it would repeat [1, 2].
            Back at the root, choosing the first 2 produces [2] and [2, 2];
            choosing the second 2 at the root is skipped for the same reason.

    Examples:
        >>> subsets_ii([1, 2, 2])
        [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
        >>> subsets_ii([0, 0])
        [[], [0], [0, 0]]
        >>> subsets_ii([-1, -1])
        [[], [-1], [-1, -1]]
        >>> subsets_ii([1])
        [[], [1]]

    Time Complexity:
        O(n * 2**n) worst case, where n = len(nums). There are at most 2**n
        subsets, reached when all values are distinct. Each call copies up to
        n elements and its for loop can check up to n remaining candidates.
        These costs add rather than multiply, giving an O(n) allowance per
        call. Appending the saved copy costs amortized O(1); making the copy
        costs O(k) for a subset of length k. Sorting initially costs O(n log n)
        and is dominated by the subset-generation bound. Duplicates reduce
        the number of subsets and calls.

    Space Complexity:
        O(n * 2**n) worst-case total space, dominated by saved subset copies.
        Auxiliary space is O(n): recursion has at most n + 1 active calls,
        and the single shared working list holds at most n values. Python's
        in-place sort may also use O(n) temporary space. Append/pop reuses
        the working list rather than allocating a separate list at each depth.
    """
    # Step 1: Group equal values by sorting the caller's list.
    nums.sort()
    size: int = len(nums)
    result: list[list[int]] = []

    def generate_subsets(index: int, subset: list[int]) -> None:
        # Step 2: Save a snapshot before the shared list changes.
        result.append(subset.copy())
        # Step 3: Try each remaining position; an empty range ends the call.
        for subset_index in range(index, size):
            # Step 4: Skip duplicate choices only at the current depth.
            if subset_index > index and nums[subset_index] == nums[subset_index - 1]:
                continue

            # Step 5: Choose a value and explore beyond its position.
            subset.append(nums[subset_index])
            generate_subsets(index=subset_index + 1, subset=subset)
            # Step 6: Undo this choice before trying the next one.
            subset.pop()

    # Steps 1 and 7: Start with the empty subset and return all snapshots.
    generate_subsets(index=0, subset=[])
    return result


def solve() -> None:
    nums: list[int] = [1, 2, 2]
    expected: list[list[int]] = [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    result: list[list[int]] = subsets_ii(nums)
    # Ignore ordering while still detecting duplicate or missing subsets.
    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    from itertools import combinations

    # Minimum length with zero.
    nums = [0]
    expected = [[], [0]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length with minimum value.
    nums = [-10]
    expected = [[], [-10]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length with maximum value.
    nums = [10]
    expected = [[], [10]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Distinct values from the second example.
    nums = [1, 2]
    expected = [[], [1], [2], [1, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values from the first example.
    nums = [1, 2, 2]
    expected = [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Third example preserves both copies of three.
    nums = [1, 3, 3]
    expected = [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All equal values allow each frequency exactly once.
    nums = [2, 2, 2]
    expected = [[], [2], [2, 2], [2, 2, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated zeros must not collapse subsets of different lengths.
    nums = [0, 0]
    expected = [[], [0], [0, 0]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative duplicates mixed with zero.
    nums = [-1, 0, -1]
    expected = [[], [-1], [-1, -1], [0], [-1, 0], [-1, -1, 0]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicates at the beginning.
    nums = [1, 1, 2]
    expected = [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicates at the end.
    nums = [2, 1, 1]
    expected = [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separated duplicates in unsorted input.
    nums = [1, 2, 1]
    expected = [[], [1], [1, 1], [2], [1, 2], [1, 1, 2]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two duplicate groups allow independent frequencies.
    nums = [2, 1, 2, 1]
    expected = [[1] * ones + [2] * twos for ones in range(3) for twos in range(3)]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Distinct minimum, zero, and maximum values.
    nums = [10, 0, -10]
    expected = [[], [-10], [0], [10], [-10, 0], [-10, 10], [0, 10], [-10, 0, 10]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending distinct values.
    nums = [3, 2, 1]
    expected = [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all zeros.
    nums = [0] * 10
    expected = [[0] * count for count in range(11)]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all minimum values.
    nums = [-10] * 10
    expected = [[-10] * count for count in range(11)]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with all maximum values.
    nums = [10] * 10
    expected = [[10] * count for count in range(11)]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with two repeated boundary values.
    nums = [10, -10] * 5
    expected = [
        [-10] * negatives + [10] * positives
        for negatives in range(6)
        for positives in range(6)
    ]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with distinct values yields 1024 subsets.
    nums = list(range(-5, 5))
    expected = [
        list(subset)
        for length in range(11)
        for subset in combinations(range(-5, 5), length)
    ]
    result = subsets_ii(nums)

    assert sorted(map(sorted, result)) == sorted(map(sorted, expected))
    assert len({id(subset) for subset in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
