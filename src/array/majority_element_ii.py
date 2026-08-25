"""Majority Element II

Given an integer array ``nums`` of size ``n``, return all elements that appear
more than ``n / 3`` times in the array. The output may be returned in any
order.

Example 1:
    Input: nums = [1, 2, 1, 1, 3, 2]
    Output: [1]

    Explanation: Here, n / 3 = 6 / 3 = 2. The value 1 appears 3 times, which
    is more than 2.

Example 2:
    Input: nums = [1, 2, 1, 1, 3, 2, 2]
    Output: [1, 2]

    Explanation: Here, n / 3 = 7 / 3. Both 1 and 2 appear 3 times, which is
    more than n / 3.

Constraints:
    - n == nums.length
    - 2 <= n <= 10^5
    - -10^4 <= nums[i] <= 10^4

https://www.youtube.com/watch?v=vwZj1K0e9U8&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=19
"""

from collections import defaultdict


def majority_element_ii_brute_froce(nums: list[int]) -> list[int]:
    """Return all values appearing more than one-third of the input size.

    Approach: Brute-Force Frequency Counting
        1. Store the input size, create the result list, and calculate the
           integer frequency threshold as ``size // 3``.
        2. Treat each value in ``nums`` as a possible majority candidate.
        3. Reset the candidate's count before examining it.
        4. Skip a candidate that is already in ``result`` so the same majority
           value is not returned more than once. Membership in ``result`` is
           effectively O(1) here because there can be at most two valid
           majority elements.
        5. For a candidate not already returned, scan the complete input and
           count every matching occurrence.
        6. Append the candidate when its frequency is strictly greater than
           ``size // 3``. The strict ``>`` matches the problem requirement of
           appearing more than ``n / 3`` times.
        7. Stop once two valid values have been found because three different
           values cannot each occur more than one-third of the time.
        8. Return the list of qualifying values in encounter order.

    Parameters:
        nums: An integer list containing at least two elements.

    Returns:
        A list containing every distinct value whose frequency is greater than
        ``len(nums) / 3``. The list contains at most two values.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n^2) in the worst case. Up to n candidates can each cause a complete
        O(n) scan of the input. This is too slow for the maximum constraint of
        100,000 elements.

    Space Complexity:
        O(1) additional space. The result contains at most two values, and the
        function otherwise stores only integer variables.

    Current Limitation:
        The current implementation contains invalid syntax in its candidate
        membership condition: ``if len(candidate not in result:``. The intended
        uniqueness check described above cannot execute until that syntax is
        corrected.
    """
    # 1. Initialize the size, result, and strict one-third threshold.
    size: int = len(nums)
    result: list[int] = []

    min_count: int = size // 3

    # 2. Treat each input value as a possible majority candidate.
    for candidate in nums:
        # 3. Reset the frequency for the current candidate.
        count: int = 0

        # 4. Avoid recounting a candidate already present in the result.
        if len(candidate not in result):
            # 5. Count the candidate across the complete input.
            for new_candidate in nums:
                if candidate == new_candidate:
                    count += 1

            # 6. Add candidates occurring strictly more than size // 3 times.
            if count > min_count:
                result.append(candidate)

        # 7. At most two distinct values can satisfy the threshold.
        if len(result) == 2:
            break

    # 8. Return the qualifying values in encounter order.
    return result


def majority_element_ii_time_optimized(nums: list[int]) -> list[int]:
    """Return all values appearing more than one-third of the input size.

    Approach: Frequency Map
        Count values during one traversal using a dictionary. A value qualifies
        once its frequency becomes strictly greater than ``len(nums) / 3``.

        1. Create a frequency map whose missing keys begin with count zero, and
           create the result list.
        2. Calculate the integer threshold as ``len(nums) // 3``.
        3. Traverse every number in the input.
        4. Increment the current number's frequency in the map.
        5. Append the number only when its frequency becomes exactly
           ``minimum_count + 1``. This is the first count strictly greater than
           ``n / 3``. Using equality instead of ``>`` ensures the same number
           is appended only once if it appears additional times later.
        6. Stop after finding two qualifying numbers. At most two distinct
           values can each occur more than one-third of the time.
        7. Return the qualifying values in the order in which their frequencies
           first crossed the threshold. Any output order is permitted.

    Parameters:
        nums: An integer list containing at least two elements.

    Returns:
        A list containing every distinct value whose frequency is greater than
        ``len(nums) / 3``. The list contains zero, one, or two values.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n) expected time, where ``n`` is the length of ``nums``. The function
        scans the input at most once, and dictionary lookup and update
        operations take O(1) expected time.

    Space Complexity:
        O(k) additional space, where ``k`` is the number of distinct values
        encountered before the function finishes. In the worst case, ``k`` can
        be O(n). The returned list itself contains at most two values.

    Assumptions:
        ``2 <= len(nums) <= 100_000``, as guaranteed by the problem constraints.
        Negative numbers, zeroes, and duplicate values are supported.
    """

    # 1. Create the frequency map and result list.
    count_map: defaultdict[int, int] = defaultdict(int)
    result: list[int] = []

    # 2. Calculate the integer one-third threshold.
    min_count: int = len(nums) // 3

    # 3. Process each input number once.
    for num in nums:
        # 4. Increment this number's frequency.
        count_map[num] += 1

        # 5. Append it once, when its count first exceeds the threshold.
        if count_map[num] == min_count + 1:
            result.append(num)

        # 6. Stop after finding the maximum of two qualifying values.
        if len(result) == 2:
            break

    # 7. Return the qualifying values in threshold-crossing order.
    return result


