"""Maximum Consecutive Ones

Given a binary array ``nums``, return the maximum number of consecutive 1s in
the array.

A binary array is an array that contains only 0s and 1s.

Example 1:
    Input: nums = [1, 1, 0, 0, 1, 1, 1, 0]
    Output: 3
    Explanation: The maximum consecutive 1s occur from index 4 through index 6,
    giving a total of three consecutive 1s.

Example 2:
    Input: nums = [0, 0, 0, 0, 0, 0, 0, 0]
    Output: 0
    Explanation: No 1s are present in nums, so 0 is returned.
"""


def maximum_consecutive_ones(nums: list[int]) -> int:
    """Return the length of the longest consecutive sequence of 1s.

    Approach:
        1. Initialize a counter for the longest sequence found and another
           counter for the current consecutive sequence.
        2. Traverse every value in the binary array from left to right.
        3. When the current value is 1, extend the current sequence by one and
           update the maximum with the longer of the two counts.
        4. When the current value is 0, reset the current count because the
           consecutive sequence has ended.
        5. Return the maximum sequence length after processing the entire array.

    Time Complexity:
        O(n), where n is the length of ``nums``, because every element is
        examined exactly once.

    Space Complexity:
        O(1) auxiliary space because only the current and maximum counters are
        stored regardless of the input size.
    """
    # Step 1: Initialize the maximum and current consecutive-one counters.
    maximum_consecutive_ones: int = 0
    current_consecutive_ones: int = 0

    # Step 2: Examine every value from left to right.
    for num in nums:
        if num == 1:
            # Step 3: Extend the current run and update the maximum run.
            current_consecutive_ones += 1
            maximum_consecutive_ones = max(
                maximum_consecutive_ones, current_consecutive_ones
            )
        else:
            # Step 4: A zero ends the current consecutive run.
            current_consecutive_ones = 0

    # Step 5: Return the longest consecutive run found.
    return maximum_consecutive_ones


def solve() -> None:
    nums: list[int] = [1, 1, 0, 0, 1, 1, 1, 0]

    expected: int = 3
    result: int = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0, 0, 0, 0, 0]

    expected = 0
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1, 1]

    expected = 5
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = 1
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = 0
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 0, 1, 0]

    expected = 3
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 1, 0, 1, 1, 1]

    expected = 3
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 0, 1, 0, 1, 0]

    expected = 1
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 0, 1, 1, 0]

    expected = 2
    result = maximum_consecutive_ones(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
