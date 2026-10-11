"""71. Cheapest Flight Within K Stops

There are n cities connected by m directed flights. Each entry in flights
has the form [from_city, to_city, price], indicating a flight from from_city
to to_city with the given cost. Here, m = len(flights).

Given src, dst, and k, return the cheapest price from src to dst with at
most k stops. If no such route exists, return -1.

Stops are intermediate cities between source and destination. A route with
at most k stops uses at most k + 1 flights. With k = 0, only a direct flight
can connect two distinct cities.

Example 1:
    Input:
        n = 4
        flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100],
                   [1, 3, 600], [2, 3, 200]]
        src = 0, dst = 3, k = 1
    Output: 700
    Explanation:
        The optimal valid route is 0 -> 1 -> 3, with one stop and cost
        100 + 600 = 700. The cheaper route 0 -> 1 -> 2 -> 3 is invalid
        because it uses two stops.

Example 2:
    Input:
        n = 3
        flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
        src = 0, dst = 2, k = 1
    Output: 200
    Explanation:
        The optimal route is 0 -> 1 -> 2, with one stop and cost
        100 + 100 = 200.

Now Your Turn:
    Input:
        n = 3
        flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
        src = 0, dst = 2, k = 0
    Pick the correct output:
        A. 600
        B. 700
        C. 200
        D. 500

Constraints:
    - 1 <= n <= 100.
    - 0 <= len(flights) <= n * (n - 1) / 2.
    - Each flight entry has exactly three elements.
    - 0 <= from_city, to_city < n.
    - from_city != to_city.
    - 1 <= price <= 10**4.
    - There are no multiple flights between the two cities.
    - 0 <= src, dst, k < n.

Discussion Questions:
    - Why use a priority queue instead of a simple queue (BFS)?
    - How does this compare to the standard shortest path problem?
    - What if additional constraints were introduced, such as layover time
      between flights?
    - What if flights had negative costs?
"""

from collections import defaultdict, deque


def cheapest_flight_within_k_stops(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """Return the cheapest directed route using at most k intermediate stops.

    Args:
        n: Number of cities, labeled 0 through n - 1, with 1 <= n <= 100.
        flights: Entries [from_city, to_city, price], with valid distinct
            endpoints and integer prices from 1 to 10**4. There are no
            duplicate flights and at most n * (n - 1) / 2 entries.
        src: Starting city, with 0 <= src < n.
        dst: Destination city, with 0 <= dst < n.
        k: Maximum intermediate stops, with 0 <= k < n. This permits
            at most k + 1 flights.

    Returns:
        The minimum total price within the flight limit, or -1 if no valid
        route exists. Returns 0 when src equals dst, even with no flights.
        The input flights are not modified.

    Approach:
        Breadth-First Search (BFS) by flight count with cost relaxation.
        Unlike ordinary unweighted BFS, record cheaper routes and allow a
        city to be queued again. The FIFO queue orders routes by flights
        used, not by price, so the first arrival need not be cheapest.

        1. Initialize each city's best price to -1 (unreachable). Build a
           directed adjacency list mapping each departure city to its
           (destination, price) pairs using the nested helper.
        2. Set the source price to 0 and enqueue (0, src, 0). Each entry
           stores (route cost, current city, flights used).
        3. Pop the next route. If it has already used k + 1 flights, skip
           expansion: taking another flight would exceed the allowance.
           Its cost was already recorded when the entry was enqueued.
        4. For each outgoing flight, add its price to this entry's cost
           and increment the number of flights used.
        5. If the neighbor has not been reached, or this candidate is
           cheaper, and the candidate uses at most k + 1 flights, record
           its price and enqueue the complete route state.
        6. After all queued routes are processed, return the destination's
           recorded price. It remains -1 if no allowed route reaches it.

        Why the queue order matters:
            FIFO processing generates candidates in nondecreasing flight
            count. When a candidate fails to improve a recorded price,
            that recorded route uses no more flights than the candidate,
            so discarding the candidate is safe.

            However, an already queued route may later become more expensive
            than the recorded price while still using fewer flights. Keep
            processing its stored cost: the extra remaining flight allowance
            may be necessary. Do not add a cost > distances[node] skip or
            replace the stored cost with distances[node]. Do not return on
            the first arrival at the destination, since prices vary.

    Time Complexity:
        Let m = len(flights), P be the total number of popped queue entries,
        and D be the maximum number of outgoing flights from any city.
        Time is O(n + m + P * (D + 1)): initialization costs O(n + m), and
        each entry takes O(1) queue work plus at most D neighbor checks.
        Multiple improvements can queue the same city at the same flight
        count, so this implementation does not guarantee O((k + 1) * m).

        A loose bound in terms of input limits is obtained with W = 10**4:
        every queued cost is an integer at most (k + 1) * W, and each new
        entry for a city strictly lowers its recorded price after its first
        discovery. Thus P <= 1 + n * (k + 1) * W. This bound is conservative;
        actual work depends on the number of successful improvements.

    Space Complexity:
        O(n + m + H) extra space, where H is the largest queue size. The
        adjacency list stores m flights, distances stores n prices, and
        the queue stores H route states, potentially several per city.
        H <= P, giving a loose bound of O(n + m + n * (k + 1) * W).
    """
    # 1. Initialize best prices and group directed flights by departure city.
    distances: list[int] = [-1] * n
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)

    def build_adjacency_list() -> None:
        for from_node, to_node, cost in flights:
            adj[from_node].append((to_node, cost))

    build_adjacency_list()

    # 2. Begin at the chosen source with zero cost and zero flights used.
    queue: deque[tuple[int, int, int]] = deque([(0, src, 0)])
    distances[src] = 0

    while queue:
        # 3. Process routes by flight count; stop expanding at the allowance.
        cost, node, step = queue.popleft()

        if step == k + 1:
            continue

        # 4. Extend this entry's route by one flight using its stored cost.
        for neighbor, weight in adj[node]:
            next_step: int = step + 1
            next_cost: int = cost + weight

            # 5. Record and queue only cheaper routes within the flight limit.
            if (
                distances[neighbor] == -1 or next_cost < distances[neighbor]
            ) and next_step <= k + 1:
                distances[neighbor] = next_cost
                queue.append((next_cost, neighbor, next_step))

    # 6. Return the cheapest allowed price, or -1 if still unreachable.
    return distances[dst]


