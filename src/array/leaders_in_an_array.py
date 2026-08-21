"""Leaders in an Array

Given an integer array ``nums``, return a list of all the leaders in the array.

A leader in an array is an element whose value is strictly greater than all
elements to its right in the given array. The rightmost element is always a
leader. The elements in the leader array must appear in the order they appear
in ``nums``.

Example 1:
    Input: nums = [1, 2, 5, 3, 1, 2]
    Output: [5, 3, 2]

    Explanation: 2 is the rightmost element, 3 is the largest element in the
    index range [3, 5], and 5 is the largest element in the index range [2, 5].

Example 2:
    Input: nums = [-3, 4, 5, 1, -4, -5]
    Output: [5, 1, -4, -5]

    Explanation: -5 is the rightmost element, -4 is the largest element in the
    index range [4, 5], 1 is the largest element in the index range [3, 5], and
    5 is the largest element in the index range [2, 5].

Example 3:
    Input: nums = [-3, 4, 5, 1, -30, -10]
    Output: [5, 1, -10]

    Explanation: -10 is always a leader because it is the rightmost element.
    Moving left, 1 is greater than both -30 and -10, and 5 is greater than every
    element to its right. The values -3, 4, and -30 each have a greater value
    somewhere to their right.

Example 4:
    Input: nums = [7, 6, 5, 4]
    Output: [7, 6, 5, 4]

    Explanation: Every element is greater than all the elements to its right,
    so every element is a leader.

Example 5:
    Input: nums = [1, 2, 3, 4]
    Output: [4]

    Explanation: Every element except 4 has a greater element to its right.
    Therefore, only the rightmost element is a leader.

Example 6:
    Input: nums = [5, 5, 3]
    Output: [5, 3]

    Explanation: The second 5 is greater than 3, so it is a leader. The first 5
    is not a leader because it is equal to the second 5, and leaders must be
    strictly greater than every value to their right.

Example 7:
    Input: nums = [2, 2, 2]
    Output: [2]

    Explanation: Equal values are not strictly greater than one another, so
    only the rightmost 2 is a leader.

Example 8:
    Input: nums = [10]
    Output: [10]

    Explanation: A single element is also the rightmost element, so it is
    always a leader.


Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4

https://www.youtube.com/watch?v=cHrH9CQ8pmY&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=12
"""


def leaders_in_an_array_brute_force(nums: list[int]) -> list[int]:
    """Return every array leader in its original order using brute force.

    A leader is strictly greater than every element to its right. The rightmost
    element is always a leader because no elements appear after it.

    Approach:
        1. Create an empty list that will store the leaders.
        2. Visit each element from left to right and treat it as a candidate.
        3. Compare the candidate with every element to its right. If any value
           is greater than or equal to the candidate, mark the candidate as not
           being a leader and stop checking it.
        4. If no value to the right disqualifies the candidate, append it to the
           result. Processing candidates from left to right preserves their
           original order.
        5. Return the collected leaders.

    Parameters:
        nums: The list of integers to inspect for leaders.

    Returns:
        A new list containing all leaders in the order they appear in ``nums``.

    Mutation Behavior:
        The function does not modify ``nums``.

    Assumptions:
        ``nums`` contains 1 to 100,000 integers, and every value is between
        -10,000 and 10,000 inclusive.

    Time Complexity:
        O(n^2) in the worst case, where ``n`` is the length of ``nums``. For an
        array in decreasing order, each candidate is compared with every value
        to its right. The early ``break`` can reduce work for some inputs but
        does not change the worst-case complexity.

    Space Complexity:
        O(n) for the returned list in the worst case, when every element is a
        leader. Excluding the output, the algorithm uses O(1) additional space
        for the size, indices, candidate, and Boolean flag.
    """
    # Step 1: Create the list that will store all discovered leaders.
    size: int = len(nums)
    leaders: list[int] = []

    # Step 2: Consider each element from left to right as a candidate.
    for outer_index in range(size):
        is_leader: bool = True
        candidate: int = nums[outer_index]

        # Step 3: Check whether a value to the right disqualifies the candidate.
        for inner_index in range(outer_index + 1, size):
            if candidate <= nums[inner_index]:
                is_leader = False
                break

        # Step 4: Preserve each qualifying candidate in its original order.
        if is_leader:
            leaders.append(candidate)

    # Step 5: Return all leaders found in the array.
    return leaders


