import heapq


def johnsons_algorithm(
    vertices: int,
    edges: list[tuple[int, int, int]],
) -> list[list[float]] | None:
    """Return shortest distances between every ordered pair of vertices.

    Args:
        vertices: Number of original vertices. Vertices must use consecutive
            integer IDs from 0 through vertices - 1.
        edges: Directed edges stored as (start, end, weight). Weights must be
            integers and may be negative. Parallel edges are supported.

    Returns:
        A vertices-by-vertices matrix where result[u][v] is the shortest
        distance from u to v. An unreachable pair keeps float("inf"). Returns
        None if any negative cycle exists, because repeatedly following that
        cycle would make affected path costs decrease without a finite limit.

    Mutation:
        The function does not mutate edges. It copies the edge list before
        adding temporary edges and builds a separate reweighted graph.

    Approach:
        Johnson's Algorithm, combining the Bellman-Ford Algorithm with
        Dijkstra's Algorithm.

        Add a temporary source
            -> Run Bellman-Ford once
            -> Detect a negative cycle
            -> Reweight every original edge to be nonnegative
            -> Remove the temporary source
            -> Run Dijkstra from every original vertex
            -> Convert all distances back to their original weights

        1. Give a temporary source the next unused ID, vertices, and connect
           it to every original vertex with a zero-weight directed edge. This
           lets one Bellman-Ford run reach every vertex, including vertices in
           disconnected sections of the original directed graph.
        2. Run Bellman-Ford from the temporary source. Its shortest distance
           to each vertex becomes that vertex's potential h[vertex]. Stop
           early when a full relaxation pass makes no changes.
        3. Inspect every edge once more. If an edge can still improve a
           potential after the required passes, a negative cycle exists.
           Return None because all-pairs finite shortest paths do not exist.
        4. Remove the temporary source conceptually by considering only the
           original edges. Reweight each original edge u -> v with:

               new_weight = weight + h[u] - h[v]

           Bellman-Ford's shortest-distance rule guarantees these new weights
           are nonnegative. Build an adjacency list at the same time so that
           Dijkstra can inspect only the outgoing edges of the node it pops.
           For every path with fixed endpoints, intermediate potential values
           cancel, so reweighting does not change which path is shortest.
        5. Run min-heap Dijkstra once from every original source. For one
           source, initialize its distance to zero and all other distances to
           infinity. Pop the smallest known distance, skip stale heap entries,
           and relax each outgoing edge. The reweighted edges are nonnegative,
           which makes Dijkstra valid.
        6. Dijkstra's answers use reweighted edges, so convert each reachable
           source-to-destination distance back with:

               original_distance = (
                   reweighted_distance - h[source] + h[destination]
               )

           Leave unreachable destinations at infinity. Append this converted
           row to the final all-pairs matrix, then repeat for the next source.

        Reweighting example:
            Suppose h[B] = -2, h[C] = 0, and the original B -> C edge
            weighs 3. Its reweighted cost is 3 + (-2) - 0 = 1. Dijkstra sees
            distance 1 from B to C. Converting it back gives
            1 - (-2) + 0 = 3, recovering the original shortest distance.

    Time Complexity:
        Let V = vertices and E = len(edges).

        Adding the temporary source creates V extra edges, so Bellman-Ford
        processes E + V edges for at most V passes. This phase costs
        O(V(E + V)). Reweighting and building adjacency cost O(V + E).

        One Dijkstra run initializes V distances, examines at most E outgoing
        edge entries, and performs logarithmic heap operations. For a simple
        graph, each heap operation is O(log V), so one run costs
        O((V + E) log V). Running it from all V sources costs
        O(V(V + E) log V). Converting V result entries for each of V sources
        adds O(V**2), which is already covered by that bound.

        Combining the sequential phases gives O(V(V + E) log V) for V >= 2.
        When E is at least proportional to V, this is commonly written as
        O(VE log V). Unlike Floyd-Warshall's O(V**3), Johnson's algorithm is
        especially useful for sparse graphs where E is much smaller than
        V**2. Python's duplicate-entry heap can contain O(E) entries; in a
        graph allowing arbitrarily many parallel edges, replace log V with
        log E in the heap term.

        Interview summary: Bellman-Ford runs once, and then Dijkstra runs V
        times, giving O(V(V + E) log V) on a simple graph.

    Space Complexity:
        O(V**2 + E), including the returned matrix. The all_distances matrix
        stores exactly V**2 entries. For example, V = 4 creates 16 result
        entries. The copied Bellman-Ford edge list stores E + V edges, the
        adjacency list stores V lists and E edge entries, and potentials,
        the two distance rows, and other per-vertex data each use O(V) space.
        The heap can hold O(E) entries because improved distances leave stale
        entries behind until they are popped.

        The distance arrays and heap are reused for one source at a time, so
        their memory is not multiplied by V. Excluding the required V-by-V
        output matrix and excluding the input, auxiliary space is O(V + E).
        The implementation uses no recursion.

        https://www.youtube.com/watch?v=MV7EAD9zL64
    """

    # ---------------------------------------------------------
    # Step 1: Add temporary source S.
    # ---------------------------------------------------------
    temporary_source = vertices
    total_vertices = vertices + 1

    bellman_ford_edges = edges.copy()

    # S has a zero-weight edge to every original vertex.
    for node in range(vertices):
        bellman_ford_edges.append((temporary_source, node, 0))

    # ---------------------------------------------------------
    # Step 2: Run Bellman-Ford from S.
    # These distances become the potential values h[node].
    # ---------------------------------------------------------
    potentials: list[float] = [float("inf")] * total_vertices
    potentials[temporary_source] = 0

    # A graph with total_vertices vertices needs at most
    # total_vertices - 1 relaxation rounds.
    for _ in range(total_vertices - 1):
        updated = False

        for start, end, weight in bellman_ford_edges:
            if potentials[start] == float("inf"):
                continue

            new_distance = potentials[start] + weight

            if new_distance < potentials[end]:
                potentials[end] = new_distance
                updated = True

        # Stop early if no distance changed during this round.
        if not updated:
            break

    # ---------------------------------------------------------
    # Step 3: Detect a negative cycle.
    # ---------------------------------------------------------
    for start, end, weight in bellman_ford_edges:
        if potentials[start] == float("inf"):
            continue

        if potentials[start] + weight < potentials[end]:
            return None

    # ---------------------------------------------------------
    # Step 4: Reweight all original edges.
    # ---------------------------------------------------------
    adjacency_list: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]

    for start, end, weight in edges:
        new_weight = int(weight + potentials[start] - potentials[end])

        adjacency_list[start].append((end, new_weight))

    # ---------------------------------------------------------
    # Step 5: Run Dijkstra from every original vertex.
    # ---------------------------------------------------------
    all_distances: list[list[float]] = []

    for source in range(vertices):
        reweighted_distances: list[float] = [float("inf")] * vertices

        reweighted_distances[source] = 0

        min_heap: list[tuple[float, int]] = [(0, source)]

        while min_heap:
            current_distance, node = heapq.heappop(min_heap)

            # Skip outdated heap entries.
            if current_distance > reweighted_distances[node]:
                continue

            for neighbor, edge_weight in adjacency_list[node]:
                new_distance = current_distance + edge_weight

                if new_distance < reweighted_distances[neighbor]:
                    reweighted_distances[neighbor] = new_distance

                    heapq.heappush(
                        min_heap,
                        (new_distance, neighbor),
                    )

        # -----------------------------------------------------
        # Step 6: Convert distances back to original weights.
        # -----------------------------------------------------
        original_distances: list[float] = [float("inf")] * vertices

        for destination in range(vertices):
            if reweighted_distances[destination] == float("inf"):
                continue

            original_distances[destination] = (
                reweighted_distances[destination]
                - potentials[source]
                + potentials[destination]
            )

        all_distances.append(original_distances)

    return all_distances


