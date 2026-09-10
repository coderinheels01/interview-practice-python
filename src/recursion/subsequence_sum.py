"""Subsequences With a Target Sum

Recursion practice variant related to LeetCode 40: Combination Sum II.
Related problem: https://leetcode.com/problems/combination-sum-ii/
This is a custom subsequence exercise, not the exact LeetCode statement.

Given an integer array ``nums`` and an integer ``target``, return every
subsequence whose elements add up to ``target``. Use recursion.

A subsequence selects zero or more elements without changing their original
relative order. Selected elements do not need to be adjacent. Each array
position may be selected at most once.

Return the subsequences in any order, preserving element order within each
subsequence. Selections using different positions are separate results, even
when their values are identical. Include the empty subsequence when target
is zero. Return an empty list if there are no matching subsequences.

Unlike this exercise, LeetCode 40 requests unique combinations and uses
different constraints. The constraints below belong to this practice variant.

Example 1:
    Input: nums = [1, 2, 1], target = 2
    Output: [[1, 1], [2]]
    Explanation: Select the first and last elements, or just the middle one.

Example 2:
    Input: nums = [1, 1], target = 1
    Output: [[1], [1]]
    Explanation: Each position independently supplies a matching subsequence.

Example 3:
    Input: nums = [1, 2], target = 4
    Output: []

Example 4:
    Input: nums = [0], target = 0
    Output: [[], [0]]

Practice constraints:
    - 1 <= nums.length <= 10
    - -10 <= nums[i] <= 10
    - -100 <= target <= 100
    - Duplicate values are allowed.
"""

from functools import cache


def subsequences_with_sum(nums: list[int], target: int) -> list[list[int]]:
    """Return all subsequences whose sum equals target, preserving input order.

    Args:
        nums: Integers under the module's practice constraints; duplicates,
            negative values, and zeros are allowed. The list is not modified.
        target: Required sum, including negative values and zero.

    Returns:
        Independent lists for every matching position selection. Equal values
        at different positions can produce duplicate lists. The empty selection
        is included when target is zero; no matches produces an empty list.

    Approach:
        Depth-First Search with Backtracking (include/exclude recursion).
        1. Initialize the output and an empty path with sum zero.
        2. At a leaf, all positions have been considered. Copy the path into
           the output if its sum matches, then return. Copying prevents later
           backtracking from changing a stored result.
        3. Include the current element and recursively explore the next index.
        4. Undo the inclusion, then explore excluding the current element.
           Increasing indices preserve order and use each position at most once.
           Check sums only at leaves: zeros and negative values can extend or
           correct a partial sum, so overshooting is not a stopping condition.
        5. Return all matches after both branches have been explored.

    Examples:
        >>> subsequences_with_sum([1, 2, 1], 2)
        [[1, 1], [2]]
        >>> subsequences_with_sum([1, 1], 1)
        [[1], [1]]
        >>> subsequences_with_sum([0], 0)
        [[0], []]
        >>> subsequences_with_sum([1, 2], 4)
        []

    Time Complexity:
        O(2**n + L), where n is len(nums) and L is the total number of
        elements copied into matching lists. The recursion visits a binary
        tree with 2**n leaves. Worst case: O(n * 2**n), including copies.

    Space Complexity:
        O(n) auxiliary space for the recursion stack and shared path.
        Output uses O(k + L) for k result lists and their elements; total
        space is O(n + k + L), or O(n * 2**n) in the worst case.
    """
    # Step 1: Initialize the output and input size.
    result: list[list[int]] = []
    size: int = len(nums)

    def generate_subsets(index: int, sub_set_sum: int, sub_set: list[int]) -> None:
        # Step 2: Record a copy only at a matching leaf.
        if index >= size:
            if sub_set_sum == target:
                result.append(sub_set.copy())
            return

        # Step 3: Explore selections that include this position.
        sub_set.append(nums[index])
        sub_set_sum += nums[index]
        generate_subsets(index=index + 1, sub_set_sum=sub_set_sum, sub_set=sub_set)
        # Step 4: Restore the path and sum before excluding this position.
        sub_set.pop()
        sub_set_sum -= nums[index]
        generate_subsets(index=index + 1, sub_set_sum=sub_set_sum, sub_set=sub_set)

    # Steps 1 and 5: Search from the empty path, then return all matches.
    generate_subsets(0, 0, [])
    return result


