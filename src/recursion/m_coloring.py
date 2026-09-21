"""M-Coloring Problem

Given an undirected graph and an integer m, determine whether all vertices
can be colored using at most m node_colors such that no two adjacent vertices
have the same color.

Return 1 if such a coloring is possible, and 0 otherwise.

Input representation for this template:
    - The number of vertices is n = len(graph), with labels 0 through n - 1.
    - m is the maximum number of node_colors available.
    - graph is an adjacency list of length n; graph[node] lists its neighbors.
    - Each undirected connection appears in both vertices' neighbor lists.
    - An isolated vertex has an empty neighbor list.

Example 1:
    Input:
        m = 3
        graph = [[1, 3, 2], [0, 2], [1, 3, 0], [2, 0]]
    Output: 1
    Explanation: The graph can be colored using three node_colors. For example,
        vertices 0, 1, 2, and 3 can receive node_colors 1, 2, 3, and 2,
        respectively. Every edge connects vertices with different node_colors.

https://www.youtube.com/watch?v=wuVwUK25Rfc&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9&index=18
"""


def m_coloring(m: int, graph: list[list[int]]) -> int:
    """Return 1 if the entire graph can use at most m colors, otherwise 0.

    Args:
        m: Number of available colors, represented by integers 1 through m.
        graph: Undirected adjacency list. Vertices are indexed 0 through
            len(graph) - 1, and graph[node] lists that vertex's neighbors.
            Neighbor indices must be valid and undirected connections must
            appear in both lists. Isolated vertices have empty neighbor lists.
            The input graph is not modified. Self-loops cannot be colored.

    Returns:
        Integer 1 if at least one valid coloring of all vertices exists,
        otherwise 0. The actual assignment is not returned. Disconnected
        components must all be colorable using the same available palette.

    Approach:
        Depth-First Search with Backtracking.
        1. Derive n from len(graph) and initialize node_colors with n zeros.
           Zero means uncolored; valid colors start at 1. Begin at vertex 0.
        2. If current_node == n, every vertex has a valid color. Return True.
           Vertices are processed in numerical order, including isolated
           vertices and vertices in disconnected components.
        3. Try each available color for the current vertex. Check its neighbor
           list: reject self-loops and any neighbor already using that color.
           Uncolored neighbors have value zero and do not conflict yet; they
           will check this vertex when their own colors are assigned later.
        4. Assign a safe color and recurse to current_node + 1. If the child
           succeeds, return True immediately: only one complete coloring is
           needed, rather than an enumeration of all valid assignments.
        5. If the child fails, reset this vertex to zero and try the next color.
           If every color fails, return False to let the parent reconsider its
           choice. One failed branch does not prove the graph is uncolorable;
           the full search must fail before concluding that no solution exists.
        6. Convert the initial recursive call's boolean result to integer 1 or 0.

        Backtracking example:
            With graph=[[2], [3], [0, 3], [2, 1]] and m=2, vertices 0 and 1
            initially both receive color 1. Vertex 2 then receives color 2.
            Vertex 3 sees neighbors of both colors and cannot be colored.
            Backtracking eventually changes vertex 1 to color 2, allowing
            vertex 2 to use color 2 and vertex 3 to use color 1. The first
            failed assignment therefore does not mean the graph is impossible.

    Examples:
        >>> m_coloring(3, [[1, 2], [0, 2], [0, 1]])
        1
        >>> m_coloring(2, [[1, 2], [0, 2], [0, 1]])
        0
        >>> m_coloring(1, [[], []])
        1
        >>> m_coloring(3, [[0]])
        0

    Time Complexity:
        For m >= 2, O(n * m**n) is a conservative worst-case bound for a
        simple graph, where n = len(graph). Each of n vertices has up to m
        color choices. The search tree has O(m**n) attempted assignments,
        and checking a candidate color scans up to n neighbors. Early success
        and rejected colors often reduce the actual search substantially.
        With m=1 there is no branching: time is O(n + E), where E is the
        number of undirected edges. Repeated neighbor entries, if supplied,
        add scanning work; the simple-graph bound assumes no repeated edges.

    Space Complexity:
        O(n) auxiliary space for node_colors and the recursion stack, which
        has at most n + 1 active coloring calls. The graph is shared by all
        calls, and no copies or collection of solutions are created. The
        integer return value requires constant space.
    """
    # Step 1: Derive the vertex count and mark every vertex uncolored.
    n: int = len(graph)
    node_colors: list[int] = [0] * n

    def is_safe(current_node: int, current_color: int) -> bool:
        # Step 3: Reject self-loops and conflicts with colored neighbors.
        for neighbor in graph[current_node]:
            if neighbor == current_node:
                return False
            if node_colors[neighbor] == current_color:
                return False
        return True

    def is_coloring_possible(current_node: int) -> bool:
        # Step 2: All vertices have been colored successfully.
        if current_node == n:
            return True
        # Step 3: Try each color for this vertex in numerical order.
        for color in range(1, m + 1):
            if is_safe(current_node=current_node, current_color=color):
                # Step 4: Choose a safe color and explore the next vertex.
                node_colors[current_node] = color
                if is_coloring_possible(current_node=current_node + 1):
                    return True
                # Step 5: Undo the failed choice before trying another color.
                node_colors[current_node] = 0

        # Step 5: All choices failed; let the parent reconsider its color.
        return False

    # Step 6: Return the requested integer success or failure indicator.
    return 1 if is_coloring_possible(0) else 0


