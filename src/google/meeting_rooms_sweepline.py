"""
Meeting Rooms II — Medium · Intervals / Heap / Sweep Line

Given an array of meeting time intervals where intervals[i] = [start_i, end_i],
return the minimum number of conference rooms required so all meetings can take place.

Example 1:
    Input:  [[0,30],[5,10],[15,20]]
    Output: 2

Example 2:
    Input:  [[7,10],[2,4]]
    Output: 1

Constraints:
    1 <= intervals.length <= 10⁴
    0 <= start_i < end_i <= 10⁶

---

Approach 1: Sweep Line (Difference Array)

The key insight is that we only care about how many meetings are active at any
point in time — we don't need to track which rooms hold which meetings.

Steps:
    1. Find the maximum end time across all intervals to size the sweep array.
    2. Create a difference array of length (max_end + 1), initialised to 0.
    3. For each meeting [start, end]:
           difference[start] += 1   # a room is occupied at start
           difference[end]   -= 1   # the room is freed at end
    4. Iterate through the difference array accumulating a running sum.
       The running sum at any index represents the number of rooms in use at
       that moment. Track the maximum value seen — that is the answer.

Why it works:
    A +1 at 'start' means one more concurrent meeting begins.
    A -1 at 'end' means one meeting ends (room freed).
    Summing the deltas left-to-right reconstructs the room occupancy at every
    time unit without explicitly simulating each time step per meeting.

Complexity:
    Time:  O(N + M)
               N = number of meetings (to build the difference array)
               M = max end time (to scan the difference array)
           In the worst case M >> N (e.g. one meeting [0, 10⁶]), so this
           approach is O(max_end).  Compare to the heap approach which is
           O(N log N).
    Space: O(M) for the difference array of size max_end + 1.

---

Approach 2: Sweep Line (Two Min-Heaps)

Store every start time in one min-heap and every end time in another. The top
of each heap is the next start or end event. If a start occurs before the next
end, a new room is needed. Otherwise, a meeting has ended and a room is freed.
When the times are equal, process the end first so the freed room can be reused.

Steps:
    1. Add all start times to start_heap and all end times to end_heap.
    2. Compare the next start time with the next end time.
    3. Process a start by increasing the active-room count, or process an end
       by decreasing it.
    4. Track the maximum active-room count seen during the sweep.

Complexity:
    Time:  O(N log N), because each of the N start and end times is pushed to
           and popped from a heap.
    Space: O(N), because the two heaps store 2N values in total.

---

Approach 3: Sweep Line (Two Sorted Arrays)

Separate the start and end times into two sorted arrays. Use one pointer for
the next start and another for the next end. Whichever time comes first is the
next event: a start occupies a room, while an end frees one. If a start and an
end have the same time, process the end first so that room can be reused.

Steps:
    1. Create and sort an array of all start times.
    2. Create and sort an array of all end times.
    3. Compare the values at the two pointers:
           start < end  -> process the start and increase the room count.
           start >= end -> process the end and decrease the room count.
    4. Track the maximum room count seen while processing all starts.

Complexity:
    Time:  O(N log N), because sorting both arrays dominates the O(N) sweep.
    Space: O(N), because the two arrays contain 2N values in total.

https://www.youtube.com/watch?v=FdzJmTCVyJU
"""

import heapq


def meeting_rooms_difference_array(meetings: list[tuple[int, int]]) -> int:
    # Step 1: Find the largest time so we know how large the array must be.
    max_end = 0

    for _, end in meetings:
        max_end = max(max_end, end)

    # Step 2: Create an array that records the change at each time.
    rolling_count_array: list[int] = [0] * (max_end + 1)

    # Step 3: A meeting uses a room at start and frees it at end.
    for start, end in meetings:
        rolling_count_array[start] += 1
        rolling_count_array[end] -= 1

    # Step 4: Build the prefix sum and remember the highest occupancy.
    max_room: int = 0
    rolling_count = 0

    for c in rolling_count_array:
        rolling_count += c
        max_room = max(max_room, rolling_count)

    return max_room


def meeting_rooms_min_heap(meetings: list[tuple[int, int]]) -> int:

    if len(meetings) == 0:
        return 0

    start_heap: list[int] = []
    end_heap: list[int] = []
    res, count = 0, 0

    # Step 1: Put all starts and ends into separate min-heaps.
    for start, end in meetings:
        heapq.heappush(start_heap, start)
        heapq.heappush(end_heap, end)

    # Steps 2-4: Process events in chronological order and track the maximum
    # number of rooms simultaneously in use.
    while start_heap:
        # A start before the next end requires another room.
        if start_heap[0] < end_heap[0]:
            count += 1
            heapq.heappop(start_heap)
        else:
            # Process an end first when times are equal, allowing room reuse.
            count -= 1
            heapq.heappop(end_heap)

        res = max(res, count)

    return res


def meeting_rooms_sorted_array(meetings: list[tuple[int, int]]) -> int:
    # Steps 1-2: Separate and sort all start and end times.
    start_array: list[int] = sorted([s for s, e in meetings])
    end_array: list[int] = sorted([e for s, e in meetings])

    start_index, end_index = 0, 0
    count, result = 0, 0

    # Steps 3-4: Process events chronologically until every start is handled.
    while start_index < len(start_array):
        # The next event is a start, so another room is occupied.
        if start_array[start_index] < end_array[end_index]:
            count += 1
            start_index += 1
        else:
            # Process an end first on a tie so its room can be reused.
            # The same start is compared again on the next iteration, which
            # naturally drains all earlier end times without an inner loop.
            count -= 1
            end_index += 1

        # count is current occupancy; result is the peak occupancy.
        result = max(result, count)

    return result


def solve():
    meetings:list[tuple[int, int]] = [[0,30],[5,10],[15,20]]
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")
   
    meetings: list[tuple[int, int]] = [[1,5],[6,10],[11,15]]
    # Expected: 1
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

    meetings: list[tuple[int, int]] = [[1,10],[2,10],[3,10]]
    # Expected: 3
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

    meetings: list[tuple[int, int]] = [[1,5],[5,10]]
    # Expected: 1
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

    meetings: list[tuple[int, int]] = [[5,10]]
    # Expected: 1
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

    meetings: list[tuple[int, int]] = [[1,20],[5,10],[6,8]]
    # Expected: 3
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

    meetings: list[tuple[int, int]] = [[0,10],[1,5],[2,6],[3,8],[9,12]]
    # Expected: 4
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_difference_array(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_min_heap(meetings=meetings)} ")
    print(f"meeting rooms needed for meetings {meetings} is {meeting_rooms_sorted_array(meetings=meetings)} ")

solve()
