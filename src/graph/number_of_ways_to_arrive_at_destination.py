"""462. Number of Ways to Arrive at Destination

A city consists of n intersections numbered from 0 to n - 1, with
bidirectional roads between some intersections. Every intersection is
reachable from every other intersection, and there is at most one road
between any two intersections.

Given n and a 2D integer array roads, each entry [u, v, time] represents a
road between intersections u and v that takes time minutes to travel.
Determine the number of ways to travel from intersection 0 to intersection
n - 1 in the shortest amount of time.

Since the answer may be large, return the count modulo 10**9 + 7.
Here, m = len(roads). Return the number of shortest routes, not their travel
time or the sequences of intersections along them.

Example 1:
    Input:
        n = 7, m = 10
        roads = [[0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3],
                 [6, 3, 3], [3, 5, 1], [6, 5, 1], [2, 5, 1],
                 [0, 4, 5], [4, 6, 2]]
    Output: 4
    Explanation:
        The shortest travel time is 7 minutes. The four routes are:
        - 0 -> 6
        - 0 -> 4 -> 6
        - 0 -> 1 -> 2 -> 5 -> 6
        - 0 -> 1 -> 3 -> 5 -> 6

Example 2:
    Input:
        n = 6, m = 8
        roads = [[0, 5, 8], [0, 2, 2], [0, 1, 1], [1, 3, 3],
                 [1, 2, 3], [2, 5, 6], [3, 4, 2], [4, 5, 2]]
    Output: 3
    Explanation:
        The shortest travel time is 8 minutes. The three routes are:
        - 0 -> 5
        - 0 -> 2 -> 5
        - 0 -> 1 -> 3 -> 4 -> 5

Now Your Turn:
    Input:
        n = 4, m = 4
        roads = [[0, 1, 10], [1, 2, 7], [2, 3, 4], [0, 3, 3]]
    Pick the correct output:
        A. 7
        B. 4
        C. 0
        D. 1

Constraints:
    - 1 <= n <= 200.
    - n - 1 <= len(roads) <= n * (n - 1) / 2.
    - Each road entry has exactly three elements.
    - 0 <= u, v <= n - 1.
    - 1 <= time <= 10**9.
    - u != v.
    - The graph is connected, with at most one road between any two nodes.

Discussion Questions:
    - How do we handle multiple shortest paths to a node?
    - Why use Dijkstra's Algorithm instead of BFS?
    - How would you return all actual paths instead of just the count?
    - How does this compare to Floyd-Warshall?

https://www.youtube.com/watch?v=_-0mx0SmYxA&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=40

"""

import heapq
from collections import defaultdict


