"""Prim's Algorithm: Minimum Spanning Tree

Practice problem:
Given a connected, weighted, undirected graph with vertices labeled from
0 to vertices - 1, find a minimum spanning tree and its total weight using
Prim's Algorithm.

Each entry [u, v, weight] in edges represents a bidirectional edge between
vertices u and v with the given weight.

A spanning tree connects every vertex without cycles and contains exactly
vertices - 1 edges. A minimum spanning tree has the smallest total edge
weight among all spanning trees of the graph.

Return (min_spanning_tree, min_weight), where min_spanning_tree contains
(from_node, to_node, weight) tuples for the selected edges. Multiple minimum
spanning trees may exist, but their total weights are equal. For a single
vertex with no edges, return ([], 0).

Example 1:
    Input:
        vertices = 3
        edges = [[0, 1, 5], [1, 2, 3], [0, 2, 1]]
    Output: ([(0, 2, 1), (2, 1, 3)], 4)
    Explanation:
        Choose edges 0 -- 2 (weight 1) and 2 -- 1 (weight 3).
        They connect all three vertices without a cycle.
        Their total weight is 1 + 3 = 4, the minimum possible.

Practice constraints (chosen for this exercise):
    - 1 <= vertices <= 1000.
    - vertices - 1 <= len(edges) <= vertices * (vertices - 1) / 2.
    - Each edge contains exactly three integers [u, v, weight].
    - 0 <= u, v < vertices and u != v.
    - 1 <= weight <= 10**4.
    - The graph is connected.
    - There is at most one edge between any pair of vertices.

Discussion Questions:
    - How does a minimum spanning tree differ from a shortest-path tree?
    - What changes if the graph is disconnected?
    - How does Prim's Algorithm compare to Kruskal's Algorithm?

https://www.youtube.com/watch?v=mJcZjjKzeqk&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=45

https://www.youtube.com/watch?v=f7JOBJIC-NA


"""

import heapq


