"""948. Articulation Point in Graph

Given an undirected graph with V vertices and adjacency list adj, find all
vertices whose removal, together with their incident edges, would increase
the number of connected components in the graph. Such vertices are called
articulation points.

The graph may initially be disconnected. Vertices are numbered from 0 to
V - 1, and self-loops may be present.

Return the articulation points in ascending order. If there are none,
return [-1].

Example 1:
    Input: V = 7,
           adj = [[1, 2, 3], [0], [0, 3, 4, 5], [2, 0], [2, 6], [2, 6], [4, 5]]
    Output: [0, 2]
    Explanation: Removing vertex 0 or vertex 2 increases the number of
    connected components.

Example 2:
    Input: V = 5, adj = [[1], [0, 4], [3, 4], [2, 4], [1, 2, 3]]
    Output: [1, 4]
    Explanation: Removing either vertex 1 or vertex 4 breaks the graph into
    multiple connected components.

Practice question:
    Input: V = 3, adj = [[1, 2], [0, 2], [0, 1]]
    Choices: [1, 2], [1], [2, 3], [-1]

Constraints:
    - 1 <= V <= 10^4
    - 1 <= E <= 10^4, where E is the number of undirected edges.
    - Vertex IDs range from 0 to V - 1.
    - adj contains V neighbor lists.
    - The graph may be disconnected and may contain self-loops.

https://www.youtube.com/watch?v=64KK9K4RpKE

https://www.youtube.com/watch?v=j1QDfU21iZk&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=56

"""


