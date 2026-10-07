"""Word Ladder II: All Shortest Transformation Paths

Given distinct words begin_word and end_word and a list of unique words,
return every shortest transformation path from begin_word to end_word,
together with the number of transformations in each shortest path.

This practice variant uses the return format discussed in the walkthrough:
    (paths, transformations)

Rules:
    - All words contain lowercase English letters and have equal length.
    - Each transformation changes exactly one letter.
    - Every transformed word, including end_word, must be in word_list.
    - begin_word may or may not be in word_list.
    - Each returned path includes both begin_word and end_word.
    - Return all shortest paths without duplicates, in any order.
    - Longer paths must not be included.
    - If no transformation path exists, return ([], 0).

The transformation count is one less than the number of words in a path.
For example, a path containing four words requires three transformations.

Example:
    Input: begin_word = "hot", end_word = "cog",
           word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    Output: (
        [
            ["hot", "dot", "dog", "cog"],
            ["hot", "lot", "log", "cog"],
        ],
        3,
    )
    Explanation: Both paths require three single-letter changes. There is
    no shorter valid path. Either ordering of these two paths is accepted.
"""

import string
from collections import defaultdict, deque


def build_adjacency_list(words: set[str]) -> list[list[int]]:
    adj: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        for index in range(len(word)):
            for c in string.ascii_lowercase:
                new_word: str = word[:index] + c + word[index + 1 :]
                if new_word in words and new_word != word:
                    adj[word].append(new_word)

    return adj


