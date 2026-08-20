"""Sort an Array of 0s, 1s, and 2s

Given an array ``nums`` consisting only of 0, 1, and 2, sort the array in
non-decreasing order.

The sorting must be done in place without making a copy of the original array.

Example 1:
    Input: nums = [1, 0, 2, 1, 0]
    Output: [0, 0, 1, 1, 2]
    Explanation: The sorted array has two zeroes, two ones, and one two.

Example 2:
    Input: nums = [0, 0, 1, 1, 1]
    Output: [0, 0, 1, 1, 1]
    Explanation: The sorted array has two zeroes, three ones, and no twos.

Now your turn:
    Input: nums = [1, 1, 2, 2, 1]
    Output: [1, 1, 1, 2, 2]

Constraints:
    - 1 <= len(nums) <= 10^5
    - nums[i] is 0, 1, or 2
https://www.youtube.com/watch?v=tp8JIuCXBaU&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=6
"""

from collections import Counter
from contextlib import redirect_stdout
from io import StringIO


def sort_array_of_zeros_ones_and_twos(nums: list[int]) -> None:
    """Sort ``nums`` in place using the frequencies of 0, 1, and 2.

    Approach: Counting Sort
        1. Count how many times each allowed value appears in ``nums``.
        2. Store the input size and initialize an index at the beginning of the
           array.
        3. Visit every position in ``nums`` from left to right.
        4. Write the smallest value whose remaining frequency is positive:
           write all zeroes first, followed by all ones and then all twos. After
           writing a value, decrement its remaining frequency.
        5. Advance the index and continue until every position has been
           overwritten in non-decreasing order. The function returns ``None``
           because it modifies the original list directly.

    Time Complexity:
        O(n), where n is the length of ``nums``. Constructing the Counter scans
        all n elements once, and the while loop overwrites all n positions once.
        These two consecutive passes simplify to O(n) total time.

    Space Complexity:
        O(1) auxiliary space under the problem's constraints. A Counter normally
        requires O(k) space for k distinct values, but ``nums`` can contain only
        0, 1, and 2, so it stores at most three keys regardless of n. The size
        and index variables also use constant space.
    """
    # Step 1: Count each of the three possible values.
    frequency_count: Counter[int] = Counter(nums)

    # Step 2: Store the input size and initialize the writing index.
    size: int = len(nums)
    index: int = 0

    # Step 3: Visit every position that must be overwritten.
    while index < size:
        # Step 4: Write the smallest remaining value and consume one count.
        if frequency_count[0] > 0:
            nums[index] = 0
            frequency_count[0] -= 1
        elif frequency_count[1] > 0:
            nums[index] = 1
            frequency_count[1] -= 1
        elif frequency_count[2] > 0:
            nums[index] = 2
            frequency_count[2] -= 1

        # Step 5: Advance to the next output position.
        index += 1


