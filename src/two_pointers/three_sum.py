"""
3Sum

Difficulty: Medium
Topics: Two Pointers
Company Tags
Hints

Given an integer array nums, return all the triplets
[nums[i], nums[j], nums[k]] where nums[i] + nums[j] + nums[k] == 0 and the
indices i, j, and k are all distinct.

The output should not contain any duplicate triplets. You may return the output
and the triplets in any order.

Example 1:
    Input:
        nums = [-1, 0, 1, 2, -1, -4]

    Output:
        [[-1, -1, 2], [-1, 0, 1]]

    Explanation:
        nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
        nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
        The distinct triplets are [-1, 0, 1] and [-1, -1, 2].

Example 2:
    Input:
        nums = [0, 1, 1]

    Output:
        []

    Explanation:
        The only possible triplet does not sum to 0.

Example 3:
    Input:
        nums = [0, 0, 0]

    Output:
        [[0, 0, 0]]

    Explanation:
        The only possible triplet sums up to 0.

Constraints:
    - 3 <= len(nums) <= 3,000
    - -10^5 <= nums[i] <= 10^5
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    """Return all unique triplets whose values sum to zero."""
    look_up:dict[int, int] = 
    pass


def solve() -> None:
    nums: list[int] = [-1, 0, 1, 2, -1, -4]
    expected: list[list[int]] = [[-1, -1, 2], [-1, 0, 1]]
    result: list[list[int]] = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


if __name__ == "__main__":
    solve()