def word_ladder_bfs_parents(
    begin_word: str, end_word: str, word_list: list[str]
) -> tuple[list[list[str]], int]:
    """Return all shortest word-transformation paths and their edge count.

    Args:
        begin_word: Starting lowercase English word.
        end_word: Distinct target word of the same length as begin_word.
        word_list: Unique lowercase English words of that same length.
            Every transformed word must be listed, including end_word.
            begin_word need not be listed. The input list is not modified.

    Returns:
        (paths, transformations), where each path includes both endpoints
        and transformations is len(path) - 1, not the number of paths or
        words. Paths may be returned in any order. Returns ([], 0) if the
        target is absent or cannot be reached.

    Approach:
        Use Breadth-First Search (BFS) with multiple parent tracking, then
        recursive DFS backtracking to reconstruct all shortest paths.
        1. Create a working set from word_list and include begin_word.
           Return ([], 0) if the target is absent. Set membership avoids
           repeatedly scanning the input list while generating neighbors.
        2. Build adjacency by replacing every character position of each
           word with every lowercase English letter. Keep a candidate only
           if it is in the working set and differs from the original word.
           Each edge represents exactly one transformation of cost 1.
        3. Enqueue (begin_word, 0), record its distance as zero, and initialize
           lists of parents. The distance dictionary also tracks discovery;
           recording the starting word prevents rediscovery through a neighbor.
        4. Pop queue entries in FIFO order. Stop when end_word is popped.
           BFS processes increasing distances, so all words in the preceding
           layer have already been processed by then. Thus all shortest-path
           parents of the target have been recorded, not just the first one.
        5. For an undiscovered neighbor, save distance + 1, record its first
           parent, and enqueue it. If a discovered neighbor has that same
           distance, append this additional parent without enqueueing again.
           Ignore longer routes. First discovery is shortest because every
           edge costs 1 and BFS processes nearer layers first; no later
           shorter-path comparison is necessary.
        6. Reconstruct paths backward from end_word. Append a parent to the
           working path, recurse, then pop it to undo that choice before
           trying another parent. Each parent is one distance layer closer
           to the start, so parent links cannot form cycles. At begin_word,
           save path[::-1], a reversed shallow copy in start-to-target order.
           Later append/pop operations change the working list, not the saved
           copy; the string elements themselves are immutable.
        7. Before calling reconstruction, return ([], 0) if BFS never discovered
           end_word. Dictionary membership only establishes that a target is
           allowed; it does not establish reachability.
        8. Return the completed paths and distances[end_word]. The latter is
           the transformation count, while len(paths) counts distinct routes.

        Walkthrough: hot -> cog with hot, dot, dog, lot, log, cog available.
            BFS discovers dot and lot at distance 1, then dog and log at 2.
            Dog first discovers cog at 3. Log also reaches cog at 3, so
            parents[cog] contains both dog and log. Backtracking constructs
            cog -> dog -> dot -> hot and cog -> log -> lot -> hot. Reversing
            copies gives two four-word paths, each with 3 transformations.

    Time Complexity:
        Let W be the number of distinct working words including begin_word,
        L the word length, A the number of directed adjacency entries, P the
        number of shortest paths returned, and D their number of words.
        Building adjacency takes O(26 * W * L**2) expected time: there are
        26 * W * L candidates, and creating and hashing each string costs
        O(L). Set operations assume average hash-table behavior. BFS takes
        O((W + A) * L) expected time when string hashing/comparison costs
        are included (O(W + A) with constant-cost word labels). Since
        A <= 25 * W * L, graph construction and BFS together are bounded
        by O(W * L**2) with alphabet size fixed. Backtracking takes at most
        O(P * D * L) expected time including string-key lookups and copying
        paths. Total: O(W * L**2 + P * D * L) expected time. With word-key
        operations treated as constant cost, reconstruction is O(P * D).
        The number of shortest paths can be exponential in graph size.

    Space Complexity:
        O((W + A) * L + P * D) including output. Adjacency retains newly
        generated length-L strings, while the working set, distances, queue,
        and parent lists store O(W + A) entries, mostly word references.
        Backtracking uses O(D) stack frames and working-path entries. The
        returned P paths store O(P * D) references; slicing copies lists,
        not the strings. Without output, auxiliary space is O((W + A) * L).

    Limitation:
        Reconstruction is recursive, so a sufficiently long shortest path
        can exceed Python's recursion limit. Returning all shortest paths
        can also require substantial time and memory when there are many.
    """

    # 1. Prepare output, the graph, and a membership set including the start.
    paths: list[list[str]] = []
    words: set[str] = set(word_list)
    words.add(begin_word)

    if end_word not in words:
        return [], 0

    # 2. Connect words that differ at exactly one character position.

    adj: defaultdict[str, list[str]] = build_adjacency_list(words=words)

    # 3. Track shortest distances and all equally short predecessor choices.
    queue: deque[tuple[str, int]] = deque([(begin_word, 0)])
    parents: defaultdict[str, list[str]] = defaultdict(list)
    distances: dict[str, int] = {begin_word: 0}
    # 4. FIFO traversal finishes the preceding layer before popping the target.
    while queue:
        word, distance = queue.popleft()
        new_distance = distance + 1

        if word == end_word:
            break

        # 5. Discover once, but retain additional parents at the same distance.
        for neighbor in adj[word]:
            if neighbor not in distances:
                distances[neighbor] = new_distance
                parents[neighbor].append(word)
                queue.append((neighbor, new_distance))
            elif distances[neighbor] == new_distance:
                parents[neighbor].append(word)

    # 6. Reconstruct paths backward using choose, explore, and undo.
    def build_paths(chld_word: str, path: list[str]) -> None:
        if chld_word == begin_word:
            # Slicing saves a reversed copy, independent of later backtracking.
            paths.append(path[::-1])
            return

        for parent in parents[chld_word]:
            path.append(parent)
            build_paths(chld_word=parent, path=path)
            path.pop()

    # 7. A listed target can still be disconnected; reconstruct only if reached.
    if end_word not in distances:
        return [], 0

    build_paths(chld_word=end_word, path=[end_word])

    # 8. Return all shortest paths and their shared number of transformations.
    return paths, distances[end_word]