def sort_array_of_zeros_ones_and_twos_optimized(nums: list[int]) -> None:
    """Sort a list containing only 0, 1, and 2 in place.

    ``nums`` is the list to mutate. The function returns ``None`` because the
    sorted values replace the contents of the original list. It assumes every
    element is 0, 1, or 2, as required by the problem constraints.

    This implementation uses the Dutch National Flag algorithm to partition
    the three possible values with ``low``, ``mid``, and ``high`` pointers.

    Approach: Dutch National Flag Algorithm
        1. Initialize three pointers: ``low`` marks where the next 0 belongs,
           ``mid`` marks the current unprocessed value, and ``high`` marks where
           the next 2 belongs. These pointers divide the list into a 0 region,
           a 1 region, an unknown region, and a 2 region.

           Region invariants:
               [0 : low]          → sorted zeroes
               [low : mid]        → sorted ones
               [mid : high + 1]   → unprocessed
               [high + 1 : end]   → sorted twos

           The ranges use Python's half-open slice convention: the starting
           index is included and the ending index is excluded.
        2. Process values while the unknown region from ``mid`` through
           ``high`` is not empty.
        3. If ``nums[mid]`` is 0, swap it with ``nums[low]``. Both positions are
           then classified, so advance both ``low`` and ``mid``.
        4. If ``nums[mid]`` is 2, swap it with ``nums[high]`` and move ``high``
           left. Do not advance ``mid`` because the value swapped in from the
           right side has not been examined yet.
        5. Otherwise, ``nums[mid]`` is 1 and is already in the correct middle
           region, so advance only ``mid``.
        6. When ``mid`` passes ``high``, the unknown region is empty and the
           original list is sorted in non-decreasing order.

    Time Complexity:
        O(n), where n is the length of ``nums``. Every loop iteration either
        advances ``mid`` or decreases ``high``. Each pointer moves in only one
        direction and can cross the list at most once.

    Space Complexity:
        O(1) auxiliary space. The algorithm stores only ``size`` and the three
        integer pointers and performs all swaps inside the original list.
    """
    # Step 1: Initialize the boundaries of the four logical regions.
    size: int = len(nums)
    low: int = 0
    mid: int = 0
    high: int = size - 1

    # Step 2: Continue until the unknown region has been fully processed.
    while mid <= high:
        # Step 3: Move a 0 into the low region and advance both pointers.
        if nums[mid] == 0:
            nums[mid], nums[low] = nums[low], nums[mid]
            low += 1
            mid += 1

        # Step 4: Move a 2 into the high region and recheck the swapped-in value.
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

        # Step 5: A 1 already belongs in the middle region, so advance mid.
        else:
            mid += 1

    # Step 6: The original list is now sorted; the function returns None.


def solve() -> None:
    nums: list[int] = [1, 0, 2, 1, 0]

    expected: list[int] = [0, 0, 1, 1, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 1, 1]

    expected = [0, 0, 1, 1, 1]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2, 1]

    expected = [1, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 1, 2, 2]

    expected = [0, 0, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 1, 1, 0, 0]

    expected = [0, 0, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = [0]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = [1]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2]

    expected = [2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0]

    expected = [0, 0, 0, 0]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1]

    expected = [1, 1, 1, 1]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2, 2]

    expected = [2, 2, 2, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 0, 2, 0]

    expected = [0, 0, 2, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 0]

    expected = [0, 1, 2]
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 0, 1, 2, 0, 1]
    original_id: int = id(nums)

    expected = True
    sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = id(nums) == original_id and nums == [0, 0, 1, 1, 2, 2]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = ([2] * 33_334) + ([1] * 33_333) + ([0] * 33_333)

    expected = True
    with redirect_stdout(StringIO()):
        sort_array_of_zeros_ones_and_twos_optimized(nums)
    result = (
        len(nums) == 100_000
        and nums[:33_333] == [0] * 33_333
        and nums[33_333:66_666] == [1] * 33_333
        and nums[66_666:] == [2] * 33_334
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """
    nums: list[int] = [1, 0, 2, 1, 0]

    expected: list[int] = [0, 0, 1, 1, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 1, 1]

    expected = [0, 0, 1, 1, 1]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2, 1]

    expected = [1, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 1, 1, 2, 2]

    expected = [0, 0, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 1, 1, 0, 0]

    expected = [0, 0, 1, 1, 2, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0]

    expected = [0]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = [1]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2]

    expected = [2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [0, 0, 0, 0]

    expected = [0, 0, 0, 0]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1]

    expected = [1, 1, 1, 1]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 2, 2, 2]

    expected = [2, 2, 2, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 0, 2, 0]

    expected = [0, 0, 2, 2]
    sort_array_of_zeros_ones_and_twos(nums)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [2, 0, 1, 2, 0, 1]
    original_id: int = id(nums)

    expected = True
    sort_array_of_zeros_ones_and_twos(nums)
    result = id(nums) == original_id and nums == [0, 0, 1, 1, 2, 2]

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = ([2] * 33_334) + ([1] * 33_333) + ([0] * 33_333)

    expected = True
    sort_array_of_zeros_ones_and_twos(nums)
    result = (
        len(nums) == 100_000
        and nums[:33_333] == [0] * 33_333
        and nums[33_333:66_666] == [1] * 33_333
        and nums[66_666:] == [2] * 33_334
    )

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    """


if __name__ == "__main__":
    solve()