def prims_algorithm(
    vertices: int, edges: list[list[int]]
) -> tuple[list[tuple[int, int, int]], int]:
    """Return a minimum spanning tree and its total weight.

    Args:
        vertices: Number V of vertices labeled 0 through V - 1, with
            1 <= V <= 1000.
        edges: Undirected edges [u, v, weight] with distinct valid endpoints,
            weights from 1 to 10**4, and at most one edge per vertex pair.
            The graph must be connected. The input is not modified.

    Returns:
        (min_spanning_tree, min_weight), where the tree contains selected
        (from_node, to_node, weight) tuples in acceptance order. The total
        weight is the sum of these V - 1 edges. A single vertex returns
        ([], 0). Equal weights may allow multiple valid minimum trees.
        Connectivity is assumed rather than validated: on disconnected
        input, this implementation only spans the component containing 0.

    Approach:
        Prim's Algorithm with a min heap of candidate connecting edges.

        1. Allocate an adjacency list and visited flags. Initialize an empty
           tree and total weight 0. Seed the heap with (0, 0, -1), a dummy
           entry that starts the tree at vertex 0 without selecting an edge.
        2. Store every input edge in both directions. Adjacency entries are
           (weight, neighbor); heap entries are (weight, to_node, from_node).
        3. Pop the smallest-weight candidate. If its destination is already
           visited, skip it: that vertex has already joined the tree and
           accepting this edge would create a cycle.
        4. Mark the new vertex visited. For a real edge (from_node != -1),
           append (from_node, to_node, weight) to the tree and add its weight
           to the total. Stop after accepting V - 1 edges, but only after
           adding the final edge's weight. The dummy entry contributes no
           edge or weight.
        5. Push edges from the accepted vertex to unvisited neighbors.
           Do not mark neighbors visited when pushing: another vertex may
           later offer a cheaper connecting edge. Multiple candidates for
           the same destination can coexist until one is accepted.
        6. Return the selected edges and their total weight. For V = 1,
           processing the dummy entry leaves the heap empty and returns
           the empty tree with weight 0.

        Why the greedy choice works:
            Visited vertices form the growing tree. Every queued edge was
            offered by a visited vertex; after discarding entries whose
            destinations are visited, the smallest remaining edge connects
            the tree to an outside vertex. The minimum-edge cut property
            guarantees that this edge can extend a minimum spanning tree.

            Heap priority is the individual edge weight, not the total
            path distance from vertex 0. For A--B = 2, A--C = 5, B--C = 4,
            Prim's selects A--B and B--C for total tree weight 6, even though
            the resulting path from A to C is longer than the direct edge.

        Note on disconnected graphs:
            A disconnected graph has no spanning tree covering all vertices,
            so it has no minimum spanning tree for the entire graph. Finding
            an MST within each connected component produces a minimum
            spanning forest. This implementation starts only at vertex 0,
            so on disconnected input it returns only that component's tree.
            After the search, len(min_spanning_tree) != vertices - 1 would
            detect that a full spanning tree was not found. The practice
            problem guarantees connectivity, so no such check is required.

    Time Complexity:
        O(V + E log(E + 1)), where E = len(edges). Initialization and building
        the adjacency list take O(V + E). Each accepted vertex's neighbors
        are scanned at most once, examining at most 2E adjacency entries.
        Each undirected edge is pushed at most once, when its first endpoint
        joins the tree while the other is unvisited. Thus there are O(E)
        pushes and pops, each costing O(log(E + 1)). Early termination can
        avoid processing leftover candidates. For a connected simple graph
        with V >= 2, this is commonly written O(E log V); V = 1 takes O(1).

    Space Complexity:
        O(V + E) extra space including the returned tree. The adjacency list
        stores V lists and 2E entries, visited stores V flags, the heap holds
        up to O(E) candidates, and the tree stores V - 1 edges. Excluding the
        output tree does not change the O(V + E) bound.
    """
    # 1. Initialize the growing tree and a dummy entry for starting vertex 0.
    adjacency_list: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    min_heap: list[tuple[int, int, int]] = [(0, 0, -1)]
    visited: list[bool] = [False] * vertices
    min_spanning_tree: list[tuple[int, int, int]] = []
    min_weight: int = 0

    # 2. Store (weight, neighbor) pairs for both directions of every edge.
    for from_node, to_node, weight in edges:
        adjacency_list[from_node].append((weight, to_node))
        adjacency_list[to_node].append((weight, from_node))

    while min_heap:
        # 3. Choose the cheapest candidate; discard already-connected endpoints.
        weight, to_node, from_node = heapq.heappop(min_heap)

        if visited[to_node]:
            continue
        # 4. Accept this vertex and its real connecting edge, then check completion.
        visited[to_node] = True
        if from_node != -1:
            min_spanning_tree.append((from_node, to_node, weight))
            min_weight += weight
            if len(min_spanning_tree) == vertices - 1:
                break

        # 5. Offer outgoing edges without marking their destinations visited yet.
        for cost, neighbor in adjacency_list[to_node]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (cost, neighbor, to_node))

    # 6. Return the accepted edges and their combined weight.
    return (min_spanning_tree, min_weight)