def find_one_unique_subsequences_with_sum(
    nums: list[int], target: int
) -> list[list[int]]:
    """Return the first matching subsequence found by include-first search.

    Args:
        nums: Integers under the module's practice constraints; duplicates,
            negative values, and zeros are allowed. The list is not modified.
        target: Required sum, including negative values and zero.

    Returns:
        One flat list of selected values in input order, despite the current
        nested-list return annotation. Returns [] for no match or an empty
        match. The name does not mean that all distinct subsequences are
        returned: this function stops after its first successful leaf.

    Approach:
        Depth-First Search with Backtracking and early termination.
        1. Initialize an empty result and begin with an empty path and sum zero.
        2. At a leaf, keep the path and signal success if its sum matches;
           otherwise signal failure. The result references the shared path,
           which remains intact because successful branches return immediately.
        3. Include the current element and search the next index. Propagate
           success immediately without undoing the successful path.
        4. If inclusion fails, undo it and search the exclusion branch.
           Propagate success if found. If both branches fail, the helper
           implicitly returns None, which callers currently treat as false.
           Leaf-only checks allow zeros and negative values to extend matches.
        5. Return the selected path, or the initial empty result on failure.

    Examples:
        >>> find_one_unique_subsequences_with_sum([1, 2, 1], 2)
        [1, 1]
        >>> find_one_unique_subsequences_with_sum([1, 1], 1)
        [1]
        >>> find_one_unique_subsequences_with_sum([1, -1, 0], 0)
        [1, -1, 0]
        >>> find_one_unique_subsequences_with_sum([1, 2], 0)
        []
        >>> find_one_unique_subsequences_with_sum([1, 2], 4)
        []

    Time Complexity:
        O(2**n) worst case for the binary decision tree, where n is len(nums).
        A match on the first leaf takes O(n); early termination does not
        guarantee that fewer than exponentially many nodes are visited.

    Space Complexity:
        O(n) for the recursion stack and shared path. The returned path has
        at most n elements and is not copied, so total space remains O(n).
    """
    # Step 1: Initialize the search state.
    size: int = len(nums)
    result: list[int] = []

    def generate_unique_subsequence(
        index: int, subset_sum: int, subset: list[int]
    ) -> bool:
        nonlocal result
        # Step 2: Keep the first matching leaf and signal success.
        if index >= size:
            if subset_sum == target:
                result = subset
                return True
            return False

        # Step 3: Include this position; return immediately on success.
        subset.append(nums[index])
        subset_sum += nums[index]

        if generate_unique_subsequence(
            index=index + 1, subset_sum=subset_sum, subset=subset
        ):
            return True

        # Step 4: Undo the failed inclusion and explore exclusion.
        subset.pop()
        subset_sum -= nums[index]

        if generate_unique_subsequence(
            index=index + 1, subset_sum=subset_sum, subset=subset
        ):
            return True

            return False

    # Steps 1 and 5: Run the search and return its selected path.
    generate_unique_subsequence(index=0, subset_sum=0, subset=[])

    return result


