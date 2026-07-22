# =============================================================================
# Course Schedule (LeetCode #207)
#
# There are numCourses courses, labeled 0 to numCourses - 1. You're given an
# array prerequisites, where prerequisites[i] = [a, b] means you must take
# course b before course a.
#
# Return true if it's possible to finish all courses, or false if it's
# impossible (i.e., there's a circular dependency).
#
# Example 1:
#   numCourses = 2
#   prerequisites = [[1, 0]]
#   Output: true
#   Explanation: Take course 0 first, then course 1.
#
# Example 2:
#   numCourses = 2
#   prerequisites = [[1, 0], [0, 1]]
#   Output: false
#   Explanation: Course 1 needs 0, but 0 needs 1 — a cycle, so neither can
#                be taken first.
#
# Constraints (typical):
#   1 ≤ numCourses ≤ 10^5
#   0 ≤ prerequisites.length ≤ 5000
#   prerequisites[i].length == 2
#   0 ≤ a, b < numCourses
#   All pairs [a, b] are unique
# =============================================================================

from collections import defaultdict, deque


def course_scheudle_dfs(
    number_of_courses: int, prerequisites: list[tuple[int, int]]
) -> bool:
    """
    Determines whether all courses can be finished using DFS cycle detection.

    The problem reduces to detecting a cycle in a directed graph where each
    node is a course and each directed edge (a → b) means "course a requires
    course b as a prerequisite."  If any cycle exists, it is impossible to
    complete all courses.

    Approach — DFS with a "visiting" set:
      - Build an adjacency list mapping each course to its prerequisites.
      - For every course, run a DFS that tracks the current recursion path in
        `visited`.  If we reach a node that is already in `visited`, we have
        found a back-edge (cycle) → return False.
      - Once all prerequisites of a course are confirmed cycle-free, clear its
        adjacency list entry so it acts as a memo and we never re-process it
        (effectively memoising "this node is safe").

    Args:
        number_of_courses: Total number of courses (nodes), labeled 0..n-1.
        prerequisites:     List of [course, prereq] pairs.

    Returns:
        True if all courses can be completed; False if a cycle is detected.

    Time Complexity:  O(V + E)
        - V = number_of_courses (nodes), E = len(prerequisites) (edges).
        - Each node and edge is visited at most once thanks to the memoisation
          step (clearing the adjacency list after a safe traversal).

    Space Complexity: O(V + E)
        - O(V + E) for the adjacency list (course_map).
        - O(V) for the visited set and the DFS call stack (in the worst case
          the stack depth equals the longest path, which is at most V).
    """
    # Build adjacency list: course → list of its prerequisites
    course_map: defaultdict[int, list[int]] = defaultdict(list)
    visited: set[int] = set()

    for course, prereq in prerequisites:
        course_map[course].append(prereq)

    def dfs(course: int) -> bool:
        """
        Recursively checks whether `course` is reachable from itself
        (i.e., part of a cycle).

        - If `course` is already in `visited` (current DFS path), a cycle
          exists → return False.
        - If `course` has no prerequisites left (empty list, either originally
          or cleared after a previous safe visit), it is safe → return True.
        - Otherwise, add `course` to `visited`, recurse on each prerequisite,
          then remove `course` from `visited` (backtrack).  Clear the
          adjacency list entry so future calls skip re-processing.

        Args:
            course: The course node being explored.

        Returns:
            False if a cycle is detected; True otherwise.
        """
        if course in visited:
            # Back-edge found — cycle detected
            return False
        if course_map[course] == []:
            # No prerequisites or already confirmed safe
            return True

        # Mark course as part of the current DFS path
        visited.add(course)

        for prereq in course_map[course]:
            if not dfs(prereq):
                return False

        # Backtrack: remove from current path
        visited.remove(course)
        # Memoise: mark as fully explored and safe
        course_map[course] = []
        return True

    print(f"number_of_courses {number_of_courses}")
    for c in range(number_of_courses):
        if not dfs(c):
            return False

    return True


