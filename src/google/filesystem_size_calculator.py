"""
=============================================================================
QUESTION: Filesystem Size Calculator
=============================================================================
Goal:
    Given a filesystem represented as a dictionary of entities, calculate
    the total size of any entity by its ID.

Input:
    - A dictionary mapping EntityId (int) to Entity objects.
    - Each Entity is either:
        - FILE: has a name and a size (int)
        - DIRECTORY: has a name and a list of child EntityIds (no direct size)
    - An EntityId to query.

Desired Output:
    The total size of the entity:
        - For a FILE: return its size directly.
        - For a DIRECTORY: return the sum of sizes of all its descendants
          (recursively).

Key Requirements:
    - Directories do not have a size field — their size must be computed
      from their children.
    - The filesystem can be arbitrarily deep (nested directories).
    - Memoize computed directory sizes to avoid redundant work if the same
      directory is queried multiple times.

Example:
    filesystem = {
        1: FILE  "file2"  size=200
        2: FILE  "file"   size=100
        3: FILE  "file3"  size=300
        4: DIRECTORY "dir" children=[2, 1]
    }

    find_file_size(4) → 300  (100 + 200)
    find_file_size(1) → 200
    find_file_size(2) → 100

Approach — Recursive DFS with Memoization:
    - If the entity is a FILE, return its size directly.
    - If the entity is a DIRECTORY, recurse into each child and sum their
      sizes. Cache the result back onto the entity so repeated queries are O(1).

Time Complexity:
    - First call on a directory: O(n) where n is the number of descendants.
    - Subsequent calls on the same directory: O(1) due to memoization.

Space Complexity:
    - O(d) where d is the maximum depth of the directory tree (call stack).
=============================================================================
"""

from dataclasses import dataclass
from typing import Literal

# Type alias for clarity — entity IDs are just ints.
EntityId = int

# An entity is either a FILE or a DIRECTORY.
EntityType = Literal["FILE", "DIRECTORY"]


@dataclass
class Entity:
    type: EntityType
    name: str
    # FILES have a size; DIRECTORIES compute theirs from children.
    # After computing, a directory's size is cached here too.
    size: int | None = None
    # DIRECTORIES have a list of child entity IDs; FILES do not.
    children: list[int] | None = None


def find_file_size(id: EntityId, filesystem: dict[EntityId, Entity]) -> int:
    # Base case: entity already has a size (FILE, or previously computed DIRECTORY).
    # This also serves as the memoization check for directories.
    if filesystem[id].size is not None:
        return filesystem[id].size

    # If we reach here, it's a DIRECTORY with no cached size yet.
    assert filesystem[id].children is not None

    # Recursively sum the sizes of all children.
    size: int = 0
    for child in filesystem[id].children:
        size += find_file_size(child, filesystem)

    # Memoize: store the computed size so repeated calls are O(1).
    filesystem[id].size = size
    return size


def solve():
    filesystem: dict[EntityId, Entity] = {
        1: Entity(type="FILE", name="file2", size=200),
        2: Entity(type="FILE", name="file", size=100),
        3: Entity(type="FILE", name="file3", size=300),
        # dir contains file (id=2, size=100) and file2 (id=1, size=200) → total 300
        4: Entity(type="DIRECTORY", name="dir", children=[2, 1]),
    }

    print(f"file size for id - 1 is {find_file_size(id=1, filesystem=filesystem)}")
    print(f"file size for id - 2 is {find_file_size(id=2, filesystem=filesystem)}")
    print(f"file size for id - 4 is {find_file_size(id=4, filesystem=filesystem)}")
    # Second call on id=4: hits the memoized size, no recursion needed.
    print(f"file size for id - 4 is {find_file_size(id=4, filesystem=filesystem)}")


solve()
