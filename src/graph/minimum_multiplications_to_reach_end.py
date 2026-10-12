"""857. Minimum Multiplications to Reach End

Given start, end, and an array arr of n numbers, at each step multiply the
current value by any number in arr and take the result modulo 100000:

    next_value = (current_value * multiplier) % 100000

Find the minimum number of steps needed to reach end starting from start.
If reaching end is impossible, return -1. Array elements may be reused
across steps. Here, n = len(arr).

Example 1:
    Input: arr = [2, 5, 7], start = 3, end = 30
    Output: 2
    Explanation:
        Step 1: (3 * 2) % 100000 = 6.
        Step 2: (6 * 5) % 100000 = 30.
        The minimum number of multiplications is 2. The end number can be
        treated as the destination node of a graph.

Example 2:
    Input: arr = [3, 4, 65], start = 7, end = 66175
    Output: 4
    Explanation:
        Step 1: (7 * 3) % 100000 = 21.
        Step 2: (21 * 3) % 100000 = 63.
        Step 3: (63 * 65) % 100000 = 4095.
        Step 4: (4095 * 65) % 100000 = 266175 % 100000 = 66175.
        The minimum number of multiplications is 4. The end number can be
        treated as the destination node of a graph.

Now Your Turn:
    Input: arr = [3, 4, 65], start = 7, end = 21
    Pick the correct output:
        A. 0
        B. 1
        C. 3
        D. 2

Constraints:
    - 1 <= n <= 10**4.
    - 1 <= arr[i] <= 10**4.
    - 1 <= start, end < 10**5.

https://www.youtube.com/watch?v=_BvEJ3VIDWw&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=39

"""

from collections import deque


def minimum_multiplications_to_reach_end(arr: list[int], start: int, end: int) -> int:
    """Return the fewest multiplications modulo 100000 needed to reach end.

    Args:
        arr: Between 1 and 10**4 integer multipliers, each from 1 to 10**4.
            Multipliers may be reused, and duplicate values are allowed.
        start: Initial integer, with 1 <= start < 100000.
        end: Target integer, with 1 <= end < 100000.

    Returns:
        The minimum number of multiplications, or -1 if end is unreachable.
        Returns 0 when start equals end. The input array is not modified.

    Approach:
        Breadth-First Search (BFS) on an implicit, unweighted directed graph.
        Each remainder from 0 through 99999 is a node. Multiplying by an
        allowed number and taking modulo 100000 creates an edge costing
        one step. Generate these edges as needed instead of storing them.

        1. Build a set of unique multipliers so duplicate array entries do
           not cause repeated checks of the same transition.
        2. Allocate a distance array for all 100000 possible remainders,
           including 0 and 99999. Initialize distances to 10**9, an
           unreachable sentinel larger than any shortest path. Mark start
           with distance 0 and enqueue (0, start). Marking start prevents
           an identity multiplication or cycle from enqueueing it again.
        3. Pop the next (step count, remainder) from the FIFO queue. If it
           equals end, return the count. Every transition costs one step,
           so BFS processes nodes in nondecreasing distance and the first
           discovery of a node gives its shortest distance.
        4. For each unique multiplier, calculate (node * number) % 100000
           and a candidate distance of step + 1. Consider every remainder:
           values larger than end can wrap around to reach it later. Zero
           must also be a valid internal state, even though endpoints are
           positive under the constraints.
        5. If the candidate improves the next node's recorded distance,
           record it before enqueueing the node. Since first discovery is
           shortest, each node is enqueued at most once. Equal or longer
           routes, self-loops, and cycles cannot cause repeated visits.
        6. If the queue empties without reaching end, all reachable states
           have been explored, so return -1.

        Example: with arr = [2], start = 40000, and end = 20000, the route
        is 40000 -> 80000 -> 60000 -> 20000, requiring three multiplications.
        Restricting intermediate values to at most end would miss this path.

    Time Complexity:
        O(n + M * U), where n = len(arr), U is the number of unique
        multipliers, and M = 100000. Constructing the set takes O(n) expected
        time, and initializing distances takes O(M). At most M nodes are
        processed, each checking U multipliers in constant time. Since
        U >= 1, O(n + M + M * U) simplifies to O(n + M * U).
        Early termination can reduce traversal work, but the set and full
        distance array are still initialized even when start equals end.

    Space Complexity:
        O(M + U) extra space. The distance array stores M entries, the queue
        holds at most M node states, and the multiplier set stores U values.
        Edges are generated on demand; no adjacency list or input copy is
        stored beyond the set of unique multipliers.
    """
    # 1. Remove duplicate multipliers without changing the input array.
    unique_multipliers = set(arr)
    # 2. Initialize all remainder distances and mark the source before queueing.
    steps: list[int] = [10**9] * 100000
    queue: deque[tuple[int, int]] = deque([(0, start)])
    steps[start] = 0
    while queue:
        # 3. Process the next BFS state; reaching the target gives its minimum.
        step, node = queue.popleft()

        if node == end:
            return step

        # 4. Generate every next remainder, including values above the target.
        for number in unique_multipliers:
            next_node: int = (node * number) % 100000
            next_step: int = step + 1

            # 5. Record first discovery before enqueueing to prevent revisits.
            if next_step < steps[next_node]:
                steps[next_node] = next_step
                queue.append((next_step, next_node))

    # 6. Exhausting all reachable states means the target cannot be reached.
    return -1


