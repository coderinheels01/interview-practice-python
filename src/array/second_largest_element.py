"""Second Largest Element

Given an array of integers ``nums``, return the second-largest element in the
array. If the second-largest element does not exist, return -1.

Example 1:
    Input: nums = [8, 8, 7, 6, 5]
    Output: 7
    Explanation: The largest value in nums is 8, and the second largest is 7.

Example 2:
    Input: nums = [10, 10, 10, 10, 10]
    Output: -1
    Explanation: The only value in nums is 10, so there is no second-largest
    value. Therefore, -1 is returned.

Now your turn:
    Input: nums = [7, 7, 2, 2, 10, 10, 10]
    Output: Choose from 10, 2, 7, or 0.

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - nums may contain duplicate elements.

    https://www.youtube.com/watch?v=37E9ckMDdTk&t=767s
"""


def second_largest_element_brute_force(nums: list[int]) -> int:
    """Return the second-largest distinct value after sorting ``nums``.

    Approach:
        1. Sort ``nums`` in ascending order so the largest values are at the
           end of the array.
        2. Store the array length and take the last element as the largest
           value.
        3. Traverse backward from the second-to-last element toward the start
           of the array.
        4. Return the first value that differs from the largest value. Because
           the array is sorted, this is the second-largest distinct value.
        5. Return -1 if every value is equal to the largest value.

    Time Complexity:
        O(n log n), where n is the length of ``nums``. Sorting dominates the
        runtime, while the backward traversal takes at most O(n) time.

    Space Complexity:
        O(n) in the worst case because Python's in-place list sort may use
        temporary auxiliary storage. The function does not create another
        list, but it modifies the order of the input list.
    """
    # Step 1: Sort the values in ascending order in place.
    nums.sort()

    # Step 2: Store the length and largest value.
    n: int = len(nums)
    largest: int = nums[n - 1]

    # Step 3: Traverse backward from the second-to-last element.
    for i in range(n - 2, -1, -1):
        # Step 4: Return the first value distinct from the largest.
        if nums[i] != largest:
            return nums[i]

    # Step 5: No second-largest distinct value exists.
    return -1


def second_largest_element_optimized1(nums: list[int]) -> int:
    """Return the second-largest distinct value using two array traversals.

    Approach:
        1. Store the length of ``nums`` and return -1 if the array is empty.
        2. Initialize ``largest`` with the first element.
        3. Traverse the remaining elements and update ``largest`` whenever a
           greater value is encountered.
        4. Initialize ``second_largest`` to negative infinity to represent that
           no second-largest distinct value has been found yet.
        5. Traverse the entire array again. For every value distinct from
           ``largest``, update ``second_largest`` when that value is greater
           than the current second-largest candidate.
        6. Return -1 if no second-largest distinct value was found; otherwise,
           return ``second_largest``.

    Time Complexity:
        O(n), where n is the length of ``nums``. The function performs two
        separate linear traversals, O(n) + O(n), which simplifies to O(n).

    Space Complexity:
        O(1), because only ``n``, ``largest``, ``second_largest``, and the loop
        index are used regardless of the input size.
    """
    # Step 1: Store the length and handle an empty input.
    n: int = len(nums)
    if n < 1:
        return -1

    # Step 2: Initialize the largest value with the first element.
    largest: int = nums[0]

    # Step 3: Find the largest value during the first traversal.
    for i in range(1, n):
        largest = max(largest, nums[i])

    # Step 4: Initialize the not-found sentinel for the second-largest value.
    second_largest: int | float = -float("inf")

    # Step 5: Find the largest value that is distinct from the maximum.
    for i in range(n):
        if nums[i] != largest and nums[i] > second_largest:
            second_largest = nums[i]

    # Step 6: Return -1 when no second-largest distinct value exists.
    return -1 if second_largest == -float("inf") else second_largest


def second_largest_element_optimized2(nums: list[int]) -> int:
    """Return the second-largest distinct value in ``nums``, or -1 if absent.

    Approach:
        1. Initialize ``largest`` with the first number and initialize
           ``second_largest`` to negative infinity to represent that no second
           distinct value has been found yet. Store the length of ``nums``.
        2. Traverse indices 1 through n - 1 once because the value at index 0
           is already stored in ``largest``.
        3. If the current number is greater than ``largest``, move the previous
           largest value into ``second_largest`` and make the current number
           the new largest value.
        4. Otherwise, if the current number is smaller than ``largest`` but
           greater than ``second_largest``, record it as the new second-largest
           distinct value. Values equal to ``largest`` are ignored.
        5. After the traversal, return -1 if ``second_largest`` is still
           negative infinity; otherwise, return the second-largest value.

    Time Complexity:
        O(n), where n is the length of ``nums``. The function examines each
        remaining number once, and each iteration takes O(1) time.

    Space Complexity:
        O(1), because the function uses only ``largest``, ``second_largest``,
        ``n``, and the loop index regardless of the input size.
    """
    # Step 1: Initialize the largest value, not-found sentinel, and array length.
    largest: int = nums[0]
    second_largest: float | int = -float("inf")
    n: int = len(nums)

    # Step 2: Examine every remaining number by index once.
    for i in range(1, n):
        # Step 3: Shift the previous largest value into second place.
        if nums[i] > largest:
            second_largest, largest = largest, nums[i]
        # Step 4: Record a distinct value between the current two largest values.
        elif nums[i] < largest and nums[i] > second_largest:
            second_largest = nums[i]

    # Step 5: Return -1 when no second-largest distinct value was found.
    return -1 if second_largest == -float("inf") else second_largest


def solve() -> None:
    nums: list[int] = [8, 8, 7, 6, 5]

    expected: int = 7
    result: int = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, 10, 10, 10, 10]

    expected = -1
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 7, 2, 2, 10, 10, 10]

    expected = 7
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = 1
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = -1
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3]

    expected = -2
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -2]

    expected = -2
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10, 0, 10, 5]

    expected = 5
    result = second_largest_element_brute_force(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [8, 8, 7, 6, 5]

    expected = 7
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, 10, 10, 10, 10]

    expected = -1
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 7, 2, 2, 10, 10, 10]

    expected = 7
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = 1
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = -1
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3]

    expected = -2
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -2]

    expected = -2
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10, 0, 10, 5]

    expected = 5
    result = second_largest_element_optimized1(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [8, 8, 7, 6, 5]

    expected: int = 7
    result: int = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [10, 10, 10, 10, 10]

    expected = -1
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7, 7, 2, 2, 10, 10, 10]

    expected = 7
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2]

    expected = 1
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [5]

    expected = -1
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3]

    expected = -2
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -1, -2]

    expected = -2
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-10, 0, 10, 5]

    expected = 5
    result = second_largest_element_optimized2(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
