"""Maximum Sum of Non-Adjacent Elements

Given a list nums containing n integers, return the maximum sum of a
subsequence such that no two selected elements are adjacent in the original
list. Selected indexes must differ by at least 2.

A subsequence is formed by deleting zero or more elements while keeping
the remaining elements in their original order. Adjacency is determined
by positions in the original list, not by the values of the elements.

Example 1 (from the question):
    Input: nums = [1, 2, 4]
    Output: 5
    Explanation:
        Select indexes 0 and 2: 1 + 4 = 5.
        These indexes are not adjacent, and 5 is greater than selecting 2.

Example 2 (from the question):
    Input: nums = [2, 1, 4, 9]
    Output: 11
    Explanation:
        Select the values 2 and 9 at indexes 0 and 3.
        They are not adjacent, and their sum is 11, the maximum possible.

Example 3 (additional):
    Input: nums = [8]
    Output: 8
    Explanation: The only element can be selected.

Example 4 (additional):
    Input: nums = [3, 9]
    Output: 9
    Explanation: The elements are adjacent, so select only the larger one.

Example 5 (additional):
    Input: nums = [0, 0, 0]
    Output: 0
    Explanation: Every possible selection has a sum of 0.

Example 6 (additional):
    Input: nums = [5, 5, 5, 5, 5]
    Output: 15
    Explanation: Select indexes 0, 2, and 4: 5 + 5 + 5 = 15.

Example 7 (additional):
    Input: nums = [1, 10, 1]
    Output: 10
    Explanation: Selecting the middle value beats selecting both endpoints.

Example 8 (additional):
    Input: nums = [4, 1, 1, 4]
    Output: 8
    Explanation:
        Select indexes 0 and 3: 4 + 4 = 8.
        Selected indexes do not have to be exactly two positions apart.

Input Format (original problem):
    The first line contains t, the number of test cases.
    For each test case:
        The first line contains n, the number of elements.
        The second line contains n space-separated integers.

Output Format:
    For each test case, output the maximum sum of non-adjacent elements.

Constraints:
    - 1 <= t <= 500
    - 1 <= n <= 1000
    - 0 <= nums[i] <= 100000
    - Time limit: 1 second.

Original Sample Input:
    2
    3
    1 2 4
    4
    2 1 4 9

Original Sample Output:
    5
    11



                                  f(4)
                     Pick 4 /              \\ Skip 4
                           /                \
                        f(2)                f(3)
                Pick 2 /   \\ Skip 2  Pick 3 /   \\ Skip 3
                      /     \\             /     \
                   f(0)     f(1)        f(1)     f(2)
                         P /   \\ S    P /   \\ S  P /   \\ S
                          /     \\      /     \\    /     \
                       f(-1)   f(0) f(-1)   f(0) f(0)   f(1)
                                                      P /   \\ S
                                                       /     \
                                                    f(-1)   f(0)
"""


