"""Target Sum

Difficulty: Medium

Problem Statement:
    Given a nonnegative integer array nums and an integer target, assign
    either a plus sign or a minus sign to every element. Return the number
    of sign assignments whose resulting expression evaluates to target.

    Use every array position exactly once and preserve the element order.
    Assignments are distinct if any position receives a different sign,
    even when values repeat or an element is zero. Return the exact count.

Constraints (LeetCode 494 version):
    1 <= len(nums) <= 20
    0 <= nums[i] <= 1000
    0 <= sum(nums) <= 1000
    -1000 <= target <= 1000

Sample:
    nums = [1, 1, 1, 1, 1]
    target = 3
    Output: 5

    Assign a minus sign to exactly one of the five positions and a plus
    sign to the other four. Each choice gives four positive ones minus
    one, which equals 3, so there are five expressions.

Additional Examples (added for practice):
    1. A single matching number:
        nums = [1]
        target = 1
        Output: 1
        Only +1 matches; -1 does not.

    2. A negative target:
        nums = [1, 2]
        target = -1
        Output: 1
        The expression +1 - 2 equals -1.

    3. Zero creates distinct sign assignments:
        nums = [0, 1]
        target = 1
        Output: 2
        Both +0 + 1 and -0 + 1 equal 1.

    4. An unreachable target:
        nums = [2, 4]
        target = 3
        Output: 0
        The possible expression values are 6, -2, 2, and -6; none is 3.

    5. Two ways to make zero:
        nums = [2, 2]
        target = 0
        Output: 2
        Both +2 - 2 and -2 + 2 equal zero.

Sources:
    https://www.youtube.com/watch?v=b3GD8263-PQ
    https://leetcode.com/problems/target-sum/
    The video covers Target Sum; the statement, constraints, and sample
    here use the matching LeetCode 494 version.
"""


def target_sum(nums: list[int], target: int) -> int:
    """Count sign assignments whose expression evaluates to target.

    Args:
        nums: A nonnegative integer list. Every position receives exactly
            one plus or minus sign. Equal values at different positions
            are distinct choices, and zeros are supported.
        target: The required integer expression value, possibly negative.

    Returns:
        The exact number of matching sign assignments, or zero if impossible.
        Assigning plus or minus to zero counts as two different choices.
        Empty input returns one for target zero and zero otherwise, although
        the stated problem requires at least one element. No modulo is used.

    Mutation and assumptions:
        The input list is not modified or sorted. Nonnegative integer
        elements are assumed and are not validated. Negative array elements
        are unsupported by the subset transformation and pruning. Recursion
        depth is O(N); the stated maximum of 20 elements keeps it shallow.

    Approach:
        Depth-First Search (DFS), using include/exclude recursion after
        reducing sign assignments to subset counting.
        1. Read size and total_sum. Let P be the sum of elements assigned
           plus and M the sum assigned minus. P + M = total_sum and
           P - M = target. Subtracting the second equation from the first
           cancels P and gives 2 * M = total_sum - target. Therefore
           subset_sum = (total_sum - target) // 2 is the required sum of
           the minus group, provided the following checks pass.
        2. Reject abs(target) > total_sum because every expression lies
           between -total_sum and total_sum. Also reject an odd
           total_sum - target: dividing by two would require a fractional
           subset sum. Integer division rounds down, so it cannot replace
           this check. Negative expression targets are valid and still use
           the same formula when they are within the possible range.
        3. In count_subsets_with_sum, index is the last available position
           and k is the remaining minus-group sum needed. Once index is
           negative, return one if k is zero, otherwise zero. This counts
           a complete successful index selection, not its numeric sum.
           Do not stop early at k == 0: remaining zeros may be included
           or excluded, producing additional sign assignments.
        4. Calculate not_take by skipping the current position and searching
           earlier indexes for the same k. This leaves the current element
           out of the minus group, so it receives a plus sign.
        5. Initialize take to zero. If nums[index] <= k, include it in
           the minus group and search earlier indexes for k - nums[index].
           Decreasing index prevents reusing a position. A zero fits even
           at k == 0 and gives a distinct minus choice without changing k.
        6. Return take + not_take. These index selections are disjoint,
           so both counts contribute. Each zero doubles the choices for
           any matching selection. For [1, 1, 1, 1, 1] and target 3,
           subset_sum is 1: any one of five positions can receive minus,
           while the remaining positions receive plus, giving five ways.
        7. Begin at size - 1 with k equal to subset_sum and return the
           count. Choosing the minus-group indexes determines every sign;
           no expression or subset needs to be constructed explicitly.

    Time Complexity:
        O(2**N) in the worst case, where N is the array length. Each
        position may create a take and skip branch; impossible targets
        return after the O(N) total-sum calculation.

    Space Complexity:
        O(N) extra space, excluding the input list. The recursive stack
        holds at most N + 1 helper calls with constant local storage per
        call, and no collection of subsets or expressions is stored.
    """

    # Step 1: Transform the sign target into the required minus-group sum.
    size: int = len(nums)
    total_sum: int = sum(nums)
    subset_sum: int = (total_sum - target) // 2

    # Step 2: Reject out-of-range targets and fractional required subset sums.
    if abs(target) > total_sum or (total_sum - target) % 2 != 0:
        return 0

    def count_subsets_with_sum(index: int, k: int) -> int:
        # Step 3: Count a match only after all positions have been considered.
        if index < 0:
            if k == 0:
                return 1
            else:
                return 0

        # Step 4: Exclude this position from the minus group (assign plus).
        not_take: int = count_subsets_with_sum(index=index - 1, k=k)
        # Step 5: Include it in the minus group when it fits, including zero.
        take: int = 0
        if nums[index] <= k:
            take = count_subsets_with_sum(index=index - 1, k=k - nums[index])

        # Step 6: Add the counts for the two distinct sign choices.
        return take + not_take

    # Step 7: Count all minus-group selections for the transformed target.
    return count_subsets_with_sum(index=size - 1, k=subset_sum)


