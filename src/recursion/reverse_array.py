"""Reverse an Array Using Recursion

Given an integer array ``nums``, reverse the array in place using recursion.
Do not use Python's built-in ``reverse()`` method or slicing. Return the same
array after it has been reversed.

Example 1:
    Input: nums = [1, 2, 3, 4, 5]
    Output: [5, 4, 3, 2, 1]

Example 2:
    Input: nums = [10, -2, 7, 0]
    Output: [0, 7, -2, 10]

Now your turn:
    Input: nums = [3, 8, 1, 9, 4, 6]

Constraints:
    - 1 <= nums.length <= 1000
    - -10^4 <= nums[i] <= 10^4
"""


def reverse_array(nums: list[int]) -> list[int]:
    """Reverse ``nums`` in place recursively and return the same list.

    Approach: Two-Pointer Recursion
        1. Define a helper that swaps the values at two given indexes.
        2. Start the recursive process with ``left`` at the beginning of the
           list and ``right`` at the end.
        3. Stop when ``left`` meets or passes ``right`` because every outer
           pair has been reversed.
        4. Otherwise, swap the values at ``left`` and ``right``.
        5. Recursively process the remaining inner portion by moving ``left``
           one position right and ``right`` one position left.
        6. Return ``nums`` after the recursive calls finish.

    Parameters:
        nums: The list of integers to reverse.

    Returns:
        The same list object after its elements have been reversed.

    Mutation Behavior:
        The function modifies ``nums`` in place.

    Time Complexity:
        O(n), where n is the length of ``nums``. Each recursive call handles
        one pair, so there are approximately n / 2 calls. Dropping the constant
        factor gives O(n).

    Space Complexity:
        O(n) call-stack space. The recursion depth is approximately n / 2,
        which simplifies to O(n). No additional list is created.

    Assumptions:
        ``nums`` contains between 1 and 1000 integers, as stated by the problem
        constraints.
    """

    # Step 1: Swap the values at two indexes.
    def swap(left: int, right: int):
        nums[left], nums[right] = nums[right], nums[left]

    # Steps 3 through 5: Stop at the middle or swap an outer pair and recurse.
    def reverse_recursively(left: int, right: int):
        if left >= right:
            return
        swap(left=left, right=right)
        reverse_recursively(left + 1, right - 1)

    # Step 2: Begin with pointers at the two ends of the list.
    reverse_recursively(0, len(nums) - 1)

    # Step 6: Return the same, now-reversed list.
    return nums


def solve() -> None:
    nums: list[int] = [1, 2, 3, 4, 5]
    expected: list[int] = [5, 4, 3, 2, 1]
    result: list[int] = reverse_array(nums)
    assert result == expected
    assert result is nums
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, -2, 7, 0]
    expected = [0, 7, -2, 10]
    result = reverse_array(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 8, 1, 9, 4, 6]
    expected = [6, 4, 9, 1, 8, 3]
    result = reverse_array(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    expected = [7]
    result = reverse_array(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