def maximum_sum_non_adjacent_elements_recursion(nums: list[int]) -> int:
    """Return the largest sum obtainable without selecting adjacent elements.

    Approach: Naive Recursion (Pick or Skip)
        1. Define a helper that finds the best sum using indexes 0 through
           index. That index is a candidate, not an element we must pick.
        2. If the index is 0, return nums[0]. Only that element remains,
           and values are nonnegative. If the index is negative, return 0:
           no elements remain to contribute to the sum. This return happens
           before accessing the list, so a negative helper index is safe.
        3. Try picking the current element. Add its value to the best sum
           through index - 2. Skipping the immediate neighbor prevents
           adjacent selections. The smaller call can still pick OR skip its
           own current element, so earlier choices are not forced.
        4. Try skipping the current element. Add 0 and find the best sum
           through index - 1. That neighbor is now available to select.
        5. Return the larger of the pick and skip totals. Each smaller call
           makes its own choices, so we can select more than two elements.
        6. Start at the last index and return the helper's answer.

        Example: nums = [5, 1, 5, 1, 5].
            Pick index 4: add 5 and continue at index 2.
            Pick index 2: add 5 and continue at index 0.
            At index 0, return 5. This route totals 15.
            Other routes are compared too; 15 is the largest valid sum.

    Parameters:
        nums: A list of 1 through 1000 integers, each from 0 through 100000.

    Returns:
        Maximum sum of elements whose original indexes are not adjacent.
        Returns 0 when all values are zero.

    Mutation Behavior:
        Reads nums without changing it or any other caller-owned data.

    Time Complexity: O(2^n)
        Here n is len(nums). Each non-base call explores picking and skipping,
        repeating earlier calculations. This exponential approach is too slow
        for the maximum input size of 1000.

    Space Complexity: O(n)
        Up to n recursive calls can be waiting at once. They share the same
        input list, which is excluded from extra space.

    Assumptions:
        Inputs satisfy the stated nonempty, nonnegative constraints. Python
        must have enough recursion depth; a size of 1000 can exceed the usual
        recursion limit. Arithmetic is treated as constant cost for this range.
    """

    # Step 1: Find the best sum from index 0 through the candidate index.
    def max_non_adjacent_sum(index: int) -> int:
        # Step 2: Handle the last remaining element or no remaining elements.
        if index == 0:
            return nums[index]
        if index < 0:
            return 0

        # Step 3: Select this value and exclude its immediate neighbor.
        pick: int = nums[index] + max_non_adjacent_sum(index=index - 2)

        # Step 4: Skip this value and leave the previous index available.
        not_pick: int = 0 + max_non_adjacent_sum(index=index - 1)

        # Step 5: Return the better of the two complete choices.
        return max(pick, not_pick)

    # Step 6: Begin with all elements available, up to the last index.
    return max_non_adjacent_sum(index=len(nums) - 1)


def maximum_sum_non_adjacent_elements_memoization(nums: list[int]) -> int:
    """Return the maximum sum of elements with no adjacent selected indexes.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Make a table with one slot per element. Start each slot at -1,
           meaning its answer has not been calculated. Valid sums are
           nonnegative, so even a saved zero is different from -1.
        2. Define the helper as the best sum using indexes 0 through index.
           At index 0, return the first value because it is nonnegative.
           Below index 0, return 0 because no elements remain. These checks
           happen before list access, so negative helper indexes are safe.
        3. If this index already has a saved answer, return it immediately.
           This avoids repeating the same smaller calculations.
        4. Try picking this element: add its value to the best sum through
           index - 2. This excludes its immediate neighbor. The earlier
           helper call still chooses which of its own elements to pick.
        5. Try skipping this element: add 0 to the best sum through index - 1.
           The previous element is now available to select.
        6. Save the larger total and return it. Each index has its own
           saved answer, so future calls can reuse it.
        7. Start at the last index and return the helper's answer.

        Example: nums = [2, 1, 4, 9].
            Best through index 0: 2.
            Best through index 1: max(1 + 0, 2) = 2.
            Best through index 2: max(4 + 2, 2) = 6.
            Best through index 3: max(9 + 2, 6) = 11.
            Return 11, selecting indexes 0 and 3.

    Parameters:
        nums: A nonempty list of at most 1000 integers, each from 0 to 100000.

    Returns:
        Maximum sum with no two selected elements adjacent in the original
        list. Returns 0 when all values are zero.

    Mutation Behavior:
        Updates only its local cache; nums is not modified.

    Time Complexity: O(n)
        Here n is len(nums). Each index's answer is calculated once;
        later calls return its saved answer instead of repeating the work.

    Space Complexity: O(n)
        The cache holds n entries, and the recursion stack can grow to O(n).
        The input list is excluded from extra space.

    Assumptions:
        Inputs satisfy the nonempty, nonnegative constraints. Python needs
        enough recursion depth; memoization does not remove that limit.
        Arithmetic is treated as constant cost for the stated value range.
    """
    # Step 1: Reserve a cache entry for every index.
    size: int = len(nums)
    sum_dp: list[int] = [-1] * size

    # Step 2: Find the best sum ending at or before this index.
    def max_non_adjacent_sum(index: int) -> int:
        # Step 2: Handle one remaining element or no remaining elements.
        if index == 0:
            return nums[index]
        if index < 0:
            return 0

        # Step 3: Return a saved answer immediately.
        if sum_dp[index] != -1:
            return sum_dp[index]

        # Step 4: Pick this value and skip its neighbor.
        pick: int = nums[index] + max_non_adjacent_sum(index=index - 2)
        # Step 5: Skip this value and consider the previous index.
        not_pick: int = 0 + max_non_adjacent_sum(index=index - 1)
        # Step 6: Save and return the better choice.
        sum_dp[index] = max(pick, not_pick)
        return sum_dp[index]

    # Step 7: Start with the last index, allowing all elements.
    return max_non_adjacent_sum(index=size - 1)


