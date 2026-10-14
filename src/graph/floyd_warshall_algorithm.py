"""127. Floyd Warshall Algorithm

Given a weighted, directed graph with n vertices numbered from 0 to n - 1,
find the shortest distances between every pair of vertices.

The graph is represented by an n x n adjacency matrix. matrix[i][j] gives
the weight of the edge from i to j. A value of -1 means there is no edge
from i to j.

Return the shortest-distance matrix, where entry [i][j] gives the shortest
distance from vertex i to vertex j. Use -1 for unreachable pairs.

Example 1:
    Input:
        matrix = [[0, 2, -1, -1],
                  [1, 0, 3, -1],
                  [-1, -1, 0, 1],
                  [3, 5, 4, 0]]
    Output:
        [[0, 2, 5, 6],
         [1, 0, 3, 4],
         [4, 6, 0, 1],
         [3, 5, 4, 0]]
    Explanation:
        Entry [0][0] stores the distance from vertex 0 to itself, which
        is 0. Entry [0][1] stores the distance from vertex 0 to vertex 1,
        which is 2, and so on.

Example 2:
    Input: matrix = [[0, 25], [-1, 0]]
    Output: [[0, 25], [-1, 0]]
    Explanation:
        The matrix already contains the shortest distances.

Now Your Turn:
    Input: matrix = [[0, 1, 43], [1, 0, 6], [-1, -1, 0]]
    Pick the correct output:
        A. [[0, 1, 43], [1, 0, 6], [-1, -1, 0]]
        B. [[0, 1, 43], [1, 0, 6], [13, -1, 0]]
        C. [[0, 1, 7], [1, 0, 6], [-1, -1, 0]]
        D. [[0, 1, 13], [1, 0, 6], [-1, -1, 0]]

Constraints:
    - 1 <= n <= 100.
    - The matrix has n rows and n columns.
    - -1 <= matrix[i][j] <= 1000.
    - -1 denotes a missing edge, not a negative edge weight.

Discussion Questions:
    - Why use Floyd-Warshall instead of Dijkstra's Algorithm?
    - How does Floyd-Warshall compare to Bellman-Ford?
    - How could you reconstruct the shortest paths, not just distances?
    - What if the graph were very large (V > 10**4)? How would Johnson's
      Algorithm, which combines Bellman-Ford and Dijkstra, compare?

https://www.youtube.com/watch?v=sLg6Leb-xt0
https://www.youtube.com/watch?v=YbY8cVwWAvw&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=42
"""