def leaders_in_an_array_optimized(nums: list[int]) -> list[int]:
    """Return every array leader in its original order using a linear scan.

    A leader is strictly greater than every element to its right. The rightmost
    element is always a leader because no elements appear after it.

    Approach:
        1. Treat the rightmost element as the first leader and as the greatest
           value seen to the right.
        2. Scan the remaining elements from right to left.
        3. If the current candidate is strictly greater than the greatest value
           seen to its right, append it as a leader and update that maximum.
        4. Reverse the collected leaders because they were discovered from
           right to left, restoring their original left-to-right order.
        5. Return the ordered list of leaders.

    Parameters:
        nums: The non-empty list of integers to inspect for leaders.

    Returns:
        A new list containing all leaders in the order they appear in ``nums``.

    Mutation Behavior:
        The function does not modify ``nums``. It reverses only the newly
        created ``leaders`` list.

    Assumptions:
        ``nums`` contains 1 to 100,000 integers, and every value is between
        -10,000 and 10,000 inclusive. An empty list is not allowed because the
        function accesses ``nums[-1]``.

    Time Complexity:
        O(n), where ``n`` is the length of ``nums``. The function scans the
        input once and reverses at most ``n`` collected leaders.

    Space Complexity:
        O(n) for the returned list in the worst case, when every element is a
        leader. Excluding the output, the function uses O(1) additional space
        for the size, index, candidate, and maximum value.
    """
    # Step 1: Start with the rightmost element as a leader and suffix maximum.
    size: int = len(nums)
    max_value_on_right: int = nums[-1]
    leaders: list[int] = [max_value_on_right]

    # Step 2: Scan all remaining elements from right to left.
    for index in range(size - 2, -1, -1):
        candidate: int = nums[index]

        # Step 3: Record candidates strictly greater than everything to the right.
        if candidate > max_value_on_right:
            leaders.append(candidate)
            max_value_on_right = candidate

    # Step 4: Restore the leaders to their original left-to-right order.
    leaders.reverse()

    # Step 5: Return the ordered leaders.
    return leaders


def solve() -> None:
    # Normal case with leaders at the middle and end.
    nums: list[int] = [1, 2, 5, 3, 1, 2]

    expected: list[int] = [5, 3, 2]
    result: list[int] = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    # Provided example containing negative values.
    nums = [-3, 4, 5, 1, -4, -5]

    expected = [5, 1, -4, -5]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Provided multiple-choice example.
    nums = [-3, 4, 5, 1, -30, -10]

    expected = [5, 1, -10]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length and minimum allowed value.
    nums = [-10_000]

    expected = [-10_000]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing input leaves only the rightmost value as a leader.
    nums = [-10_000, 0, 10_000]

    expected = [10_000]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing input makes every value a leader.
    nums = [10_000, 0, -10_000]

    expected = [10_000, 0, -10_000]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal values test the strictly-greater requirement.
    nums = [5, 5, 3]

    expected = [5, 3]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All-identical zero values leave only the rightmost occurrence as a leader.
    nums = [0, 0, 0]

    expected = [0]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Leaders occur at the beginning, middle, and end.
    nums = [10, 3, 5, 2]

    expected = [10, 5, 2]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length with duplicate values.
    nums = [0] * 100_000

    expected = [0]
    result = leaders_in_an_array_brute_force(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized implementation preserves leaders in their original order.
    nums = [1, 2, 5, 3, 1, 2]

    expected = [5, 3, 2]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized implementation with negative values.
    nums = [-3, 4, 5, 1, -4, -5]

    expected = [5, 1, -4, -5]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimized implementation for the provided multiple-choice example.
    nums = [-3, 4, 5, 1, -30, -10]

    expected = [5, 1, -10]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum input length and minimum allowed value.
    nums = [-10_000]

    expected = [-10_000]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Increasing input and both allowed-value boundaries.
    nums = [-10_000, 0, 10_000]

    expected = [10_000]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Decreasing input makes every element a leader.
    nums = [10_000, 0, -10_000]

    expected = [10_000, 0, -10_000]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate values exercise the strictly-greater requirement.
    nums = [5, 5, 3]

    expected = [5, 3]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All-identical zero values leave only the rightmost occurrence as a leader.
    nums = [0, 0, 0]

    expected = [0]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Leaders appear at the beginning, middle, and end.
    nums = [10, 3, 5, 2]

    expected = [10, 5, 2]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum input length with duplicate values.
    nums = [0] * 100_000

    expected = [0]
    result = leaders_in_an_array_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
