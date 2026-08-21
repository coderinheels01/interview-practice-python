"""Longest Consecutive Sequence in an Array

Given an array ``nums`` of ``n`` integers, return the length of the longest
sequence of consecutive integers. The integers in this sequence can appear in
any order in the original array.

Consecutive integers are numbers that follow each other with a difference of 1,
such as [1, 2, 3, 4].

Example 1:
    Input: nums = [100, 4, 200, 1, 3, 2]
    Output: 4

    Explanation: The longest sequence of consecutive elements is
    [1, 2, 3, 4], which has a length of 4. This sequence can be formed
    regardless of the initial order of the elements in the array.

Example 2:
    Input: nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    Output: 9

    Explanation: The longest sequence of consecutive elements is
    [0, 1, 2, 3, 4, 5, 6, 7, 8], which has a length of 9.

Example 3:
    Input: nums = [-2, 5, -3, -1]
    Output: 3

    Explanation: The longest sequence is [-3, -2, -1].

Example 4:
    Input: nums = [1, 2, 2, 3]
    Output: 3

    Explanation: Duplicate values do not extend the sequence [1, 2, 3].

Example 5:
    Input: nums = [10, 30, 20]
    Output: 1

    Explanation: No two values are consecutive, so the longest length is 1.

Example 6:
    Input: nums = [10]
    Output: 1

    Explanation: A single value forms a sequence of length 1.

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^9 <= nums[i] <= 10^9

https://www.youtube.com/watch?v=oO5uLE7EUlM&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=13
"""


def longest_consecutive_sequence_brute_force(nums: list[int]) -> int:
    """Return the length of the longest consecutive sequence using brute force.

    Approach:
        1. Initialize the maximum sequence length to zero.
        2. Treat each value in ``nums`` as the possible beginning of a
           consecutive sequence, with an initial length of one.
        3. Repeatedly search the entire list for the next integer. Each time
           ``current_num + 1`` exists, advance the current number and increase
           the current sequence length.
        4. Compare the completed sequence length with the maximum found so far.
        5. Return the greatest sequence length after checking every value.

    Parameters:
        nums: A non-empty list of integers whose consecutive values may appear
        in any order.

    Returns:
        The length of the longest sequence of consecutive integers in ``nums``.

    Mutation Behavior:
        The function does not modify ``nums``. Updating ``current_num`` changes
        only the local loop variable.

    Assumptions:
        ``nums`` contains 1 to 100,000 integers, and every value is between
        -1,000,000,000 and 1,000,000,000 inclusive.

    Time Complexity:
        O(n^3) in the worst case, where ``n`` is the length of ``nums``. The
        outer loop tries ``n`` starting values, a sequence can advance up to
        ``n`` times, and each ``in nums`` membership search takes O(n) time.

    Space Complexity:
        O(1) additional space. The function stores only the maximum length,
        current value, and current length, regardless of the input size.
    """
    # Step 1: Track the greatest sequence length found so far.
    max_len: int = 0

    # Step 2: Treat each array value as a possible sequence beginning.
    for current_num in nums:
        current_len: int = 1

        # Step 3: Extend the sequence while its next integer exists in the list.
        while current_num + 1 in nums:
            current_len += 1
            current_num += 1

        # Step 4: Preserve the longest completed sequence length.
        max_len = max(max_len, current_len)

    # Step 5: Return the longest length found.
    return max_len


def longest_consecutive_sequence_sorting_optimized(nums: list[int]) -> int:
    """Return the longest consecutive-sequence length using sorted adjacency.

    Approach:
        This is a sorting-based approach.

        1. Sort ``nums`` in ascending order so equal and consecutive values are
           adjacent.
        2. Initialize both the longest and current sequence lengths to one,
           relying on the constraint that ``nums`` is non-empty.
        3. Visit every adjacent pair. Ignore equal values because duplicates do
           not extend or interrupt a consecutive sequence.
        4. Apply the adjacent-difference check. If it identifies consecutive
           values, extend the current sequence; otherwise, reset its length.
        5. Update the longest length after each non-duplicate pair and return it
           after the scan finishes.

        The current comparison uses ``nums[index] - nums[index + 1] == 1``.
        Because the array is sorted in ascending order, this condition cannot
        be true for distinct adjacent values. Therefore, the current
        implementation does not yet correctly detect consecutive sequences.

    Parameters:
        nums: A non-empty list of integers to inspect.

    Returns:
        The length calculated for the longest consecutive sequence.

    Mutation Behavior:
        The function sorts ``nums`` in place, permanently changing its order.

    Assumptions:
        ``nums`` contains 1 to 100,000 integers, and every value is between
        -1,000,000,000 and 1,000,000,000 inclusive.

    Time Complexity:
        O(n log n), where ``n`` is the length of ``nums``. Sorting costs
        O(n log n), and the adjacent-pair scan costs O(n).

    Space Complexity:
        Python's in-place ``list.sort()`` may use O(n) auxiliary space in the
        worst case because it uses Timsort. The variables used by the explicit
        scan require O(1) additional space.
    """
    # Step 1: Sort values so duplicates and consecutive values are adjacent.
    nums.sort()
    size: int = len(nums)

    # Step 2: Begin with the guaranteed non-empty sequence length of one.
    max_len: int = 1
    current_len: int = 1

    # Step 3: Inspect each adjacent pair and ignore duplicate values.
    for index in range(size - 1):
        if nums[index] == nums[index + 1]:
            continue

        # Step 4: Apply the current difference check and update the sequence.
        if nums[index] - nums[index + 1] == 1:
            current_len += 1
        else:
            current_len = 1

        # Step 5: Preserve the greatest sequence length encountered.
        max_len = max(max_len, current_len)

    # Step 5: Return the final longest length.
    return max_len