def floyd_warshall_algorithm(matrix: list[list[int]]) -> list[list[int]]:
    """Compute all-pairs shortest distances in place and return the same matrix.

    Args:
        matrix: A square n x n directed adjacency matrix, with 1 <= n <= 100.
            Entries are -1 for missing edges or weights from 0 to 1000.
            Zero-weight edges are valid; -1 is not a negative edge weight.

    Returns:
        The input matrix, modified so entry [i][j] is the shortest distance
        from i to j, or -1 if j is unreachable from i. Diagonal entries are
        always 0 because the empty path costs nothing. This includes a
        single-vertex graph, even if its original diagonal is -1 or positive.
        Callers needing the original weights must copy each row beforehand.

    Approach:
        Floyd-Warshall Algorithm, using dynamic programming over the set
        of permitted intermediate vertices.

        1. Replace missing edges with 10**9 and set every diagonal entry
           to 0. The sentinel is larger than any finite shortest distance:
           a simple path has at most 99 edges, each of weight at most 1000.
        2. Consider each vertex as via_index in the outermost loop. After
           this iteration, distances permit intermediate vertices from 0
           through via_index. Keeping this loop outermost ensures the
           subpaths needed for each update have already been considered.
        3. For each starting row, skip its column loop if it cannot reach
           via_index: no route from that start through this vertex exists.
        4. For every destination column, compare the current distance with
           matrix[row][via] + matrix[via][col] and retain the smaller value.
           A shortest route either avoids the newly permitted intermediate
           vertex or splits there into two previously considered subpaths.
           In-place updates are safe here because weights are nonnegative
           and the zero diagonal prevents changes to the via row or column
           during this phase.
        5. Convert any remaining 10**9 entries back to -1. These pairs never
           acquired a finite route. Return the same, now updated matrix.

        If via_index cannot reach a destination, the second term of the
        sum is 10**9. Since all finite distances are nonnegative, that sum
        cannot improve any stored entry. This is why only the first leg
        needs an explicit unreachable check under these constraints.

        Example: if 0 -> 1 costs 1, 1 -> 2 costs 6, and 0 -> 2 costs 43,
        considering vertex 1 changes distance[0][2] to min(43, 1 + 6) = 7.

    Time Complexity:
        O(n**3) worst case. Initialization and final conversion each take
        O(n**2). The main loops consider n intermediate vertices, n starting
        vertices, and up to n destinations, doing constant work per update.
        Skipping unreachable first legs can reduce the work on sparse graphs
        but does not change the worst-case bound.

    Space Complexity:
        O(1) extra space. All distances overwrite the provided matrix; only
        the size and loop indices are stored separately. The input/output
        matrix occupies O(n**2) space, but no additional matrix is allocated.
    """
    size: int = len(matrix)

    # 1. Convert absent edges to a sentinel and initialize empty-path distances.
    for row_index in range(size):
        for col_index in range(size):
            if matrix[row_index][col_index] == -1:
                matrix[row_index][col_index] = 10**9
            if row_index == col_index:
                matrix[row_index][col_index] = 0

    # 2. Expand the allowed intermediate vertices one at a time.
    for via_index in range(size):
        for row_index in range(size):
            # 3. No route through via_index exists if its first leg is missing.
            if matrix[row_index][via_index] == 10**9:
                continue
            # 4. Compare the current distance with a route through via_index.
            for col_index in range(size):
                matrix[row_index][col_index] = min(
                    matrix[row_index][col_index],
                    matrix[row_index][via_index] + matrix[via_index][col_index],
                )

    # 5. Restore the required unreachable marker and return the modified input.
    for row_index in range(size):
        for col_index in range(size):
            if matrix[row_index][col_index] == 10**9:
                matrix[row_index][col_index] = -1

    return matrix


