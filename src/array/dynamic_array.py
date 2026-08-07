r"""
Design a Dynamic Array

Design a Dynamic Array (also known as a resizable array), such as an ArrayList
in Java or a vector in C++.

Your DynamicArray class should support the following operations:

- DynamicArray(int capacity) initializes an empty array with a capacity of
  capacity, where capacity > 0.
- int get(int i) returns the element at index i. Assume index i is valid.
- void set(int i, int n) sets the element at index i to n. Assume index i is
  valid.
- void pushback(int n) pushes n to the end of the array.
- int popback() pops and returns the element at the end of the array. Assume
  the array is non-empty.
- void resize() doubles the capacity of the array.
- int getSize() returns the number of elements in the array.
- int getCapacity() returns the capacity of the array.

If pushback(int n) is called when the array is full, resize() the array first.

Example 1:
    Input:
        ["Array", 1, "getSize", "getCapacity"]

    Output:
        [null, 0, 1]

Example 2:
    Input:
        ["Array", 1, "pushback", 1, "getCapacity", "pushback", 2,
         "getCapacity"]

    Output:
        [null, null, 1, null, 2]

Example 3:
    Input:
        ["Array", 1, "getSize", "getCapacity", "pushback", 1, "getSize",
         "getCapacity", "pushback", 2, "getSize", "getCapacity", "get", 1,
         "set", 1, 3, "get", 1, "popback", "getSize", "getCapacity"]

    Output:
        [null, 0, 1, null, 1, 1, null, 2, 2, 2, null, 3, 3, 1, 2]

Note:
    The index i provided to get(int i) and set(int i) is guaranteed to satisfy:

        0 <= i < number of elements in the array
"""

from dataclasses import dataclass, field

@dataclass
class DynamicArray:
    capacity: int
    dynamic_array:list[int] = field(default_factory= list, init= False)
    size: int = field(default= 0, init= False)


    def increment_size(self):
        if self.capacity >= self.size:
            self.size += 1
        else:
            raise OverflowError("array is at capacity")
    
    def decrement_size(self):
        if self.size > 0:
            self.size -= 1

    def validate_index(self, index:int):
        return 0<= index < self.capacity

    def is_full(self):
        return self.capacity - 1 == self.size 

    def get(self, i:int) -> int:
        self.validate_index(index=i)
        return self.dynamic_array[i]

    def set(self, i: int, n: int) -> None:
        self.validate_index(index=i)
        self.dynamic_array[i] = n
        self.increment_size()

    def pushback(self, n: int) -> None:
        if self.is_full():
            self.resize()
        index: int = len(self.dynamic_array) - 1
        self.dynamic_array[index] = n
        self.increment_size()


    def popback(self) -> int:
        index:int = len(self.dynamic_array) -1
        value:int = self.dynamic_array[index]
        self.dynamic_array[index] = None
        return value
    
    def resize(self) -> None:
        self.dynamic_array.extend([None] * self.capacity)
        self.capacity = len(self.dynamic_array)

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

    def __post_init__(self):
        self.dynamic_array = [None] * self.capacity


def solve():
    # Example 1: new array starts empty with the requested capacity.
    dynamic_array = DynamicArray(1)
    print(f"expected size = 0, result = {dynamic_array.getSize()}")
    print(f"expected capacity = 1, result = {dynamic_array.getCapacity()}")

    # Example 2: pushing into a full array doubles its capacity.
    dynamic_array = DynamicArray(1)
    dynamic_array.pushback(1)
    print(f"expected capacity = 1, result = {dynamic_array.getCapacity()}")
    dynamic_array.pushback(2)
    print(f"expected capacity = 2, result = {dynamic_array.getCapacity()}")

    # Example 3: size, get, set, popback, and resize work together.
    dynamic_array = DynamicArray(1)
    print(f"expected size = 0, result = {dynamic_array.getSize()}")
    print(f"expected capacity = 1, result = {dynamic_array.getCapacity()}")

    dynamic_array.pushback(1)
    print(f"expected size = 1, result = {dynamic_array.getSize()}")
    print(f"expected capacity = 1, result = {dynamic_array.getCapacity()}")

    dynamic_array.pushback(2)
    print(f"expected size = 2, result = {dynamic_array.getSize()}")
    print(f"expected capacity = 2, result = {dynamic_array.getCapacity()}")
    print(f"expected get(1) = 2, result = {dynamic_array.get(1)}")

    dynamic_array.set(1, 3)
    print(f"expected get(1) = 3, result = {dynamic_array.get(1)}")
    print(f"expected popback = 3, result = {dynamic_array.popback()}")
    print(f"expected size = 1, result = {dynamic_array.getSize()}")
    print(f"expected capacity = 2, result = {dynamic_array.getCapacity()}")

    # Popping removes elements in last-in, first-out order.
    dynamic_array = DynamicArray(2)
    dynamic_array.pushback(10)
    dynamic_array.pushback(20)
    print(f"expected popback = 20, result = {dynamic_array.popback()}")
    print(f"expected popback = 10, result = {dynamic_array.popback()}")
    print(f"expected size = 0, result = {dynamic_array.getSize()}")

solve()
