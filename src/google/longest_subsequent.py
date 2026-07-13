# =============================================================================
# Consecutive Subsequence
#
# Write a function which, given an array of integers, returns the length of the
# longest subsequence where every next value is 1 bigger than the previous one.
# Subsequence might not be consecutive, but must be in the same order as the
# given array.
#
# Example:
#   [3, 1, 2, 3, 4]  -> 4  (subsequence: 1, 2, 3, 4)
#   [1, 2, 3, 4, 5]  -> 5  (entire array)
#   [6, 5, 4, 3, 2]  -> 1  (no increasing consecutive pair)
#
# Approach: Dynamic Programming - https://www.youtube.com/watch?v=cjWnW0hdF1Y&t=2s
#   - dp[i] = length of the longest valid subsequence ending at index i
#   - For each element i, look back at all j < i where nums[i] == nums[j] + 1
#     and extend that chain by 1
#   - Time:  O(n^2)
#   - Space: O(n)
# =============================================================================

def longest_consecutive_subsequence_dp(nums: list[int]) -> int:
    n = len(nums)

    # dp[i] stores the length of the longest consecutive subsequence ending at i
    dp: list[int] = [1] * n  # every element is at minimum a subsequence of length 1

    for i in range(1, n):
        for j in range(i):
            # check if nums[i] is exactly 1 more than nums[j],
            # meaning it can extend the subsequence ending at j
            if nums[i] == nums[j] + 1:
                dp[i] = max(dp[i], dp[j] + 1)

    # the answer is the maximum length found across all ending positions
    return max(dp)

# =============================================================================
# Optimized approach using a hash map
#
# Key insight: instead of tracking chains by index (O(n^2)), track them by
# value. lis[v] = length of the longest consecutive subsequence ending at
# value v seen so far.
#
# For each number `num`:
#   - If num-1 exists in the map, we can extend that chain: lis[num] = lis[num-1] + 1
#   - Otherwise, we start a new chain of length 1
#   - If num appears again later, we overwrite with the longer chain
#     (since we process left-to-right, a later occurrence can only extend
#      a chain that was already built — duplicates are handled naturally)
#
# Time:  O(n)  — single pass, O(1) hash map lookups
# Space: O(n)  — hash map stores at most n distinct values
# =============================================================================
def longest_consecutive_subsequence_optimized(nums: list[int]) -> int:
    best: int = 0
    n: int = len(nums)
    lis: dict[int, int] = {}  # lis[v] = longest consecutive chain ending at value v
    for num in nums:
        # extend the chain ending at num-1, or start a new chain of length 1
        lis[num] = lis.get(num - 1, 0) + 1
        best = max(best, lis[num])
    return best


print()  # blank line separator between the two problems

# =============================================================================
# Below: original problem — longest subsequence where each next value is
# exactly 1 larger, solved with backward DP (forward pass variant above).
# =============================================================================

def longest_subsequent_number_dynamic_programming(nums: list[int]) -> int:
    # Backward DP approach:
    # result[i] = length of the longest consecutive subsequence starting at index i
    n: int = len(nums)
    result: list[int] = [0] * n

    # base case: the last element is always a subsequence of length 1
    result[n-1] = 1

    # iterate from the second-to-last element back to the front
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            # if nums[j] is exactly 1 more than nums[i], extend the chain
            if nums[j] - nums[i] == 1:
                result[i] = max(result[i], 1 + result[j])

    # return the longest chain found starting from any index
    return max(result)


def solve():
    nums:list[int] = [3, 1, 2, 3, 4]
    print(f"DP solution: longest subsequent of {nums} is {longest_subsequent_number_dynamic_programming(nums)}")
    print(f"Optimized: longest subsequent of {nums} is {longest_consecutive_subsequence_optimized(nums)}")
    nums:list[int] = [1, 2, 3, 4, 5, 6]
    print(f"DP solution: longest subsequent of {nums} is {longest_subsequent_number_dynamic_programming(nums)}")
    print(f"Optimized: longest subsequent of {nums} is {longest_consecutive_subsequence_optimized(nums)}")
    nums:list[int] = [6, 5, 4, 3, 2, 1]
    print(f"DP solution: longest subsequent of {nums} is {longest_subsequent_number_dynamic_programming(nums)}")
    print(f"Optimized: longest subsequent of {nums} is {longest_consecutive_subsequence_optimized(nums)}")

solve()