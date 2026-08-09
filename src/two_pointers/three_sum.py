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
    """
    Approach: Sort and Use Two Pointers
        1. Return an empty list when nums has fewer than three values because a
           triplet cannot be formed.
        2. Sort a copy of nums. Sorting places equal values next to each other,
           which makes duplicate values easy to skip, and lets pointer movement
           predictably increase or decrease a sum.
        3. Use start to fix the first value of each possible triplet. Only use
           start positions that leave at least two values to their right.
        4. Skip a fixed value when it is equal to the previously processed fixed
           value. This prevents generating the same triplets again from an
           identical first value. If the fixed value is positive, stop early:
           every value after it is at least as large, so their sum cannot be 0.
        5. For each fixed value, place left immediately after start and right at
           the end of the sorted array.
        6. Add the values at start, left, and right:
              - If the sum is less than 0, move left rightward to increase it.
              - If the sum is greater than 0, move right leftward to decrease it.
              - If the sum is 0, add the triplet to result and move both pointers
                inward to continue looking for another pair with the same first
                value.
        7. After finding a triplet, skip all repeated values at left and right.
           This prevents different index combinations containing the same three
           values from adding duplicate triplets to result.

    Time Complexity:
        O(n^2), where n is the length of nums. Creating and sorting the copy
        takes O(n log n) time. The outer loop can process O(n) fixed values. For
        each fixed value, left and right move only inward and together examine
        at most O(n) positions. This gives O(n * n) = O(n^2) for the two-pointer
        search. O(n^2) dominates O(n log n), so the total time is O(n^2).

        The duplicate-skipping loops do not add another factor of n. They move
        the same left and right pointers in the same direction, and neither
        pointer can visit an index more than once for a fixed start position.

    Space Complexity:
        O(n) auxiliary space because sorted(nums) creates a new list containing
        all n input values. The start, end, left, right, first, and current_sum
        variables each use O(1) space.

        The returned result is output space and can contain O(n^2) triplets in
        the worst case. Including the required output, total space can therefore
        be O(n^2); excluding the output, the auxiliary space is O(n).

    https://www.youtube.com/watch?v=jzZsG8n2R9A&t=472s
    """
    # Step 1: Fewer than three values cannot form a triplet.
    if len(nums) <= 2:
        return []

    # Step 2: Sort a copy so pointer movement and duplicate skipping are valid.
    nums = sorted(nums)

    # Step 3: Start with the first fixed value and collect unique triplets.
    start: int = 0
    end: int = len(nums) - 2
    result: list[list[int]] = []

    while start < len(nums) - 2:
        first: int = nums[start]

        # Step 4: Once the fixed value is positive, no later triplet can sum to 0.
        if first > 0:
            break

        # Step 5: Search the remaining range with one pointer at each end.
        left: int = start + 1
        right: int = len(nums) - 1

        # Step 4: Do not process the same fixed value more than once.
        if start > 0 and nums[start] == nums[start - 1]:
            start += 1
            continue

        while left < right:
            # Step 6: Compare the current triplet's sum with the required sum, 0.
            current_sum: int = first + nums[left] + nums[right]

            if current_sum == 0:
                result.append([first, nums[left], nums[right]])
                left += 1
                right -= 1

                # Step 7: Skip values already used in the triplet just appended.
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

            # A large sum needs a smaller right-hand value.
            elif current_sum > 0:
                right -= 1

            # A small sum needs a larger left-hand value.
            else:
                left += 1

        # Advance to the next candidate for the fixed first value.
        start += 1

    return result


def solve() -> None:

    nums: list[int] = [-2, 0, 0, 2, 2]
    expected: list[list[int]] = [[-2, 0, 2]]
    result: list[list[int]] = three_sum(nums)
    # assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums: list[int] = [-1, 0, 1, 2, -1, -4]
    expected: list[list[int]] = [[-1, -1, 2], [-1, 0, 1]]
    result: list[list[int]] = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [0, 1, 1]
    expected = []
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [0, 0, 0]
    expected = [[0, 0, 0]]
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [-1, 0, 1]
    expected = [[-1, 0, 1]]
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [1, 2, 3, 4]
    expected = []
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [-4, -3, -2, -1]
    expected = []
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [-2, 0, 1, 1, 2]
    expected = [[-2, 0, 2], [-2, 1, 1]]
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    nums = [-1, -1, -1, 0, 1, 2]
    expected = [[-1, -1, 2], [-1, 0, 1]]
    result = three_sum(nums)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


if __name__ == "__main__":
    solve()