def maximum_sum_non_adjacent_elements_tabulation(nums: list[int]) -> int:
    """Return the largest sum of non-adjacent elements using a table.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Make a table with one slot per element. sum_dp[index] will hold
           the best sum using elements from index 0 through that index.
           The initial -1 values are placeholders, not actual answers.
        2. Save nums[0] as the first answer. Only the first element is
           available there, and the problem allows only nonnegative values.
        3. Visit each remaining index in order. First consider skipping
           this element: its answer is the best sum through the previous
           index. Adding 0 means this element contributes nothing.
        4. Consider picking this element: start with its own value. When
           index - 2 exists, add the saved best sum through that earlier
           index. This avoids selecting the immediate neighbor. At index 1,
           picking just nums[1] is valid, so no earlier sum is needed.
        5. Save the larger of the pick and skip totals. The earlier saved
           answers already include their own pick-or-skip decisions.
        6. Return the last table entry, which covers the entire list.
           For a single element, the loop is skipped and nums[0] is returned.

        Example: nums = [2, 1, 4, 9].
            Start: sum_dp = [2, -1, -1, -1].
            Index 1: pick 1 or skip for 2. Save 2.
            Index 2: pick 4 + 2 = 6 or skip for 2. Save 6.
            Index 3: pick 9 + 2 = 11 or skip for 6. Save 11.
            Final table: [2, 2, 6, 11]. Return 11.

    Parameters:
        nums: A list of 1 through 1000 integers, each from 0 through 100000.

    Returns:
        Maximum sum with no two selected indexes adjacent in the original
        list. Returns 0 when all values are zero.

    Mutation Behavior:
        Changes only its local table; nums is not modified.

    Time Complexity: O(n)
        Here n is len(nums). Creating the table and visiting each index
        both take linear time. Each visit does a fixed amount of work.

    Space Complexity: O(n)
        The table stores n answers. The input list is excluded from extra
        space, and no recursion stack is needed.

    Assumptions:
        nums is nonempty and contains only nonnegative values within the
        stated constraints. Arithmetic is treated as constant cost.
    """
    # Step 1: Reserve a slot for the best sum through each index.
    size: int = len(nums)
    sum_dp: list[int] = [-1] * size
    # Step 2: With only the first element available, use its value.
    sum_dp[0] = nums[0]

    # Step 3: Visit each remaining index and consider skipping its value.
    for index in range(1, size):
        not_pick: int = 0 + sum_dp[index - 1]
        # Step 4: Pick this value, adding an earlier sum only if it exists.
        pick: int = nums[index]
        if index - 2 >= 0:
            pick += sum_dp[index - 2]
        # Step 5: Save the better of picking and skipping.
        sum_dp[index] = max(pick, not_pick)

    # Step 6: Return the best sum covering the whole list.
    return sum_dp[size - 1]


