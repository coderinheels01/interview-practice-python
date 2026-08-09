"""
Dijkstra's Algorithm

Difficulty: Medium
Company Tags

Implement Dijkstra's shortest path algorithm.

Given a weighted, directed graph and a starting vertex, return the shortest
distance from the starting vertex to every vertex in the graph.

Input:
    n: The number of vertices in the graph, where 2 <= n <= 100. Each vertex
       is labeled from 0 to n - 1.
    edges: A list of tuples, each representing a directed edge in the form
           (u, v, w), where u is the source vertex, v is the destination
           vertex, and w is the edge weight, where 1 <= w <= 10.
    src: The source vertex from which to start the algorithm, where
         0 <= src < n.

Note:
    If a vertex is unreachable from the source vertex, its shortest path
    distance should be -1.

Example 1:
    Input:
        n = 5
        edges = [
            [0, 1, 10],
            [0, 2, 3],
            [1, 3, 2],
            [2, 1, 4],
            [2, 3, 8],
            [2, 4, 2],
            [3, 4, 5],
        ]
        src = 0

    Output:
        {0: 0, 1: 7, 2: 3, 3: 9, 4: 5}

Approach: Adjacency list + min-heap
    First, convert the edge list into an adjacency list. For each source
    vertex, the adjacency list stores its outgoing (neighbor, weight) pairs.
    This allows the algorithm to inspect only the edges leaving the current
    vertex instead of scanning the complete edge list each time.

    Store the shortest distance found so far for every vertex in `result`.
    The source starts at distance 0, while -1 means a vertex has not yet been
    reached. A min-heap holds (distance, vertex) pairs, causing the vertex with
    the smallest known distance to be removed first.

    For every outgoing edge, calculate the distance to its neighbor through
    the current vertex:

        current distance + edge weight

    If this is the first path to the neighbor, or it is shorter than the
    recorded path, update the neighbor's distance and push that new distance
    onto the heap. This operation is called edge relaxation.

Why this works:
    Every edge weight is positive, so extending a path can never reduce its
    total distance. The min-heap processes available paths from smallest to
    largest. Once the smallest distance for a vertex is processed, following
    its outgoing edges safely extends that shortest path to its neighbors.

    A vertex may appear in the heap more than once if a shorter route is found
    after an earlier route was pushed. If a popped distance is larger than the
    distance currently stored in `result`, that heap entry is stale and can be
    ignored.

Complexity:
    Let V be the number of vertices and E be the number of directed edges.

    Time: O((V + E) log E)
        Building the adjacency list takes O(E). Each edge is examined at most
        once from a non-stale heap entry and may cause one heap push. The heap
        can hold O(E) entries, so each push and pop costs O(log E). This is
        commonly simplified to O((V + E) log V).

    Space: O(V + E)
        The result dictionary stores V distances, the adjacency list stores E
        edges, and the heap may contain O(E) entries including stale entries.
"""

import heapq


def build_adjacency_map(edges: list[tuple[int, int, int]]) ->  dict[int, list[tuple[int, int]]]:
    # Step 1: Group every directed edge by its source vertex.
    adj: dict[int, list[tuple[int, int]]] = {}

    for u, v, weight in edges:
        # Store each outgoing edge as (destination, edge weight).
        if u not in adj:
            adj[u] = [(v, weight)]
        else:
            adj[u].append((v, weight))

    return adj

def dijkstra(
    n: int, edges: list[tuple[int, int, int]], src: int
) -> dict[int, int]:
    # Step 2: Initialize every vertex as unreachable.
    result: dict[int, int] = {vertex: -1 for vertex in range(n)}
    adjacency_map: dict[int, list[tuple[int, int]]] = build_adjacency_map(edges=edges)

    # Step 3: Begin at the source with distance 0. The distance comes first in
    # each tuple because heapq compares tuple values from left to right.
    min_heap: list[tuple[int, int]] = [(0, src)]
    result[src] = 0

    # Step 4: Process reachable paths in increasing order of distance.
    while min_heap:
        current_distance, vertex = heapq.heappop(min_heap)

        # Step 5: Skip an old heap entry when a shorter route to this vertex
        # has already been discovered.
        if current_distance > result[vertex]:
            continue

        # Step 6: Vertices without outgoing edges are absent from the map.
        if vertex in adjacency_map:
            for neighbor, edge in adjacency_map[vertex]:
                # Step 7: Calculate the path distance through this vertex.
                new_weight: int = current_distance + edge

                # Step 8: Relax the edge if this is the first known route to
                # the neighbor or if it improves the previous route.
                if result[neighbor] == -1 or result[neighbor] > new_weight:
                    result[neighbor] = new_weight

                    # Step 9: Queue the improved route for later processing.
                    heapq.heappush(min_heap, (new_weight, neighbor))

    # Step 10: Any vertex that was never reached still has distance -1.
    return result



def solve():
    n = 5
    edges = [
        (0, 1, 10),
        (0, 2, 3),
        (1, 3, 2),
        (2, 1, 4),
        (2, 3, 8),
        (2, 4, 2),
        (3, 4, 5),
    ]
    src = 0
    expected = {0: 0, 1: 7, 2: 3, 3: 9, 4: 5}
    result = dijkstra(n, edges, src)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    n = 4
    edges = [(0, 1, 2)]
    src = 0
    expected = {0: 0, 1: 2, 2: -1, 3: -1}
    result = dijkstra(n, edges, src)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    n = 3
    edges = [(2, 0, 5), (2, 1, 1), (1, 0, 2)]
    src = 2
    expected = {0: 3, 1: 1, 2: 0}
    result = dijkstra(n, edges, src)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    n = 4
    edges = [(0, 1, 8), (0, 2, 2), (2, 1, 3), (1, 3, 1), (2, 3, 9)]
    src = 0
    expected = {0: 0, 1: 5, 2: 2, 3: 6}
    result = dijkstra(n, edges, src)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

    n = 3
    edges = [(0, 1, 4), (1, 2, 3), (2, 0, 1)]
    src = 1
    expected = {0: 4, 1: 0, 2: 3}
    result = dijkstra(n, edges, src)
    assert result == expected
    print(f"expected: {expected}")
    print(f"result: {result}")

solve()

