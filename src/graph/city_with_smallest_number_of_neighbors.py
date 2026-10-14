"""City With the Smallest Number of Neighbors at a Threshold Distance

There are n cities numbered from 0 to n - 1. Each entry in edges has the
form [from_city, to_city, weight] and represents a bidirectional, weighted
edge between the two cities.

Given distance_threshold, find the city with the smallest number of other
cities reachable through a path whose total distance is at most
distance_threshold. If multiple cities have the same smallest count,
return the city with the greatest number.

The distance of a path is the sum of the weights of its edges. Count each
reachable city once, and do not count the starting city as its own neighbor.
Return the selected city's index, not its neighbor count.

Example 1:
    Input:
        n = 4, m = 4
        edges = [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]]
        distance_threshold = 4
    Output: 3
    Explanation:
        The reachable neighboring cities within distance 4 are:
        City 0 -> [1, 2]
        City 1 -> [0, 2, 3]
        City 2 -> [0, 1, 3]
        City 3 -> [1, 2]

        Cities 0 and 3 each have the smallest count of 2 neighbors.
        Return 3 because it has the greater city number.

Input notes:
    - m = len(edges); it does not need a separate function parameter.
    - The screenshot does not show numerical input constraints.

https://www.youtube.com/watch?v=PwMVNSJ5SLI&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=43

"""


def city_with_smallest_number_of_neighbors(
    n: int, edges: list[list[int]], distance_threshold: int
) -> int:
    """Return the city with the fewest neighbors within the distance threshold.

    Args:
        n: Positive number of cities, labeled 0 through n - 1.
        edges: Undirected roads [from_city, to_city, weight], with valid,
            distinct endpoints, nonnegative weights, and at most one road
            per pair. The input edge list is not modified.
        distance_threshold: Nonnegative inclusive limit on shortest-path
            distance. This implementation assumes the threshold and all
            finite shortest distances are below its 10**9 sentinel.

    Returns:
        The index of the city with the fewest other reachable cities within
        the threshold. Ties favor the greatest city index. An isolated city
        has zero neighbors; for a single-city graph, returns 0.

    Approach:
        Floyd-Warshall Algorithm (all-pairs shortest paths).

        Use Floyd-Warshall to compute the shortest distance between every
        pair of cities. Then count each city's neighbors within the threshold
        and select the city with the smallest count, breaking ties by the
        greatest city index.

        1. Initialize the selected city to -1 and the best neighbor count
           to n, larger than any possible count of other cities. Allocate
           an n x n distance matrix with a zero diagonal and 10**9 for
           initially unreachable pairs.
        2. Store each road's weight in both directions because the graph
           is undirected.
        3. Consider each city as an intermediate vertex in the outermost
           loop. For each starting city, skip the destination loop if it
           cannot reach this intermediate vertex. Otherwise, update each
           distance to the smaller of its current value and the sum of
           the two distances through the intermediate city.
        4. After all intermediate vertices have been considered, count
           the other cities whose shortest distance from each starting
           city is <= distance_threshold. Exclude the starting city itself.
           Each destination is counted once, regardless of how many routes
           reach it. A path exactly at the threshold is included.
        5. Visit starting cities in increasing index order. Replace the
           selected city when its neighbor count is <= the best count.
           A lower count improves the answer; an equal count replaces it
           with the larger city index, implementing the tie-breaking rule.
        6. Return the selected city index, not the neighbor count.

        Why the distance updates work:
            After processing intermediate vertex k, each matrix entry is
            the shortest distance allowing intermediate vertices 0 through
            k. A route either avoids k or splits there into two subpaths.
            The outermost intermediate loop ensures those subpaths have
            already been considered. Nonnegative weights and zero diagonal
            entries allow the distance matrix to be updated in place.

    Time Complexity:
        O(n**3 + m), where m = len(edges). Matrix initialization takes
        O(n**2), loading roads takes O(m), and Floyd-Warshall performs up to
        n**3 constant-time updates. Counting neighbors takes O(n**2).
        For a simple graph, m = O(n**2), so the total is O(n**3).
        Skipping unreachable first legs reduces some work but does not
        change the worst-case bound.

    Space Complexity:
        O(n**2) extra space for the newly allocated distance matrix. The
        selected city, counts, and loop variables use O(1) additional space.
        Unlike a version that receives and overwrites an adjacency matrix,
        this function constructs its own matrix from the supplied edges.
    """
    # 1. Initialize the best candidate and all-pairs distance matrix.
    city: int = -1
    city_count: int = n
    adjacentcy_matrix: list[list[int]] = [
        [0 if row == col else 10**9 for col in range(n)] for row in range(n)
    ]

    # 2. Every road can be traversed in either direction.
    for from_city, to_city, weight in edges:
        adjacentcy_matrix[from_city][to_city] = weight
        adjacentcy_matrix[to_city][from_city] = weight

    # 3. Allow each intermediate city and improve distances through it.
    for via_index in range(n):
        for row_index in range(n):
            if adjacentcy_matrix[row_index][via_index] == 10**9:
                continue
            for col_index in range(n):
                adjacentcy_matrix[row_index][col_index] = min(
                    adjacentcy_matrix[row_index][col_index],
                    adjacentcy_matrix[row_index][via_index]
                    + adjacentcy_matrix[via_index][col_index],
                )

    # 4. Count distinct other cities within the inclusive distance threshold.
    for row_index in range(n):
        current_city_count: int = 0
        for col_index in range(n):
            if (
                row_index != col_index
                and adjacentcy_matrix[row_index][col_index] <= distance_threshold
            ):
                current_city_count += 1
        # 5. Equal counts favor this later, larger city index.
        if current_city_count <= city_count:
            city_count = current_city_count
            city = row_index

    # 6. Return the chosen city rather than its neighbor count.
    return city