def count_subsequences_with_sum(nums: list[int], target: int) -> int:
    """Count position selections whose elements sum to target.

    Args:
        nums: Integers under the module's practice constraints; duplicates,
            negative values, and zeros are allowed. The list is not modified.
        target: Required sum, including negative values and zero.

    Returns:
        The number of matching subsequences. Different position selections
        count separately even when values are identical. The empty selection
        contributes one when target is zero. No matches returns zero.

    Approach:
        Top-Down Dynamic Programming (memoized include/exclude recursion).
        1. Start at index zero with sum zero. The inner helper's @cache stores
           a count for each (index, subset_sum) pair. A repeated pair returns
           its saved count without executing the helper body again. Each outer
           call creates a fresh cache for its nums and target, which must stay
           unchanged during the search. Each uncached call owns its local count.
        2. At a leaf, return one if the sum matches, otherwise zero.
        3. Include the current element and add the count from the next index.
        4. Restore the sum to exclude that element, then add the count from
           the next index. The two branches represent disjoint selections,
           so adding their counts neither misses nor double-counts positions.
           Do not stop at an intermediate match or overshoot: zeros and
           negative values can create additional matching selections.
        5. Return the combined count; @cache saves it for this argument pair.
           Each parent adds that count separately, so reusing a cached result
           still counts different position selections separately. No actual
           subsequence lists are stored.

        For nums=[1, 1, 2] and target=3, choosing either of the first two
        positions alone reaches (index=2, subset_sum=1). The first call finds
        one completion (include 2); the second reuses that cached count of 1.
        Both parent branches add it, giving two matching selections.

    Examples:
        >>> count_subsequences_with_sum([1, 2, 1], 2)
        2
        >>> count_subsequences_with_sum([1, 1, 1], 2)
        3
        >>> count_subsequences_with_sum([0], 0)
        2
        >>> count_subsequences_with_sum([10, -10, 2], 2)
        2
        >>> count_subsequences_with_sum([1, 2], 4)
        0

    Time Complexity:
        O(S), where S is the number of reachable (index, subset_sum) states:
        each state is computed once and makes at most two cached calls.
        Let n = len(nums) and A = sum(abs(value) for value in nums). All sums
        lie between -A and A, so S <= (n + 1) * (2*A + 1), giving an
        O(n * (A + 1)) bound. With |nums[i]| <= 10, A <= 10*n, so this
        bound becomes O(n**2). Without bounded values, distinct states can
        still grow exponentially. Arithmetic and cache lookup are treated
        as constant time under the practice constraints.

    Space Complexity:
        O(S + n): the cache stores S argument pairs and counts, while the
        recursion stack has depth O(n). This is O(n * (A + 1)), or O(n**2)
        with the stated element bounds. No subsequence lists are stored.
    """
    # Step 1: Set up the input size and a fresh cache for this search.
    size: int = len(nums)

    # Step 1: Reuse the saved count whenever (index, subset_sum) repeats.
    @cache
    def count_subsequences(index: int, subset_sum: int) -> int:
        count: int = 0
        # Step 2: Each matching leaf contributes exactly one selection.
        if index >= size:
            if subset_sum == target:
                count += 1
            return count

        # Step 3: Count selections that include this position.
        subset_sum += nums[index]
        count += count_subsequences(index=index + 1, subset_sum=subset_sum)
        # Step 4: Restore the sum and count selections excluding it.
        subset_sum -= nums[index]
        count += count_subsequences(index=index + 1, subset_sum=subset_sum)
        # Step 5: Return both branch counts; @cache remembers this result.
        return count

    return count_subsequences(index=0, subset_sum=0)


