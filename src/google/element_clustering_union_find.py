"""
=============================================================================
QUESTION: Elements Clustering
=============================================================================
Goal:
    Group a collection of elements into clusters. Two elements belong to the
    same cluster when they share at least one property, either directly or
    through a chain of other elements.

Input:
    A list of elements, each element contains:
        - A string identifier (ID)
        - An array of exactly three property strings

Desired Output:
    A two-dimensional list where each inner list holds the IDs of elements
    that are in the same cluster.

Key Requirements:
    - Clustering must be TRANSITIVE: if element A shares a property with B,
      and B shares a property with C, then A, B, and C are all in the same
      cluster even if A and C have no direct property in common.
    - Every element appears in exactly one cluster.
    - The order of clusters or the order of IDs inside a cluster is not
      specified.

Example:
    Given elements:
        ID 1 with properties p1, p2, p3
        ID 2 with properties p3, p4, p5
        ID 3 with properties p6, p7, p8

    Because element 1 and element 2 both have p3, they belong to the same
    cluster. Element 3 shares no property with the others, so it forms its
    own cluster.

    Output: [["1", "2"], ["3"]]

Approach — Union-Find (Disjoint Set Union):
    - Use a Union-Find structure keyed by element IDs.
    - For every pair (i, j), check if their property arrays overlap.
    - If they do, union the two elements together.
    - Finally, group all elements by their root to get the clusters.

Time Complexity:
    - Pairwise comparison: O(n²) pairs, each property check is O(k) where
      k=3 (fixed by the problem) → O(k·n²) = O(n²) overall.
    - Union-Find operations (with path compression + union by rank):
      nearly O(1) amortised per call → O(n²) total.
    - Grouping by root: O(n).
    → Overall: O(n²)

Space Complexity:
    - parents dict: O(n)
    - ranks dict:   O(n)
    - result grouping dict: O(n)
    → Overall: O(n)
=============================================================================
"""

from collections import defaultdict


def has_same_property(A: list[str], B: list[str]) -> bool:
    """
    Check whether two property arrays share at least one common property.

    Converting each list to a set is O(k), and the intersection is O(k),
    where k is the number of properties per element. Because k is fixed at 3
    by the problem constraints, this is O(k) = O(1) as a bounded constant —
    not because set conversion is free, but because k never grows with n.
    """
    return len(set(A).intersection(set(B))) > 0


def find(x: str, parents: dict[str, str]) -> str:
    """
    Find the root representative of the set containing x.

    Uses PATH COMPRESSION: while traversing up to the root, each visited
    node is pointed directly at the root. This flattens the tree and keeps
    future lookups near O(1) amortised.
    """
    if parents[x] != x:
        # Recursively find root and compress the path on the way back up.
        parents[x] = find(x=parents[x], parents=parents)
    return parents[x]


def union(A: str, B: str, parents: dict[str, str], ranks: dict[str, int]):
    """
    Merge the sets containing A and B.

    Uses UNION BY RANK: attach the shallower tree under the deeper one to
    keep the tree height logarithmic.  Together with path compression this
    gives nearly O(1) amortised cost per operation (inverse-Ackermann).

    Steps:
        1. Find the roots of A and B.
        2. If they share a root, they are already in the same set — nothing
           to do.
        3. Otherwise, attach the lower-rank root under the higher-rank root.
           If ranks are equal, pick one arbitrarily and increment its rank.
    """
    parent_A = find(x=A, parents=parents)
    parent_B = find(x=B, parents=parents)

    # Already in the same cluster — no merge needed.
    if parent_A == parent_B:
        return

    # Attach smaller-rank tree under larger-rank tree to keep tree shallow.
    if ranks[parent_A] > ranks[parent_B]:
        parents[parent_B] = parent_A
    elif ranks[parent_A] < ranks[parent_B]:
        parents[parent_A] = parent_B
    else:
        # Equal ranks: choose parent_B as new root and increment its rank.
        parents[parent_A] = parent_B
        ranks[parent_B] += 1