def solve() -> None:
    n: int = 4
    edges: list[list[int]] = [
        [0, 1, 3],
        [1, 2, 1],
        [1, 3, 4],
        [2, 3, 1],
    ]
    distance_threshold: int = 4
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cities tied at the exact threshold.
    n: int = 2
    edges: list[list[int]] = [[0, 1, 4]]
    distance_threshold: int = 4
    expected: int = 1
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Threshold just below the road weight.
    n: int = 2
    edges: list[list[int]] = [[0, 1, 4]]
    distance_threshold: int = 3
    expected: int = 1
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # City zero is isolated by the threshold.
    n: int = 4
    edges: list[list[int]] = [[0, 1, 9], [1, 2, 1], [2, 3, 1], [1, 3, 1]]
    distance_threshold: int = 2
    expected: int = 0
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Interior city has the fewest reachable neighbors.
    n: int = 4
    edges: list[list[int]] = [[1, 0, 9], [0, 2, 1], [2, 3, 1], [0, 3, 1]]
    distance_threshold: int = 2
    expected: int = 1
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Final city has the fewest reachable neighbors.
    n: int = 4
    edges: list[list[int]] = [[3, 0, 9], [0, 1, 1], [1, 2, 1], [0, 2, 1]]
    distance_threshold: int = 2
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tie between cities zero and two chooses two, not the final city.
    n: int = 4
    edges: list[list[int]] = [[0, 3, 1], [1, 3, 1], [2, 1, 1]]
    distance_threshold: int = 1
    expected: int = 2
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Roads must be traversable in both directions.
    n: int = 4
    edges: list[list[int]] = [[1, 0, 9], [2, 1, 1], [3, 2, 1], [3, 1, 1]]
    distance_threshold: int = 2
    expected: int = 0
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Path exactly at the threshold counts.
    n: int = 4
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 2], [2, 3, 2]]
    distance_threshold: int = 4
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Path one above the threshold does not count.
    n: int = 4
    edges: list[list[int]] = [[0, 1, 2], [1, 2, 2], [2, 3, 2]]
    distance_threshold: int = 3
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Indirect path beats an expensive direct road.
    n: int = 5
    edges: list[list[int]] = [[0, 1, 1], [1, 2, 1], [0, 2, 9], [2, 3, 1], [3, 4, 4]]
    distance_threshold: int = 3
    expected: int = 4
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All cities can reach every other city; choose the highest index.
    n: int = 5
    edges: list[list[int]] = [[i, i + 1, 1] for i in range(4)]
    distance_threshold: int = 4
    expected: int = 4
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # No road fits the threshold; all cities tie.
    n: int = 4
    edges: list[list[int]] = [[0, 1, 5], [1, 2, 5], [2, 3, 5]]
    distance_threshold: int = 1
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal routes to a neighbor count that city only once.
    n: int = 5
    edges: list[list[int]] = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1], [3, 4, 2]]
    distance_threshold: int = 2
    expected: int = 4
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected components of different sizes.
    n: int = 5
    edges: list[list[int]] = [[0, 1, 1], [2, 3, 1], [3, 4, 1]]
    distance_threshold: int = 3
    expected: int = 1
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several isolated cities tie; choose the greatest isolated index.
    n: int = 5
    edges: list[list[int]] = [[0, 4, 1]]
    distance_threshold: int = 2
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # All cities isolated.
    n: int = 4
    edges: list[list[int]] = []
    distance_threshold: int = 1
    expected: int = 3
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single city has no other neighbors.
    n: int = 1
    edges: list[list[int]] = []
    distance_threshold: int = 1
    expected: int = 0
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero threshold with positive roads.
    n: int = 3
    edges: list[list[int]] = [[0, 1, 1], [1, 2, 1]]
    distance_threshold: int = 0
    expected: int = 2
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger chain: threshold reaches only immediate neighbors.
    n: int = 100
    edges: list[list[int]] = [[i, i + 1, 10000] for i in range(99)]
    distance_threshold: int = 10000
    expected: int = 99
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Larger dense graph with uniform weights.
    n: int = 100
    edges: list[list[int]] = [[u, v, 1] for u in range(100) for v in range(u + 1, 100)]
    distance_threshold: int = 1
    expected: int = 99
    result: int = city_with_smallest_number_of_neighbors(n, edges, distance_threshold)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