def solve() -> None:
    # Sample from the question.
    nums = [1, 1, 1, 1, 1]
    target = 3
    expected = 5
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive matching value.
    nums = [1]
    target = 1
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single negative matching target.
    nums = [1]
    target = -1
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single positive value cannot make zero.
    nums = [1]
    target = 0
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single zero has two sign choices.
    nums = [0]
    target = 0
    expected = 2
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All zeros.
    nums = [0, 0, 0, 0]
    target = 0
    expected = 16
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zeros cannot make a nonzero target.
    nums = [0, 0, 0]
    target = 1
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero before other values.
    nums = [0, 1, 2, 3]
    target = 2
    expected = 2
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero in the middle.
    nums = [1, 0, 2, 3]
    target = 2
    expected = 2
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero at the end.
    nums = [1, 2, 3, 0]
    target = 2
    expected = 2
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Multiple zeros multiply sign assignments.
    nums = [0, 0, 1, 1]
    target = 0
    expected = 8
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different signs at duplicate indexes.
    nums = [2, 2, 2, 2]
    target = 0
    expected = 6
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive total requires all plus signs.
    nums = [1, 2, 3, 4]
    target = 10
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative total requires all minus signs.
    nums = [1, 2, 3, 4]
    target = -10
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target exceeds positive total with same parity.
    nums = [1, 2, 3]
    target = 8
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target is below negative total with same parity.
    nums = [1, 2, 3]
    target = -8
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd transformed remainder is impossible.
    nums = [1, 2, 3]
    target = 1
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative target with odd transformed remainder.
    nums = [1, 2, 3]
    target = -1
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even remainder but unreachable subset.
    nums = [2, 4, 8]
    target = 0
    expected = 0
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger varied array.
    nums = [1, 2, 3, 4, 5]
    target = 3
    expected = 3
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Descending values.
    nums = [5, 4, 3, 2, 1]
    target = -3
    expected = 3
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum value total and positive target.
    nums = [1000]
    target = 1000
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum negative target.
    nums = [1000]
    target = -1000
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array size with repeated values.
    nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    target = 0
    expected = 184756
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array size and total.
    nums = [
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
    ]
    target = 1000
    expected = 1
    result = target_sum(nums, target)
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
