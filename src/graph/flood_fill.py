"""179. Flood Fill Algorithm

An image is represented by a two-dimensional array of integers, where each
integer is a pixel's color. Given a starting pixel (sr, sc) and new_color,
perform a flood fill and return the resulting image.

Replace the starting pixel's color and the color of every pixel reachable
from it by moving through pixels of the same original color. Movement is
four-directional: up, down, left, or right. Diagonal contact does not count.
Pixels outside this connected region keep their original colors.

Example 1:
    Input: image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]],
           sr = 1, sc = 1, new_color = 2
    Output: [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    Explanation: All 1s connected four-directionally to the center become 2.
    The bottom-right 1 stays unchanged because it is disconnected from them.

Example 2:
    Input: image = [[0, 1, 0], [1, 1, 0], [0, 0, 1]],
           sr = 2, sc = 2, new_color = 3
    Output: [[0, 1, 0], [1, 1, 0], [0, 0, 3]]
    Explanation: Only the starting pixel belongs to its connected region.
    The other 1s are not connected to it through four-directional moves.

Practice example:
    Input: image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]],
           sr = 1, sc = 1, new_color = 0
    Choose the correct output:
        A. [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        B. [[0, 0, 0], [0, 0, 0], [1, 0, 1]]
        C. [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
        D. [[0, 0, 0], [0, 0, 0], [0, 0, 1]]

Constraints:
    - n == len(image), m == len(image[i]).
    - 1 <= m, n <= 50.
    - 0 <= image[i][j], new_color < 2**16.
      The pasted upper bound "216" is interpreted as 2 to the power of 16.
    - 0 <= sr < n.
    - 0 <= sc < m.

    https://www.youtube.com/watch?v=C-2_uSRli8o&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=9
"""


def flood_fill(
    image: list[list[int]], sr: int, sc: int, new_color: int
) -> list[list[int]]:

    """Recolor the starting pixel's four-directionally connected region.

    Args:
        image: A nonempty rectangular matrix of pixel colors, with at most
            50 rows and 50 columns. Zero is a color, not a blocked cell.
        sr: Valid starting row index.
        sc: Valid starting column index.
        new_color: The replacement color.

    Returns:
        The same image object, modified in place. Only pixels connected to
        (sr, sc) through its original color are recolored. Diagonal contact
        does not connect pixels. The function assumes valid problem inputs.

    Approach:
        Iterative Depth-First Search (DFS) using an explicit stack.
        1. Read the image dimensions, define the four movement offsets, and
           save the starting pixel's original color in start_pixel.
        2. If start_pixel equals new_color, return immediately. No work is
           needed, and unchanged colors could not serve as visited markers.
        3. Push the starting coordinates onto a list used as a stack.
        4. While the stack is nonempty, pop the most recently added coordinates
           and recolor that pixel. Recoloring replaces a separate visited
           array: the pixel no longer matches start_pixel.
        5. Check all four neighbors. Push a neighbor only if its coordinates
           are inside the image and its color still equals start_pixel.
           Repeating steps 4 and 5 follows both direct and indirect connections
           without creating recursive function calls.
        6. Return the modified image after the stack becomes empty.

        Example:
            image = [[7, 7], [7, 1]], sr = 0, sc = 0, new_color = 8.
            - Pop (0, 0), recolor it, and push (0, 1) and (1, 0).
            - Pop (1, 0) and recolor it. Its neighbor (0, 0) is now 8,
              so it no longer matches the original color 7.
            - Pop (0, 1) and recolor it. The pixel containing 1 is excluded.
            - Return [[8, 8], [8, 1]].

        Implementation detail:
            Why use an explicit stack instead of recursion?
            Recursive DFS is logically valid, but Python limits the depth of
            nested function calls (usually around 1,000 by default). An allowed
            50 x 50 image contains 2,500 pixels, and DFS through a large region
            can create a chain of calls deeper than that limit, causing
            RecursionError. The recursive version failed large-image tests
            for this reason. Iterative DFS stores pending coordinates in a
            regular list, which is not subject to the recursion-depth limit.
            It still uses memory, but avoids accumulating nested function
            calls. This changes how DFS is executed, not its Big-O complexity.

            This version recolors on pop, not on push. A pixel waiting in
            the stack can therefore be pushed again from another neighbor.
            Such duplicate entries may later be popped and scanned again;
            the implementation does not guarantee one stack entry per pixel.
            Recoloring prevents newly pushing pixels already processed.

    Time Complexity:
        O(rows * cols) in the worst case, where rows and cols are the image
        dimensions. The connected region can contain every pixel. Each pixel
        has only four neighbors, and the depth-first traversal does bounded
        work per pixel/neighbor connection, including pending duplicate stack
        entries. It does not scan the entire image for each popped pixel.
        The unchanged-color early return takes O(1) time.

    Space Complexity:
        O(rows * cols) auxiliary space in the worst case for the coordinate
        stack, including pending duplicate entries. The four directions and
        scalar variables use O(1) space. There is no separate visited matrix
        or recursion stack. The image is modified directly rather than copied,
        so returning it does not allocate a second output matrix. When the
        colors already match, auxiliary space is O(1).
    """
    # 1. Record dimensions, movement directions, and the original color.
    row_size: int = len(image)
    col_size: int = len(image[0])
    directions: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    start_pixel: int = image[sr][sc]

    # 2. Stop if recoloring would leave the image unchanged.
    if start_pixel == new_color:
        return image

    # 3. Start DFS with the starting pixel coordinates.
    stack: list[int] = [(sr, sc)]

    while stack:
        # 4. Process the latest pending pixel; its new color marks it visited.
        row, col = stack.pop()
        image[row][col] = new_color

        # 5. Push valid neighbors that still have the original color.
        for row_diff, col_diff in directions:
            new_row = row + row_diff
            new_col = col + col_diff
            if (
                0 <= new_row < row_size
                and 0 <= new_col < col_size
                and image[new_row][new_col] == start_pixel
            ):
                stack.append((new_row, new_col))

    # 6. Return the same image after filling the connected region.
    return image