def longest_consecutive_sequence_optimized(nums: list[int]) -> int:
    """Return the longest consecutive-sequence length using a hash set.

    Approach:
        1. Convert ``nums`` to a set so membership checks take O(1) average
           time and duplicate values do not affect those checks.
        2. Initialize the longest sequence length to zero.
        3. Treat each unique value as a possible sequence starting point and
           create a separate variable for advancing through that sequence.
        4. Skip the value if its predecessor exists, because it is not the
           beginning of a sequence.
        5. From each sequence beginning, repeatedly check for the next integer
           in the set and count every consecutive value found.
        6. Update the longest length and return it after all values are checked.

    Parameters:
        nums: A list of integers whose consecutive values may appear in any
        order.

    Returns:
        The length of the longest sequence of consecutive integers in ``nums``.

    Mutation Behavior:
        The function does not modify ``nums``. It creates a separate set and
        changes only local variables while traversing sequences.

    Assumptions:
        ``nums`` contains 1 to 100,000 integers, and every value is between
        -1,000,000,000 and 1,000,000,000 inclusive.

    Time Complexity:
        O(n) on average, where ``n`` is the number of input values. Creating and
        scanning the set takes O(n), and each membership check takes O(1) on
        average.

        The nested ``while`` loop does not make the total O(n^2) because it runs
        only from the first value of each sequence. Every other value in that
        sequence is skipped by the predecessor check. As a result, all while
        loops combined advance through at most ``n`` unique values, rather than
        advancing through ``n`` values for every outer-loop iteration.

        In the rare worst case of severe hash collisions, set operations can
        degrade and the running time can become O(n^2).

    Space Complexity:
        O(n) additional space for ``unique_numbers``. The counters and current
        number use O(1) additional space.
    """
    # Step 1: Build a hash set for average O(1) membership checks.
    unique_numbers: set[int] = set(nums)

    # Step 2: Track the greatest sequence length found so far.
    max_len: int = 0

    # Step 3: Treat each unique value as a possible sequence beginning.
    for num in unique_numbers:
        current_len: int = 1
        current_num: int = num

        # Step 4: Skip values that have a predecessor in the set.
        if current_num - 1 in unique_numbers:
            continue

        # Step 5: Count consecutive values beginning with current_num.
        while current_num + 1 in unique_numbers:
            current_len += 1
            current_num += 1

        # Step 6: Preserve the greatest completed sequence length.
        max_len = max(max_len, current_len)

    # Step 6: Return the longest length found.
    return max_len


def solve() -> None:
    # Provided example with values in arbitrary order.
    nums: list[int] = [100, 4, 200, 1, 3, 2]

    expected: int = 4
    result: int = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Provided example containing a duplicate zero.
    nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]

    expected = 9
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative consecutive values in arbitrary order.
    nums = [-2, 5, -3, -1]

    expected = 3
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values do not increase the sequence length.
    nums = [1, 2, 2, 3]

    expected = 3
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No two values are consecutive.
    nums = [10, 30, 20]

    expected = 1
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length.
    nums = [10]

    expected = 1
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum and maximum allowed values are not consecutive.
    nums = [-1_000_000_000, 1_000_000_000]

    expected = 1
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A consecutive sequence crosses from negative values through zero.
    nums = [2, -2, 0, -1, 1]

    expected = 5
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All values are identical.
    nums = [7, 7, 7, 7]

    expected = 1
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length.
    nums = [0] * 100_000

    expected = 1
    result = longest_consecutive_sequence_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Better-optimized implementation with values in arbitrary order.
    nums = [100, 4, 200, 1, 3, 2]

    expected = 4
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Provided example containing a duplicate zero.
    nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]

    expected = 9
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative consecutive values in arbitrary order.
    nums = [-2, 5, -3, -1]

    expected = 3
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values do not increase the sequence length.
    nums = [1, 2, 2, 3]

    expected = 3
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No two values are consecutive.
    nums = [10, 30, 20]

    expected = 1
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length.
    nums = [10]

    expected = 1
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum and maximum allowed values are not consecutive.
    nums = [-1_000_000_000, 1_000_000_000]

    expected = 1
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A consecutive sequence crosses from negative values through zero.
    nums = [2, -2, 0, -1, 1]

    expected = 5
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All values are identical.
    nums = [7, 7, 7, 7]

    expected = 1
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A decreasing input becomes one consecutive sequence after sorting.
    nums = [5, 4, 3, 2, 1]

    expected = 5
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length with identical values.
    nums = [0] * 100_000

    expected = 1
    result = longest_consecutive_sequence_sorting_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Hash-set optimized implementation with values in arbitrary order.
    nums = [100, 4, 200, 1, 3, 2]

    expected = 4
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Hash-set optimized implementation with a duplicate zero.
    nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]

    expected = 9
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative consecutive values in arbitrary order.
    nums = [-2, 5, -3, -1]

    expected = 3
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values do not increase the sequence length.
    nums = [1, 2, 2, 3]

    expected = 3
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No two values are consecutive.
    nums = [10, 30, 20]

    expected = 1
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length.
    nums = [10]

    expected = 1
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum and maximum allowed values are not consecutive.
    nums = [-1_000_000_000, 1_000_000_000]

    expected = 1
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A consecutive sequence crosses from negative values through zero.
    nums = [2, -2, 0, -1, 1]

    expected = 5
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All values are identical.
    nums = [7, 7, 7, 7]

    expected = 1
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A decreasing input forms one consecutive sequence.
    nums = [5, 4, 3, 2, 1]

    expected = 5
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length forming one consecutive sequence.
    nums = list(range(-50_000, 50_000))

    expected = 100_000
    result = longest_consecutive_sequence_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
