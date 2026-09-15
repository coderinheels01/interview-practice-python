"""46. Permutations

Given an array nums of distinct integers, return all possible permutations.
The answer may be returned in any order.

A permutation is an ordering of all elements of nums, using each element
exactly once. Order within a permutation matters: [1, 2] and [2, 1] are
different permutations.

Example 1:
    Input: nums = [1, 2, 3]
    Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3],
             [2, 3, 1], [3, 1, 2], [3, 2, 1]]

Example 2:
    Input: nums = [0, 1]
    Output: [[0, 1], [1, 0]]

Example 3:
    Input: nums = [1]
    Output: [[1]]

Input requirement:
    - All integers in nums are distinct.
    - Numeric and length constraints are not shown in the provided screenshot.

https://www.youtube.com/watch?v=YK78FU5Ffjw&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=14
"""


def permutations(nums: list[int]) -> list[list[int]]:
    """Return every ordering of the distinct integers in nums.

    Args:
        nums: A list of distinct integers. Negative values and zero are
            supported. The function does not modify the input list.

    Returns:
        Independent lists, each containing every input element exactly once.
        Order within a permutation matters. Results follow input-index search
        order; the problem allows any order for the outer list. Distinct input
        values are required to avoid duplicate value permutations.

    Approach:
        Depth-First Search with Backtracking and a used-position array.
        1. Initialize the output, an empty current_permutation, and a boolean
           used list. used[index] indicates whether that input position is
           already selected in the current recursion path. The nested helper
           shares this list through its enclosing scope.
        2. When current_permutation contains len(nums) elements, save a copy
           and return. Copying preserves the completed ordering while later
           append/pop operations change the shared working list.
        3. Loop over every input index and skip positions already marked used.
           Each level starts scanning from zero because any unused element
           can occupy the next position, including an earlier input element.
        4. Append an unused element and mark its position used. Recursively
           fill the next position. The parent loop waits for this child to
           finish, so the search explores one branch deeply before another.
        5. After recursion returns, unmark the position and pop the element.
           Restoring both structures lets sibling branches choose it again
           without allowing repeated use within a single permutation.
        6. Return the collected permutations after the search finishes.

        Example walkthrough:
            For [1, 2, 3], choose 1, then 2, then 3 and save [1, 2, 3].
            Undo choosing 3, then undo choosing 2. With [1] still selected,
            choose 3 and then 2 to save [1, 3, 2]. After all branches starting
            with 1 finish, restore the empty working list and explore branches
            starting with 2 and then 3. The used flags follow each choice and
            are reset as recursion returns.

    Examples:
        >>> permutations([1, 2, 3])
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        >>> permutations([0, 1])
        [[0, 1], [1, 0]]
        >>> permutations([1])
        [[1]]
        >>> permutations([-1, 0])
        [[-1, 0], [0, -1]]

    Time Complexity:
        O(n * n!), where n = len(nums). The first position has n choices,
        the next has n - 1, and so on, producing n! complete permutations.
        Each completed permutation copies n elements; appending that copy
        costs amortized O(1). Nonterminal calls scan n indices each. There
        are O(n!) such calls in total, so their loop work also fits this
        bound. Loop work and copying costs add, not multiply together.

    Space Complexity:
        O(n * n!) total space, dominated by the n! saved lists of length n.
        Auxiliary space is O(n): used has n booleans, the shared working list
        holds at most n elements, and the stack has at most n + 1 active calls.
        Passing the working list to a child does not copy it. Each call adds
        one selection; unlike subset generation, there is no recursive skip
        branch because used positions are skipped directly by the for loop.
    """
    # Step 1: Initialize the output and shared used-position flags.
    size: int = len(nums)
    result: list[list[int]] = []
    used: list[bool] = [False] * size

    def generate_permutations(current_permutation: list[int]) -> None:
        # Step 2: Save a snapshot when every position has been filled.
        if len(current_permutation) == size:
            result.append(current_permutation.copy())
            return

        # Step 3: Consider every input position, skipping those already used.
        for index in range(size):
            if used[index]:
                continue
            # Step 4: Choose this value, mark its position, and recurse.
            current_permutation.append(nums[index])
            used[index] = True
            generate_permutations(current_permutation=current_permutation)
            # Step 5: Restore both the flag and working list for other branches.
            used[index] = False
            current_permutation.pop()

    # Steps 1 and 6: Start with no selections and return all completed orderings.
    generate_permutations(current_permutation=[])
    return result


def solve() -> None:
    nums: list[int] = [1, 2, 3]
    expected: list[list[int]] = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    result: list[list[int]] = permutations(nums)
    # Ignore output order while preserving the order within each permutation.
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    from itertools import permutations as expected_permutations

    # Boundary cases follow https://leetcode.com/problems/permutations/description/
    # Single positive element.
    nums = [1]
    expected = [[1]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero.
    nums = [0]
    expected = [[0]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single minimum value.
    nums = [-10]
    expected = [[-10]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single maximum value.
    nums = [10]
    expected = [[10]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements including zero.
    nums = [0, 1]
    expected = [[0, 1], [1, 0]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reversed two-element input.
    nums = [1, 0]
    expected = [[0, 1], [1, 0]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Both value boundaries.
    nums = [-10, 10]
    expected = [[-10, 10], [10, -10]]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original three-element example.
    nums = [1, 2, 3]
    expected = [list(order) for order in expected_permutations([1, 2, 3])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending input.
    nums = [3, 2, 1]
    expected = [list(order) for order in expected_permutations([1, 2, 3])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted input with zero between the boundaries.
    nums = [10, 0, -10]
    expected = [list(order) for order in expected_permutations([-10, 0, 10])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All negative values.
    nums = [-3, -1, -2]
    expected = [list(order) for order in expected_permutations([-3, -2, -1])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Four elements exercise restoration across deeper branches.
    nums = [4, 1, 3, 2]
    expected = [list(order) for order in expected_permutations([1, 2, 3, 4])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Five elements with zero and mixed signs.
    nums = [0, 2, -2, 1, -1]
    expected = [list(order) for order in expected_permutations([-2, -1, 0, 1, 2])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length includes both boundaries and produces 720 permutations.
    nums = [10, -10, 0, 1, -1, 5]
    expected = [list(order) for order in expected_permutations([-10, -1, 0, 1, 5, 10])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length in ascending order.
    nums = [1, 2, 3, 4, 5, 6]
    expected = [list(order) for order in expected_permutations([1, 2, 3, 4, 5, 6])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum length in descending order.
    nums = [6, 5, 4, 3, 2, 1]
    expected = [list(order) for order in expected_permutations([1, 2, 3, 4, 5, 6])]
    result = permutations(nums)

    assert sorted(result) == sorted(expected)
    assert len({id(order) for order in result}) == len(result)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
