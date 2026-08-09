"""
Alien Dictionary (LeetCode #269)

You are given a list of words sorted according to the rules of an alien
language's alphabet. The ordering of letters in that alphabet is unknown.
Determine a valid ordering of the alien alphabet's letters based on the
sorted word list. If no valid ordering exists (a cycle/contradiction), or
the input is invalid (a longer word appears before its prefix), return "".

This is Kahn's algorithm (multi-source BFS topological sort, like Course
Schedule) — but with a twist: you must derive the directed edges yourself
by comparing adjacent words, rather than being given the graph directly.

Example:
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    One valid output: "wertf"

References:
    https://www.youtube.com/watch?v=6kTZYvNNyps
    https://www.youtube.com/watch?v=cIBFEhD77b4&t=336s
"""

"""
Approach: Build graph from adjacent word pairs + Kahn's BFS topological sort
  Phase 1 — Graph construction: compare every pair of adjacent words
  character by character. The first position where they differ gives us a
  directed edge: word1[j] → word2[j] (word1[j] comes before word2[j] in
  the alien alphabet). We also detect the one invalid input case: if word1
  is longer than word2 and word2 is a prefix of word1, the list can't be
  validly sorted, so we return "" immediately.

  Phase 2 — Kahn's BFS (topological sort): seed the queue with all letters
  that have in-degree 0 (no prerequisites). Process each letter, decrement
  its neighbors' in-degrees, and enqueue any neighbor that reaches 0. If
  the result contains every unique letter, we have a valid ordering.
  If not, a cycle exists (contradiction) and we return "".

Time Complexity:  O(C) where C = total number of characters across all words.
                  Graph construction scans each adjacent pair once; BFS visits
                  each unique letter and each derived edge at most once.
Space Complexity: O(1) — at most 26 letters, so neighbor_map, in_degree,
                  queue, and result are all bounded by the alphabet size.
"""


from collections import defaultdict, deque


def alien_dictionary_bfs(words: list[str]) -> str:

    n: int = len(words)
    neighbor_map: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = defaultdict(int)
    queue: deque[str] = deque()
    result: list[str] = []

    # Step 1: Compare each adjacent word pair to extract ordering edges.
    # Zip through characters; the first mismatch reveals one ordering rule.
    for i in range(0, n - 1):
        word1 = words[i]
        word2 = words[i + 1]
        # Step 2: Invalid input check — a longer word cannot precede its own
        # prefix in a validly sorted list.
        if len(word1) > len(word2) and word1[: len(word2)] == word2:
            return ""
        for j in range(min(len(word1), len(word2))):
            if word1[j] != word2[j]:
                # Step 3: word1[j] must come before word2[j] in the alphabet.
                # Add a directed edge and track in-degree of the destination.
                neighbor_map[word1[j]].append(word2[j])
                in_degree[word2[j]] += 1
                break  # Only the first differing character gives us an edge.

    # Step 4: Register every letter that appears in the word list.
    # Letters with no incoming edges won't be in in_degree yet — add them
    # with in-degree 0 so they're picked up as BFS sources.
    for i in range(n):
        for j in range(len(words[i])):
            if words[i][j] not in in_degree:
                in_degree[words[i][j]] = 0

    # Step 5: Seed the BFS queue with all letters that have no prerequisites
    # (in-degree 0). These are valid starting points in the alien alphabet.
    for key in in_degree:
        if in_degree[key] == 0:
            queue.append(key)

    # Step 6: Kahn's BFS — process letters in topological order.
    while queue:
        current = queue.popleft()
        result.append(current)
        for neighbor in neighbor_map[current]:
            # Step 7: Remove this edge. If the neighbor now has no remaining
            # prerequisites, it's ready to be placed in the ordering.
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 8: If result doesn't contain every unique letter, a cycle exists
    # (some letters never reached in-degree 0) — return "" for contradiction.
    return "" if len(result) != len(in_degree) else "".join(result)


"""
Approach: Build reverse graph from adjacent word pairs + DFS topological sort
  Phase 1 — Graph construction: same adjacent-word comparison as BFS, but
  edges are stored in REVERSE: word2[j] → word1[j]. This means each node's
  neighbor list holds its "must come before me" predecessors. Building the
  map as {c: [] for every char in words} also registers every unique letter
  upfront, avoiding a separate pass.

  Phase 2 — DFS topological sort with tri-colour cycle detection:
    • White  — not yet visited
    • Grey   — currently in the DFS call stack (active path)
    • Black  — fully processed and appended to result

  For each unvisited node we run DFS: mark it grey, recurse into its
  predecessors (reverse-graph neighbours), then mark it black and append
  it to the result string. Because edges are reversed, appending on the
  way *out* of DFS produces the correct alien alphabet order (post-order
  on the reversed graph == topological order on the original graph).

  Cycle detection: if we reach a grey node during DFS, a cycle exists —
  return "" immediately. Black nodes are already fully resolved and can be
  skipped safely.

Time Complexity:  O(C) where C = total number of characters across all words.
                  Graph construction scans each adjacent pair once; DFS visits
                  each unique letter and each derived edge at most once.
Space Complexity: O(1) — at most 26 letters, so neighbors, white/grey/black
                  sets, the call stack, and result are all bounded by the
                  alphabet size.
"""