def solve() -> None:
    image: list[list[int]] = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    sr: int = 1
    sc: int = 1
    new_color: int = 2
    expected: list[list[int]] = [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1],
    ]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Example 2: isolated bottom-right pixel.
    image: list[list[int]] = [[0, 1, 0], [1, 1, 0], [0, 0, 1]]
    sr: int = 2
    sc: int = 2
    new_color: int = 3
    expected: list[list[int]] = [[0, 1, 0], [1, 1, 0], [0, 0, 3]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: recolor to zero.
    image: list[list[int]] = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    sr: int = 1
    sc: int = 1
    new_color: int = 0
    expected: list[list[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum image and minimum original color.
    image: list[list[int]] = [[0]]
    sr: int = 0
    sc: int = 0
    new_color: int = 65535
    expected: list[list[int]] = [[65535]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum original color and minimum new color.
    image: list[list[int]] = [[65535]]
    sr: int = 0
    sc: int = 0
    new_color: int = 0
    expected: list[list[int]] = [[0]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single pixel with unchanged color.
    image: list[list[int]] = [[7]]
    sr: int = 0
    sc: int = 0
    new_color: int = 7
    expected: list[list[int]] = [[7]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Connected region with unchanged color.
    image: list[list[int]] = [[1, 1], [1, 1]]
    sr: int = 0
    sc: int = 0
    new_color: int = 1
    expected: list[list[int]] = [[1, 1], [1, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-colored region beside ones.
    image: list[list[int]] = [[0, 0], [1, 0]]
    sr: int = 0
    sc: int = 0
    new_color: int = 4
    expected: list[list[int]] = [[4, 4], [1, 4]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original color other than one.
    image: list[list[int]] = [[7, 7], [7, 1]]
    sr: int = 0
    sc: int = 0
    new_color: int = 8
    expected: list[list[int]] = [[8, 8], [8, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diagonal-only matches are disconnected.
    image: list[list[int]] = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    sr: int = 1
    sc: int = 1
    new_color: int = 9
    expected: list[list[int]] = [[1, 0, 1], [0, 9, 0], [1, 0, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Existing new color must not bridge disconnected regions.
    image: list[list[int]] = [[1, 2, 1], [1, 2, 1], [1, 2, 1]]
    sr: int = 0
    sc: int = 0
    new_color: int = 2
    expected: list[list[int]] = [[2, 2, 1], [2, 2, 1], [2, 2, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Wide rectangular image, starting at top-right.
    image: list[list[int]] = [[1, 1, 1], [0, 1, 0]]
    sr: int = 0
    sc: int = 2
    new_color: int = 3
    expected: list[list[int]] = [[3, 3, 3], [0, 3, 0]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tall rectangular image, starting at bottom-left.
    image: list[list[int]] = [[1, 0], [1, 1], [1, 0]]
    sr: int = 2
    sc: int = 0
    new_color: int = 3
    expected: list[list[int]] = [[3, 0], [3, 3], [3, 0]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One row, starting in the middle of a region.
    image: list[list[int]] = [[1, 1, 1, 0, 1]]
    sr: int = 0
    sc: int = 1
    new_color: int = 2
    expected: list[list[int]] = [[2, 2, 2, 0, 1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One column, starting in the middle of a region.
    image: list[list[int]] = [[1], [1], [1], [0], [1]]
    sr: int = 1
    sc: int = 0
    new_color: int = 2
    expected: list[list[int]] = [[2], [2], [2], [0], [1]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Region surrounding a barrier.
    image: list[list[int]] = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    sr: int = 2
    sc: int = 2
    new_color: int = 5
    expected: list[list[int]] = [[5, 5, 5], [5, 0, 5], [5, 5, 5]]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum width with minimum height.
    image: list[list[int]] = [[1] * 50]
    sr: int = 0
    sc: int = 49
    new_color: int = 2
    expected: list[list[int]] = [[2] * 50]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum height with minimum width.
    image: list[list[int]] = [[1] for _ in range(50)]
    sr: int = 49
    sc: int = 0
    new_color: int = 2
    expected: list[list[int]] = [[2] for _ in range(50)]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum image: every pixel belongs to the region.
    image: list[list[int]] = [[1] * 50 for _ in range(50)]
    sr: int = 0
    sc: int = 0
    new_color: int = 2
    expected: list[list[int]] = [[2] * 50 for _ in range(50)]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum image with unchanged color.
    image: list[list[int]] = [[1] * 50 for _ in range(50)]
    sr: int = 49
    sc: int = 49
    new_color: int = 1
    expected: list[list[int]] = [[1] * 50 for _ in range(50)]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum image: isolated maximum-color starting pixel.
    image: list[list[int]] = [
        [65535 if (r, c) == (49, 49) else 0 for c in range(50)] for r in range(50)
    ]
    sr: int = 49
    sc: int = 49
    new_color: int = 0
    expected: list[list[int]] = [[0] * 50 for _ in range(50)]
    result: list[list[int]] = flood_fill(image, sr, sc, new_color)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