def solve() -> None:
    matrix: list[list[int]] = [
        [0, 2, -1, -1],
        [1, 0, 3, -1],
        [-1, -1, 0, 1],
        [3, 5, 4, 0],
    ]
    expected: list[list[int]] = [
        [0, 2, 5, 6],
        [1, 0, 3, 4],
        [4, 6, 0, 1],
        [3, 5, 4, 0],
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single vertex with zero diagonal.
    matrix: list[list[int]] = [[0]]
    expected: list[list[int]] = [[0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Missing self-edge still has zero distance to itself.
    matrix: list[list[int]] = [[-1]]
    expected: list[list[int]] = [[0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive self-edge does not beat the empty path.
    matrix: list[list[int]] = [[1000]]
    expected: list[list[int]] = [[0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example preserves an unreachable direction.
    matrix: list[list[int]] = [[0, 25], [-1, 0]]
    expected: list[list[int]] = [[0, 25], [-1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example improves a direct edge.
    matrix: list[list[int]] = [[0, 1, 43], [1, 0, 6], [-1, -1, 0]]
    expected: list[list[int]] = [[0, 1, 7], [1, 0, 6], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two isolated vertices.
    matrix: list[list[int]] = [[0, -1], [-1, 0]]
    expected: list[list[int]] = [[0, -1], [-1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different weights in opposite directions.
    matrix: list[list[int]] = [[0, 2], [7, 0]]
    expected: list[list[int]] = [[0, 2], [7, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A zero-weight edge is traversable.
    matrix: list[list[int]] = [[0, 0, -1], [-1, 0, 5], [-1, -1, 0]]
    expected: list[list[int]] = [[0, 0, 5], [-1, 0, 5], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-weight cycle connects all vertices.
    matrix: list[list[int]] = [[0, 0, -1], [-1, 0, 0], [0, -1, 0]]
    expected: list[list[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All entries are missing edges, including the diagonal.
    matrix: list[list[int]] = [[-1] * 3 for _ in range(3)]
    expected: list[list[int]] = [
        [0 if i == j else -1 for j in range(3)] for i in range(3)
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First vertex is the necessary intermediate.
    matrix: list[list[int]] = [[0, -1, 3], [2, 0, -1], [-1, -1, 0]]
    expected: list[list[int]] = [[0, -1, 3], [2, 0, 5], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Last vertex is the necessary intermediate.
    matrix: list[list[int]] = [[0, -1, 2], [-1, 0, -1], [-1, 3, 0]]
    expected: list[list[int]] = [[0, 5, 2], [-1, 0, -1], [-1, 3, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several intermediate vertices in non-index order.
    matrix: list[list[int]] = [
        [0, -1, -1, 1],
        [-1, 0, 1, -1],
        [-1, -1, 0, -1],
        [-1, 1, -1, 0],
    ]
    expected: list[list[int]] = [
        [0, 2, 3, 1],
        [-1, 0, 1, -1],
        [-1, -1, 0, -1],
        [-1, 1, 2, 0],
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct route beats a longer indirect route.
    matrix: list[list[int]] = [[0, 4, 2], [-1, 0, 5], [-1, -1, 0]]
    expected: list[list[int]] = [[0, 4, 2], [-1, 0, 5], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal-cost routes preserve the same distance.
    matrix: list[list[int]] = [[0, 2, 5], [-1, 0, 3], [-1, -1, 0]]
    expected: list[list[int]] = [[0, 2, 5], [-1, 0, 3], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive directed cycle creates reverse-direction paths.
    matrix: list[list[int]] = [[0, 2, -1], [-1, 0, 3], [4, -1, 0]]
    expected: list[list[int]] = [[0, 2, 5], [7, 0, 3], [4, 6, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two disconnected components.
    matrix: list[list[int]] = [
        [0, 1, -1, -1],
        [1, 0, -1, -1],
        [-1, -1, 0, 2],
        [-1, -1, 2, 0],
    ]
    expected: list[list[int]] = [
        [0, 1, -1, -1],
        [1, 0, -1, -1],
        [-1, -1, 0, 2],
        [-1, -1, 2, 0],
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Path distance can exceed the maximum individual edge weight.
    matrix: list[list[int]] = [[0, 1000, -1], [-1, 0, 1000], [-1, -1, 0]]
    expected: list[list[int]] = [[0, 1000, 2000], [-1, 0, 1000], [-1, -1, 0]]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size with no connections.
    matrix: list[list[int]] = [
        [0 if i == j else -1 for j in range(100)] for i in range(100)
    ]
    expected: list[list[int]] = [
        [0 if i == j else -1 for j in range(100)] for i in range(100)
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size with all-zero weights.
    matrix: list[list[int]] = [[0] * 100 for _ in range(100)]
    expected: list[list[int]] = [[0] * 100 for _ in range(100)]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size complete graph with maximum edge weights.
    matrix: list[list[int]] = [
        [0 if i == j else 1000 for j in range(100)] for i in range(100)
    ]
    expected: list[list[int]] = [
        [0 if i == j else 1000 for j in range(100)] for i in range(100)
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum forward chain gives a 99000 distance.
    matrix: list[list[int]] = [
        [0 if i == j else 1000 if j == i + 1 else -1 for j in range(100)]
        for i in range(100)
    ]
    expected: list[list[int]] = [
        [(j - i) * 1000 if j >= i else -1 for j in range(100)] for i in range(100)
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum reverse chain checks the opposite direction.
    matrix: list[list[int]] = [
        [0 if i == j else 1 if j == i - 1 else -1 for j in range(100)]
        for i in range(100)
    ]
    expected: list[list[int]] = [
        [i - j if i >= j else -1 for j in range(100)] for i in range(100)
    ]
    result: list[list[int]] = floyd_warshall_algorithm(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
