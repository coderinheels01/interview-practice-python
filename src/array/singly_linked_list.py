"""
Design Singly Linked List

Difficulty: Easy
Company Tags

Design a Singly Linked List class.

Approach:
    Store the values in a Python list and use its built-in indexed operations.
    Reading by index is constant time, but inserting at the head or removing an
    element requires shifting the elements that follow it. getValues returns a
    copy so callers cannot modify the internal list directly.

Time and auxiliary space complexity (n = number of stored values):
    - LinkedList():   O(1) time, O(1) space.
    - get(i):         O(1) time, O(1) space.
    - insertHead():   O(n) time, O(1) auxiliary space.
    - insertTail():   O(1) amortized time, O(1) auxiliary space.
                      A list resize can occasionally take O(n) time.
    - remove(i):      O(n) time in the worst case, O(1) auxiliary space.
                      Elements after index i must shift one position left.
    - getValues():    O(n) time, O(n) space because it returns a copy.

Reference:
    https://neetcode.io/courses/dsa-for-beginners/5

Your LinkedList class should support the following operations:

- LinkedList() initializes an empty linked list.
- int get(int i) returns the value of the ith node (0-indexed). If the index is
  out of bounds, return -1.
- void insertHead(int val) inserts a node with val at the head of the list.
- void insertTail(int val) inserts a node with val at the tail of the list.
- bool remove(int i) removes the ith node (0-indexed). If the index is out of
  bounds, return false; otherwise, return true.
- int[] getValues() returns an array containing all values in the linked list,
  ordered from head to tail.

Example 1:
    Input:
        ["insertHead", 1, "insertTail", 2, "insertHead", 0, "remove", 1,
         "getValues"]

    Output:
        [null, null, null, true, [0, 2]]

Example 2:
    Input:
        ["insertHead", 1, "insertHead", 2, "get", 5]

    Output:
        [null, null, -1]

Note:
    The index i provided to get(int i) and remove(int i) is guaranteed to be
    greater than or equal to 0.
"""
from dataclasses import dataclass, field

@dataclass
class LinkedList:
    linked_list: list[int] = field(default_factory=list, init= False)

    def is_index_valid(self, index:int) -> bool:
        return index < len(self.linked_list)

    def get(self, index: int) -> int:
        if not self.is_index_valid(index=index):
            return -1
        return self.linked_list[index]
    
    def insertHead(self, val:int) -> None:
        self.linked_list.insert(0, val)
    
    def insertTail(self, val:int) -> None:
        self.linked_list.append(val)
    
    def remove(self, index:int) -> bool:
        if not self.is_index_valid(index=index):
            return False

        self.linked_list.pop(index)

        return True

    def getValues(self) -> list[int]:
        return self.linked_list.copy()
        

def solve():
    # Example 1: insert at the head and tail, then remove the middle node.
    linked_list = LinkedList()
    linked_list.insertHead(1)
    linked_list.insertTail(2)
    linked_list.insertHead(0)
    print(f"expected remove(1) = True, result = {linked_list.remove(1)}")
    print(f"expected values = [0, 2], result = {linked_list.getValues()}")

    # Example 2: getting an index outside the list returns -1.
    linked_list = LinkedList()
    linked_list.insertHead(1)
    linked_list.insertHead(2)
    print(f"expected get(5) = -1, result = {linked_list.get(5)}")

    # An empty list contains no values.
    linked_list = LinkedList()
    print(f"expected values = [], result = {linked_list.getValues()}")
    print(f"expected get(0) = -1, result = {linked_list.get(0)}")
    print(f"expected remove(0) = False, result = {linked_list.remove(0)}")

    # Insert several tail values and retrieve the first, middle, and last nodes.
    linked_list = LinkedList()
    linked_list.insertTail(10)
    linked_list.insertTail(20)
    linked_list.insertTail(30)
    print(f"expected get(0) = 10, result = {linked_list.get(0)}")
    print(f"expected get(1) = 20, result = {linked_list.get(1)}")
    print(f"expected get(2) = 30, result = {linked_list.get(2)}")

    # Remove the head and then the tail.
    print(f"expected remove(0) = True, result = {linked_list.remove(0)}")
    print(f"expected values = [20, 30], result = {linked_list.getValues()}")
    print(f"expected remove(1) = True, result = {linked_list.remove(1)}")
    print(f"expected values = [20], result = {linked_list.getValues()}")

    # Removing an out-of-bounds index leaves the list unchanged.
    print(f"expected remove(5) = False, result = {linked_list.remove(5)}")
    print(f"expected values = [20], result = {linked_list.getValues()}")

solve()