def solve() -> None:
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 5], [1, 2, 3], [0, 2, 1]]
    expected: tuple[list[tuple[int, int, int]], int] = ([(0, 2, 1), (2, 1, 3)], 4)
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    def assert_valid_tree(
        vertices: int,
        edges: list[list[int]],
        result: tuple[list[tuple[int, int, int]], int],
    ) -> None:
        """Check the returned edges form a spanning tree of the input graph.

        Accept any valid minimum tree when several trees share the same cost;
        each test separately asserts its independently known minimum weight.
        """
        tree, total = result
        assert len(tree) == vertices - 1
        assert sum(weight for _, _, weight in tree) == total
        available = {(min(u, v), max(u, v), w) for u, v, w in edges}
        adjacency: list[list[int]] = [[] for _ in range(vertices)]
        selected = set()
        for u, v, weight in tree:
            assert 0 <= u < vertices and 0 <= v < vertices and u != v
            edge = (min(u, v), max(u, v), weight)
            assert edge in available and edge not in selected
            selected.add(edge)
            adjacency[u].append(v)
            adjacency[v].append(u)
        seen = {0}
        stack = [0]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        # Connectivity and V - 1 distinct edges imply no cycles.
        assert len(seen) == vertices

    # Minimum graph: empty tree and zero total weight.
    vertices: int = 1
    edges: list[list[int]] = []
    expected: int = 0
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Minimum edge weight.
    vertices: int = 2
    edges: list[list[int]] = [[0, 1, 1]]
    expected: int = 1
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Maximum edge weight, listed in reverse direction.
    vertices: int = 2
    edges: list[list[int]] = [[1, 0, 10000]]
    expected: int = 10000
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Cheaper connection is discovered after an expensive candidate.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 10], [0, 2, 1], [2, 1, 2]]
    expected: int = 3
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # MST differs from the source shortest-path tree.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 2], [0, 2, 5], [1, 2, 4]]
    expected: int = 6
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # A later accepted edge can be lighter than the previous one.
    vertices: int = 4
    edges: list[list[int]] = [[0, 1, 10], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 5]]
    expected: int = 4
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Equal-weight triangle: accept any valid minimum tree.
    vertices: int = 3
    edges: list[list[int]] = [[0, 1, 1], [1, 2, 1], [0, 2, 1]]
    expected: int = 2
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Equal-weight cycle with expensive diagonals.
    vertices: int = 4
    edges: list[list[int]] = [
        [0, 1, 2],
        [1, 2, 2],
        [2, 3, 2],
        [3, 0, 2],
        [0, 2, 9],
        [1, 3, 9],
    ]
    expected: int = 6
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Input is already a tree with mixed endpoint orientation.
    vertices: int = 5
    edges: list[list[int]] = [[1, 0, 4], [1, 2, 2], [3, 2, 7], [3, 4, 1]]
    expected: int = 14
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # High-index hub with the source as a leaf.
    vertices: int = 5
    edges: list[list[int]] = [[4, 0, 1], [4, 1, 2], [4, 2, 3], [4, 3, 4]]
    expected: int = 10
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Two groups require one expensive connecting edge.
    vertices: int = 6
    edges: list[list[int]] = [
        [0, 1, 1],
        [1, 2, 1],
        [0, 2, 3],
        [3, 4, 1],
        [4, 5, 1],
        [3, 5, 3],
        [2, 3, 100],
    ]
    expected: int = 104
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Competing routes with reordered and reversed input edges.
    vertices: int = 4
    edges: list[list[int]] = [[3, 2, 5], [3, 1, 1], [1, 2, 2], [2, 0, 1], [1, 0, 10]]
    expected: int = 4
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Maximum vertices, minimum edges, all minimum weights.
    vertices: int = 1000
    edges: list[list[int]] = [[i, i + 1, 1] for i in range(999)]
    expected: int = 999
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Maximum vertices, minimum edges, all maximum weights.
    vertices: int = 1000
    edges: list[list[int]] = [[i + 1, i, 10000] for i in range(999)]
    expected: int = 9990000
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Maximum vertices in a star; all other vertices attach to source.
    vertices: int = 1000
    edges: list[list[int]] = [[0, i, i] for i in range(1, 1000)]
    expected: int = 499500
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")

    # Maximum edge count with equal weights and many valid minimum trees.
    vertices: int = 1000
    edges: list[list[int]] = [
        [u, v, 10000] for u in range(1000) for v in range(u + 1, 1000)
    ]
    expected: int = 9990000
    result: tuple[list[tuple[int, int, int]], int] = prims_algorithm(vertices, edges)

    assert result[1] == expected
    assert_valid_tree(vertices, edges, result)
    print(f"Expected weight: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