def maximum_sum_non_adjacent_elements_tabulation_space_optimization(
    nums: list[int],
) -> int:
    """Return the maximum non-adjacent sum using only saved earlier answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Start one_index_back at nums[0]: with only the first element,
           its nonnegative value is the best sum. Start two_indexes_back
           at 0 because there are no elements before index 0. Also set
           max_sum to nums[0] so a single-element list works without a loop.
        2. Visit each remaining index. To skip its value, use one_index_back,
           the best sum through the previous index. Adding 0 means the
           current element contributes nothing.
        3. To pick its value, add nums[index] to two_indexes_back. That saved
           sum ends before the immediate neighbor, preventing adjacent picks.
        4. Choose the larger total as max_sum, the best sum through this index.
        5. Move the saved answers forward. Set two_indexes_back to not_picked,
           which still holds the OLD one_index_back. Then set one_index_back
           to max_sum. These saved sums describe earlier ranges, not whether
           the elements at those indexes were picked.
        6. Return max_sum after the loop. Only the previous two answers were
           needed, so no table of every answer is stored.

        Example: nums = [2, 1, 4, 9].
            Start: two_indexes_back = 0, one_index_back = 2, max_sum = 2.
            Index 1: pick 1 + 0 = 1 or skip for 2. Choose 2.
                Saved answers become 2 and 2.
            Index 2: pick 4 + 2 = 6 or skip for 2. Choose 6.
                Saved answers become 2 and 6.
            Index 3: pick 9 + 2 = 11 or skip for 6. Choose 11.
                Saved answers become 6 and 11. Return 11.

    Parameters:
        nums: A list of 1 through 1000 integers, each from 0 through 100000.

    Returns:
        Maximum sum with no two selected indexes adjacent in the original
        list. For a single element, returns its value; for all zeros, returns 0.

    Mutation Behavior:
        Updates only local variables; nums is not modified.

    Time Complexity: O(n)
        Here n is len(nums). The loop visits each remaining element once,
        doing a fixed amount of work per visit.

    Space Complexity: O(1)
        Only a fixed number of variables are kept, regardless of list size.
        The input list is excluded from extra space.

    Assumptions:
        nums is nonempty and contains nonnegative values within the stated
        constraints. Arithmetic is treated as constant cost.
    """
    # Step 1: Save the starting answers, including the single-element result.
    two_indexes_back: int = 0
    one_index_back: int = nums[0]
    size: int = len(nums)
    max_sum: int = nums[0]

    # Step 2: Visit each remaining element and consider skipping it.
    for index in range(1, size):
        not_picked: int = 0 + one_index_back
        # Step 3: Pick it and add the best sum from two indexes back.
        picked: int = nums[index] + two_indexes_back

        # Step 4: Choose the better of picking and skipping.
        max_sum = max(picked, not_picked)
        # Step 5: Preserve the old earlier answer, then save the new answer.
        two_indexes_back = not_picked
        one_index_back = max_sum

    # Step 6: Return the best sum for the entire list.
    return max_sum