def course_scheudle_bfs(
    number_of_courses: int, prerequisites: list[tuple[int, int]]
) -> bool:
    """
    Determines whether all courses can be finished using BFS (Kahn's algorithm).

    This is a topological sort approach.  A valid topological ordering exists
    if and only if the directed graph has no cycle.  Kahn's algorithm processes
    nodes level-by-level, always picking a node with in-degree 0 (nothing left
    to satisfy before it), reducing the in-degree of its neighbours, and
    enqueueing any neighbour whose in-degree drops to 0.  If we can process
    every node this way, the graph is acyclic and all courses can be finished.

    Approach — BFS with in-degree tracking:
      - Build an adjacency list where course_map[prereq] lists all courses
        that directly depend on prereq (i.e. edges point from prereq → course).
      - Track in_degree[course]: how many prerequisites course still needs.
      - Seed the queue with every course that has in-degree 0 (no prerequisites).
      - Each time a course is dequeued, increment `completed` and decrement the
        in-degree of each course that depends on it.  Enqueue any that reach 0.
      - At the end, if completed == number_of_courses every node was processed
        → no cycle.  Otherwise some nodes were stuck in a cycle.

    Args:
        number_of_courses: Total number of courses (nodes), labeled 0..n-1.
        prerequisites:     List of [course, prereq] pairs.

    Returns:
        True if all courses can be completed; False if a cycle is detected.

    Time Complexity:  O(V + E)
        - V = number_of_courses (nodes), E = len(prerequisites) (edges).
        - Each node is enqueued and dequeued exactly once; each edge is
          examined exactly once when its source node is dequeued.

    Space Complexity: O(V + E)
        - O(V + E) for the adjacency list (course_map).
        - O(V) for the in_degree array and the BFS queue (at most all nodes
          can sit in the queue simultaneously).
    """
    # in_degree[i] = number of prerequisites course i still needs
    in_degree: list[int] = [0] * number_of_courses
    # Adjacency list: prereq → list of courses that depend on it
    course_map: defaultdict[list[int, int]] = defaultdict(list)
    # BFS queue seeded with all courses that have no prerequisites
    queue: deque[int] = deque([])
    # Counts how many courses we successfully "take"
    completed: int = 0

    # Build the graph and populate in-degree counts
    for course, prereq in prerequisites:
        in_degree[course] += 1  # course has one more prerequisite
        course_map[prereq].append(course)  # prereq unlocks course

    # Seed queue with courses that are immediately available (no prerequisites)
    for i in range(number_of_courses):
        if in_degree[i] == 0:
            queue.append(i)

    # Process courses in topological order
    while queue:
        course: int = queue.popleft()
        completed += 1  # we can take this course

        # Unlock courses that depended on the just-completed course
        for dependent in course_map[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                # All prerequisites for `dependent` are now satisfied
                queue.append(dependent)

    # If every course was completed, the graph is acyclic
    return completed == number_of_courses


def solve():
    """
    Driver function that runs a few test cases against course_scheudle_dfs.

    Test cases:
      1. 4 courses with a diamond-shaped dependency graph — no cycle → True.
      2. 2 courses, one prerequisite — no cycle → True.
      3. 2 courses with a mutual dependency — cycle → False.
    """
    # Test case 1: Diamond-shaped dependency graph (no cycle).
    # 0 must come before 1 and 2; both 1 and 2 must come before 3.
    # Graph: 1→0, 2→0, 3→1, 3→2  →  valid ordering exists. Expected: True.
    number_of_courses: int = 4
    prerequisites: list[tuple[int, int]] = [[1, 0], [2, 0], [3, 1], [3, 2]]
    print(
        f"can {number_of_courses} be finished - dfs ? {course_scheudle_dfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )
    print(
        f"can {number_of_courses} be finished - bfs ? {course_scheudle_bfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )

    # Test case 2: Simple linear dependency (no cycle).
    # Course 1 requires course 0. Take 0 first, then 1. Expected: True.
    number_of_courses: int = 2
    prerequisites: list[tuple[int, int]] = [[1, 0]]
    print(
        f"can {number_of_courses} be finished - dfs? {course_scheudle_dfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )
    print(
        f"can {number_of_courses} be finished - bfs ? {course_scheudle_bfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )
    # Test case 3: Mutual dependency — forms a cycle.
    # Course 1 needs 0, and course 0 needs 1 → neither can be taken first.
    # Graph: 1→0→1 (cycle). Expected: False.
    number_of_courses: int = 2
    prerequisites: list[tuple[int, int]] = [[1, 0], [0, 1]]
    print(
        f"can {number_of_courses} be finished? {course_scheudle_dfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )
    print(
        f"can {number_of_courses} be finished - bfs ? {course_scheudle_bfs(number_of_courses=number_of_courses, prerequisites=prerequisites)}"
    )


solve()
