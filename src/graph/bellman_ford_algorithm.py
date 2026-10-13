"""118. Bellman Ford Algorithm

Given a weighted, directed graph with V vertices and E edges, each edge
[a, b, w] represents a directed edge from vertex a to vertex b with weight w.
Find the shortest distance from source vertex S to every vertex.

Return a list of V distances in vertex-index order. If a vertex cannot be
reached from S, use 10**9 for its distance. If the graph contains a negative
cycle, return [-1]. Here, E = len(edges).

Example 1:
    Input:
        V = 6
        edges = [[3, 2, 6], [5, 3, 1], [0, 1, 5], [1, 5, -3],
                 [1, 2, -2], [3, 4, -2], [2, 4, 3]]
        S = 0
    Output: [0, 5, 3, 3, 1, 2]
    Explanation:
        Node 0: source, distance 0.
        Node 1: 0 -> 1, distance 5.
        Node 2: 0 -> 1 -> 2, distance 3.
        Node 3: 0 -> 1 -> 5 -> 3, distance 3.
        Node 4: 0 -> 1 -> 5 -> 3 -> 4, distance 1.
        Node 5: 0 -> 1 -> 5, distance 2.

Example 2:
    Input: V = 2, edges = [[0, 1, 9]], S = 0
    Output: [0, 9]
    Explanation:
        The shortest path to node 1 is 0 -> 1, with distance 9.

Now Your Turn:
    Input: V = 3,
           edges = [[0, 1, 5], [1, 0, 3], [1, 2, -1], [2, 0, 1]],
           S = 2
    Pick the correct output:
        A. [1, 6, 0]
        B. [0, 6, 1]
        C. [1, 5, 0]
        D. [1, 1, 0]

Constraints:
    - 1 <= V <= 500.
    - 1 <= E <= V * (V - 1).
    - -1000 <= edges[i][2] <= 1000 (the edge weight).
    - 0 <= S < V.

Statement notes:
    - The supplied weight constraint says edges[i][3], but a three-element
      edge stores its weight at index 2.
    - The stated edge-count bounds cannot be satisfied when V = 1.
    - The statement does not specify whether a negative cycle disconnected
      from S should also trigger [-1].

https://www.youtube.com/watch?v=0vVofAhAYjc&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=41

"""


def bellman_ford_algorithm(
    vertices: int, edges: list[list[int]], source: int
) -> list[int]:
    """Return shortest source distances, or [-1] for a reachable negative cycle.

    Args:
        vertices: Number of vertices V, labeled 0 through V - 1, with
            1 <= V <= 500.
        edges: Directed edges [from_node, to_node, weight] with valid vertex
            indices and integer weights from -1000 to 1000. The stated
            bounds are 1 <= len(edges) <= V * (V - 1), which exclude V = 1.
        source: Starting vertex, with 0 <= source < V.

    Returns:
        A list indexed by vertex containing shortest distances from source.
        Unreachable vertices retain 10**9. Returns [-1] if a negative cycle
        is reachable from source. Disconnected negative cycles are ignored:
        this implementation uses the source-reachable interpretation of the
        statement. The input edge list is not modified.

    Approach:
        Bellman-Ford Algorithm with early termination and an extra
        relaxation pass to detect a reachable negative cycle.

        1. Initialize all distances to 10**9 except the source, whose
           distance is 0. Set iteration to 0 and updated to True so the
           first pass runs. Without a reachable negative cycle, a shortest
           simple path uses at most V - 1 edges, so its absolute weight is
           at most 499000. The sentinel safely exceeds valid distances.
        2. Enter the loop only while the preceding pass changed a distance.
           At the top, if iteration >= V, return [-1]. iteration counts
           completed passes: reaching this check after V passes means that
           the V-th pass still improved a distance, proving a reachable
           negative cycle. No (V + 1)-th edge scan is performed.
        3. Clear updated and scan all directed edges. Skip any edge whose
           starting vertex is still unreachable. This prevents adding a
           negative weight to the sentinel and inventing a reachable path.
        4. Relax each reachable edge: if the distance to from_node plus
           weight is smaller than the distance to to_node, replace the
           latter and set updated to True. Updates happen in place, so
           later edges in the same pass may use newly improved distances.
        5. Increment iteration after the complete scan. If nothing changed,
           the next loop condition is false and the search stops early.
           Otherwise, another pass may propagate improvements farther.
        6. Return distances when a pass makes no changes. Unreachable
           vertices remain at the sentinel, while reachable distances have
           settled. Positive and zero-total cycles do not keep improving
           distances because relaxation requires a strict decrease.

        Why V passes are enough:
            After V - 1 passes, all shortest simple paths have been covered,
            even if the edge order allows only one useful edge per pass.
            A V-th pass with an improvement therefore indicates that a
            reachable negative cycle allows distances to decrease further.
            A change on pass V - 1 alone is not evidence of a negative cycle;
            the extra pass distinguishes it from a long valid shortest path.

    Time Complexity:
        O(V * E) worst case, where E = len(edges). Initializing distances
        takes O(V), and at most V full passes examine E edges each, doing
        constant work per edge. More precisely, P completed passes cost
        O(V + P * E), with P <= V. Early termination can reduce P, giving
        O(V + E) when the first scan makes no changes.

    Space Complexity:
        O(V) extra space for the distances list. iteration, updated, and
        edge variables use O(1) space. Edges are read directly from the
        input; no adjacency list, queue, or copy of the graph is created.
    """
    # 1. Initialize source and unreachable distances and force the first pass.
    distances: list[int] = [10**9] * vertices
    distances[source] = 0
    iteration: int = 0
    updated: bool = True

    while updated:
        # 2. An improvement on the completed V-th pass proves a negative cycle.
        if iteration >= vertices:
            return [-1]
        # 3. Start a fresh pass and consider only edges reachable from source.
        updated = False
        for from_node, to_node, weight in edges:
            if distances[from_node] == 10**9:
                continue
            # 4. Relax the edge in place and record any strict improvement.
            if distances[from_node] + weight < distances[to_node]:
                distances[to_node] = distances[from_node] + weight
                updated = True
        # 5. Count the completed pass; no updates ends the loop early.
        iteration += 1

    # 6. Distances have settled; unreachable vertices still hold 10**9.
    return distances


