"""132. Find the MST Weight

Given a weighted, undirected, connected graph with V vertices numbered
from 0 to V - 1, find the sum of the edge weights in a Minimum Spanning
Tree (MST).

The input is an adjacency list: adj[u] contains pairs [v, w], representing
an edge between vertex u and vertex v with weight w. Each undirected edge
is represented in the adjacency lists of both endpoints.

A minimum spanning tree connects all vertices without cycles and has the
minimum possible total edge weight. Return the total weight, not the
selected edges. Multiple MSTs may exist, but their total weights are equal.

Note: The function receives an adjacency list, not a list of [u, v, w] edges.

Example 1:
    Input:
        V = 4
        adj = [[[1, 1], [3, 4]],
               [[0, 1], [2, 2]],
               [[1, 2], [3, 3]],
               [[0, 4], [2, 3]]]
    Output: 6
    Explanation:
        Choose edges 0 -- 1 (weight 1), 1 -- 2 (weight 2), and
        2 -- 3 (weight 3). They connect all four vertices without cycles.
        The minimum total weight is 1 + 2 + 3 = 6.

Example 2:
    Input:
        V = 3
        adj = [[[1, 5], [2, 15]],
               [[0, 5], [2, 10]],
               [[0, 15], [1, 10]]]
    Output: 15
    Explanation:
        Choose edges 0 -- 1 (weight 5) and 1 -- 2 (weight 10).
        The minimum total weight is 5 + 10 = 15.

Now Your Turn:
    Input:
        V = 4
        adj = [[[1, 1], [3, 4]],
               [[0, 1], [2, 2]],
               [[1, 2], [3, 3]],
               [[0, 4], [2, 3]]]
    Pick the correct output:
        A. 7
        B. 6
        C. 8
        D. 5

Constraints:
    - 2 <= V <= 10**3.
    - V - 1 <= E <= 10**4, where E counts undirected edges once.
    - 1 <= w <= 10**5.
    - The graph is undirected and connected.

https://www.youtube.com/watch?v=DMnDM_sxVig&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=47
"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    parents: list[int] = field(init=False)
    ranks: list[int] = field(init=False)

    def __post_init__(self) -> None:
        self.parents = list(range(self.vertices))
        self.ranks = [0] * self.vertices

    def _findParent(self, node: int) -> int:
        if self.parents[node] == node:
            return node

        self.parents[node] = self._findParent(self.parents[node])

        return self.parents[node]

    def find(self, node1: int, node2: int) -> bool:
        root1: int = self._findParent(node=node1)
        root2: int = self._findParent(node=node2)

        return root1 == root2

    def unionByRank(self, node1: int, node2: int) -> None:
        root1: int = self._findParent(node=node1)
        root2: int = self._findParent(node=node2)

        if root1 == root2:
            return False

        if self.ranks[root1] == self.ranks[root2]:
            self.parents[root2] = root1
            self.ranks[root1] += 1
        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

        return True


def find_mst_weight(vertices: int, adj: list[list[list[int]]]) -> int:
    """Return the total weight of a minimum spanning tree.

    Args:
        vertices: Number V of vertices, labeled 0 through V - 1, with
            2 <= V <= 1000.
        adj: Symmetric undirected adjacency list. Each adj[u] contains
            [v, weight] entries, with the reverse entry also present in
            adj[v]. The graph is connected, V - 1 <= E <= 10000, and weights
            are integers from 1 to 100000. E counts undirected edges once.

    Returns:
        The minimum total weight needed to connect every vertex without
        cycles. Only the sum is returned, not the selected edges. The input
        adjacency list is not modified. Connectivity is assumed, not checked;
        disconnected input would produce a minimum spanning forest's weight.

    Approach:
        Kruskal's Algorithm with Disjoint Set Union (Union-Find), using
        union by rank and path compression.

        1. Extract (weight, from_node, to_node) tuples from the adjacency
           list. Keep only from_node < to_node so each undirected edge is
           included once. Putting weight first makes it the sort priority.
        2. Sort the edges in nondecreasing weight order. Equal-weight edges
           are ordered by endpoint indices; ties may yield different valid
           MSTs, but the minimum total weight is unchanged.
        3. Initialize a disjoint set with each vertex in a separate component,
           the accumulated weight to 0, and the accepted-edge count to 0.
        4. Examine sorted edges. unionByRank finds both roots using path
           compression. If the roots match, it returns False: the endpoints
           are already connected, so accepting the edge would create a cycle.
           Otherwise, it attaches the lower-rank root under the higher-rank
           root (incrementing the surviving rank on ties) and returns True.
        5. Only on a successful merge, add the edge weight and increment
           edges_used. This combines connectivity checking and merging in
           one call, avoiding a separate find call for the same endpoints.
        6. Stop once edges_used equals V - 1. Each accepted edge reduces the
           number of components by one, so these edges form a spanning tree.
           Return the accumulated weight.

        Why the greedy choice works:
            Each accepted edge is a cheapest available edge joining two
            different components of the growing forest. By the minimum-edge
            cut property, it is safe to add such an edge to an MST. Skipping
            edges within a component prevents cycles while processing edges
            by weight minimizes the final total.

        Helper annotation note:
            unionByRank currently declares -> None but returns a boolean.
            The conditional in this function uses that actual return value;
            the helper's annotation should be -> bool.

    Time Complexity:
        O(V + E log(E + 1) + E * alpha(V)), where alpha is the inverse
        Ackermann function. Scanning the V adjacency lists and 2E neighbor
        entries costs O(V + E). Sorting E tuples takes O(E log(E + 1)).
        Initializing Union-Find costs O(V), and up to E union attempts cost
        O(E * alpha(V)) amortized with rank balancing and path compression.
        For a connected graph, this is commonly written O(E log E), with
        the one-edge case taking constant time. Early stopping reduces union
        attempts but does not avoid extracting and sorting the full edge list.

    Space Complexity:
        O(V + E) extra space. The extracted edge list stores E tuples, and
        Python's sort may use O(E) temporary space. Union-Find stores V
        parents and V ranks. Recursive root lookup uses O(log V) stack space
        in the worst case under rank balancing, within the overall bound.
        The input adjacency list is not copied or modified.
    """
    # 1. Extract each undirected edge once, with weight first for sorting.
    edges: list[tuple[int, int, int]] = []

    for from_node, neighbors in enumerate(adj):
        for to_node, weight in neighbors:
            if from_node < to_node:
                edges.append((weight, from_node, to_node))

    # 2. Consider the lightest edges first.
    edges.sort()

    # 3. Begin with V separate components and no accepted edges.
    ds = DisjointSet(vertices)
    mst_weight: int = 0
    edges_used: int = 0

    for weight, from_node, to_node in edges:
        # 4. Merge only distinct components; an existing connection means a cycle.
        if ds.unionByRank(node1=from_node, node2=to_node):
            # 5. Include the weight only when the edge is accepted.
            mst_weight += weight
            edges_used += 1

        # 6. V - 1 successful merges complete the spanning tree.
        if edges_used == vertices - 1:
            break

    return mst_weight


def solve() -> None:
    vertices: int = 4
    adj: list[list[list[int]]] = [
        [[1, 1], [3, 4]],
        [[0, 1], [2, 2]],
        [[1, 2], [3, 3]],
        [[0, 4], [2, 3]],
    ]
    expected: int = 6
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    def build_adj(
        vertices: int, roads: list[tuple[int, int, int]]
    ) -> list[list[list[int]]]:
        """Construct symmetric adjacency lists for the test inputs."""
        adj: list[list[list[int]]] = [[] for _ in range(vertices)]
        for u, v, weight in roads:
            adj[u].append([v, weight])
            adj[v].append([u, weight])
        return adj

    # Minimum vertices and minimum edge weight.
    vertices: int = 2
    adj: list[list[list[int]]] = build_adj(vertices, [(0, 1, 1)])
    expected: int = 1
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum vertices and maximum edge weight.
    vertices: int = 2
    adj: list[list[list[int]]] = build_adj(vertices, [(0, 1, 100000)])
    expected: int = 100000
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    vertices: int = 3
    adj: list[list[list[int]]] = build_adj(
        vertices, [(0, 1, 5), (0, 2, 15), (1, 2, 10)]
    )
    expected: int = 15
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cheap edges beat an expensive direct connection.
    vertices: int = 3
    adj: list[list[list[int]]] = build_adj(vertices, [(0, 1, 10), (0, 2, 1), (2, 1, 2)])
    expected: int = 3
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum spanning tree differs from shortest-path tree.
    vertices: int = 3
    adj: list[list[list[int]]] = build_adj(vertices, [(0, 1, 2), (0, 2, 5), (1, 2, 4)])
    expected: int = 6
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal-weight triangle accepts any minimum spanning tree.
    vertices: int = 3
    adj: list[list[list[int]]] = build_adj(vertices, [(0, 1, 7), (1, 2, 7), (2, 0, 7)])
    expected: int = 14
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal-weight cycle with expensive diagonals.
    vertices: int = 4
    adj: list[list[list[int]]] = build_adj(
        vertices, [(0, 1, 2), (1, 2, 2), (2, 3, 2), (3, 0, 2), (0, 2, 9), (1, 3, 9)]
    )
    expected: int = 6
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Input already forms a tree.
    vertices: int = 5
    adj: list[list[list[int]]] = build_adj(
        vertices, [(1, 0, 4), (1, 2, 2), (3, 2, 7), (3, 4, 1)]
    )
    expected: int = 14
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Highest-index vertex is the hub.
    vertices: int = 5
    adj: list[list[list[int]]] = build_adj(
        vertices, [(4, 0, 1), (4, 1, 2), (4, 2, 3), (4, 3, 4)]
    )
    expected: int = 10
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two groups require an expensive bridge.
    vertices: int = 6
    adj: list[list[list[int]]] = build_adj(
        vertices,
        [(0, 1, 1), (1, 2, 1), (0, 2, 3), (3, 4, 1), (4, 5, 1), (3, 5, 3), (2, 3, 100)],
    )
    expected: int = 104
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheap cycles must not inflate the result.
    vertices: int = 5
    adj: list[list[list[int]]] = build_adj(
        vertices, [(0, 1, 1), (1, 2, 1), (2, 0, 1), (2, 3, 5), (3, 4, 2), (1, 4, 10)]
    )
    expected: int = 9
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted roads and reversed endpoints.
    vertices: int = 4
    adj: list[list[list[int]]] = build_adj(
        vertices, [(3, 2, 5), (3, 1, 1), (1, 2, 2), (2, 0, 1), (1, 0, 10)]
    )
    expected: int = 4
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with minimum edge count and minimum weights.
    vertices: int = 1000
    adj: list[list[list[int]]] = build_adj(
        vertices, [(i, i + 1, 1) for i in range(999)]
    )
    expected: int = 999
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with maximum weights; sum exceeds one edge weight.
    vertices: int = 1000
    adj: list[list[list[int]]] = build_adj(
        vertices, [(i + 1, i, 100000) for i in range(999)]
    )
    expected: int = 99900000
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices in a star.
    vertices: int = 1000
    adj: list[list[list[int]]] = build_adj(
        vertices, [(999, i, i + 1) for i in range(999)]
    )
    expected: int = 499500
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exactly 10000 edges with a cheap spanning chain.
    vertices: int = 1000
    adj: list[list[list[int]]] = build_adj(
        vertices,
        [(i, i + 1, 1) for i in range(999)]
        + [(u, v, 100000) for u in range(1000) for v in range(u + 2, 1000)][:9001],
    )
    expected: int = 999
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Exactly 10000 edges, all maximum weight.
    vertices: int = 1000
    adj: list[list[list[int]]] = build_adj(
        vertices,
        [(i, i + 1, 100000) for i in range(999)]
        + [(u, v, 100000) for u in range(1000) for v in range(u + 2, 1000)][:9001],
    )
    expected: int = 99900000
    result: int = find_mst_weight(vertices, adj)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