def solve() -> None:
    # m: int = 3
    # graph = [[1, 3, 2], [0, 2], [1, 3, 0], [2, 0]]
    # expected: int = 1
    # result: int = m_coloring(m, graph)

    # assert result == expected
    # print(f"Expected: {expected}")
    # print(f"Result: {result}")

    # One isolated vertex needs one color.
    m = 1
    graph = [[]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several isolated vertices share one color.
    m = 1
    graph = [[], [], [], []]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge cannot use one color.
    m = 1
    graph = [[1], [0]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge can use two node_colors.
    m = 2
    graph = [[1], [0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Triangle requires more than two node_colors.
    m = 2
    graph = [[1, 2], [0, 2], [1, 0]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Triangle with exactly three node_colors.
    m = 3
    graph = [[1, 2], [0, 2], [1, 0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original graph with three node_colors.
    m = 3
    graph = [[1, 3, 2], [0, 2], [1, 3, 0], [2, 0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Original graph cannot use only two node_colors.
    m = 2
    graph = [[1, 3, 2], [0, 2], [1, 3, 0], [2, 0]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Even cycle uses two node_colors.
    m = 2
    graph = [[1, 3], [0, 2], [1, 3], [2, 0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd cycle cannot use two node_colors.
    m = 2
    graph = [[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Odd cycle with three node_colors.
    m = 3
    graph = [[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete four-vertex graph with insufficient node_colors.
    m = 3
    graph = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete four-vertex graph with exactly four node_colors.
    m = 4
    graph = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected edges share the same two node_colors.
    m = 2
    graph = [[1], [0], [3], [2], [5], [4]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # An isolated first vertex must not hide an uncolorable component.
    m = 2
    graph = [[], [2, 3], [1, 3], [2, 1]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the highest numbered vertices are connected.
    m = 1
    graph = [[], [], [], [4], [3]]
    expected = 0
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Highest numbered vertices with enough node_colors.
    m = 2
    graph = [[], [], [], [4], [3]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted neighbor lists still describe an undirected path.
    m = 2
    graph = [[1], [0, 2], [3, 1], [2]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star graph reuses a color across leaves.
    m = 2
    graph = [[1, 2, 3, 4, 5], [0], [0], [0], [0], [0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Available node_colors may exceed the number of vertices.
    m = 3
    graph = [[1], [0]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two-color path requires undoing an early choice in this vertex order.
    m = 2
    graph = [[2], [3], [0, 3], [2, 1]]
    expected = 1
    result = m_coloring(m, graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
