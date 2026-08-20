"""Linear Search

Given an array of integers ``nums`` and an integer ``target``, find the smallest
index, using zero-based indexing, where ``target`` appears in the array. If the
target is not found in the array, return -1.

Example 1:
    Input: nums = [2, 3, 4, 5, 3], target = 3
    Output: 1
    Explanation: The first occurrence of 3 in nums is at index 1.

Example 2:
    Input: nums = [2, -4, 4, 0, 10], target = 6
    Output: -1
    Explanation: The value 6 does not occur in the array, so -1 is returned.

Now your turn:
    Input: nums = [1, 3, 5, -4, 1], target = 1

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - -10^4 <= target <= 10^4

https://www.youtube.com/watch?v=wvcQg43_V8U&t=2330s
"""


def linear_search(nums: list[int], target: int) -> int:
    """Return the first index containing ``target``, or -1 if it is absent.

    Approach: Linear Search
        1. Traverse ``nums`` from left to right with ``enumerate`` so each
           iteration provides both the current index and value.
        2. Compare the current value with ``target``.
        3. When they are equal, immediately return the current index. Because
           traversal begins at index 0, the first match is the smallest index
           containing ``target``.
        4. If the traversal finishes without finding a match, return -1.

    Time Complexity:
        O(n) in the worst case, where n is the length of ``nums``. The function
        may examine every element when the target is absent or appears at the
        final index. It returns earlier when a match is found sooner.

    Space Complexity:
        O(1), because the function uses only the current ``index`` and value
        ``n`` regardless of the input size.


    """
    # Step 1: Visit every value from left to right with its index.
    for index, num in enumerate(nums):
        # Steps 2 and 3: Compare with target and return the first matching index.
        if num == target:
            return index

    # Step 4: The target does not appear in nums.
    return -1


def solve() -> None:
    nums: list[int] = [2, 3, 4, 5, 3]
    target: int = 3

    expected: int = 1
    result: int = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, -4, 4, 0, 10]
    target = 6

    expected = -1
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 3, 5, -4, 1]
    target = 1

    expected = 0
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    target = 7

    expected = 0
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    target = -7

    expected = -1
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 5]
    target = 5

    expected = 4
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [4, 4, 4, 4]
    target = 4

    expected = 0
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-5, -3, -1, -3]
    target = -3

    expected = 1
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, -1, 0, 1, 2]
    target = 0

    expected = 2
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 0, 10_000]
    target = -10_000

    expected = 0
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, 0, 10_000]
    target = 10_000

    expected = 2
    result = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
