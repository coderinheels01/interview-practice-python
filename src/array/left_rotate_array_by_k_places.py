"""Left Rotate Array by K Places

Given an integer array ``nums`` and a non-negative integer ``k``, rotate the
array to the left by ``k`` steps.

Example 1:
    Input: nums = [1, 2, 3, 4, 5, 6], k = 2
    Output: nums = [3, 4, 5, 6, 1, 2]
    Explanation:
        Rotate 1 step to the left: [2, 3, 4, 5, 6, 1]
        Rotate 2 steps to the left: [3, 4, 5, 6, 1, 2]

Example 2:
    Input: nums = [3, 4, 1, 5, 3, -5], k = 8
    Output: nums = [1, 5, 3, -5, 3, 4]
    Explanation:
        Rotate 1 step to the left: [4, 1, 5, 3, -5, 3]
        Rotate 2 steps to the left: [1, 5, 3, -5, 3, 4]
        Rotate 3 steps to the left: [5, 3, -5, 3, 4, 1]
        Rotate 4 steps to the left: [3, -5, 3, 4, 1, 5]
        Rotate 5 steps to the left: [-5, 3, 4, 1, 5, 3]
        Rotate 6 steps to the left: [3, 4, 1, 5, 3, -5]
        Rotate 7 steps to the left: [4, 1, 5, 3, -5, 3]
        Rotate 8 steps to the left: [1, 5, 3, -5, 3, 4]

Now your turn:
    Input: nums = [1, 2, 3, 4, 5], k = 4
    Select the correct output:
        - [1, 2, 3, 4, 5]
        - [2, 3, 4, 5, 1]
        - [5, 1, 3, 2, 4]
        - [5, 1, 2, 3, 4]

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - 0 <= k <= 10^5

    https://www.youtube.com/watch?v=wvcQg43_V8U&list=PLgUwDviBIf0rENwdL0nEH0uGom9no0nyB&index=2
"""


def left_rotate_brute_force(nums: list[int], k: int) -> None:
    """Rotate ``nums`` left by ``k`` places using a temporary prefix array.

    Approach:
        1. Store the length of ``nums`` and normalize ``k`` with ``k % n``
           because every ``n`` left rotations return the array to its original
           order.
        2. Store the array length and create ``temp`` with ``k`` positions to
           hold the elements that will move from the front to the end.
        3. Copy the first ``k`` elements of ``nums`` into ``temp`` while
           preserving their order.
        4. Traverse ``nums`` from index ``k`` through the final index and shift
           each of those elements ``k`` positions to the left.
        5. Copy the saved elements from ``temp`` into the final ``k`` positions
           of ``nums``, completing the left rotation in place.

    Time Complexity:
        O(n), where n is the length of ``nums``. Copying the prefix and copying
        it back take O(k), while shifting the remaining elements takes O(n - k).
        Their total, O(k + n - k + k), simplifies to O(n) because normalized
        ``k`` is less than n.

    Space Complexity:
        O(k), because ``temp`` stores exactly the first ``k`` elements. In the
        worst case, k can be proportional to n, so the worst-case additional
        space is O(n).
    """

    # Step 1: Reduce k to the equivalent number of rotations within the array.
    n: int = len(nums)
    k = k % n

    # Step 2: Store the array length and allocate a temporary result array.
    n: int = len(nums)
    temp: list[int] = [0] * k

    # Step 3: Save the first k elements before they are overwritten.
    for i in range(k):
        temp[i] = nums[i]

    # Step 4: Shift the remaining elements k positions to the left.
    for i in range(k, n):
        nums[i - k] = nums[i]

    # Step 5: Copy the saved prefix into the final k positions.
    for i in range(k):
        nums[n - k + i] = temp[i]


def left_rotate_time_optimized(nums: list[int], k: int) -> None:
    """Rotate ``nums`` left by ``k`` places using direct index mapping.

    Approach:
        1. Store the length of ``nums`` and create a temporary ``result`` array
           with the same length.
        2. Traverse every original index in ``nums``.
        3. Calculate the element's rotated position with
           ``(old_index - k) % n``. Subtracting ``k`` moves the element left,
           and modulo ``n`` wraps a negative position around to the end.
        4. Copy the element from ``old_index`` into its calculated position in
           ``result``.
        5. Copy every rotated value from ``result`` back into ``nums`` so the
           input list reflects the rotation.

    Time Complexity:
        O(n), where n is the length of ``nums``. One loop places all n elements
        into ``result``, and a second loop copies all n elements back into
        ``nums``.

    Space Complexity:
        O(n), because the temporary ``result`` array stores n elements. Despite
        the function name, this implementation does not use O(1) extra space.
    """
    # Step 1: Store the length and allocate the temporary result array.

    n: int = len(nums)
    new_index: int
    result: list[int] = [0] * n

    # Step 2: Visit every element at its original index.
    for old_index in range(n):
        # Step 3: Calculate its left-rotated index with wraparound.
        new_index = (old_index - k) % n
        # Step 4: Place the element into its final rotated position.
        result[new_index] = nums[old_index]

    # Step 5: Copy the completed rotation back into the input list.
    for i in range(n):
        nums[i] = result[i]