def articulation_points_in_graph_brute_force(
    vertices: int, adjacency_list: list[list[int]]
) -> list[int]:
    """Find articulation points by simulating each possible vertex removal.

    Args:
        vertices: Number V of vertices, with IDs from 0 to V - 1.
        adjacency_list: V neighbor lists describing an undirected graph.
            The graph may be disconnected and may contain self-loops.
            E denotes the number of undirected edges.

    Returns:
        Articulation-point IDs in ascending order, or [-1] if none exist.
        Removing an articulation point increases the number of connected
        components relative to the ORIGINAL graph. The input adjacency list
        is never modified: removal is simulated by skipping a vertex.

    Approach:
        Depth-First Search (DFS) with brute-force vertex removal.

        1. Define DFS to explore one component while ignoring removed_node.
           Mark vertices visited on entry. Skip neighbors that are removed
           or already visited. The entry guard also prevents exploration if
           DFS is called directly on the removed vertex. Passing -1 means
           remove nothing, since valid vertex IDs are nonnegative.
        2. Count original_components before trying any removal. Loop over all
           vertices, starting DFS only from unvisited vertices. Each new DFS
           visits one whole component, so increment the count once per start,
           not once per visited vertex. Keep visited shared across these calls.
        3. Try every vertex as removed_node, in ascending ID order. Clear
           visited and reset components for EACH candidate. Previous trials
           must not affect which vertices are explored in this trial.
        4. Count components with that candidate excluded. The outer loop skips
           both the removed vertex and visited vertices, using OR. DFS also
           skips edges into the removed vertex. Both checks matter: do not
           start there, and do not reach it through another vertex. Increment
           components once for each DFS started from an unvisited survivor.
        5. Append the candidate only if components > original_components.
           This tests whether removal split a group, rather than whether the
           remaining graph merely happens to be disconnected. Iterating IDs
           in order already produces sorted output without an extra sort.
        6. Return the collected IDs, or [-1] if the list is empty. The existing
           return also checks whether every vertex was collected; this is
           redundant for a correctly counted undirected graph, which cannot
           have every vertex be an articulation point.

        Why count original components?
            The input may already have several components. An articulation
            point must INCREASE that number. Checking components > 1 assumes
            the original graph was connected and fails on disconnected inputs.

            Original graph:
                0 --- 1 --- 2       3 --- 4 --- 5
                original_components = 2

            Remove endpoint 0:
                      1 --- 2       3 --- 4 --- 5
                components = 2; 2 > 2 is false. Nothing split.
                Checking 2 > 1 would incorrectly mark vertex 0.

            Remove middle vertex 1 instead:
                0           2       3 --- 4 --- 5
                components = 3; 3 > 2 is true. Vertex 1 is an articulation point.

            Removing 4 likewise increases the count to 3. The result is [1, 4].
            Removing 2, 3, or 5 leaves 2 components, so they are not included.
            No vertex is physically deleted; each trial starts from the same
            adjacency list with a fresh visited set state.

        Edge cases:
            - Removing an isolated vertex reduces the component count; it is
              not an articulation point.
            - Removing the sole vertex leaves zero components, so return [-1].
            - Self-loops do not cause infinite recursion because the current
              vertex is marked visited before its neighbors are explored.
            - A connected graph has original_components = 1, but that value
              must be measured rather than assumed for this problem.

    Time Complexity:
        O(V * (V + E)) expected time, assuming average O(1) set operations.

        V is the number of vertices; E is the number of undirected edges.
        In the two-path example above, V = 6 and E = 4. The adjacency lists
        contain 8 neighbor entries because each undirected edge is stored
        at both endpoints.

        1. The original-component count scans V vertices and explores each
           vertex once. Across those DFS calls, at most 2E neighbor entries
           are examined. This costs O(V + E).
        2. For ONE removal candidate, clearing visited costs at most O(V),
           the outer start-node loop checks V vertices, and DFS explores each
           surviving vertex once. At most 2E neighbor entries are examined,
           including entries skipped because they lead to the removed node.
           The total per candidate is O(V + E).
        3. There are V candidates. Each performs a separate full component
           count, so multiply: V * O(V + E) = O(V * (V + E)).

        Sequential baseline work adds to the repeated work:
            O(V + E) + O(V * (V + E)) = O(V * (V + E)).
        Unlike one DFS covering all components, these trials deliberately reset
        visited and explore the graph again. For V = 6 there is one baseline
        count plus six removal trials. At V = 10000 this brute-force approach
        may be slow; it does not provide the O(V + E) low-link optimization.

    Space Complexity:
        O(V) additional space, excluding the supplied adjacency list.

        - visited: at most V vertex IDs -> O(V).
        - Recursive DFS stack: at most V nested calls on a path -> O(V).
        - articulation_points: at most V IDs -> O(V).
        - Counters, loop variables, and removed_node: O(1) outside the call stack.

        For the six-vertex example, visited holds at most six IDs at once.
        It is cleared between trials, not saved as six separate sets. Likewise,
        one trial's recursive calls finish before the next trial starts.
        Repeating DFS increases time, but does not multiply peak memory by V.
        All DFS calls share the adjacency list and visited set; no graph copy
        is made for a removal.

        Add peak live storage:
            O(V + V + V + 1) = O(V).
        Excluding the returned list still gives O(V) auxiliary space. Including
        the existing input graph in total storage would give O(V + E).

    Limitation:
        DFS is recursive and can exceed Python's recursion limit on deep graphs
        allowed by V <= 10000. Shallow large-input tests do not address that
        limitation. This function does not change the recursion limit.

    Interview Summary:
        I count the original connected components, then skip each vertex in
        turn and count again with DFS. A vertex is an articulation point only
        if its removal increases that original count. This takes O(V * (V + E))
        expected time and O(V) additional space.
    """
    visited: set[int] = set()
    articulation_points: list[int] = []

    # Step 1: Explore one component while ignoring the selected vertex.
    def dfs(node: int, removed_node: int) -> None:

        if node == removed_node:
            return

        visited.add(node)

        for neighbor in adjacency_list[node]:
            if neighbor == removed_node or neighbor in visited:
                continue

            dfs(node=neighbor, removed_node=removed_node)

    # Step 2: Establish the baseline; disconnected input may already have >1.
    original_components: int = 0
    for node in range(vertices):
        if node not in visited:
            original_components += 1
            dfs(node=node, removed_node=-1)

    # Step 3: Reset traversal state for each independent removal trial.
    for removed_node in range(vertices):
        visited.clear()
        components: int = 0
        # Step 4: Count surviving components, skipping removed OR visited nodes.
        for start_node in range(vertices):
            if start_node == removed_node or start_node in visited:
                continue
            components += 1
            dfs(node=start_node, removed_node=removed_node)

        # Step 5: Only an INCREASE from the original count marks articulation.
        if components > original_components:
            articulation_points.append(removed_node)

    # Step 6: Return ascending IDs or the required no-articulation sentinel.
    return (
        [-1]
        if len(articulation_points) == 0 or len(articulation_points) == vertices
        else articulation_points
    )


