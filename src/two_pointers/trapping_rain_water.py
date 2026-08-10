"""
Trapping Rain Water

Difficulty: Hard
Topics: Two Pointers
Company Tags
Hints

You are given an array of non-negative integers height that represents an
elevation map. Each value height[i] represents the height of a bar with a width
of 1.

Return the maximum area of water that can be trapped between the bars.

Example 1:
    Input:
        height = [0, 2, 0, 3, 1, 0, 1, 3, 2, 1]

    Output:
        9

Constraints:
    - 1 <= len(height) <= 20,000
    - 0 <= height[i] <= 100,000
"""


def trapping_rain_water_brute_force(heights: list[int]) -> int:
    """
    Approach: Brute-Force Left and Right Maximums
        1. Return 0 when there are fewer than three bars. Trapped water requires
           a left boundary, an interior position, and a right boundary.
        2. For each index i, scan every bar to its left to find the index of the
           tallest left boundary.
        3. Scan every bar to the right of i to find the index of the tallest
           right boundary.
        4. If both boundaries exist, the water level at i is limited by the
           shorter boundary. Calculate:

               water at i = min(max_left, max_right) - heights[i]

        5. Add the calculated amount only when it is positive. A negative or
           zero value means the current bar is at least as tall as the limiting
           boundary and therefore holds no water above it.
        6. Repeat this independent boundary search for every position and return
           the accumulated amount of trapped water.

    Time Complexity:
        O(n^2), where n is the number of bars. The outer for loop runs n times.
        At index i, max_left scans i positions and max_right scans n - i - 1
        positions. Together, the helpers examine:

            i + (n - i - 1) = n - 1

        positions during each outer iteration. Across all n iterations, this is
        n * (n - 1) = n^2 - n operations, which simplifies to O(n^2). The
        repeated rescanning of the same bars for different values of i is why
        this is considered a brute-force approach.

    Space Complexity:
        O(1) additional space. The algorithm uses a fixed number of integer
        variables for the total, indices, boundaries, and current water. The
        helper functions scan the input directly and do not create arrays,
        dictionaries, or other collections that grow with n. They are not
        recursive, so their call-stack usage is also constant.
    """
    # Step 1: At least three bars are required to trap any water.
    if len(heights) < 3:
        return 0

    # Track the accumulated water and the input length.
    body_of_water: int = 0
    n: int = len(heights)
    left: int = 0
    right: int = left + 1

    # Step 2: Scan all positions left of the current bar for the tallest one.
    def max_left(left: int) -> int:
        index: int = left - 1
        max_index: int = -1
        while index >= 0:
            if max_index == -1 or heights[index] > heights[max_index]:
                max_index = index
            index -= 1
        return max_index

    # Step 3: Scan all positions right of the current bar for the tallest one.
    def max_right(right: int) -> int:
        index: int = right + 1
        max_index: int = -1
        while index < n:
            if max_index == -1 or heights[index] > heights[max_index]:
                max_index = index
            index += 1
        return max_index

    # Step 6: Calculate the independently trapped water at every position.
    for i in range(n):
        # Steps 2 and 3: Find the tallest boundary on each side of i.
        max_left_index: int = max_left(i)
        max_right_index: int = max_right(i)

        # Step 4: Both boundaries must exist before this position can hold water.
        if max_left_index > -1 and max_right_index > -1:
            current_water = (
                min(heights[max_left_index], heights[max_right_index]) - heights[i]
            )

            # Step 5: Add only water above the current bar, never a negative area.
            if current_water > 0:
                body_of_water += (
                    min(heights[max_left_index], heights[max_right_index]) - heights[i]
                )

    # Step 6: Return the total water held across every position.
    return body_of_water


def trapping_rain_water(heights: list[int]) -> int:
    """
    Approach: Prefix/Suffix Maximum Preprocessing (Dynamic Programming)
        This technique precomputes information that would otherwise be searched
        repeatedly for every position. The left maximums are prefix information,
        and the right maximums are suffix information. It is also considered a
        dynamic-programming approach because each maximum reuses the answer from
        the adjacent, previously solved subproblem.

        1. Create two arrays of length n. Despite their names, left_max_height
           and right_max_height store indices: left_max_height[i] identifies the
           tallest bar from index 0 through i, and right_max_height[i] identifies
           the tallest bar from index i through n - 1.
        2. Initialize the first left-maximum index to 0 and the last
           right-maximum index to n - 1. At those endpoints, the only available
           maximum is the bar itself.
        3. Build left_max_height from left to right. At each index, compare the
           current bar with the tallest bar found before it and store the index
           of the taller one.
        4. Build right_max_height from right to left. At each index, compare the
           current bar with the tallest bar found to its right and store the
           index of the taller one.
        5. For every position, use the stored indices to find its tallest left
           and right boundaries. Water is limited by the shorter boundary, so
           calculate:

               water at i = min(max left height, max right height) - heights[i]

           Because both maximum ranges include i, each boundary is at least as
           tall as heights[i], so this value cannot be negative.
        6. Add the water from every position and return the total.

    Time Complexity:
        O(n), where n is the number of bars. Initializing each maximum-index
        array takes O(n). The left-to-right loop visits n - 1 positions, the
        right-to-left loop visits n - 1 positions, and the final water loop
        visits n positions. Each iteration performs only O(1) indexing,
        comparisons, arithmetic, and assignment. The total is therefore
        O(n) + O(n) + O(n) = O(n).

    Space Complexity:
        O(n) additional space. left_max_height and right_max_height each contain
        n integer indices, requiring O(n) + O(n) = O(n) space. The remaining
        variables, including n, i, and body_of_water, use O(1) space. The input
        is read directly and is not modified.

        https://www.youtube.com/watch?v=KFdHpOlz8hs
    """
    # Step 1: Allocate arrays for the maximum boundary index on each side.
    n: int = len(heights)
    left_max_height: list[int] = [-1] * n
    right_max_height: list[int] = [-1] * n
    body_of_water: int = 0

    # Step 2: Each endpoint initially serves as its own maximum boundary.
    left_max_height[0] = 0
    right_max_height[n - 1] = n - 1

    # Step 3: Store the tallest boundary index seen from the left through i.
    for i in range(1, n):
        if heights[left_max_height[i - 1]] > heights[i]:
            left_max_height[i] = left_max_height[i - 1]
        else:
            left_max_height[i] = i

    # Step 4: Store the tallest boundary index seen from the right through i.
    for i in range(n - 2, -1, -1):
        if heights[right_max_height[i + 1]] > heights[i]:
            right_max_height[i] = right_max_height[i + 1]
        else:
            right_max_height[i] = i

    # Steps 5 and 6: Calculate and accumulate water above every bar.
    for i in range(0, n):
        body_of_water += (
            min(heights[left_max_height[i]], heights[right_max_height[i]]) - heights[i]
        )

    # Step 6: Return the accumulated water across the entire elevation map.
    return body_of_water