def solve() -> None:
    vertices: int = 6
    edges: list[list[int]] = [
        [3, 2, 6],
        [5, 3, 1],
        [0, 1, 5],
        [1, 5, -3],
        [1, 2, -2],
        [3, 4, -2],
        [2, 4, 3],
    ]
    source: int = 0
    expected: list[int] = [0, 5, 3, 3, 1, 2]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example; smallest feasible graph under edge bounds.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 9]]
    source: int = 0
    expected: list[int] = [0, 9]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example with a nonzero source.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 5], [1, 0, 3], [1, 2, -1], [2, 0, 1]]
    source: int = 2
    expected: list[int] = [1, 6, 0]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum edge weight.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, -1000]]
    source: int = 0
    expected: list[int] = [0, -1000]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge weight.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 1000]]
    source: int = 0
    expected: list[int] = [0, 1000]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-weight edge.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 0]]
    source: int = 0
    expected: list[int] = [0, 0]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A directed edge cannot be traversed backwards.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 7]]
    source: int = 1
    expected: list[int] = [10**9, 0]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unreachable negative edge must not relax the sentinel.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 3], [2, 3, -1000]]
    source: int = 0
    expected: list[int] = [0, 3, 10**9, 10**9]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated interior source.
    vertices: int = 4
    edges: list[list[int]] = [[0, 3, -4]]
    source: int = 2
    expected: list[int] = [10**9, 10**9, 0, 10**9]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Highest-index source reaches city zero.
    vertices: int = 3
    edges: list[list[int]] = [[2, 1, -2], [1, 0, 5]]
    source: int = 2
    expected: list[int] = [3, -2, 0]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reverse-ordered chain requires all V - 1 relaxation passes.
    vertices: int = 4
    edges: list[list[int]] = [[2, 3, 2], [1, 2, -3], [0, 1, 5]]
    source: int = 0
    expected: list[int] = [0, 5, 2, 4]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheaper indirect route replaces the direct route.
    vertices: int = 3
    edges: list[list[int]] = [[0, 2, 10], [0, 1, 5], [1, 2, -4]]
    source: int = 0
    expected: list[int] = [0, 5, 1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal-cost alternatives do not change distances.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 2], [0, 2, 2], [1, 3, 3], [2, 3, 3]]
    source: int = 0
    expected: list[int] = [0, 2, 2, 5]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive cycle is allowed.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 3], [2, 0, 4]]
    source: int = 0
    expected: list[int] = [0, 2, 5]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-total cycle with negative and positive edges is allowed.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 2], [1, 2, -3], [2, 0, 1]]
    source: int = 0
    expected: list[int] = [0, 2, -1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All-zero cycle terminates without reporting a negative cycle.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 0], [1, 2, 0], [2, 0, 0]]
    source: int = 0
    expected: list[int] = [0, 0, 0]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable two-vertex negative cycle.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, -1], [1, 0, 0]]
    source: int = 0
    expected: list[int] = [-1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable negative cycle excludes the source and affects downstream nodes.
    vertices: int = 5
    edges: list[list[int]] = [[0, 1, 2], [1, 2, -4], [2, 1, 1], [2, 3, 2], [3, 4, 1]]
    source: int = 0
    expected: list[int] = [-1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Negative cycle reached only after a reverse-ordered chain.
    vertices: int = 5
    edges: list[list[int]] = [[4, 3, -2], [3, 4, 1], [2, 3, 1], [1, 2, 1], [0, 1, 1]]
    source: int = 0
    expected: list[int] = [-1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable negative cycle from the highest-index source.
    vertices: int = 3
    edges: list[list[int]] = [[2, 1, 1], [1, 0, -2], [0, 1, 1]]
    source: int = 2
    expected: list[int] = [-1]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with minimum edge count.
    vertices: int = 500
    edges: list[list[int]] = [[0, 499, 1000]]
    source: int = 0
    expected: list[int] = [0] + [10**9] * 498 + [1000]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum reverse-ordered positive chain; distances exceed edge bounds.
    vertices: int = 500
    edges: list[list[int]] = [[i, i + 1, 1000] for i in range(498, -1, -1)]
    source: int = 0
    expected: list[int] = [i * 1000 for i in range(500)]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum reverse-ordered negative chain without cycles.
    vertices: int = 500
    edges: list[list[int]] = [[i, i + 1, -1000] for i in range(498, -1, -1)]
    source: int = 0
    expected: list[int] = [-i * 1000 for i in range(500)]
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum source index and reverse direction chain.
    vertices: int = 500
    edges: list[list[int]] = [[i, i - 1, 1] for i in range(1, 500)]
    source: int = 499
    expected: list[int] = list(range(499, -1, -1))
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge count: every ordered pair with weight 1000.
    vertices: int = 500
    edges: list[list[int]] = [
        [u, v, 1000] for u in range(500) for v in range(500) if u != v
    ]
    source: int = 0
    expected: list[int] = [0] + [1000] * 499
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum edge count with all-zero weights.
    vertices: int = 500
    edges: list[list[int]] = [
        [u, v, 0] for u in range(500) for v in range(500) if u != v
    ]
    source: int = 499
    expected: list[int] = [0] * 500
    result: list[int] = bellman_ford_algorithm(vertices, edges, source)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