def group_elements_by_root(parents: dict[str, str]) -> list[list[str]]:
    """
    Collect all elements into clusters by their root representative.

    After all unions are done, call find() on every element so path
    compression gives us the true root (not just an intermediate ancestor),
    then bucket elements by that root.

    Time:  O(n) — one pass over all elements.
    Space: O(n) — the result dictionary.
    """
    clusters: dict[str, list[str]] = defaultdict(list)
    for element_id in parents:
        # find() here ensures we use the fully-compressed root.
        root = find(x=element_id, parents=parents)
        clusters[root].append(element_id)
    return list(clusters.values())


def element_clustering_union_find(
    elements: list[dict[str, str | list[str]]],
) -> list[list[str]]:
    """
    Main driver: initialise Union-Find, run pairwise unions, return clusters.

    Algorithm outline:
        1. Initialise every element as its own parent (n singleton sets).
        2. For every ordered pair (i, j) with i < j, check property overlap.
        3. If they share a property, union the two elements.
        4. Group all elements by their root to produce the final clusters.

    Time:  O(n²)  — dominated by the pairwise comparison loop.
    Space: O(n)   — for parents, ranks, and result dictionaries.
    """
    # Step 1: Each element starts in its own cluster (self-parenting).
    parents: dict[str, str] = {element["id"]: element["id"] for element in elements}
    ranks: dict[str, int] = {element["id"]: 0 for element in elements}
    n: int = len(elements)

    # Step 2 & 3: Compare every unique pair; union if they share a property.
    for i in range(n):
        for j in range(i + 1, n):
            if has_same_property(elements[i]["properties"], elements[j]["properties"]):
                union(
                    A=elements[i]["id"],
                    B=elements[j]["id"],
                    parents=parents,
                    ranks=ranks,
                )

    # Step 4: Gather elements into clusters by their root representative.
    return group_elements_by_root(parents=parents)


def solve():
    # -------------------------------------------------------------------------
    # Example from the problem statement:
    #   1 (p1,p2,p3) and 2 (p3,p4,p5) share p3  → same cluster
    #   3 (p6,p7,p8) shares nothing              → its own cluster
    # Expected output: two clusters, e.g. [["1","2"], ["3"]]
    # -------------------------------------------------------------------------
    elements = [
        {"id": "1", "properties": ["p1", "p2", "p3"]},
        {"id": "2", "properties": ["p3", "p4", "p5"]},
        {"id": "3", "properties": ["p6", "p7", "p8"]},
    ]
    print(f"Example result: {element_clustering_union_find(elements=elements)}")

    # -------------------------------------------------------------------------
    # Transitive chain test:
    #   A-B share p3, B-C share p5, C-D share p7  → all in one cluster
    #   E (x,y,z) shares nothing                  → its own cluster
    # Expected: [["A","B","C","D"], ["E"]]
    # -------------------------------------------------------------------------
    elements = [
        {"id": "A", "properties": ["p1", "p2", "p3"]},
        {"id": "B", "properties": ["p3", "p4", "p5"]},
        {"id": "C", "properties": ["p5", "p6", "p7"]},
        {"id": "D", "properties": ["p7", "p8", "p9"]},
        {"id": "E", "properties": ["x", "y", "z"]},
    ]
    print(f"Chain result:   {element_clustering_union_find(elements=elements)}")

    # -------------------------------------------------------------------------
    # Mixed test:
    #   A-B share c, B-D share e, D-E share g  → {A,B,D,E} one cluster
    #   C-F share z                             → {C,F} one cluster
    # Expected: [["A","B","D","E"], ["C","F"]]
    # -------------------------------------------------------------------------
    elements = [
        {"id": "A", "properties": ["a", "b", "c"]},
        {"id": "B", "properties": ["c", "d", "e"]},
        {"id": "C", "properties": ["x", "y", "z"]},
        {"id": "D", "properties": ["e", "f", "g"]},
        {"id": "E", "properties": ["g", "h", "i"]},
        {"id": "F", "properties": ["z", "j", "k"]},
    ]
    print(f"Mixed result:   {element_clustering_union_find(elements=elements)}")


solve()