def number_of_ways_to_arrive_at_destination(n: int, roads: list[list[int]]) -> int:
    """Count shortest routes from intersection 0 to n - 1 modulo 10**9 + 7.

    Args:
        n: Number of intersections, labeled 0 through n - 1, with
            1 <= n <= 200.
        roads: Entries [u, v, time] describing undirected roads with valid,
            distinct endpoints and integer travel times from 1 to 10**9.
            The graph is connected and has at most one road per pair.

    Returns:
        The number of minimum-time routes modulo 10**9 + 7. For n = 1,
        returns 1 for the empty route from the source to itself.
        The input roads are not modified.

    Approach:
        Dijkstra's Algorithm with shortest-path counting. Track both the
        minimum travel time and the number of routes achieving that time
        for each intersection. The heap is ordered by total travel time.

        1. Initialize all route counts to 0 and distances to 10**18. The
           source has distance 0 and one route: the empty route. Seed the
           min heap with (0, 0). The sentinel exceeds any possible shortest
           distance: a simple path uses at most 199 roads of time 10**9.
        2. Build an adjacency list using the nested helper, storing each
           road in both directions as (neighbor, travel time).
        3. Pop the smallest (distance, node) entry. Skip it if a better
           distance is already recorded for that node. Improved distances
           leave old entries in the heap, so these stale entries must not
           propagate route counts again.
        4. If the popped node is the destination, return its route count.
           Strictly positive road times ensure every predecessor on a
           shortest route has a smaller distance and has already been
           processed. Thus both the distance and count are finalized.
        5. For each neighbor, calculate the candidate travel time by adding
           the road time to the current node's distance.
        6. If the candidate equals the neighbor's best distance, add the
           current node's route count to the neighbor's count modulo
           10**9 + 7. Do not enqueue again: the distance has not changed,
           and this count will be complete before the neighbor is popped.
        7. If the candidate is shorter, replace the neighbor's distance and
           route count with this candidate and ways[node], then push the
           improved entry using heappush. Routes at the old, longer distance
           no longer count. Longer candidates are ignored.
        8. If the heap empties, return the recorded destination count as a
           fallback. Under the connected-graph assumption, step 4 returns
           first. Applying modulo to counts never changes travel distances.

        Counting example: if two shortest routes reach node u, extending
        them along a road to v contributes two routes. A shorter arrival
        at v replaces its old count; an equally short arrival adds to it.
        This distinction avoids counting routes that are no longer shortest.

    Time Complexity:
        O((n + m) log n) for n >= 2, where m = len(roads); O(1) for n = 1.
        Initialization and adjacency construction take O(n + m). Each node's
        adjacency list is expanded once from its finalized heap entry, so
        O(m) road entries are examined. Strict improvements cause at most
        O(m) heap pushes and pops, each costing O(log m). Because the simple
        graph has m <= n * (n - 1) / 2, log m is O(log n). Equal-distance
        arrivals update counts in constant time without adding heap entries.

    Space Complexity:
        O(n + m) extra space. The ways and distances arrays store n entries
        each, the adjacency list stores both directions of m roads, and the
        heap can hold O(m) entries including stale ones. No actual routes
        are stored, and modulo arithmetic keeps route counts bounded.
    """
    # 1. Initialize distances, route counts, and the source heap entry.
    ways: list[int] = [0] * n
    ways[0] = 1
    distances: list[int] = [10**18] * n
    distances[0] = 0
    adjacentcy_list: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    priority_queue: list[tuple[int, int]] = [(0, 0)]

    # 2. Store both directions of every road for neighbor traversal.
    def build_adjacentcy_list() -> None:
        for from_node, to_node, weight in roads:
            adjacentcy_list[from_node].append((to_node, weight))
            adjacentcy_list[to_node].append((from_node, weight))

    build_adjacentcy_list()

    while priority_queue:
        # 3. Process the smallest distance and discard superseded heap entries.
        weight, node = heapq.heappop(priority_queue)

        if weight > distances[node]:
            continue

        # 4. Positive road times make the destination's count final when popped.
        if node == n - 1:
            return ways[node] % (10**9 + 7)

        # 5. Calculate the travel time through this node to each neighbor.
        for neighbor, neighbor_weight in adjacentcy_list[node]:
            new_weight: int = weight + neighbor_weight

            if new_weight == distances[neighbor]:
                # 6. Another shortest arrival adds routes without requeueing.
                ways[neighbor] = (ways[neighbor] + ways[node]) % (10**9 + 7)
            elif new_weight < distances[neighbor]:
                # 7. A shorter arrival replaces the old count and enters the heap.
                distances[neighbor] = new_weight
                ways[neighbor] = ways[node]
                heapq.heappush(priority_queue, (new_weight, neighbor))

    # 8. Fallback if the heap is exhausted before returning the destination.
    return ways[n - 1] % (10**9 + 7)