def word_ladder_bfs_paths(
    begin_word: str, end_word: str, word_list: list[str]
) -> tuple[list[list[str]], int]:
    """Return all shortest transformation paths using a queue of full paths.

    Args:
        begin_word: Starting lowercase English word.
        end_word: Distinct target word of the same length as begin_word.
        word_list: Unique lowercase English words of that same length.
            Every transformed word, including the target, must be listed.
            The starting word need not be listed. The input is not modified.

    Returns:
        (paths, transformations), where each path includes both endpoints.
        The count is the number of letter changes, len(path) - 1, not the
        number of paths. Paths may appear in any order. Returns ([], 0) if
        the target is absent or no valid transformation sequence exists.

    Approach:
        Use level-order Breadth-First Search (BFS), storing complete paths
        and delaying global visitation until the current level finishes.
        1. Create a working word set including begin_word. If end_word is
           absent, return ([], 0). Build adjacency using one-letter changes
           that produce another word in the set.
        2. Enqueue the one-word path [begin_word], mark begin_word visited,
           and initialize the output list. Each queue entry is a whole path,
           so no parent map or separate reconstruction phase is needed.
        3. At the start of each level, create visited_per_level and evaluate
           range(len(queue)). That queue length is captured once: exactly
           those existing paths are processed. New paths appended during
           this loop wait for the next outer iteration. All paths processed
           in the current level contain the same number of words.
        4. Pop a path and examine its final word. If it is end_word, save
           path[:], a shallow copy, and continue to the next path in this
           level without expanding the target. Continue does not leave the
           level loop, so every target path of that length can be collected.
        5. Otherwise, inspect its neighbors. For each neighbor absent from
           global visited, enqueue path + [neighbor], creating a new list,
           and record the neighbor in visited_per_level. Do not reject words
           merely because they are in visited_per_level: another path in
           this same level must be allowed to reach them equally quickly.
        6. After the entire level finishes, stop if any target paths were
           found. BFS processes increasing path lengths, so these are all
           shortest paths; later levels cannot improve them. No explicit
           comparison with len(paths[0]) is needed within a single level.
           Non-target paths in this level may have queued longer candidates,
           but those candidates are never processed after this break.
        7. If no target was found, merge visited_per_level into visited.
           This marks all new discoveries together, preventing later, longer
           routes from revisiting them. Previously completed levels are
           already visited, which also prevents cycles within queued paths.
        8. If the search ends without paths, return ([], 0). Otherwise return
           the paths and len(paths[0]) - 1. Every saved path has equal length.

        Walkthrough: hot -> cog with hot, dot, dog, lot, log, cog available.
            One level contains hot -> dot -> dog and hot -> lot -> log.
            Dog enqueues its path to cog and records cog in visited_per_level,
            but does not globally mark it yet. Log can therefore enqueue its
            own path to cog. At the level boundary, cog becomes visited.
            The next level pops both four-word paths and saves both. Marking
            cog visited does not remove already queued paths. After that
            entire level finishes, stop and return both paths with count 3.

    Time Complexity:
        Let W be the number of working words, L their length, and A the
        number of directed adjacency entries. Graph construction takes
        O(26 * W * L**2) expected time, or O(W * L**2) with alphabet size
        fixed: each length-L candidate must be constructed and hashed.
        Let Q be the total number of path entries created, D their maximum
        word count, and H the total neighbor entries examined across all
        processed paths. Unlike ordinary vertex-only BFS, a vertex may be
        expanded once for each shortest prefix reaching it. Copying queued
        and returned path lists takes O(Q * D) in total; graph lookups and
        membership checks cost O((Q + H) * L) expected time including string
        hashing/comparison. Overall: O(W * L**2 + Q * D + (Q + H) * L).
        Q and H can be exponential in graph size, including prefixes that
        never reach the target. Hash-table operations assume average behavior.

    Space Complexity:
        O((W + A) * L + F * D + P * D), including output, where F is the
        maximum number of simultaneously queued paths and P is the number
        of returned paths. Adjacency retains generated length-L neighbor
        strings. Word and visited sets use O(W) entries. Queued paths and
        output copies hold references to strings rather than copying their
        contents. Full-path storage can use more memory than parent links.
        The implementation uses no recursion.

    https://www.youtube.com/watch?v=DREutrv2XD0&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=30
    """
    # 1. Prepare allowed words, reject a missing target, and build the graph.
    words: set[str] = set(word_list)
    words.add(begin_word)

    if end_word not in words:
        return [], 0

    adj: defaultdict[str, list[str]] = build_adjacency_list(words=words)
    # 2. Start with one full path and mark only the starting word visited.
    queue: deque[list[str]] = deque([[begin_word]])
    visited: set[str] = {begin_word}
    paths: list[list[str]] = []

    while queue:
        # 3. Process a fixed number of current-level paths before advancing.
        visited_per_level: set[str] = set()
        for _ in range(len(queue)):
            path: list[str] = queue.popleft()
            word: str = path[-1]

            # 4. Save target paths without expanding them; finish this level.
            if word == end_word:
                paths.append(path[:])
                continue

            # 5. Allow shared discoveries within this level, using separate paths.
            for neighbor in adj[word]:
                if neighbor not in visited:
                    queue.append(path + [neighbor])
                    visited_per_level.add(neighbor)

        # 6. All target paths in this first successful level are shortest.
        if paths:
            break

        # 7. Mark every delayed discovery together before the next level.
        visited.update(visited_per_level)

    # 8. Return all shortest paths and their transformation count, or no result.
    if not paths:
        return [], 0

    return paths, len(paths[0]) - 1