def solve() -> None:
    nums: list[int] = [1, 2, 1]
    target: int = 2
    expected: list[list[int]] = [[1, 1], [2]]
    result: list[list[int]] = subsequences_with_sum(nums, target)

    # Allow any result order while preserving subsequence order and duplicates.
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length, zero target, and empty subsequence.
    nums = [0]
    target = 0
    expected = [[], [0]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [0]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element matches the minimum element value.
    nums = [-10]
    target = -10
    expected = [[-10]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [-10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element matches the maximum element value.
    nums = [10]
    target = 10
    expected = [[10]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element does not match.
    nums = [1]
    target = 2
    expected = []
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [1]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the empty subsequence matches zero.
    nums = [1, 2]
    target = 0
    expected = [[]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [1, 2]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal example: nonadjacent pair and middle singleton.
    nums = [1, 2, 1]
    target = 2
    expected = [[1, 1], [2]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [1, 2, 1]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the beginning.
    nums = [2, 4, 8]
    target = 2
    expected = [[2]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [2, 4, 8]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the end.
    nums = [4, 8, 2]
    target = 2
    expected = [[2]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [4, 8, 2]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical values at different positions stay separate.
    nums = [1, 1, 1]
    target = 2
    expected = [[1, 1], [1, 1], [1, 1]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [1, 1, 1]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unreachable target despite multiple elements.
    nums = [2, 4]
    target = 3
    expected = []
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [2, 4]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative values and a negative target.
    nums = [-1, -2, -3]
    target = -3
    expected = [[-1, -2], [-3]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [-1, -2, -3]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A partial sum above target can later decrease to it.
    nums = [10, -10, 2]
    target = 2
    expected = [[10, -10, 2], [2]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [10, -10, 2]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cancellation and zero extend an already matching sum.
    nums = [1, -1, 0]
    target = 0
    expected = [[], [0], [1, -1], [1, -1, 0]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [1, -1, 0]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Preserve original element order in a matching pair.
    nums = [3, 1, 2]
    target = 4
    expected = [[3, 1]]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [3, 1, 2]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and maximum target, requiring every element.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = 100
    expected = [[10] * 10]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and minimum target, requiring every element.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = -100
    expected = [[-10] * 10]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target is unreachable for this input.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = 100
    expected = []
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum target is unreachable for this input.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = -100
    expected = []
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    from math import comb

    # Maximum length with all zeros: all 1024 position selections match.
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    target = 0
    expected = [[0] * length for length in range(11) for _ in range(comb(10, length))]
    result = subsequences_with_sum(nums, target)

    assert sorted(result) == sorted(expected)
    assert nums == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert len({id(subsequence) for subsequence in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Contract: return one flat subsequence, the first found by include-first
    # search at a leaf; return [] when no match exists (also the empty match).

    # Minimum length with a matching positive value.
    nums = [10]
    target = 10
    expected = [10]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length with a matching negative value.
    nums = [-10]
    target = -10
    expected = [-10]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero is selected before the empty subsequence.
    nums = [0]
    target = 0
    expected = [0]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element does not match.
    nums = [1]
    target = 2
    expected = []
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal example: return the first include-first match.
    nums = [1, 2, 1]
    target = 2
    expected = [1, 1]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 2, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the beginning.
    nums = [2, 4, 8]
    target = 2
    expected = [2]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [2, 4, 8]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton in the middle.
    nums = [4, 2, 8]
    target = 2
    expected = [2]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [4, 2, 8]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the end.
    nums = [4, 8, 2]
    target = 2
    expected = [2]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [4, 8, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicates: return one matching subsequence.
    nums = [1, 1, 1]
    target = 2
    expected = [1, 1]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 1, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No combination reaches the target.
    nums = [2, 4]
    target = 3
    expected = []
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [2, 4]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the empty subsequence matches zero.
    nums = [1, 2]
    target = 0
    expected = []
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative target with multiple possible matches.
    nums = [-1, -2, -3]
    target = -3
    expected = [-1, -2]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-1, -2, -3]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An overshoot can be corrected by a later negative value.
    nums = [10, -10, 2]
    target = 2
    expected = [10, -10, 2]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, -10, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero and cancellation extend a matching prefix.
    nums = [1, -1, 0]
    target = 0
    expected = [1, -1, 0]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, -1, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Keep original order in the returned subsequence.
    nums = [3, 1, 2]
    target = 4
    expected = [3, 1]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [3, 1, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and maximum target require every element.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = 100
    expected = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and minimum target require every element.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = -100
    expected = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target is unreachable.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = 100
    expected = []
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum target is unreachable.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = -100
    expected = []
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of identical zeros returns the full first match.
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    target = 0
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result = find_one_unique_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Normal example with two matching selections.
    nums = [1, 2, 1]
    target = 2
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 2, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length and maximum element value match.
    nums = [10]
    target = 10
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum length and minimum element value match.
    nums = [-10]
    target = -10
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero counts both the selected and empty subsequences.
    nums = [0]
    target = 0
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element cannot be selected twice.
    nums = [1]
    target = 2
    expected = 0
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the empty subsequence matches zero.
    nums = [1, 2]
    target = 0
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the beginning.
    nums = [2, 4, 8]
    target = 2
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [2, 4, 8]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton in the middle.
    nums = [4, 2, 8]
    target = 2
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [4, 2, 8]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Matching singleton at the end.
    nums = [4, 8, 2]
    target = 2
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [4, 8, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values at different positions count separately.
    nums = [1, 1]
    target = 1
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All-identical values allow multiple matching pairs.
    nums = [1, 1, 1]
    target = 2
    expected = 3
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 1, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No selection reaches the target.
    nums = [2, 4]
    target = 3
    expected = 0
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [2, 4]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative target has singleton and multi-element matches.
    nums = [-1, -2, -3]
    target = -3
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-1, -2, -3]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A later negative value can undo an overshoot.
    nums = [10, -10, 2]
    target = 2
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, -10, 2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A later positive value can undo an undershoot.
    nums = [-10, 10, -2]
    target = -2
    expected = 2
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10, 10, -2]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cancellation and zero count the empty selection and extensions.
    nums = [1, -1, 0]
    target = 0
    expected = 4
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, -1, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zeros before and after a match multiply its selections.
    nums = [0, 1, 0]
    target = 1
    expected = 4
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0, 1, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonadjacent elements form a matching subsequence.
    nums = [3, 10, 1]
    target = 4
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [3, 10, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and maximum target require every element.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = 100
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length and minimum target require every element.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = -100
    expected = 1
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum target is unreachable with negative elements.
    nums = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    target = 100
    expected = 0
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum target is unreachable with positive elements.
    nums = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    target = -100
    expected = 0
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length with duplicate values counts every five-position choice.
    nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    target = 5
    expected = 252
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length of zeros counts all 1024 position selections.
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    target = 0
    expected = 1024
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros cannot reach a nonzero target.
    nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    target = 1
    expected = 0
    result = count_subsequences_with_sum(nums, target)

    assert result == expected
    assert nums == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