def solve() -> None:
    # Negative edges without a negative cycle.
    vertices: int = 4
    edges: list[tuple[int, int, int]] = [
        (0, 1, -2),
        (0, 2, 4),
        (1, 2, 3),
        (1, 3, 2),
        (2, 3, 2),
        (3, 1, 1),
    ]
    expected: list[list[float]] | None = [
        [0, -2, 1, 0],
        [float("inf"), 0, 3, 2],
        [float("inf"), 3, 0, 2],
        [float("inf"), 1, 4, 0],
    ]
    result: list[list[float]] | None = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive weights with a cheaper indirect route.
    vertices = 4
    edges = [
        (0, 1, 4),
        (0, 2, 1),
        (2, 1, 2),
        (1, 3, 1),
        (2, 3, 5),
    ]
    expected = [
        [0, 3, 1, 4],
        [float("inf"), 0, float("inf"), 1],
        [float("inf"), 2, 0, 3],
        [float("inf"), float("inf"), float("inf"), 0],
    ]
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum graph: one vertex and no edges.
    vertices = 1
    edges = []
    expected = [[0]]
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected components leave unreachable pairs at infinity.
    vertices = 4
    edges = [
        (0, 1, 5),
        (2, 3, -1),
    ]
    expected = [
        [0, 5, float("inf"), float("inf")],
        [float("inf"), 0, float("inf"), float("inf")],
        [float("inf"), float("inf"), 0, -1],
        [float("inf"), float("inf"), float("inf"), 0],
    ]
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-weight and negative edges without a negative cycle.
    vertices = 3
    edges = [
        (0, 1, 0),
        (1, 2, -1),
        (0, 2, 4),
    ]
    expected = [
        [0, 0, -1],
        [float("inf"), 0, -1],
        [float("inf"), float("inf"), 0],
    ]
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parallel directed edges use the cheaper edge.
    vertices = 2
    edges = [
        (0, 1, 10),
        (0, 1, 3),
    ]
    expected = [
        [0, 3],
        [float("inf"), 0],
    ]
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Reachable negative cycle prevents finite shortest paths.
    vertices = 3
    edges = [
        (0, 1, 1),
        (1, 2, -2),
        (2, 0, 0),
    ]
    expected = None
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # The temporary source exposes a negative cycle in another component.
    vertices = 4
    edges = [
        (0, 1, 2),
        (2, 3, -2),
        (3, 2, 1),
    ]
    expected = None
    result = johnsons_algorithm(vertices, edges)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