def articulation_points_in_graph_tarjans(
    vertices: int, adjacency_list: list[list[int]]
) -> list[int]:
    r"""Return articulation points in ascending order, or [-1] if none exist.

    Args:
        vertices: Number V of vertices, identified by integers 0 through V - 1.
        adjacency_list: V neighbor lists for an undirected graph with E edges.
            The graph may be disconnected and may contain self-loops. Neighbor
            IDs must be valid. Each ordinary undirected edge appears at both
            endpoints. The input lists are not modified.

    Returns:
        Each vertex whose removal increases the number of connected components,
        exactly once and in ascending order. Returns [-1] when none qualify.
        An isolated vertex, including one with only self-loops, is not an
        articulation point.

    Approach:
        Tarjan's Articulation-Point Algorithm using DFS discovery and low values.

        1. Allocate parent, discovery, low, and boolean articulation arrays.
           Discovery -1 means unvisited; parent -1 identifies a DFS root.
           A shared discovery_time counter supplies entry timestamps.
        2. Start DFS from every unvisited vertex to cover all components. On
           entry, assign discovery[node] = low[node] = discovery_time, then
           increment the counter. Discovery stays fixed; low may decrease.
           Initialize children = 0 locally for each recursive call. Each node
           counts its own direct DFS children, not all descendants. A child's
           local counter does not reset or modify its parent's counter.
        3. For an unvisited neighbor, count one direct DFS child, assign its
           parent BEFORE recursion, and explore it.
           After it returns, propagate low[neighbor] into low[node] using min.
           The parent can travel through its child to use the earlier connection
           discovered in that child's subtree. This information must travel
           upward so ancestors can correctly judge whether their removal splits
           a child subtree from the rest of the component.
        4. After each child returns, mark a DFS ROOT if children > 1.
           This check runs inside the unvisited-child branch, not after the
           entire neighbor loop. Once the second child has been explored,
           the root already qualifies; later children cannot undo that fact.
           Repeatedly setting its boolean flag to True is harmless.
           A root has no parent side to separate from one child subtree.
           Two DFS children form separate branches after its removal: if they
           had an edge connecting them, DFS would have discovered them within
           the same child subtree. Count DFS children, not adjacency-list size.
        5. For each such child, mark a NON-ROOT node when
           low[child] >= discovery[node]. That child's subtree cannot reach
           an ancestor of node without passing through node. One dependent
           child is sufficient. Equality also qualifies: an alternative edge
           reaching node itself does not help when node is removed. Check
           children individually; another child's escape route cannot rescue
           this subtree after their common parent is removed.
        6. In the elif branch, for an already visited non-parent neighbor,
           update low[node] using
           discovery[neighbor], not low[neighbor]. This records the direct
           connection to a discovered vertex. A self-loop cannot lower low
           because it points to the current node's own discovery time.
           A visited parent matches neither branch and is ignored implicitly;
           no separate parent-edge continue statement is needed.
        7. Scan vertex IDs from 0 to V - 1 and collect the marked ones. Boolean
           marks prevent duplicates when multiple children identify the same
           vertex. The scan gives ascending output without sorting. Return
           [-1] if the collected list is empty.

        Meaning of low:
            In the usual graph without parallel edges, low[u] is the earliest
            discovery time reachable by descending zero or more DFS tree edges
            in u's subtree and then taking at most one back edge. It represents
            a subtree's connection to earlier vertices, not a vertex ID.
            A visited descendant's later discovery time cannot reduce low[u].

        Visual example with seven vertices:
            adjacency_list = [
                [1, 2, 3], [0], [0, 3, 4, 5], [2, 0], [2, 6], [2, 6], [4, 5]
            ]

                  1
                  |
                  0
                 / \
                3---2
                   / \
                  4   5
                   \ /
                    6

            With the listed neighbor order, the DFS tree is:
                  0
                 / \
                1   2
                   / \
                  3   4
                      |
                      6
                      |
                      5

            Non-tree connections: 3--0 and 5--2.
            Vertex:       0  1  2  3  4  5  6
            Discovery:    0  1  2  3  4  6  5
            Final low:    0  1  0  0  2  2  2

        Vertex 5 sees 2, so low[5] becomes discovery[2] = 2. Vertex 6 inherits
        2 through the route 6 -> 5 -> 2; vertex 4 inherits it through
        4 -> 6 -> 5 -> 2. After returning from child 4, vertex 2 checks
        low[4] = 2 >= discovery[2] = 2 and is marked. Removing 2 separates
        {4, 5, 6} from {0, 1, 3}. Its other child 3 can reach 0, but this
        does not rescue the subtree rooted at 4.

        Root 0 has two DFS children, 1 and 2. It is marked immediately after
        DFS returns from child 2, while still inside its neighbor loop.
        Neighbor 3 was already visited through 2 and is not a third DFS child.
        Removing 0 isolates 1. Marking may happen in order 2 then 0, but the
        final boolean-array scan returns [0, 2].

        Disconnected graphs:
            Each outer-loop DFS start creates a separate root and applies the
            same rules within its component. Unlike brute force, no original
            component count is needed: these rules directly detect splitting
            within one component. Other components are unaffected by removal.

    Time Complexity:
        O(V + E), where V counts vertices and E counts undirected edges.

        1. Four arrays each have V entries -> O(V) initialization.
        2. The outer loop checks V vertices. Each enters DFS once; each neighbor
           list is scanned once. Across all lists there are O(E) entries (2E
           when each undirected edge, including loops, is represented twice).
           Every discovery, low update, and marking operation is O(1).
           Thus all DFS calls together take O(V + E), not O(V * E).
        3. The final scan checks V flags and appends at most V IDs -> O(V).

        In the example, V = 7 and E = 8, so DFS scans 16 neighbor entries.
        Nested calls share discovery state; they do not restart a whole-graph
        traversal for every node. Add sequential work:
            O(V) + O(V + E) + O(V) = O(V + E).
        No sorting term is needed because result IDs are collected in order.

    Space Complexity:
        O(V) additional space, excluding the supplied adjacency list.

        - parents, discovery, low, is_articulation: V entries each -> O(V).
          For seven vertices these arrays hold 7 + 7 + 7 + 7 = 28 entries.
        - Recursive DFS stack: at most V active calls along a path -> O(V).
          children is a local counter per call; these counters are included
          in the stack bound, not separate length-V arrays per call.
        - result: at most V IDs -> O(V), with no duplicates.
        - Shared timer and other nonrecursive local values: O(1).

        All calls share the arrays and input graph. Separate component searches
        finish before the next begins, so memory is not multiplied by the
        number of components. Peak storage adds to
            O(4V + V + V + 1) = O(V).
        Excluding the output still gives O(V). Including the existing input
        adjacency list in total storage would give O(V + E).

    Implementation Notes:
        Recursive DFS can exceed Python's recursion limit on deep graphs allowed
        by V <= 10000. Shallow maximum-size tests do not cover that limitation;
        this function does not change the recursion limit.
        Parent-vertex skipping ignores all parallel edges to the parent. This
        can change conventional low values, but does not change articulation
        points: extra edges to a vertex cannot bypass that vertex's removal.
        Do not reuse that reasoning for bridges, where individual edges matter.

    Interview Summary:
        I use DFS discovery times and low values to determine whether a child's
        subtree depends on its parent. A non-root needs one dependent child;
        a root needs at least two DFS children. Boolean marks and an ascending
        scan give unique sorted output in O(V + E) time and O(V) extra space.
    """
    # Step 1: Initialize per-vertex state and articulation flags.
    parents: list[int] = [-1] * vertices
    discovery: list[int] = [-1] * vertices
    low: list[int] = [-1] * vertices
    is_articulation: list[bool] = [False] * vertices

    discovery_time: int = 0

    def dfs(node: int) -> None:
        # Step 2: Record entry time and create this node's own child counter.
        nonlocal discovery_time
        discovery[node] = low[node] = discovery_time
        discovery_time += 1
        children: int = 0

        for neighbor in adjacency_list[node]:
            # Step 3: Count and explore each unvisited direct child.
            if discovery[neighbor] == -1:
                children += 1
                parents[neighbor] = node
                dfs(node=neighbor)
                # Step 3: Inherit the earliest connection found by this child.
                low[node] = min(low[node], low[neighbor])

                # Step 4: Mark a root as soon as its second child has been explored.
                if children > 1 and parents[node] == -1:
                    is_articulation[node] = True
                # Step 5: One dependent child makes a non-root an articulation point.
                if parents[node] != -1 and low[neighbor] >= discovery[node]:
                    is_articulation[node] = True
            elif neighbor != parents[node]:
                # Step 6: Update from visited non-parent neighbors; ignore the parent.
                low[node] = min(low[node], discovery[neighbor])

    # Step 2: Start a new DFS root for each unvisited component.
    for vertex in range(vertices):
        if discovery[vertex] != -1:
            continue
        dfs(node=vertex)

    # Step 7: Read flags in ID order for unique, sorted results without sorting.
    result: list[int] = [
        vertex for vertex in range(vertices) if is_articulation[vertex]
    ]

    return result if result else [-1]