def solve() -> None:
    nums: list[int] = [2, 1, 4, 9]
    expected: int = 11
    result: int = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum size and value.
    nums = [0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single element at maximum value.
    nums = [100000]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements; choose the last.
    nums = [3, 9]
    expected = 9
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two elements; choose the first.
    nums = [9, 3]
    expected = 9
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Adjacent equal values cannot both be selected.
    nums = [5, 5]
    expected = 5
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Question example.
    nums = [1, 2, 4]
    expected = 5
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Choose the middle instead of both endpoints.
    nums = [1, 10, 1]
    expected = 10
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Choose endpoints more than two indexes apart.
    nums = [4, 1, 1, 4]
    expected = 8
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Select more than two elements.
    nums = [5, 1, 5, 1, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros.
    nums = [0, 0, 0, 0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All equal positive values.
    nums = [5, 5, 5, 5, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing values.
    nums = [1, 2, 3, 4, 5]
    expected = 9
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing values.
    nums = [5, 4, 3, 2, 1]
    expected = 9
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple optimal selections.
    nums = [2, 2, 2, 2]
    expected = 4
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated maximum values separated by zeros.
    nums = [100000, 0, 100000, 0, 100000]
    expected = 300000
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_recursion(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: the question's example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum size and value.
    nums = [0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum element value.
    nums = [100000]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose the last of two adjacent values.
    nums = [3, 9]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose the first of two adjacent values.
    nums = [9, 3]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Adjacent duplicates.
    nums = [5, 5]
    expected = 5
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Question example.
    nums = [1, 2, 4]
    expected = 5
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose the middle.
    nums = [1, 10, 1]
    expected = 10
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose distant endpoints.
    nums = [4, 1, 1, 4]
    expected = 8
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Select more than two elements.
    nums = [5, 1, 5, 1, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All zeros.
    nums = [0, 0, 0, 0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All equal values.
    nums = [5, 5, 5, 5, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Increasing values.
    nums = [1, 2, 3, 4, 5]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Decreasing values.
    nums = [5, 4, 3, 2, 1]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tied optimal choices.
    nums = [2, 2, 2, 2]
    expected = 4
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Multiple maximum values.
    nums = [100000, 0, 100000, 0, 100000]
    expected = 300000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Original example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum length and element values.
    nums = [100000] * 1000
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum value in the middle.
    nums = [0, 100000, 0]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum length with all zeros.
    nums = [0] * 1000
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Odd length just below maximum.
    nums = [100000] * 999
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Active memoization tests.
    # Memoization: Single zero.
    nums = [0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Single maximum value.
    nums = [100000]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose last element.
    nums = [3, 9]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose first element.
    nums = [9, 3]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Adjacent duplicates.
    nums = [5, 5]
    expected = 5
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: First question example.
    nums = [1, 2, 4]
    expected = 5
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Second question example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose middle element.
    nums = [1, 10, 1]
    expected = 10
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Choose distant endpoints.
    nums = [4, 1, 1, 4]
    expected = 8
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Select three elements.
    nums = [5, 1, 5, 1, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All zeros.
    nums = [0, 0, 0, 0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: All equal positive values.
    nums = [5, 5, 5, 5, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Increasing values.
    nums = [1, 2, 3, 4, 5]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Decreasing values.
    nums = [5, 4, 3, 2, 1]
    expected = 9
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tied choices.
    nums = [2, 2, 2, 2]
    expected = 4
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Repeated maximum values.
    nums = [100000, 0, 100000, 0, 100000]
    expected = 300000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum length with zeros.
    nums = [0] * 1000
    expected = 0
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum length and values.
    nums = [100000] * 1000
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_memoization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: the question's example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum size and value.
    nums = [0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single maximum value.
    nums = [100000]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Choose last of two elements.
    nums = [3, 9]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Choose first of two elements.
    nums = [9, 3]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Adjacent duplicates.
    nums = [5, 5]
    expected = 5
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Question example.
    nums = [1, 2, 4]
    expected = 5
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Original example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Middle element is best.
    nums = [1, 10, 1]
    expected = 10
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Distant endpoints.
    nums = [4, 1, 1, 4]
    expected = 8
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Select three elements.
    nums = [5, 1, 5, 1, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All zeros.
    nums = [0, 0, 0, 0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: All equal positive values.
    nums = [5, 5, 5, 5, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Increasing values.
    nums = [1, 2, 3, 4, 5]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Decreasing values.
    nums = [5, 4, 3, 2, 1]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Tied choices.
    nums = [2, 2, 2, 2]
    expected = 4
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Repeated maximum values.
    nums = [100000, 0, 100000, 0, 100000]
    expected = 300000
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum length with zeros.
    nums = [0] * 1000
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Odd length below maximum.
    nums = [100000] * 999
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum length and values.
    nums = [100000] * 1000
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_tabulation(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: the question's example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Minimum size and value.
    nums = [0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Single maximum value.
    nums = [100000]
    expected = 100000
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Choose last of two elements.
    nums = [3, 9]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Choose first of two elements.
    nums = [9, 3]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Adjacent duplicates.
    nums = [5, 5]
    expected = 5
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: First question example.
    nums = [1, 2, 4]
    expected = 5
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Original example.
    nums = [2, 1, 4, 9]
    expected = 11
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Choose middle element.
    nums = [1, 10, 1]
    expected = 10
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Distant endpoints.
    nums = [4, 1, 1, 4]
    expected = 8
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Select three elements.
    nums = [5, 1, 5, 1, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: All zeros.
    nums = [0, 0, 0, 0]
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: All equal positive values.
    nums = [5, 5, 5, 5, 5]
    expected = 15
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Increasing values.
    nums = [1, 2, 3, 4, 5]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Decreasing values.
    nums = [5, 4, 3, 2, 1]
    expected = 9
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Tied choices.
    nums = [2, 2, 2, 2]
    expected = 4
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Repeated maximum values.
    nums = [100000, 0, 100000, 0, 100000]
    expected = 300000
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Maximum length with zeros.
    nums = [0] * 1000
    expected = 0
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Odd length below maximum.
    nums = [100000] * 999
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space optimization: Maximum length and values.
    nums = [100000] * 1000
    expected = 50000000
    result = maximum_sum_non_adjacent_elements_tabulation_space_optimization(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
