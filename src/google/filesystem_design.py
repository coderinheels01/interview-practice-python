# =============================================================================
# Question: File System Design
# =============================================================================
# Design an in-memory filesystem that supports the following operations:
#
#   mkdir(path)          — create a directory
#   addFile(path, size)  — create or overwrite a file with a given size
#   getSize(path)        — return the size of a file or directory
#   ls(path)             — list children
#
# Important requirement: getSize(path) must run in O(1) time for both files
# and directories. The size of a directory is defined as the sum of the sizes
# of all files recursively contained inside it.
#
# Design all data structures and implement these operations.
# =============================================================================
#
# Approach:
#   - Each node (file or directory) stores its cumulative size.
#   - A flat path_map (dict) maps full path strings → Node for O(1) getSize.
#   - On addFile, we compute the size delta (new_size - old_size) and propagate
#     it upward through every ancestor directory node. This keeps all ancestor
#     sizes up to date so getSize is always O(1).
#
# Complexity:
#   - mkdir(path):
#       Time:  O(d)  — d = depth of path (number of path components)
#       Space: O(d)  — new nodes and path_map entries per component
#
#   - addFile(path, size):
#       Time:  O(d)  — traverse ancestors to propagate the size delta
#       Space: O(1)  — one new node (or update existing), one path_map entry
#
#   - getSize(path):
#       Time:  O(1)  — direct hash map lookup
#       Space: O(1)
#
#   - ls(path):
#       Time:  O(k)  — k = number of direct children (to build the result list)
#       Space: O(k)
#
#   Overall space: O(N) where N is total number of nodes (files + directories)
# =============================================================================

from __future__ import annotations  # noqa: F404
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Node:
    name: str
    is_file: bool
    size: int = 0  # for files: file size; for dirs: cumulative size of all descendants
    children: dict[str, Node] = field(default_factory=dict)


class FileSystem:
    def __init__(self):
        self.root = Node(name="/", is_file=False)
        # Maps full absolute path → Node for O(1) access in getSize
        self.path_map: dict[str, Node] = defaultdict(Node)

    def ls(self, path="") -> list[str]:
        """List direct children of the node at path. O(k) where k = # children."""
        parts: list[str] = [p for p in path.split("/") if p]

        prev = self.root
        for part in parts:
            if part in prev.children:
                prev = prev.children[part]

        return list(prev.children.keys())

    def mkdir(self, path: str = ""):
        """
        Create a directory (and all intermediate directories) at path.
        Idempotent — does nothing if the directory already exists.
        Time: O(d), Space: O(d)
        """
        parts: list[str] = [p for p in path.split("/") if p]

        prev: Node = self.root
        current_path: str = ""

        for part in parts:
            current_path += f"/{part}"
            if part not in prev.children:
                prev.children[part] = Node(name=part, is_file=False)
                self.path_map[current_path] = prev.children[part]
            prev = prev.children[part]

    def addFile(self, size: int, path: str = ""):
        """
        Create or overwrite a file at path with the given size.
        Propagates the size delta up through all ancestor directories so that
        every directory's .size always reflects the recursive total.
        Time: O(d), Space: O(1) amortized
        """
        parts: list[str] = [p for p in path.split("/") if p]
        n: int = len(parts)

        # Compute delta: if file already exists, only add the difference
        old_size: int = self.path_map.get(path, 0)
        delta = size - old_size

        prev = self.root

        # Walk ancestors (all but the last component), updating their sizes
        for i in range(n - 1):
            if parts[i] not in prev.children:
                raise FileNotFoundError("Parent directory does not exist")
            prev.children[parts[i]].size += delta
            prev = prev.children[parts[i]]

        # Create or update the file node itself
        file_node = prev.children.get(
            parts[n - 1], Node(name=parts[n - 1], is_file=True)
        )
        file_node.size += delta
        prev.children[parts[n - 1]] = file_node
        self.path_map[path] = file_node

    def getSize(self, path: str = "") -> int:
        """
        Return the size of a file or directory in O(1) via the path_map lookup.
        For directories, this is the sum of all descendant file sizes.
        Time: O(1), Space: O(1)
        """
        node: Node = self.path_map.get(path)
        if node is None:
            raise FileNotFoundError("{path} doesn't exist")
        return node.size


def solve():
    path1: str = "/home/user/photos"
    fs: FileSystem = FileSystem()
    fs.mkdir(path=path1)

    path2: str = "/home/user/photos2"
    fs.mkdir(path=path2)

    path3: str = f"{path1}/file.txt"
    fs.addFile(path=path3, size=100)
    path4: str = f"{path1}/test.txt"
    fs.addFile(path=path4, size=200)
    path5: str = f"{path2}/test1.txt"
    fs.addFile(path=path5, size=500)
    path6: str = f"{path2}/test2.txt"
    fs.addFile(path=path6, size=200)

    print(f"ls path = {path1} {fs.ls(path=path1)} and size is {fs.getSize(path=path1)}")
    print(f"ls path = {path2} {fs.ls(path=path2)} and size is {fs.getSize(path=path2)}")
    print(f"ls path = {path3} {fs.ls(path=path3)} and size is {fs.getSize(path=path3)}")


solve()
