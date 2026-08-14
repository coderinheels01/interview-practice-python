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
    Select the correct output:
        - -1
        - 1
        - 2
        - 0

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - -10^4 <= target <= 10^4
"""


def linear_search(nums: list[int], target: int) -> int:
    pass


def solve() -> None:
    nums: list[int] = [2, 3, 4, 5, 3]
    target: int = 3

    expected: int = 1
    result: int = linear_search(nums, target)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