def solve() -> None:
    n: int = 7
    roads: list[list[int]] = [
        [0, 6, 7],
        [0, 1, 2],
        [1, 2, 3],
        [1, 3, 3],
        [6, 3, 3],
        [3, 5, 1],
        [6, 5, 1],
        [2, 5, 1],
        [0, 4, 5],
        [4, 6, 2],
    ]
    expected: int = 4
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single intersection: the empty route is one way.
    n: int = 1
    roads: list[list[int]] = []
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two intersections with minimum travel time.
    n: int = 2
    roads: list[list[int]] = [[0, 1, 1]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two intersections with maximum travel time.
    n: int = 2
    roads: list[list[int]] = [[0, 1, 10**9]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Undirected road listed in reverse.
    n: int = 2
    roads: list[list[int]] = [[1, 0, 7]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    n: int = 6
    roads: list[list[int]] = [
        [0, 5, 8],
        [0, 2, 2],
        [0, 1, 1],
        [1, 3, 3],
        [1, 2, 3],
        [2, 5, 6],
        [3, 4, 2],
        [4, 5, 2],
    ]
    expected: int = 3
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: direct route is uniquely shortest.
    n: int = 4
    roads: list[list[int]] = [[0, 1, 10], [1, 2, 7], [2, 3, 4], [0, 3, 3]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct and two-road routes tie.
    n: int = 3
    roads: list[list[int]] = [[0, 1, 1], [1, 2, 1], [0, 2, 2]]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Diamond with two equal routes.
    n: int = 4
    roads: list[list[int]] = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Merge before a shared final road propagates both counts.
    n: int = 5
    roads: list[list[int]] = [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1], [3, 4, 1]]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two diamonds multiply the number of routes.
    n: int = 7
    roads: list[list[int]] = [
        [0, 1, 1],
        [0, 2, 1],
        [1, 3, 1],
        [2, 3, 1],
        [3, 4, 1],
        [3, 5, 1],
        [4, 6, 1],
        [5, 6, 1],
    ]
    expected: int = 4
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Later shorter route replaces an earlier tentative distance.
    n: int = 3
    roads: list[list[int]] = [[0, 2, 10], [0, 1, 1], [1, 2, 1]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Road order requires genuine heap ordering for correct propagation.
    n: int = 6
    roads: list[list[int]] = [
        [0, 2, 7],
        [1, 2, 1],
        [2, 3, 1],
        [0, 4, 7],
        [3, 4, 1],
        [0, 1, 4],
        [4, 5, 5],
    ]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same graph with reversed road order and endpoints.
    n: int = 6
    roads: list[list[int]] = [
        [5, 4, 5],
        [1, 0, 4],
        [4, 3, 1],
        [4, 0, 7],
        [3, 2, 1],
        [2, 1, 1],
        [2, 0, 7],
    ]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive cycle does not add shortest routes.
    n: int = 4
    roads: list[list[int]] = [[0, 1, 1], [1, 2, 1], [2, 0, 1], [2, 3, 1]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Intermediate shortest distance equals the old sentinel.
    n: int = 3
    roads: list[list[int]] = [[0, 1, 10**9], [1, 2, 1]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shortest distance exceeds one billion.
    n: int = 3
    roads: list[list[int]] = [[0, 1, 10**9], [1, 2, 10**9]]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two equal routes with total times above one billion.
    n: int = 4
    roads: list[list[int]] = [
        [0, 1, 10**9],
        [0, 2, 10**9],
        [1, 3, 10**9],
        [2, 3, 10**9],
    ]
    expected: int = 2
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum intersections and minimum roads, unit-weight chain.
    n: int = 200
    roads: list[list[int]] = [[i, i + 1, 1] for i in range(199)]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum chain length and maximum road times.
    n: int = 200
    roads: list[list[int]] = [[i, i + 1, 10**9] for i in range(199)]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum road count: all direct roads cost one.
    n: int = 200
    roads: list[list[int]] = [[u, v, 1] for u in range(200) for v in range(u + 1, 200)]
    expected: int = 1
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Every intermediate intersection gives an equal two-road route.
    n: int = 200
    roads: list[list[int]] = [[0, i, 1] for i in range(1, 199)] + [
        [i, 199, 1] for i in range(1, 199)
    ]
    expected: int = 198
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # 31 two-node layers create 2**31 shortest routes; apply modulo.
    n: int = 64
    roads: list[list[int]] = (
        [[0, 1, 1], [0, 2, 1]]
        + [
            [1 + 2 * layer + a, 1 + 2 * (layer + 1) + b, 1]
            for layer in range(30)
            for a in range(2)
            for b in range(2)
        ]
        + [[61, 63, 1], [62, 63, 1]]
    )
    expected: int = 147483634
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum complete graph: every increasing route is shortest.
    n: int = 200
    roads: list[list[int]] = [
        [u, v, v - u] for u in range(200) for v in range(u + 1, 200)
    ]
    expected: int = pow(2, 198, 10**9 + 7)
    result: int = number_of_ways_to_arrive_at_destination(n, roads)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
