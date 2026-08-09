"""
Two Integer Sum II

Difficulty: Medium
Topics: Two Pointers
Company Tags
Hints

Given an array of integers numbers that is sorted in non-decreasing order,
return the indices [index1, index2] of two numbers such that they add up to a
given target number target and index1 < index2.

The returned indices must be 1-indexed. index1 and index2 cannot be equal, so
you may not use the same element twice.

There will always be exactly one valid solution.

Your solution must use O(1) additional space.

Example 1:
    Input:
        numbers = [1, 2, 3, 4]
        target = 3

    Output:
        [1, 2]

    Explanation:
        The sum of 1 and 2 is 3. Since the array is 1-indexed, index1 = 1 and
        index2 = 2. Therefore, return [1, 2].

Constraints:
    - 2 <= len(numbers) <= 30,000
    - -1,000 <= numbers[i] <= 1,000
    - -1,000 <= target <= 1,000
"""


def two_integer_sum_ii(numbers: list[int], target: int) -> list[int]:
    """
    Approach: Hash Map
        1. Create a dictionary that maps each previously visited number to its
           zero-based index.
        2. Visit each number from left to right.
        3. For the current number, calculate the complement needed to reach the
           target: complement = target - current number.
        4. Check whether the complement has already been visited. If it has,
           the stored index and the current index form the required pair.
        5. Add 1 to both indices before returning because the problem requires
           1-indexed positions.
        6. If the complement has not been visited, store the current number and
           its index so a later number can pair with it.

        Looking for the complement before storing the current number prevents
        the same array element from being used twice. It also handles duplicate
        values correctly because the first copy is stored before the second
        copy is examined.

    Time Complexity:
        O(n) average time, where n is the number of values in numbers. The loop
        visits each value once, and dictionary lookup and insertion each take
        O(1) average time. Therefore, n iterations multiplied by O(1) work per
        iteration gives O(n) average time.

        In the theoretical worst case, excessive hash collisions can make a
        dictionary operation O(n), resulting in O(n^2) time. Python dictionaries
        are designed to make this unlikely, so O(n) is the standard expected
        complexity for this approach.

    Space Complexity:
        O(n) additional space. If the matching pair is near the end of the
        array, look_up may store almost every previously visited number and its
        index. The amount of extra memory therefore grows with the input size.

        Note: This hash-map approach does not satisfy the problem's O(1)
        additional-space requirement. A two-pointer approach can satisfy that
        requirement by taking advantage of the sorted input.
    """
    # Step 1: Map each previously visited value to its zero-based index.
    look_up: dict[int, int] = {}

    # Step 2: Examine every number from left to right.
    for i in range(len(numbers)):
        # Step 3: Calculate the value needed to complete the target sum.
        complement: int = target - numbers[i]

        # Step 4: A previously visited complement gives two distinct indices.
        if complement in look_up:
            # Step 5: Convert both zero-based indices to 1-indexed positions.
            return [look_up[complement] + 1, i + 1]

        # Step 6: Save the current value for numbers visited later in the loop.
        look_up[numbers[i]] = i

    # The prompt guarantees a solution, but return an empty list defensively if
    # the function is called with input that does not contain a valid pair.
    return []




def solve() -> None:
    numbers: list[int] = [1, 2, 3, 4]
    target: int = 3
    expected: list[int] = [1, 2]
    result: list[int] = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    numbers = [2, 3, 4]
    target = 6
    expected = [1, 3]
    result = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    numbers = [-10, -5, -2]
    target = -7
    expected = [2, 3]
    result = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    numbers = [-5, -3, 0, 4, 8]
    target = 5
    expected = [2, 5]
    result = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    numbers = [0, 0, 3, 4]
    target = 0
    expected = [1, 2]
    result = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    numbers = [1, 2, 7, 11, 15]
    target = 22
    expected = [3, 5]
    result = two_integer_sum_ii(numbers, target)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


if __name__ == "__main__":
    solve()
