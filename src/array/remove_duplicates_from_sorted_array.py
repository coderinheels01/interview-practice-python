"""Remove Duplicates from Sorted Array

Given an integer array ``nums`` sorted in non-decreasing order, remove all
duplicates in place so that each unique element appears only once.

Return the number of unique elements in the array.

If the number of unique elements is ``k``:
    - Change ``nums`` so that its first ``k`` elements contain the unique
      values in the order in which they originally appeared.
    - The remaining elements and the size of the array do not matter for
      correctness.
    - The driver code assesses correctness by checking only the first ``k``
      elements of the modified array.

An array sorted in non-decreasing order is an array where every element to the
right of an element is equal to or greater than that element.

Example 1:
    Input: nums = [0, 0, 3, 3, 5, 6]
    Output: 4
    Explanation: The resulting array is [0, 3, 5, 6, _, _]. There are four
    distinct elements, and the elements marked with _ may have any value.

Example 2:
    Input: nums = [-2, 2, 4, 4, 4, 4, 5, 5]
    Output: 4
    Explanation: The resulting array is [-2, 2, 4, 5, _, _, _, _]. There are
    four distinct elements, and the elements marked with _ may have any value.

Now your turn:
    Input: nums = [-30, -30, 0, 0, 10, 20, 30, 30]
    Select the possible resulting array:
        - [-30, 0, 10, 20, 30, _, _]
        - [-30, 0, 10, 20, 30, _, _, _]
        - [-30, 10, 0, 20, 30, _, _, _]
        - [-30, 0, 0, 10, 20, _, _, _]

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    - nums is sorted in non-decreasing order.

    https://www.youtube.com/watch?v=37E9ckMDdTk&t=767s
"""


def remove_duplicates_less_efficient(nums: list[int]) -> int:
    i: int = 0

    while nums and i < len(nums) - 1:
        if nums[i] == nums[i + 1]:
            nums.pop(i)
        else:
            i += 1

    return len(nums)


def remove_duplicates_brute_force(nums: list[int]) -> int:
    """Move the unique values to the front of ``nums`` and return their count.

    Approach:
        1. Pass ``nums`` to ``dict.fromkeys``. Dictionary keys are unique and
           preserve insertion order, so duplicate values are removed while
           the original order of the distinct values is retained.
        2. Convert the dictionary keys into a list named ``unique``.
        3. Traverse ``unique`` with each value's index and overwrite the same
           index at the front of ``nums``. Values after the unique prefix do
           not matter for this problem.
        4. Return the length of ``unique``, which is the number of distinct
           elements and the size of the valid prefix in ``nums``.

    Time Complexity:
        O(n) on average, where n is the length of ``nums``. Building the
        dictionary and list takes O(n), and copying at most n unique values
        back into ``nums`` takes O(n). Dictionary insertion can theoretically
        degrade with extreme hash collisions.

    Space Complexity:
        O(n), because the dictionary and ``unique`` list may each contain all
        n input values when every element is distinct. This does not satisfy
        the intended O(1) extra-space requirement of the in-place problem.
    """
    # Steps 1 and 2: Remove duplicates while preserving their original order.
    unique: list[int] = list(dict.fromkeys(nums))

    # Step 3: Copy the ordered unique values into the front of nums.
    for i, num in enumerate(unique):
        nums[i] = num

    # Step 4: Return the length of the valid unique prefix.
    return len(unique)


def remove_duplicates_space_optimized(nums: list[int]) -> int:
    """Move unique values to the front of ``nums`` using constant extra space.

    Approach: Two Pointers
        1. Store the length of ``nums`` and initialize ``last_unique_index`` to
           index 0 because the first element is always the first unique value.
        2. Use ``first_different_index`` to scan the array from index 1 through
           the final index.
        3. Compare the value at ``first_different_index`` with the most recently
           stored unique value at ``last_unique_index``.
        4. When the values differ, copy the new unique value into the position
           immediately after ``last_unique_index``, then advance
           ``last_unique_index``. When they are equal, leave both the valid
           unique prefix and ``last_unique_index`` unchanged.
        5. Return ``last_unique_index + 1`` because an index is zero-based, while
           the required result is the number of unique elements.

    Time Complexity:
        O(n), where n is the length of ``nums``. The for loop examines every
        element after the first exactly once, and each iteration takes O(1)
        time.

    Space Complexity:
        O(1), because the function modifies ``nums`` in place and uses only
        ``n``, ``last_unique_index``, and ``first_different_index`` regardless
        of the input size.
    """
    # Step 1: Store the length and identify index 0 as the first unique value.
    n: int = len(nums)

    last_unique_index: int = 0

    # Step 2: Scan every element after the first.
    for first_different_index in range(1, n):
        # Step 3: Compare the current value with the last stored unique value.
        if nums[last_unique_index] != nums[first_different_index]:
            # Step 4: Place the new unique value after the valid unique prefix.
            nums[last_unique_index + 1] = nums[first_different_index]
            last_unique_index += 1

    # Step 5: Convert the final zero-based index into the unique-element count.
    return last_unique_index + 1


def solve() -> None:
    nums: list[int] = [0, 0, 3, 3, 5, 6]

    expected: tuple[int, list[int]] = (4, [0, 3, 5, 6])
    k: int = remove_duplicates_space_optimized(nums)
    result: tuple[int, list[int]] = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 2, 4, 4, 4, 4, 5, 5]

    expected = (4, [-2, 2, 4, 5])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-30, -30, 0, 0, 10, 20, 30, 30]

    expected = (5, [-30, 0, 10, 20, 30])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = (1, [1])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1]

    expected = (1, [1])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = (4, [1, 2, 3, 4])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, -3, -2, -2, -1, -1]

    expected = (3, [-3, -2, -1])
    k = remove_duplicates_space_optimized(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [0, 0, 3, 3, 5, 6]

    expected: tuple[int, list[int]] = (4, [0, 3, 5, 6])
    k: int = remove_duplicates_brute_force(nums)
    result: tuple[int, list[int]] = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 2, 4, 4, 4, 4, 5, 5]

    expected = (4, [-2, 2, 4, 5])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-30, -30, 0, 0, 10, 20, 30, 30]

    expected = (5, [-30, 0, 10, 20, 30])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = (1, [1])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1]

    expected = (1, [1])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = (4, [1, 2, 3, 4])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, -3, -2, -2, -1, -1]

    expected = (3, [-3, -2, -1])
    k = remove_duplicates_brute_force(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums: list[int] = [0, 0, 3, 3, 5, 6]

    expected: tuple[int, list[int]] = (4, [0, 3, 5, 6])
    k: int = remove_duplicates_less_efficient(nums)
    result: tuple[int, list[int]] = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-2, 2, 4, 4, 4, 4, 5, 5]

    expected = (4, [-2, 2, 4, 5])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-30, -30, 0, 0, 10, 20, 30, 30]

    expected = (5, [-30, 0, 10, 20, 30])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = (1, [1])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 1]

    expected = (1, [1])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = (4, [1, 2, 3, 4])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-3, -3, -2, -2, -1, -1]

    expected = (3, [-3, -2, -1])
    k = remove_duplicates_less_efficient(nums)
    result = (k, nums[:k])

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
