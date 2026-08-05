"""
Snapshot Array

Difficulty: Medium
Topics: Binary Search, Design

Implement a snapshot-able array:

- SnapshotArray(length) — create an array of length, with all values set to 0.
- set(index, val) — set arr[index] = val.
- snap() — capture the array's current state and return its snap_id.
  The first snap_id is 0, and it increments with each call.
- get(index, snap_id) — return the value at index at the time that snapshot
  was taken.

Example:
    snap_arr = SnapshotArray(3)
    snap_arr.set(0, 5)
    snap_arr.snap()          # Returns 0
    snap_arr.set(0, 6)
    snap_arr.get(0, 0)      # Returns 5; snapshot 0 is unchanged
    snap_arr.snap()          # Returns 1
    snap_arr.get(0, 1)      # Returns 6

Constraints:
    - 1 <= length <= 5 * 10^4
    - 0 <= index < length
    - 0 <= val <= 10^9
    - At most 5 * 10^4 total calls are made to set, snap, and get.
    - Every get call uses a valid snap_id.
"""
from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class SnapshotArray:
    """
    Store only changes instead of copying the entire array at every snapshot.

    Approach:
        Keep a history list for each array index. Every history entry is a
        (snap_id, value) tuple. Since snapshot IDs only increase, each history
        remains sorted by snap_id.

        set() records a change under the current snapshot ID. If the same index
        is set again before snap(), its latest entry is replaced. snap() returns
        the current ID and advances to the next one. get() uses binary search to
        find the latest entry whose ID is less than or equal to the requested ID.

    Time complexity:
        Initialization: O(N), where N is the array size.
        set: O(1).
        snap: O(1).
        get: O(log K), where K is the number of recorded changes for the
        requested index.

    Space complexity:
        O(N + C), where N is the array size and C is the total number of
        recorded changes across all indexes.
    """

    # Step 1: Store the requested size and the internal snapshot state.
    size: int
    snap_id: int = field(default=0, init=False)
    snapshot_history_map: dict[int, list[tuple[int,int]]]  = field(default_factory=dict, init=False)

    def validate_index(self, index: int):
        # Reject indexes outside the valid range from 0 through size - 1.
        if index > self.size-1 or index < 0:
            raise IndexError(f"index {index} is out of bound fo array of size {self.size}")
    
    def validate_snap_id(self,snap_id:int):
        # Reject snapshot IDs outside the range created by snap().
        if snap_id < 0 or snap_id > self.snap_id:
            raise IndexError(f"snap id {snap_id} is not valid")

    def increment_snap_id(self) -> int:
        self.snap_id += 1
        return self.snap_id

    
    def dupe_check(self, snap_array:list[tuple[int, int]]) -> bool:
        # Check whether this index was already changed under the current ID.
        last_index: int = len(snap_array) - 1

        last_snap_id, _ = snap_array[last_index]

        return last_snap_id == self.snap_id

    def set(self, index:int, value: int) -> None:
        # Step 2: Record this value under the current snapshot ID.
        self.validate_index(index)
        last_index:int = len( self.snapshot_history_map[index]) -1

        # Replace a value set during the same snapshot; otherwise append a new
        # change, which keeps this index's history sorted by snapshot ID.
        if last_index >= 0 and self.dupe_check( self.snapshot_history_map[index]):
             self.snapshot_history_map[index][last_index] = (self.snap_id, value) 
             
        else:
            self.snapshot_history_map[index].append((self.snap_id, value))
        

    
    def snap(self) -> int:
        # Step 3: Return the ID being captured, then advance for future changes.
        old_snap_id = self.snap_id
        self.increment_snap_id()
        return old_snap_id

    def get(self, index:int, snap_id:int) -> int:
        # Step 4: Search this index's history for the value at snap_id.
        self.validate_index(index)
        self.validate_snap_id(snap_id)
        snap_array:list[tuple[int, int]] = self.snapshot_history_map[index]

        def binary_search(left:int ,right:int) -> int:

            # When the search ends, right points to the latest earlier entry.
            # If there is no earlier entry, this index still has value 0.
            if left > right:
                return snap_array[right][1] if right >= 0 else 0


            mid:int  = left + (right - left) // 2 

            mid_snap_id, mid_value =  snap_array[mid]


            if mid_snap_id == snap_id:
                return mid_value

            # Search left if this entry is too new. Otherwise, search right for
            # a closer entry that is still not newer than the requested ID.
            if snap_id < mid_snap_id :
                 return binary_search(left, mid-1)
            else: 
                return binary_search(mid+1, right)

        # Begin with the complete history for this index.
        return binary_search(0, len(snap_array) -1)
                 



    def __post_init__(self) -> None:
        # Step 1 continued: Each index starts with an empty change history.
        # An empty history represents the initial value 0.
        self.snapshot_history_map = {i: [] for i in range(self.size) }
        


def solve():
    # Basic example
    snap_arr = SnapshotArray(3)
    snap_arr.set(0, 5)
    print(snap_arr.snap())       # Expected: 0
    snap_arr.set(0, 6)
    print(snap_arr.get(0, 0))   # Expected: 5
    print(snap_arr.snap())       # Expected: 1
    print(snap_arr.get(0, 1))   # Expected: 6

    # An index that was never set keeps its initial value of 0.
    snap_arr = SnapshotArray(3)
    print(snap_arr.snap())       # Expected: 0
    print(snap_arr.get(0, 0))   # Expected: 0
    print(snap_arr.get(2, 0))   # Expected: 0

    # Multiple sets before one snap keep only the latest value.
    snap_arr = SnapshotArray(2)
    snap_arr.set(1, 5)
    snap_arr.set(1, 6)
    snap_arr.set(1, 7)
    print(snap_arr.snap())       # Expected: 0
    print(snap_arr.get(1, 0))   # Expected: 7

    # Consecutive snaps carry an unchanged value forward.
    snap_arr = SnapshotArray(1)
    snap_arr.set(0, 5)
    print(snap_arr.snap())       # Expected: 0
    print(snap_arr.snap())       # Expected: 1
    print(snap_arr.snap())       # Expected: 2
    print(snap_arr.get(0, 0))   # Expected: 5
    print(snap_arr.get(0, 1))   # Expected: 5
    print(snap_arr.get(0, 2))   # Expected: 5

    # A get between two changes returns the most recent earlier value.
    snap_arr = SnapshotArray(1)
    snap_arr.set(0, 5)
    print(snap_arr.snap())       # Expected: 0
    print(snap_arr.snap())       # Expected: 1
    print(snap_arr.snap())       # Expected: 2
    snap_arr.set(0, 8)
    print(snap_arr.snap())       # Expected: 3
    print(snap_arr.get(0, 1))   # Expected: 5
    print(snap_arr.get(0, 2))   # Expected: 5
    print(snap_arr.get(0, 3))   # Expected: 8

    # Changes at different indexes remain independent.
    snap_arr = SnapshotArray(3)
    snap_arr.set(0, 10)
    snap_arr.set(2, 30)
    print(snap_arr.snap())       # Expected: 0
    snap_arr.set(1, 20)
    print(snap_arr.snap())       # Expected: 1
    print(snap_arr.get(0, 1))   # Expected: 10
    print(snap_arr.get(1, 0))   # Expected: 0
    print(snap_arr.get(1, 1))   # Expected: 20
    print(snap_arr.get(2, 1))   # Expected: 30

    # Constraint boundary values work.
    snap_arr = SnapshotArray(1)
    snap_arr.set(0, 10**9)
    print(snap_arr.snap())          # Expected: 0
    print(snap_arr.get(0, 0))      # Expected: 1000000000


solve()