def majority_element_ii_optimized(nums: list[int]) -> list[int]:
    """Return all values appearing more than one-third of the input size.

    Approach: Extended Boyer-Moore Majority Vote Algorithm
        At most two distinct values can appear more than ``n / 3`` times. If
        three values each exceeded that threshold, their combined occurrences
        would be greater than the length of the array. Therefore, track two
        candidates and two vote balances.

        1. Initialize both vote balances and candidate placeholders, calculate
           the integer one-third threshold, and create the result list.
        2. Perform the candidate-selection pass:
           - If the first vote balance is zero and the number differs from the
             second candidate, select it as the first candidate.
           - Otherwise, if the second balance is zero and the number differs
             from the first candidate, select it as the second candidate.
           - If the number matches either candidate, increase that candidate's
             vote balance.
           - If it matches neither candidate, decrease both balances. This
             cancels a group of three different values, which cannot eliminate
             a value that truly appears more than ``n / 3`` times.
        3. Reset both vote balances because the first pass produces possible
           candidates but does not prove their actual frequencies.
        4. Scan the input again and count the real occurrences of both
           candidates.
        5. Append each candidate whose verified count is strictly greater than
           ``len(nums) // 3``.
        6. Return the zero, one, or two verified majority values. Their order is
           valid because the problem allows any output order.

    Parameters:
        nums: An integer list containing at least two elements.

    Returns:
        A list containing every distinct value whose frequency is greater than
        ``len(nums) / 3``.

    Mutation:
        The input list is not modified.

    Time Complexity:
        O(n), where ``n`` is the length of ``nums``. The function performs two
        linear scans, and every operation inside each scan takes constant time.

    Space Complexity:
        O(1) additional space. Only two candidates, two vote balances, the
        threshold, and a result containing at most two values are stored.

    Assumptions:
        ``2 <= len(nums) <= 100_000``, as guaranteed by the problem constraints.
        Candidate placeholders are safe because a zero vote balance indicates
        that the corresponding candidate is not currently active.
    """
    # 1. Initialize vote balances, candidates, threshold, and result.
    votes1: int = 0
    votes2: int = 0
    candidate1: int = 0
    candidate2: int = 0
    threshold: int = len(nums) // 3
    result: list[int] = []

    # 2. Select two possible candidates by matching and canceling votes.
    for num in nums:
        if votes1 == 0 and num != candidate2:
            candidate1 = num
            votes1 += 1
        elif votes2 == 0 and num != candidate1:
            candidate2 = num
            votes2 += 1
        elif num == candidate1:
            votes1 += 1
        elif num == candidate2:
            votes2 += 1
        else:
            votes1 -= 1
            votes2 -= 1

    # 3. Reset the balances before verifying actual candidate frequencies.
    votes1, votes2 = 0, 0

    # 4. Count the real occurrences of both possible candidates.
    for num in nums:
        if num == candidate1:
            votes1 += 1
        elif num == candidate2:
            votes2 += 1

    # 5. Keep only candidates occurring strictly more than n // 3 times.
    if votes1 > threshold:
        result.append(candidate1)

    if votes2 > threshold:
        result.append(candidate2)

    # 6. Return the verified majority values.
    return result


def solve() -> None:
    nums: list[int] = [1, 2, 1, 1, 3, 2]

    expected: list[int] = [1]
    result: list[int] = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2, 2]

    expected = [1, 2]
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = [1, 2]
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]

    expected = []
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2, 3, 4]

    expected = []
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -1, -2, 3]

    expected = [-1, -2]
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000]

    expected = [-10_000]
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000] * 100_000

    expected = [10_000]
    result = majority_element_ii_brute_froce(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2]

    expected = [1]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2, 2]

    expected = [1, 2]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2, 2, 3]

    expected = [1, 2]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = [1, 2]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]

    expected = []
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2, 3, 4]

    expected = []
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -1, -2, 3]

    expected = [-1, -2]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000]

    expected = [-10_000]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000] * 33_333 + [-10_000] * 33_333 + [0] * 33_334

    expected = [0]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1, 2, 3]

    expected = [1]
    result = majority_element_ii_time_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2, 2]

    expected = [1, 2]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2]

    expected = [1]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 1, 1, 3, 2, 2, 3]

    expected = [1, 2]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = [1, 2]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]

    expected = []
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2, 3, 4]

    expected = []
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -1, -2, 3]

    expected = [-1, -2]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10_000, -10_000, 10_000]

    expected = [-10_000]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1, 2, 3]

    expected = [1]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000] * 33_333 + [-10_000] * 33_333 + [0] * 33_334

    expected = [0]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10_000] * 100_000

    expected = [10_000]
    result = majority_element_ii_optimized(nums)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
