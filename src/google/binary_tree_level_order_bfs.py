from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int = 0
    left: TreeNode | None = None
    right: TreeNode | None = None


def level_order(root: TreeNode):
    """
    Binary Tree Level Order Traversal (BFS).

    Visits all nodes level by level from left to right, printing each level
    on its own line.

    Approach:
      - Use a queue (deque) to process nodes in FIFO order.
      - Each queue entry is a (node, level) tuple so we know when the level
        changes without needing a sentinel or two-queue technique.

    Steps:
      1. Initialise the queue with the root node at level 0.
      2. Dequeue the front node and its level.
      3. If the level has increased since the last printed node, print a
         newline and update current_level.
      4. Print the node's value (space-separated, same line as siblings).
      5. Enqueue the left child (if it exists) at level + 1.
      6. Enqueue the right child (if it exists) at level + 1.
      7. Repeat from step 2 until the queue is empty.
      8. Print a final newline to terminate the last level's output.

    Time Complexity : O(n) — every node is enqueued and dequeued exactly once.
    Space Complexity: O(n) — the queue holds at most O(w) nodes at a time,
                      where w is the maximum width of the tree. In the worst
                      case (a perfect binary tree) the last level has n/2
                      nodes, so w = O(n).
    """
    current_level: int = 0
    # Step 1: seed the queue with the root at level 0
    queue: deque[tuple[TreeNode, int]] = deque([(root, current_level)])

    while queue:
        # Step 2: process the next node in FIFO order
        node, level = queue.popleft()

        # Step 3: detect a level change and start a new output line
        if current_level != level:
            print("")
            current_level = level

        # Step 4: print the current node's value on the current line
        print(f"{node.val} ", end="")

        # Steps 5-6: enqueue children with their level
        if node.left:
            queue.append((node.left, level + 1))
        if node.right:
            queue.append((node.right, level + 1))

    # Step 8: terminate the last level's output line
    print()


def solve():
    """
    Build the example tree and run level-order traversal.

    Tree structure:
            3
           / \
          9  20
            /  \
           15   7

    Expected output:
      3
      9 20
      15 7
    """
    root: TreeNode = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    level_order(root)


solve()