def solve() -> None:
    arr: list[int] = [2, 5, 7]
    start: int = 3
    end: int = 30
    expected: int = 2
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum array size and values; start already equals end.
    arr: list[int] = [1]
    start: int = 1
    end: int = 1
    expected: int = 0
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum endpoint with no multiplication needed.
    arr: list[int] = [2]
    start: int = 99999
    end: int = 99999
    expected: int = 0
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example with repeated multipliers and wraparound.
    arr: list[int] = [3, 4, 65]
    start: int = 7
    end: int = 66175
    expected: int = 4
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: one multiplication.
    arr: list[int] = [3, 4, 65]
    start: int = 7
    end: int = 21
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only the identity multiplier; destination is unreachable.
    arr: list[int] = [1]
    start: int = 1
    end: int = 2
    expected: int = -1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated use of one multiplier.
    arr: list[int] = [2]
    start: int = 1
    end: int = 32
    expected: int = 5
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct route beats a route using several multiplications.
    arr: list[int] = [2, 4, 8]
    start: int = 1
    end: int = 8
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Useful multiplier at the beginning.
    arr: list[int] = [7, 1, 1]
    start: int = 3
    end: int = 21
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Useful multiplier in the middle.
    arr: list[int] = [1, 7, 1]
    start: int = 3
    end: int = 21
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Useful multiplier at the end.
    arr: list[int] = [1, 1, 7]
    start: int = 3
    end: int = 21
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate multipliers do not change the shortest distance.
    arr: list[int] = [2, 2, 2]
    start: int = 3
    end: int = 12
    expected: int = 2
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identity self-loop alongside a useful multiplier.
    arr: list[int] = [1, 2]
    start: int = 3
    end: int = 12
    expected: int = 2
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum multiplier in a single step.
    arr: list[int] = [10000]
    start: int = 1
    end: int = 10000
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum starting value and multiplier wrap in one step.
    arr: list[int] = [10000]
    start: int = 99999
    end: int = 90000
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum destination is reached in one step.
    arr: list[int] = [3]
    start: int = 33333
    end: int = 99999
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum destination is unreachable with identity multiplication.
    arr: list[int] = [1]
    start: int = 1
    end: int = 99999
    expected: int = -1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Intermediate values exceed the destination before modulo wraparound.
    arr: list[int] = [2]
    start: int = 40000
    end: int = 20000
    expected: int = 3
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum destination reached after wrapping.
    arr: list[int] = [9999]
    start: int = 9999
    end: int = 1
    expected: int = 9
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero is reachable internally but cannot lead to a positive target.
    arr: list[int] = [10000]
    start: int = 10
    end: int = 1
    expected: int = -1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # A zero self-loop cannot reach a positive destination.
    arr: list[int] = [2]
    start: int = 50000
    end: int = 1
    expected: int = -1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array length with identical minimum multipliers.
    arr: list[int] = [1] * 10000
    start: int = 1
    end: int = 2
    expected: int = -1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array length with identical maximum multipliers.
    arr: list[int] = [10000] * 10000
    start: int = 1
    end: int = 10000
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array length; useful multiplier is last.
    arr: list[int] = [1] * 9999 + [2]
    start: int = 1
    end: int = 2
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum array length spanning every allowed multiplier.
    arr: list[int] = list(range(1, 10001))
    start: int = 1
    end: int = 10000
    expected: int = 1
    result: int = minimum_multiplications_to_reach_end(arr, start, end)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