def trapping_rain_water_two_pointers(heights: list[int]) -> int:
    """
    Approach: Two Pointers with Running Maximums
        1. Return 0 for an empty elevation map.
        2. Place left at the beginning and right at the end. Track max_left and
           max_right as the tallest bars encountered from their respective
           sides, and initialize the accumulated water to 0.
        3. Compare the two running maximums. The smaller maximum determines the
           side whose trapped water can be calculated safely:
              - If max_left is smaller, move left inward and process that bar.
              - Otherwise, move right inward and process that bar.
        4. At the selected position, the shorter running maximum limits the
           water level. Subtract the current bar's height from that level and
           add the result when it is positive.
        5. Update the selected side's running maximum after processing the
           current bar. If the current bar is a new maximum, it contributes no
           water and becomes the boundary for later positions.
        6. Continue until the pointers meet. Because a pointer moves before its
           position is processed, the meeting position is included. Return the
           accumulated water.

    Why the Smaller Maximum Is Safe:
        When max_left < max_right, a right boundary at least as tall as max_left
        is already known. The water at the next left position is therefore
        limited by max_left, regardless of any taller bars that may be found
        later on the right. The same reasoning applies symmetrically when
        max_right is less than or equal to max_left. This lets the algorithm
        finalize one position without precomputing maximum arrays.

    Time Complexity:
        O(n), where n is the number of bars. Every loop iteration moves exactly
        one pointer inward. left can move right at most n - 1 times and right
        can move left at most n - 1 times, and neither pointer reverses
        direction. The loop therefore performs at most n - 1 iterations, with
        O(1) comparisons, arithmetic, and assignments in each iteration.

    Space Complexity:
        O(1) additional space. The algorithm stores only left, right, max_left,
        max_right, and body_of_water. No list, dictionary, recursion, or other
        storage grows with the size of heights.

        https://www.youtube.com/watch?v=ZI2z5pq0TqA
    """
    # Step 1: An empty elevation map cannot trap water.
    if not heights:
        return 0

    # Step 2: Start at both boundaries and record their running maximum heights.
    left: int = 0
    right: int = len(heights) - 1
    max_left: int = heights[left]
    max_right: int = heights[right]
    body_of_water: int = 0

    # Step 6: Move inward until every relevant position has been processed.
    while left < right:
        # Step 3: The smaller left maximum is the known limiting boundary.
        if max_left < max_right:
            left += 1

            # Step 4: Calculate water at the newly reached left position.
            body_of_water += max(0, min(max_left, max_right) - heights[left])

            # Step 5: Include the current bar in the running left maximum.
            max_left = max(max_left, heights[left])

        # Step 3: The right maximum is the limiting boundary, including a tie.
        else:
            right -= 1

            # Step 4: Calculate water at the newly reached right position.
            body_of_water += max(0, min(max_left, max_right) - heights[right])

            # Step 5: Include the current bar in the running right maximum.
            max_right = max(max_right, heights[right])

    # Step 6: Return the total after the pointers have met.
    return body_of_water


def solve() -> None:
    heights: list[int] = [0, 2, 0, 3, 1, 0, 1, 3, 2, 1]
    expected: int = 9
    result: int = trapping_rain_water_brute_force(heights)
    result2: int = trapping_rain_water(heights)
    result3: int = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [5]
    expected = 0
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [1, 2, 3, 4]
    expected = 0
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [4, 3, 2, 1]
    expected = 0
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [2, 2, 2]
    expected = 0
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [2, 0, 2]
    expected = 2
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    # assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [3, 0, 1, 3]
    expected = 5
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [3, 1, 2, 1, 3]
    expected = 5
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")

    heights = [4, 2, 0, 3, 2, 5]
    expected = 9
    result = trapping_rain_water_brute_force(heights)
    result2 = trapping_rain_water(heights)
    result3 = trapping_rain_water_two_pointers(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")
    assert result2 == expected
    print(f"expected: {expected}")
    print(f"result2: {result2}")
    assert result3 == expected
    print(f"expected: {expected}")
    print(f"result3: {result3}")


if __name__ == "__main__":
    solve()