def alien_dictionary_dfs(words: list[str]) -> str:

    # Step 1: Pre-populate the graph with every unique character so all
    # letters are registered even if they appear in no ordering constraint.
    # Edges are stored in REVERSE: neighbor[b] contains 'a' when a → b in
    # the alien alphabet (i.e., 'a' must come before 'b').
    neighbors: dict[str, list[str]] = {c: [] for word in words for c in word}

    # Step 2: Compare each adjacent word pair to extract ordering edges.
    # The first mismatched character gives one rule: word1[i] → word2[i].
    # Edges are added in reverse (word2[i] → word1[i]) so that post-order
    # DFS on this reversed graph yields the correct topological order.
    for word1, word2 in zip(words, words[1:]):
        for i in range(min(len(word1), len(word2))):
            if word1[i] != word2[i]:
                # Reverse edge: word2[i]'s predecessor is word1[i].
                neighbors[word2[i]].append(word1[i])
                break  # Only the first differing character gives us an edge.
        else:
            # Step 3: Invalid input check — if we exhausted the shorter word
            # without finding a difference, but word1 is longer, word1 cannot
            # legally precede its own prefix word2.
            if len(word1) > len(word2):
                return ""

    # Step 4: Tri-colour sets for DFS cycle detection.
    #   white — unvisited nodes
    #   grey  — nodes currently on the active DFS path (open call frames)
    #   black — fully processed nodes, safely appended to result
    whites: set[str] = set(neighbors.keys())
    blacks: set[str] = set()
    greys: set[str] = set()

    result: str = ""

    def move_node(node: str, current: set[str], target: set[str]):
        """Helper: atomically transfer a node between colour sets."""
        current.discard(node)
        target.add(node)

    def dfs(node: str) -> bool:
        # Step 5: Mark the current node grey — it's now on the active path.
        move_node(node, whites, greys)
        nonlocal result

        for parent in neighbors[node]:
            # Step 6: Skip nodes already fully resolved (black).
            if parent in blacks:
                continue

            # Step 7: Reaching a grey node means we've found a back edge —
            # a cycle exists, so no valid ordering is possible.
            if parent in greys:
                return False

            # Step 8: Recurse into unvisited predecessors. Propagate failure
            # upward immediately if a cycle is detected deeper in the stack.
            if not dfs(parent):
                return False

        # Step 9: All predecessors resolved — mark this node black and
        # append it to result. Post-order on the reversed graph = correct
        # topological order on the original alien-alphabet graph.
        move_node(node, greys, blacks)
        result += node
        return True

    # Step 10: Drive DFS from every unvisited node so all letters are placed,
    # even those with no ordering constraints (isolated in the graph).
    while whites:
        node: str = next(iter(whites))

        if not dfs(node):
            return ""

    return result


def solve():
    words: list[str] = ["wrt", "wrf", "er", "ett", "rftt"]
    # expected: "wertf"
    print(f"{words} the alien alphabets are {alien_dictionary_bfs(words=words)}")
    print(f"{words} the alien alphabets are {alien_dictionary_dfs(words=words)}")

    # words: list[str] = ["z", "x"]
    # # expected: "zx"
    # print(f"{words}  the alien alphabets are {alien_dictionary_bfs(words=words)}")

    words: list[str] = ["z", "x", "z"]
    # expected: "" (cycle: z -> x, then x -> z contradicts it)
    print(f"{words} the alien alphabets are {alien_dictionary_bfs(words=words)}")
    print(f"{words} the alien alphabets are {alien_dictionary_dfs(words=words)}")

    words: list[str] = ["abc", "ab"]
    # expected: "" (invalid — "abc" can't come before its own prefix "ab")
    print(f"{words} the alien alphabets are {alien_dictionary_bfs(words=words)}")
    print(f"{words} the alien alphabets are {alien_dictionary_dfs(words=words)}")

    words: list[str] = ["ab", "abc"]
    # expected: any order where 'a' comes before 'b' and 'b' comes before 'c'
    print(f"{words} the alien alphabets are {alien_dictionary_bfs(words=words)}")
    print(f"{words} the alien alphabets are {alien_dictionary_dfs(words=words)}")

    words: list[str] = ["a"]
    # expected: "a"
    print(f"{words} the alien alphabets are {alien_dictionary_bfs(words=words)}")
    print(f"{words} the alien alphabets are {alien_dictionary_dfs(words=words)}")


solve()
