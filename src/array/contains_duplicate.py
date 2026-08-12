"""217. Contains Duplicate

Difficulty: Easy

Given an integer array ``nums``, return ``True`` if any value appears at least
twice in the array, and return ``False`` if every element is distinct.

Example 1:
    Input: nums = [1, 2, 3, 1]
    Output: True
    Explanation: The element 1 occurs at indices 0 and 3.

Example 2:
    Input: nums = [1, 2, 3, 4]
    Output: False
    Explanation: All elements are distinct.

Example 3:
    Input: nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    Output: True

Constraints:
    - 1 <= nums.length <= 10^5
    - -10^9 <= nums[i] <= 10^9
"""


def contains_duplicate_time_optimized(nums: list[int]) -> bool:
    """Return whether any integer appears more than once in ``nums``.

    Approach:
        1. Convert the list into a set, which keeps only one copy of each
           distinct value.
        2. Compare the number of distinct values with the original number of
           values. If the lengths differ, at least one duplicate was removed
           while creating the set.

    Time Complexity:
        O(n) on average, where n is the number of values in ``nums``. Creating
        the set visits each value once, and getting the lengths is O(1).

    Space Complexity:
        O(n), because the set can contain all n values when every value is
        distinct.
    """
    # 1. Create a set of distinct values. 2. Compare its size with the list.
    return len(nums) != len(set(nums))


def contains_duplicate_space_optimized(nums: list[int]) -> bool:
    """Return whether any integer appears more than once in ``nums``.

    Approach:
        1. Treat ``nums`` as a complete binary tree and build a max heap in
           place by sifting each non-leaf node down. ``sift_down`` uses a loop
           instead of recursion so it requires constant auxiliary space.
        2. Sort the heap in place. Swap the maximum value at the root with the
           last value in the unsorted region, shrink the heap boundary, and
           sift the new root down. Repeating this produces ascending order.
        3. Scan every adjacent pair in the sorted list. Sorting places equal
           values next to each other, so an equal pair means a duplicate
           exists. If no adjacent pair is equal, all values are distinct.

    Time Complexity:
        O(n log n), where n is the number of values in ``nums``. Building the
        heap takes O(n), heap sort takes O(n log n), and the final scan takes
        O(n).

    Space Complexity:
        O(1), because heap sort and ``sift_down`` operate iteratively in place
        without creating an additional collection.

    Note:
        This function mutates ``nums`` by sorting it.
    """

    n: int = len(nums)
    right_boundary: int = n

    def sift_down(current_index: int):
        while True:
            largest_node_index: int = current_index
            left_node_index: int = 2 * current_index + 1
            right_node_index: int = 2 * current_index + 2

            if (
                left_node_index < right_boundary
                and nums[left_node_index] > nums[largest_node_index]
            ):
                largest_node_index = left_node_index
            if (
                right_node_index < right_boundary
                and nums[right_node_index] > nums[largest_node_index]
            ):
                largest_node_index = right_node_index

            if largest_node_index == current_index:
                return

            nums[current_index], nums[largest_node_index] = (
                nums[largest_node_index],
                nums[current_index],
            )

            current_index = largest_node_index

    def build_max_heap():
        for i in range(n // 2, -1, -1):
            sift_down(i)

    build_max_heap()

    def swap(index1: int , index2:int):
        nums[index1], nums[index2] = nums[index2], nums[index1]

    def heap_sort():
        nonlocal right_boundary
        while right_boundary > 0:
            right_boundary -= 1
            swap(0, right_boundary)
            sift_down(0)

    heap_sort()

    for i in range(n - 1):
        if nums[i] == nums[i+1]:
            return True

    return False


def solve() -> None:
    nums = [1, 2, 3, 1]

    expected = True
    result = contains_duplicate_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 2, 3, 4]

    expected = False
    result = contains_duplicate_space_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]

    expected = True
    result = contains_duplicate_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [1]

    expected = False
    result = contains_duplicate_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-1, -2, -3, -1]

    expected = True
    result = contains_duplicate_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    nums = [-(10**9), 0, 10**9]

    expected = False
    result = contains_duplicate_time_optimized(nums)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