def solve() -> None:
    n: int = 4
    flights: list[list[int]] = [
        [0, 1, 100],
        [1, 2, 100],
        [2, 0, 100],
        [1, 3, 600],
        [2, 3, 200],
    ]
    src: int = 0
    dst: int = 3
    k: int = 1
    expected: int = 700
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum city count, no flights, source equals destination.
    n: int = 1
    flights: list[list[int]] = []
    src: int = 0
    dst: int = 0
    k: int = 0
    expected: int = 0
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Empty graph with distinct endpoints.
    n: int = 2
    flights: list[list[int]] = []
    src: int = 0
    dst: int = 1
    k: int = 0
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Nonzero source equals destination with no flights.
    n: int = 3
    flights: list[list[int]] = []
    src: int = 2
    dst: int = 2
    k: int = 2
    expected: int = 0
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum flight price with zero stops.
    n: int = 2
    flights: list[list[int]] = [[0, 1, 1]]
    src: int = 0
    dst: int = 1
    k: int = 0
    expected: int = 1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum flight price and nonzero source.
    n: int = 2
    flights: list[list[int]] = [[1, 0, 10000]]
    src: int = 1
    dst: int = 0
    k: int = 0
    expected: int = 10000
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Directed flights cannot be traversed backwards.
    n: int = 2
    flights: list[list[int]] = [[0, 1, 100]]
    src: int = 1
    dst: int = 0
    k: int = 1
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example: one stop is allowed.
    n: int = 3
    flights: list[list[int]] = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    src: int = 0
    dst: int = 2
    k: int = 1
    expected: int = 200
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: zero stops requires a direct flight.
    n: int = 3
    flights: list[list[int]] = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    src: int = 0
    dst: int = 2
    k: int = 0
    expected: int = 500
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Destination reachable only beyond the stop limit.
    n: int = 3
    flights: list[list[int]] = [[0, 1, 100], [1, 2, 100]]
    src: int = 0
    dst: int = 2
    k: int = 0
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Route uses exactly k stops.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    src: int = 0
    dst: int = 3
    k: int = 2
    expected: int = 9
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Route exceeds the allowance by one flight.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    src: int = 0
    dst: int = 3
    k: int = 1
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A direct flight is cheaper than the available connection.
    n: int = 3
    flights: list[list[int]] = [[0, 1, 100], [1, 2, 100], [0, 2, 50]]
    src: int = 0
    dst: int = 2
    k: int = 2
    expected: int = 50
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # More expensive intermediate route uses fewer flights and is necessary.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 3, 1]]
    src: int = 0
    dst: int = 3
    k: int = 1
    expected: int = 6
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same graph in reverse input order.
    n: int = 4
    flights: list[list[int]] = [[2, 3, 1], [0, 2, 5], [1, 2, 1], [0, 1, 1]]
    src: int = 0
    dst: int = 3
    k: int = 1
    expected: int = 6
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Equal-cost routes merge before reaching the destination.
    n: int = 5
    flights: list[list[int]] = [[0, 1, 2], [0, 2, 2], [1, 3, 3], [2, 3, 3], [3, 4, 4]]
    src: int = 0
    dst: int = 4
    k: int = 2
    expected: int = 9
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cheaper equal-length route improves a queued city.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 8], [0, 2, 1], [1, 3, 2], [2, 3, 3]]
    src: int = 0
    dst: int = 3
    k: int = 1
    expected: int = 4
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Positive cycle does not improve the route.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 2], [1, 2, 2], [2, 0, 2], [2, 3, 2]]
    src: int = 0
    dst: int = 3
    k: int = 3
    expected: int = 6
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Source equals destination despite an available cycle.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 2], [1, 2, 2], [2, 0, 2]]
    src: int = 1
    dst: int = 1
    k: int = 3
    expected: int = 0
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected destination while reachable cities contain a cycle.
    n: int = 4
    flights: list[list[int]] = [[0, 1, 1], [1, 2, 1], [2, 0, 1]]
    src: int = 0
    dst: int = 3
    k: int = 3
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Source is an interior city and destination is city zero.
    n: int = 5
    flights: list[list[int]] = [[2, 4, 3], [4, 0, 4], [2, 0, 20]]
    src: int = 2
    dst: int = 0
    k: int = 1
    expected: int = 7
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Destination is an interior city.
    n: int = 5
    flights: list[list[int]] = [[4, 3, 2], [3, 2, 3], [2, 0, 1]]
    src: int = 4
    dst: int = 2
    k: int = 1
    expected: int = 5
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum cities and stops with no flights.
    n: int = 100
    flights: list[list[int]] = []
    src: int = 99
    dst: int = 0
    k: int = 99
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum chain length and prices; exactly enough stops.
    n: int = 100
    flights: list[list[int]] = [[i, i + 1, 10000] for i in range(99)]
    src: int = 0
    dst: int = 99
    k: int = 98
    expected: int = 990000
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum chain with one fewer allowed stop.
    n: int = 100
    flights: list[list[int]] = [[i, i + 1, 10000] for i in range(99)]
    src: int = 0
    dst: int = 99
    k: int = 97
    expected: int = -1
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum stop allowance with minimum-price chain.
    n: int = 100
    flights: list[list[int]] = [[i, i + 1, 1] for i in range(99)]
    src: int = 0
    dst: int = 99
    k: int = 99
    expected: int = 99
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum source index, descending chain to city zero.
    n: int = 100
    flights: list[list[int]] = [[i, i - 1, 1] for i in range(99, 0, -1)]
    src: int = 99
    dst: int = 0
    k: int = 99
    expected: int = 99
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum flight count: 4950 distinct directed flights, equal prices.
    n: int = 100
    flights: list[list[int]] = [
        [u, v, 10000] for u in range(100) for v in range(u + 1, 100)
    ]
    src: int = 0
    dst: int = 99
    k: int = 99
    expected: int = 10000
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum flight count with a cheap chain beating direct flights.
    n: int = 100
    flights: list[list[int]] = [
        [u, v, 1 if v == u + 1 else 10000]
        for u in range(100)
        for v in range(u + 1, 100)
    ]
    src: int = 0
    dst: int = 99
    k: int = 98
    expected: int = 99
    result: int = cheapest_flight_within_k_stops(n, flights, src, dst, k)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