def solve() -> None:
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog", "lot", "log", "cog"]
    expected: tuple[list[list[str]], int] = (
        [
            ["hot", "dot", "dog", "cog"],
            ["hot", "lot", "log", "cog"],
        ],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    # Accept either ordering of the paths while preserving order within each path.
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two shortest paths must survive when they converge on the target.
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog", "lot", "log", "cog"]
    expected: tuple[list[list[str]], int] = (
        [
            ["hot", "dot", "dog", "cog"],
            ["hot", "lot", "log", "cog"],
        ],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single-letter direct transformation.
    begin_word: str = "a"
    end_word: str = "z"
    word_list: list[str] = ["z"]
    expected: tuple[list[list[str]], int] = ([["a", "z"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target missing from dictionary.
    begin_word: str = "hit"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Target listed but disconnected.
    begin_word: str = "hit"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "cog"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Only target listed but more than one change required.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["bbb"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Starting word is also listed.
    begin_word: str = "hit"
    end_word: str = "hot"
    word_list: list[str] = ["hit", "hot"]
    expected: tuple[list[list[str]], int] = ([["hit", "hot"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One shortest chain.
    begin_word: str = "hit"
    end_word: str = "dog"
    word_list: list[str] = ["hot", "dot", "dog"]
    expected: tuple[list[list[str]], int] = ([["hit", "hot", "dot", "dog"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two shortest paths converge on target.
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog", "lot", "log", "cog"]
    expected: tuple[list[list[str]], int] = (
        [["hot", "dot", "dog", "cog"], ["hot", "lot", "log", "cog"]],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Two paths converge before the target.
    begin_word: str = "aaa"
    end_word: str = "bbc"
    word_list: list[str] = ["aab", "aba", "abb", "bbb", "bbc"]
    expected: tuple[list[list[str]], int] = (
        [["aaa", "aab", "abb", "bbb", "bbc"], ["aaa", "aba", "abb", "bbb", "bbc"]],
        4,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Six shortest paths through three changing positions.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aab", "aba", "abb", "baa", "bab", "bba", "bbb"]
    expected: tuple[list[list[str]], int] = (
        [
            ["aaa", "aab", "abb", "bbb"],
            ["aaa", "aab", "bab", "bbb"],
            ["aaa", "aba", "abb", "bbb"],
            ["aaa", "aba", "bba", "bbb"],
            ["aaa", "baa", "bab", "bbb"],
            ["aaa", "baa", "bba", "bbb"],
        ],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Direct path excludes longer alternatives.
    begin_word: str = "hot"
    end_word: str = "dot"
    word_list: list[str] = ["hot", "dot", "lot", "log", "dog"]
    expected: tuple[list[list[str]], int] = ([["hot", "dot"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Longer detour excluded when shortest path is indirect.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aab", "abb", "bbb", "aac", "acc", "bcc", "bbc"]
    expected: tuple[list[list[str]], int] = ([["aaa", "aab", "abb", "bbb"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Dead-end branch does not block a valid path.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aac", "aab", "abb", "bbb"]
    expected: tuple[list[list[str]], int] = ([["aaa", "aab", "abb", "bbb"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Changing the first position.
    begin_word: str = "aaaa"
    end_word: str = "zaaa"
    word_list: list[str] = ["zaaa"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "zaaa"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Changing a middle position.
    begin_word: str = "aaaa"
    end_word: str = "aaza"
    word_list: list[str] = ["aaza"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "aaza"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Changing the final position.
    begin_word: str = "aaaa"
    end_word: str = "aaaz"
    word_list: list[str] = ["aaaz"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "aaaz"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Ten-character words differing only at the end.
    begin_word: str = "aaaaaaaaaa"
    end_word: str = "aaaaaaaaaz"
    word_list: list[str] = ["aaaaaaaaaz"]
    expected: tuple[list[list[str]], int] = ([["aaaaaaaaaa", "aaaaaaaaaz"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shuffled dictionary preserves all shortest paths.
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["cog", "log", "lot", "dog", "dot"]
    expected: tuple[list[list[str]], int] = (
        [["hot", "dot", "dog", "cog"], ["hot", "lot", "log", "cog"]],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_paths(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Single-letter direct transformation.
    begin_word: str = "a"
    end_word: str = "z"
    word_list: list[str] = ["z"]
    expected: tuple[list[list[str]], int] = ([["a", "z"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Target missing from dictionary.
    begin_word: str = "hit"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Target listed but disconnected.
    begin_word: str = "hit"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "cog"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Only target listed but more than one change required.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["bbb"]
    expected: tuple[list[list[str]], int] = ([], 0)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Starting word is also listed.
    begin_word: str = "hit"
    end_word: str = "hot"
    word_list: list[str] = ["hit", "hot"]
    expected: tuple[list[list[str]], int] = ([["hit", "hot"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: One shortest chain.
    begin_word: str = "hit"
    end_word: str = "dog"
    word_list: list[str] = ["hot", "dot", "dog"]
    expected: tuple[list[list[str]], int] = ([["hit", "hot", "dot", "dog"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Two shortest paths converge on target.
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["hot", "dot", "dog", "lot", "log", "cog"]
    expected: tuple[list[list[str]], int] = (
        [["hot", "dot", "dog", "cog"], ["hot", "lot", "log", "cog"]],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Two paths converge before the target.
    begin_word: str = "aaa"
    end_word: str = "bbc"
    word_list: list[str] = ["aab", "aba", "abb", "bbb", "bbc"]
    expected: tuple[list[list[str]], int] = (
        [["aaa", "aab", "abb", "bbb", "bbc"], ["aaa", "aba", "abb", "bbb", "bbc"]],
        4,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Six shortest paths through three changing positions.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aab", "aba", "abb", "baa", "bab", "bba", "bbb"]
    expected: tuple[list[list[str]], int] = (
        [
            ["aaa", "aab", "abb", "bbb"],
            ["aaa", "aab", "bab", "bbb"],
            ["aaa", "aba", "abb", "bbb"],
            ["aaa", "aba", "bba", "bbb"],
            ["aaa", "baa", "bab", "bbb"],
            ["aaa", "baa", "bba", "bbb"],
        ],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Direct path excludes longer alternatives.
    begin_word: str = "hot"
    end_word: str = "dot"
    word_list: list[str] = ["hot", "dot", "lot", "log", "dog"]
    expected: tuple[list[list[str]], int] = ([["hot", "dot"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Longer detour excluded when shortest path is indirect.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aab", "abb", "bbb", "aac", "acc", "bcc", "bbc"]
    expected: tuple[list[list[str]], int] = ([["aaa", "aab", "abb", "bbb"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Dead-end branch does not block a valid path.
    begin_word: str = "aaa"
    end_word: str = "bbb"
    word_list: list[str] = ["aac", "aab", "abb", "bbb"]
    expected: tuple[list[list[str]], int] = ([["aaa", "aab", "abb", "bbb"]], 3)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Changing the first position.
    begin_word: str = "aaaa"
    end_word: str = "zaaa"
    word_list: list[str] = ["zaaa"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "zaaa"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Changing a middle position.
    begin_word: str = "aaaa"
    end_word: str = "aaza"
    word_list: list[str] = ["aaza"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "aaza"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Changing the final position.
    begin_word: str = "aaaa"
    end_word: str = "aaaz"
    word_list: list[str] = ["aaaz"]
    expected: tuple[list[list[str]], int] = ([["aaaa", "aaaz"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Ten-character words differing only at the end.
    begin_word: str = "aaaaaaaaaa"
    end_word: str = "aaaaaaaaaz"
    word_list: list[str] = ["aaaaaaaaaz"]
    expected: tuple[list[list[str]], int] = ([["aaaaaaaaaa", "aaaaaaaaaz"]], 1)
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Parents BFS: Shuffled dictionary preserves all shortest paths.
    begin_word: str = "hot"
    end_word: str = "cog"
    word_list: list[str] = ["cog", "log", "lot", "dog", "dot"]
    expected: tuple[list[list[str]], int] = (
        [["hot", "dot", "dog", "cog"], ["hot", "lot", "log", "cog"]],
        3,
    )
    result: tuple[list[list[str]], int] = word_ladder_bfs_parents(
        begin_word, end_word, word_list
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert result[1] == expected[1]
    assert sorted(result[0]) == sorted(expected[0])
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