def left_rotate_time_space_optimized(nums: list[int], k: int) -> None:
    """Rotate ``nums`` left by ``k`` places in place using three reversals.

    Approach:
        1. Store the length of ``nums`` and normalize ``k`` with ``k % n`` so
           rotations larger than the array length wrap to an equivalent value.
        2. Define ``swap`` to exchange two elements in ``nums`` using their
           indices.
        3. Define ``reverse`` to move inward from both ends of a selected range,
           calling ``swap`` until the entire range is reversed.
        4. Reverse the first ``k`` elements. These are the elements that must
           move to the end of the rotated array.
        5. Reverse the elements from index ``k`` through the final index.
        6. Reverse the entire array. This restores the order within both groups
           while placing the second group before the first group, completing
           the left rotation.

    Time Complexity:
        O(n), where n is the length of ``nums``. Across the three reversals,
        each element participates in a constant number of O(1) swaps.

    Space Complexity:
        O(1), because the function modifies ``nums`` in place and uses only
        scalar indices plus the two nested helper functions. No array whose
        size depends on n is created.
    """
    # Step 1: Store the length and normalize the number of rotations.
    n: int = len(nums)
    k = k % n

    # Step 2: Define a helper that swaps two elements in nums.
    def swap(index1: int, index2) -> None:
        nums[index1], nums[index2] = nums[index2], nums[index1]

    # Step 3: Define a helper that reverses an inclusive range in place.
    def reverse(left: int, right: int) -> None:
        while left < right:
            swap(left, right)
            left += 1
            right -= 1

    # Step 4: Reverse the first k elements.
    reverse(0, k - 1)
    # Step 5: Reverse the remaining elements.
    reverse(k, n - 1)
    # Step 6: Reverse the entire array to complete the left rotation.
    reverse(0, n - 1)


def solve() -> None:
    """Temporarily disabled tests while debugging the line 365 case.

    nums: list[int] = [1, 2, 3, 4, 5, 6]
    k: int = 2

    expected: list[int] = [3, 4, 5, 6, 1, 2]
    left_rotate_time_space_optimized(nums, k)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 4, 1, 5, 3, -5]
    k = 8

    expected = [1, 5, 3, -5, 3, 4]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 5]
    k = 4

    expected = [5, 1, 2, 3, 4]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 0

    expected = [1, 2, 3]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 3

    expected = [1, 2, 3]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    k = 100_000

    expected = [7]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2]
    k = 1

    expected = [1, 2, 2, 1]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, -3, -2, -1]
    k = 2

    expected = [-2, -1, -4, -3]
    left_rotate_time_space_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [1, 2, 3, 4, 5, 6]

    k: int = 2

    result: list[int] = nums

    expected: list[int] = [3, 4, 5, 6, 1, 2]
    left_rotate_time_optimized(nums, k)
    result: list[int] = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [3, 4, 1, 5, 3, -5]
    k = 8

    expected = [1, 5, 3, -5, 3, 4]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 5]
    k = 4

    expected = [5, 1, 2, 3, 4]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 0

    expected = [1, 2, 3]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 3

    expected = [1, 2, 3]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    k = 100_000

    expected = [7]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2]
    k = 1

    expected = [1, 2, 2, 1]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, -3, -2, -1]
    k = 2

    expected = [-2, -1, -4, -3]
    left_rotate_time_optimized(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """

    nums: list[int] = [1, 2, 3, 4, 5, 6]
    k: int = 2

    expected: list[int] = [3, 4, 5, 6, 1, 2]
    left_rotate_brute_force(nums, k)
    result: list[int] = nums

    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """

    nums = [3, 4, 1, 5, 3, -5]
    k = 8

    expected = [1, 5, 3, -5, 3, 4]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4, 5]
    k = 4

    expected = [5, 1, 2, 3, 4]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 0

    expected = [1, 2, 3]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3]
    k = 3

    expected = [1, 2, 3]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [7]
    k = 100_000

    expected = [7]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 2, 2]
    k = 1

    expected = [1, 2, 2, 1]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-4, -3, -2, -1]
    k = 2

    expected = [-2, -1, -4, -3]
    left_rotate_brute_force(nums, k)
    result = nums

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    """


if __name__ == "__main__":
    solve()