def solve() -> None:
    vertices: int = 7
    adjacency_list: list[list[int]] = [
        [1, 2, 3],
        [0],
        [0, 3, 4, 5],
        [2, 0],
        [2, 6],
        [2, 6],
        [4, 5],
    ]
    expected: list[int] = [0, 2]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second problem example.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0, 4], [3, 4], [2, 4], [1, 2, 3]]
    expected: list[int] = [1, 4]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum vertex and edge counts: one vertex with a self-loop.
    vertices: int = 1
    adjacency_list: list[list[int]] = [[0, 0]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two vertices joined by one edge.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[1], [0]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: triangle with no articulation points.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Short path with one articulation point.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[1], [0, 2], [1]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer small path: internal vertices are articulation points.
    vertices: int = 7
    adjacency_list: list[list[int]] = [[1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5]]
    expected: list[int] = [1, 2, 3, 4, 5]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS root with multiple branches: star centered at zero.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1, 2, 3, 4, 5], [0], [0], [0], [0], [0]]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star centered at the highest vertex ID.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[5], [5], [5], [5], [5], [0, 1, 2, 3, 4]]
    expected: list[int] = [5]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles share one articulation vertex.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1, 3, 4], [2, 4], [2, 3]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles joined by a bridge: both endpoints are articulation points.
    vertices: int = 6
    adjacency_list: list[list[int]] = [
        [1, 2],
        [0, 2],
        [0, 1, 3],
        [2, 4, 5],
        [3, 5],
        [3, 4],
    ]
    expected: list[int] = [2, 3]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle with one leaf; root has only one DFS child.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0, 2, 4], [1, 3], [2, 4], [3, 1]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete graph: no articulation points.
    vertices: int = 5
    adjacency_list: list[list[int]] = [
        [neighbor for neighbor in range(vertices) if neighbor != node]
        for node in range(vertices)
    ]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected triangles: no articulation points despite multiple components.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1], [4, 5], [3, 5], [3, 4]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two disconnected paths: count increases relative to the original graph.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1], [0, 2], [1], [4], [3, 5], [4]]
    expected: list[int] = [1, 4]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated first vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[], [2], [1, 3], [2]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated middle vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[2], [], [0, 3], [2]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated final vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [0, 2], [1], []]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge and isolated vertices: removing an isolated vertex reduces components.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0], [], [], []]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loops on a path do not provide routes around its middle vertex.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[0, 0, 1], [0, 1, 1, 2], [1, 2, 2]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected self-loop-only vertices.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[0, 0], [1, 1], [2, 2]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted neighbors: result must still be ascending.
    vertices: int = 7
    adjacency_list: list[list[int]] = [[3, 1], [2, 0], [1], [5, 4, 0], [3], [6, 3], [5]]
    expected: list[int] = [0, 1, 3, 5]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with the minimum edge count; shallow traversals.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [[1], [0]] + [[] for _ in range(vertices - 2)]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: shallow star.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [list(range(1, vertices))] + [
        [0] for _ in range(1, vertices)
    ]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges: star plus one leaf-to-leaf edge.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [list(range(1, vertices)), [0, 2], [0, 1]] + [
        [0] for _ in range(3, vertices)
    ]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_brute_force(
        vertices, adjacency_list
    )
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tarjan solution: first problem example.
    vertices: int = 7
    adjacency_list: list[list[int]] = [
        [1, 2, 3],
        [0],
        [0, 3, 4, 5],
        [2, 0],
        [2, 6],
        [2, 6],
        [4, 5],
    ]
    expected: list[int] = [0, 2]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Additional Tarjan tests; assertions intentionally commented out.
    # Second problem example.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0, 4], [3, 4], [2, 4], [1, 2, 3]]
    expected: list[int] = [1, 4]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum vertex and edge counts: one vertex with a self-loop.
    vertices: int = 1
    adjacency_list: list[list[int]] = [[0, 0]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two vertices joined by one edge.
    vertices: int = 2
    adjacency_list: list[list[int]] = [[1], [0]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Practice example: triangle with no articulation points.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Short path with one articulation point.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[1], [0, 2], [1]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer small path: internal vertices are articulation points.
    vertices: int = 7
    adjacency_list: list[list[int]] = [[1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5]]
    expected: list[int] = [1, 2, 3, 4, 5]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # DFS root with multiple branches: star centered at zero.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1, 2, 3, 4, 5], [0], [0], [0], [0], [0]]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Star centered at the highest vertex ID.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[5], [5], [5], [5], [5], [0, 1, 2, 3, 4]]
    expected: list[int] = [5]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles share one articulation vertex.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1, 3, 4], [2, 4], [2, 3]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two cycles joined by a bridge: both endpoints are articulation points.
    vertices: int = 6
    adjacency_list: list[list[int]] = [
        [1, 2],
        [0, 2],
        [0, 1, 3],
        [2, 4, 5],
        [3, 5],
        [3, 4],
    ]
    expected: list[int] = [2, 3]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cycle with one leaf; root has only one DFS child.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0, 2, 4], [1, 3], [2, 4], [3, 1]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Complete graph: no articulation points.
    vertices: int = 5
    adjacency_list: list[list[int]] = [
        [neighbor for neighbor in range(vertices) if neighbor != node]
        for node in range(vertices)
    ]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected triangles: no articulation points despite multiple components.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1, 2], [0, 2], [0, 1], [4, 5], [3, 5], [3, 4]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two disconnected paths: count increases relative to the original graph.
    vertices: int = 6
    adjacency_list: list[list[int]] = [[1], [0, 2], [1], [4], [3, 5], [4]]
    expected: list[int] = [1, 4]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated first vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[], [2], [1, 3], [2]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated middle vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[2], [], [0, 3], [2]]
    expected: list[int] = [2]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Isolated final vertex and a path.
    vertices: int = 4
    adjacency_list: list[list[int]] = [[1], [0, 2], [1], []]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One edge and isolated vertices: removing an isolated vertex reduces components.
    vertices: int = 5
    adjacency_list: list[list[int]] = [[1], [0], [], [], []]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Self-loops on a path do not provide routes around its middle vertex.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[0, 0, 1], [0, 1, 1, 2], [1, 2, 2]]
    expected: list[int] = [1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Disconnected self-loop-only vertices.
    vertices: int = 3
    adjacency_list: list[list[int]] = [[0, 0], [1, 1], [2, 2]]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Unsorted neighbors: result must still be ascending.
    vertices: int = 7
    adjacency_list: list[list[int]] = [[3, 1], [2, 0], [1], [5, 4, 0], [3], [6, 3], [5]]
    expected: list[int] = [0, 1, 3, 5]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices with the minimum edge count; shallow traversals.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [[1], [0]] + [[] for _ in range(vertices - 2)]
    expected: list[int] = [-1]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices: shallow star.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [list(range(1, vertices))] + [
        [0] for _ in range(1, vertices)
    ]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum vertices and edges: star plus one leaf-to-leaf edge.
    vertices: int = 10000
    adjacency_list: list[list[int]] = [list(range(1, vertices)), [0, 2], [0, 1]] + [
        [0] for _ in range(3, vertices)
    ]
    expected: list[int] = [0]
    result: list[int] = articulation_points_in_graph_tarjans(vertices, adjacency_list)
    # assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
