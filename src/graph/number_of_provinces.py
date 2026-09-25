"""Number of Provinces

Given an undirected graph representing cities, return the number of provinces.
A province contains all cities reachable from one another through direct or
indirect connections. An isolated city forms a province by itself.

The input graph is a square adjacency matrix with n = len(graph) cities:
    - graph[i][j] == 1 means cities i and j are directly connected.
    - graph[i][j] == 0 means there is no direct connection between them.
    - Connections are undirected, so graph[i][j] == graph[j][i].
    - Each diagonal entry graph[i][i] is 1.

Use zero-based city indices in Python. The screenshot labels the same cities
starting at 1. The input is an adjacency matrix, not a list of neighbors.

Example 1 (from the screenshot):
    Input: graph = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]
    Output: 2
    Explanation: Cities 0 and 2 form one province; city 1 forms another.
    These correspond to the screenshot's groups [1, 3] and [2].

Example 2:
    Input: graph = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    Output: 3
    Explanation: Each city is isolated from every other city.

Example 3 (indirect connections):
    Input: graph = [
        [1, 1, 0],
        [1, 1, 1],
        [0, 1, 1],
    ]
    Output: 1
    Explanation: Cities 0 and 2 are connected through city 1, so all three
    cities belong to the same province.

Example 4 (five cities, one province):
    Input: graph = [
        [1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
    ]
    Output: 1
    Explanation: The connections form a chain: 0 -- 1 -- 2 -- 3 -- 4.
    All five cities can reach one another, forming one province.

Example 5 (five cities, three provinces):
    Input: graph = [
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    Output: 3
    Explanation: The provinces are {0, 2}, {1, 3}, and {4}.
    City 4 is isolated and counts as its own province.

Example 6 (five cities, five provinces):
    Input: graph = [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    Output: 5
    Explanation: There are no connections between different cities.
    Each city forms its own province: {0}, {1}, {2}, {3}, and {4}.

For n cities, the matrix has n rows and n columns, and the number of
provinces ranges from 1 to n. Matrix entries represent connections between
cities, not land cells in a grid.

Constraints (supplemented from the equivalent LeetCode 547 problem because
the screenshot does not show constraints):
    - 1 <= n <= 200
    - len(graph) == n and every row has length n.
    - Every entry is 0 or 1.
    - graph[i][i] == 1.
    - graph[i][j] == graph[j][i].

Reference: https://leetcode.com/problems/number-of-provinces/

https://www.youtube.com/watch?v=ACzkVtewUYA&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=7
"""


