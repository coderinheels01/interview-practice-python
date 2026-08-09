"""
Container With Most Water

Difficulty: Medium
Topics: Two Pointers
Company Tags
Hints

You are given an integer array heights where heights[i] represents the height
of the ith bar.

You may choose any two bars to form a container. Return the maximum amount of
water a container can store.

Example 1:
    Input:
        heights = [1, 7, 2, 5, 4, 7, 3, 6]

    Output:
        36

Example 2:
    Input:
        heights = [2, 2, 2]

    Output:
        4

Constraints:
    - 2 <= len(heights) <= 100,000
    - 0 <= heights[i] <= 10,000
"""


def container_with_most_water(heights: list[int]) -> int:
    """
    Approach: Two Pointers
        1. Place left at the first bar and right at the last bar. This starts
           with the widest possible container.
        2. Calculate the container's width as right - left. Its usable height is
           the shorter of the two bars because water would spill over that bar.
        3. Multiply the width by the usable height to get the current area, then
           update max_water if this container holds more water than any
           previously examined container.
        4. Move the pointer at the shorter bar inward. Moving the taller bar
           cannot improve the area: the width becomes smaller while the shorter
           bar still limits the height. Replacing the shorter bar is the only
           movement that might find a taller limiting bar and offset the lost
           width.
        5. When both bars have the same height, either pointer may move because
           both limit the current container equally. This implementation moves
           right inward.
        6. Repeat until the pointers meet, then return the greatest area found.

    Why Moving the Shorter Bar Is Safe:
        Suppose heights[left] is shorter than heights[right]. Every container
        that keeps left and moves right inward has a smaller width, while its
        height can never exceed heights[left], the existing limiting height.
        None of those containers can beat the current one. Therefore, left can
        be discarded safely. The same reasoning applies symmetrically when the
        right bar is shorter.

    Time Complexity:
        O(n), where n is the number of bars. Each loop iteration moves exactly
        one pointer inward. left can move right at most n - 1 times and right
        can move left at most n - 1 times. Neither pointer moves backward, so
        the loop performs at most n - 1 iterations. Calculating the width,
        minimum height, area, maximum, and pointer update takes O(1) time per
        iteration, giving O(n) total time.

    Space Complexity:
        O(1) additional space. The algorithm stores only n, left, right,
        max_water, width, and height. The number of variables does not grow with
        the length of heights, and the algorithm does not copy the input or use
        any additional collection.
    """
    # Step 1: Start at both ends to examine the widest possible container.
    n: int = len(heights)
    left: int = 0
    right: int = n - 1
    max_water: int = 0

    # Step 6: Continue until no pair of distinct bars remains.
    while left < right:
        # Step 2: The distance is the width, and the shorter bar limits height.
        width = right - left
        height = min(heights[left], heights[right])

        # Step 3: Keep the greatest container area examined so far.
        max_water = max(max_water, width * height)

        # Step 4: Discard the shorter left bar to seek a taller limiting bar.
        if heights[left] < heights[right]:
            left += 1

        # Steps 4 and 5: Discard the shorter right bar, or either bar when tied.
        else:
            right -= 1

    # Step 6: Return the maximum area after every useful width was considered.
    return max_water


def solve() -> None:
    heights: list[int] = [1, 7, 2, 5, 4, 7, 3, 6]
    expected: int = 36
    result: int = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [2, 2, 2]
    expected = 4
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [1, 1]
    expected = 1
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [0, 0]
    expected = 0
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [0, 5, 0, 5, 0]
    expected = 10
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [1, 2, 3, 4, 5]
    expected = 6
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [5, 4, 3, 2, 1]
    expected = 6
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [1, 100, 100, 1]
    expected = 100
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    heights = [10, 1, 1, 1, 10]
    expected = 40
    result = container_with_most_water(heights)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")


if __name__ == "__main__":
    solve()
