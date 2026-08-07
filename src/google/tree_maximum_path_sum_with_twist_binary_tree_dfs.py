r"""
Tree Maximum Path Sum... with a Twist

Difficulty: Hard (LC 124 base, frequently reported at Google)
Topic: Tree DFS, recursion design, global-vs-local state

Given the root of a binary tree, return the maximum path sum of any non-empty
path. A path is any sequence of nodes where consecutive nodes are connected by
an edge, and no node appears twice. The path does not need to pass through the
root.

Node values can be negative.

The twist: after computing the standard maximum path sum, also return the
maximum path sum among paths that contain an odd number of nodes. Return both
as a tuple:

    (max_any, max_odd_length)

Examples:

Example 1:
    Tree:
             -10
             /  \
            9    20
                /  \
               15   7

    Output: (42, 42)

    The maximum path is 15 -> 20 -> 7. Its sum is 42 and it contains three
    nodes, so it is also the maximum odd-length path.

Example 2:
    Tree:
            1
             \
             10

    Output: (11, 10)

    The maximum path is 1 -> 10, with sum 11, but it contains two nodes. The
    maximum path containing an odd number of nodes is the single node 10.

Example 3:
    Tree:
             1
            / \
           2   3

    Output: (6, 6)

    The maximum path is 2 -> 1 -> 3. Its sum is 6 and it contains three nodes.

Example 4:
    Tree:
            -3
            / \
          -2  -5

    Output: (-2, -2)

    All values are negative, so the best non-empty path is the single node -2.
    A one-node path has odd length.

Example 5:
    Tree:
                 5
               /   \
              4     8
             /     / \
            11    13  4
           /  \       \
          7    2       1

    Output: (48, 41)

    The maximum path is 7 -> 11 -> 4 -> 5 -> 8 -> 13. Its sum is 48, but
    it contains six nodes, so it has even length.

    The maximum odd-length path is 11 -> 4 -> 5 -> 8 -> 13. Its sum is 41
    and it contains five nodes.

Example 6:
    Tree:
                 5
               /   \
              4    -8
             /     / \
            11    13  4
           /  \       \
          7    2       1

    Output: (32, 25)

    The maximum path is 7 -> 11 -> 4 -> 5 -> -8 -> 13. Its sum is 32, but
    it contains six nodes, so it has even length.

    The maximum odd-length path is 11 -> 4 -> 5 -> -8 -> 13. Its sum is 25
    and it contains five nodes.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def tree_maximum_path_sum_with_global_max_sum(
    root: TreeNode | None,
) -> tuple[int, int]:

    if not root:
        return 0, 0

    max_sum: int | float = -math.inf
    max_odd_sum: int | float = -math.inf
    max_even_sum: int | float = -math.inf

    def dfs(
        node: TreeNode | None,
    ) -> tuple[int, int | float, int | float]:
        nonlocal max_sum, max_odd_sum, max_even_sum

        # No non-empty odd or even path exists here.
        if not node:
            return 0, -math.inf, -math.inf

        left_sum, left_odd_sum, left_even_sum = dfs(node.left)
        right_sum, right_odd_sum, right_even_sum = dfs(node.right)

        # Standard completed path through the current node.
        left_gain: int = max(0, left_sum)
        right_gain: int = max(0, right_sum)

        path_through_node: int = (
            node.value + left_gain + right_gain
        )

        max_sum = max(max_sum, path_through_node)

        # Best odd downward path starting at the current node.
        #
        # current node alone              → odd
        # node + even child path          → odd
        odd_down: int | float = max(
            node.value,
            node.value + left_even_sum,
            node.value + right_even_sum,
        )

        # Best even downward path starting at the current node.
        #
        # node + odd child path → even
        even_down: int | float = max(
            node.value + left_odd_sum,
            node.value + right_odd_sum,
        )

        # Completed odd paths through the current node:
        #
        # odd + node + odd   → odd
        # even + node + even → odd
        odd_path_through_node: int | float = max(
            odd_down,
            node.value + left_odd_sum + right_odd_sum,
            node.value + left_even_sum + right_even_sum,
        )

        # Completed even paths through the current node:
        #
        # odd + node + even → even
        # even + node + odd → even
        even_path_through_node: int | float = max(
            even_down,
            node.value + left_odd_sum + right_even_sum,
            node.value + left_even_sum + right_odd_sum,
        )

        # Globals store completed answers only.
        max_odd_sum = max(
            max_odd_sum,
            odd_path_through_node,
        )

        max_even_sum = max(
            max_even_sum,
            even_path_through_node,
        )

        # Your original standard downward-path selection.
        # Only one child branch may be returned to the parent.
        if left_sum < 0 and right_sum < 0:
            best_down = node.value
        elif left_sum < right_sum:
            best_down = node.value + right_sum
        else:
            best_down = node.value + left_sum

        # Return only connected downward paths.
        return best_down, odd_down, even_down

    dfs(root)

    return int(max_sum), int(max_odd_sum)


def tree_maximum_path_sum_without_global_max_sum(root: TreeNode | None) -> int:
    if not root:
        return 0
    
    def dfs(node: TreeNode | None) -> tuple[int, int | float]:
        # Return (best_downward_sum, best_sum_anywhere_in_this_subtree).
        if not node:
            return 0, -math.inf

        left_down, best_left = dfs(node.left)


        right_down, best_right = dfs(node.right)

        left_gain: int = max(0, left_down)
        right_gain: int = max(0, right_down)

        best_down: int = node.value + max(left_gain, right_gain)

        best_path_through: int = node.value + left_gain + right_gain

        best_of_all: int | float = max(best_path_through, best_left, best_right)

        return best_down, best_of_all 


    _, max_sum = dfs(root)

    return int(max_sum)
        






def solve():
    #             -10
    #             /  \
    #            9    20
    #                /  \
    #               15   7
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    # Expected: (42, 42)
    print(f"expected = (42, 42), result = {tree_maximum_path_sum_with_global_max_sum(root)}")
    # print(f"expected = (42, 42), result = {tree_maximum_path_sum_without_global_max_sum(root)}")

    # #            1
    # #             \
    # #             10
    # root = TreeNode(1)
    # root.right = TreeNode(10)

    # # Expected: (11, 10)
    # print(f"expected = (11, 10), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # #           -3
    # #           / \
    # #         -2  -5
    # root = TreeNode(-3)
    # root.left = TreeNode(-2)
    # root.right = TreeNode(-5)

    # # Expected: (-2, -2)
    # print(f"expected = (-2, -2), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # #                 5
    # #               /   \
    # #              4     8
    # #             /     / \
    # #            11    13  4
    # #           /  \       \
    # #          7    2       1
    # root = TreeNode(5)
    # root.left = TreeNode(4)
    # root.right = TreeNode(8)
    # root.left.left = TreeNode(11)
    # root.left.left.left = TreeNode(7)
    # root.left.left.right = TreeNode(2)
    # root.right.left = TreeNode(13)
    # root.right.right = TreeNode(4)
    # root.right.right.right = TreeNode(1)

    # # Expected: (48, 41)
    # print(f"expected = (48, 41), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # # Single positive node.
    # root = TreeNode(6)

    # # Expected: (6, 6)
    # print(f"expected = (6, 6), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # # Single negative node.
    # root = TreeNode(-7)

    # # Expected: (-7, -7)
    # print(f"expected = (-7, -7), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # # The best path is entirely below the root.
    # #             -100
    # #             /   \
    # #            1     10
    # #                 /  \
    # #                20   30
    # root = TreeNode(-100)
    # root.left = TreeNode(1)
    # root.right = TreeNode(10)
    # root.right.left = TreeNode(20)
    # root.right.right = TreeNode(30)

    # # Expected: (60, 60)
    # print(f"expected = (60, 60), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # # A four-node chain: the best overall path has even length.
    # #            1
    # #             \
    # #              2
    # #               \
    # #                3
    # #                 \
    # #                  4
    # root = TreeNode(1)
    # root.right = TreeNode(2)
    # root.right.right = TreeNode(3)
    # root.right.right.right = TreeNode(4)

    # # Expected: (10, 9)
    # print(f"expected = (10, 9), result = {tree_maximum_path_sum_with_global_max_sum(root)}")

    # # The best path rejects both negative child branches.
    # #            10
    # #           /  \
    # #         -1   -2
    # root = TreeNode(10)
    # root.left = TreeNode(-1)
    # root.right = TreeNode(-2)

    # # Expected: (10, 10)
    # print(f"expected = (10, 10), result = {tree_maximum_path_sum_with_global_max_sum(root)}")


# Uncomment after implementing tree_maximum_path_sum_with_global_max_sum().
solve()