def number_of_provinces(graph: list[list[int]]) -> int:
    """Count provinces (connected components) in an undirected graph.

    Args:
        graph: An n x n adjacency matrix, with 1 <= n <= 200. Entries are
            0 or 1, the matrix is symmetric, and diagonal entries are 1.
            graph[i][j] == 1 represents a direct connection between cities
            i and j. This is not a grid of land and water cells.

    Returns:
        The number of groups of directly or indirectly connected cities.
        Each isolated city counts as one province. The input is not modified.
        The function assumes the input satisfies the problem's constraints.

    Approach:
        Depth-First Search (DFS) for connected components.
        1. Determine the number of cities from len(graph). Create one visited
           flag per city and initialize province_count to zero. Visitation
           tracks cities, not individual matrix cells.
        2. Define visit_province(city) to mark a city as visited immediately.
           Marking before exploring prevents cycles and self-connections from
           repeatedly visiting the same city. Keep the mark after returning:
           this city has already been assigned to a province.
        3. Scan the city's entire matrix row. For each directly connected city
           that is not visited, recursively visit it. Following these links
           also reaches indirectly connected cities. When the initial DFS
           finishes, every city in that province has been marked.
        4. Loop over all cities. Whenever a city is still unvisited, increment
           province_count and start DFS there. It must belong to a new
           province: if it belonged to an earlier one, that DFS would already
           have reached it. Skip visited cities so each province is counted
           once. An isolated city marks only itself and still adds one.
        5. Return province_count after every city has been visited.

        Example:
            graph = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
            - Start with visited = [False, False, False], count = 0.
            - City 0 is unvisited: count becomes 1. DFS marks city 0, follows
              its connection to city 2, and marks city 2. The connection back
              to city 0 is skipped because city 0 is already visited.
              visited is now [True, False, True].
            - City 1 is unvisited: count becomes 2. It has no connection to
              another city, so DFS marks only city 1.
            - City 2 is already visited, so skip it. Return 2.

        A matrix row or adjacency-list key represents a city, not a province.
        For example, the chain 0 -- 1 -- 2 contains three cities but only one
        province. DFS discovers that grouping by following connections.

    Time Complexity:
        O(n**2), where n is the number of cities. Each city is visited exactly
        once, and each visit scans all n entries in that city's matrix row.
        Therefore the row scans perform n * n checks in total. The outer loop
        adds O(n) work, leaving O(n**2) overall. Recursive calls do not multiply
        this by another n: they account for the same n total city visits.
        No adjacency-list conversion is performed.

    Space Complexity:
        O(n) auxiliary space, excluding the input matrix. visited stores n
        boolean flags. The recursive call stack can contain up to n calls,
        for example when DFS follows a chain through all cities. Counts and
        loop indices use constant space per call. The visited list and stack
        together require O(n) + O(n) = O(n) space. The return value is one
        integer; the existing O(n**2) input matrix is not copied.
    """
    # 1. Track visitation per city and initialize the province count.
    city_count: int = len(graph)
    visited: list[bool] = [False] * city_count
    province_count: int = 0

    def visit_province(city: int) -> None:
        # 2. Mark before exploring to prevent revisiting cycles or self-links.
        visited[city] = True

        # 3. Follow direct connections to reach every city in this province.
        for next_city in range(city_count):
            if graph[city][next_city] == 1 and not visited[next_city]:
                visit_province(city=next_city)

    # 4. Each unvisited starting city identifies one new province.
    for city in range(city_count):
        if not visited[city]:
            province_count += 1
            visit_province(city=city)

    # 5. All cities have been grouped; return the number of provinces.
    return province_count


def solve() -> None:
    graph: list[list[int]] = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ]
    expected: int = 2
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum size: one city.
    graph: list[list[int]] = [[1]]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two isolated cities.
    graph: list[list[int]] = [[1, 0], [0, 1]]
    expected: int = 2
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two connected cities.
    graph: list[list[int]] = [[1, 1], [1, 1]]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Screenshot: a connection between nonadjacent city indices.
    graph: list[list[int]] = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    expected: int = 2
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Three isolated cities.
    graph: list[list[int]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    expected: int = 3
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Indirect connection: a chain of five cities.
    graph: list[list[int]] = [
        [int(abs(row - col) <= 1) for col in range(5)] for row in range(5)
    ]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Five cities in three provinces: {0, 2}, {1, 3}, {4}.
    graph: list[list[int]] = [
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    expected: int = 3
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Five isolated cities.
    graph: list[list[int]] = [[int(row == col) for col in range(5)] for row in range(5)]
    expected: int = 5
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Fully connected graph: multiple routes to visited cities.
    graph: list[list[int]] = [[1] * 5 for _ in range(5)]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star graph with the center at the final city.
    graph: list[list[int]] = [
        [int(row == col or row == 4 or col == 4) for col in range(5)]
        for row in range(5)
    ]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated cities before and after a middle province.
    graph: list[list[int]] = [
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    expected: int = 3
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two separate cycles.
    graph: list[list[int]] = [
        [int(row // 3 == col // 3) for col in range(6)] for row in range(6)
    ]
    expected: int = 2
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size: all 200 cities isolated.
    graph: list[list[int]] = [
        [int(row == col) for col in range(200)] for row in range(200)
    ]
    expected: int = 200
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size: all cities directly connected.
    graph: list[list[int]] = [[1] * 200 for _ in range(200)]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size: a chain requires following indirect connections.
    graph: list[list[int]] = [
        [int(abs(row - col) <= 1) for col in range(200)] for row in range(200)
    ]
    expected: int = 1
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum size: 100 separate pairs.
    graph: list[list[int]] = [
        [int(row // 2 == col // 2) for col in range(200)] for row in range(200)
    ]
    expected: int = 100
    result: int = number_of_provinces(graph)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
