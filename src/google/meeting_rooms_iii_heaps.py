"""
Meeting Rooms III (LeetCode 2402)
Difficulty: Hard | Topic: Intervals + Heaps / Simulation

Problem:
    You're given n rooms numbered 0 to n - 1, and meetings[i] = [start_i, end_i)
    represents a meeting held during that half-closed interval. All start times
    are unique.

    Allocate meetings by these rules:
        1. Each meeting goes into the unused room with the lowest number.
        2. If no room is free, the meeting is delayed until one opens up; it
           keeps its original duration.
        3. When a room frees up, the delayed meeting with the earliest original
           start time gets it first.

    Return the room number that held the most meetings. If there is a tie,
    return the lowest room number.

Example 1:
    Input: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
    Output: 0

    Meeting [0,10] goes to room 0, [1,5] goes to room 1, [2,7] is
    delayed and goes to room 1 at t = 5 (running from 5 to 10), and [3,4]
    is delayed and goes to room 0 at t = 10. Both rooms held two meetings,
    so return 0.

Example 2:
    Input: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
    Output: 1

    Meeting [1,20] goes to room 0, [2,10] goes to room 1, and [3,5] goes
    to room 2. Meeting [4,9] is delayed until room 2 becomes free at t = 5
    and runs from 5 to 10. Meeting [6,8] is delayed until rooms 1 and 2
    become free at t = 10; it goes to the lower-numbered room 1 and runs
    from 10 to 12. Room 0 held one meeting, while rooms 1 and 2 each held
    two, so return room 1.

Constraints:
    1 <= n <= 100
    1 <= meetings.length <= 10^5
    0 <= start_i < end_i <= 5 * 10^5
    All start_i values are unique.
"""

import heapq


"""
Approach: Sort meetings + simulate room usage with two min-heaps

Data structures:
    1. free_rooms is a min-heap of available room numbers. Its smallest value
       is always the lowest-numbered room that can accept a meeting.

    2. end_heap is a min-heap of (end_time, room_number) pairs for rooms that
       are currently occupied. Python compares tuples from left to right, so
       the room that becomes free earliest is at the top. If multiple rooms
       become free at the same time, the lowest-numbered room comes first.

    3. occupied_rooms is an array where occupied_rooms[i] stores the number of
       meetings assigned to room i. The array index is also the room number.

Algorithm:
    1. Sort meetings by their original start times so they are processed in
       chronological order.
    2. Before assigning a meeting [start, end], remove every room from end_heap
       whose end time is less than or equal to start. Push each released room
       number into free_rooms.
    3. If free_rooms is not empty, pop its smallest room number and schedule the
       meeting at its original time. Push (end, room_number) into end_heap.
    4. If no room is free, pop the (end_time, room_number) pair at the top of
       end_heap. This is the room that becomes available first. Delay the
       meeting until end_time while preserving its original duration:

           new_end_time = end_time + (original_end - original_start)

       Push (new_end_time, room_number) back into end_heap.
    5. Increment the selected room's count in occupied_rooms after every
       assignment.
    6. Return the index of the largest count. list.index() returns the first
       matching index, so a tie is resolved in favor of the lowest room number.

Why tuple ordering works:
       end_heap stores (end_time, room_number). Python compares the end times
       first and the room numbers second. Therefore, the room that becomes free
       earliest is selected, and equal end times favor the lower room number.

Time Complexity: O(M log M + M log N)
    M = the number of meetings.
    N = the number of rooms.
    Sorting M meetings costs O(M log M). Every meeting is pushed into and popped
    from a heap at most a constant number of times. Each heap contains at most N
    rooms, so the heap operations cost O(M log N) in total.

Space Complexity: O(M + N)
    M = the number of meetings stored in the sorted meetings list.
    N = the number of room entries stored across free_rooms, end_heap, and
    occupied_rooms.

https://www.youtube.com/watch?v=2VLwjvODQbA
"""


def most_booked(n: int, meetings: list[list[int]]) -> int:
    """Return the room that hosts the most meetings."""

    end_heap: list[tuple[int, int]] = []  # [(end_time, room)]
    occupied_rooms: list[int] = [0] * n
    start_index: int = 0

    free_rooms = list(
        range(n)
    )  # 0, 1, 2, 3 ... n, no need to heapify if the array is sorted can use heap operations

    meetings = sorted(meetings, key=lambda meeting: meeting[0])

    for start, end in meetings:
        # finished meetings, so free room
        while end_heap and end_heap[0][0] <= start:
            _, room = heapq.heappop(end_heap)
            heapq.heappush(free_rooms, room)

        # if there is free room, schedule it
        if free_rooms:
            room: int = heapq.heappop(free_rooms)
            heapq.heappush(end_heap, (end, room))
            occupied_rooms[room] += 1
            start_index += 1
        elif (
            end_heap
        ):  # if there is no free room, pop from end heap and shift the end time
            min_end, room = heapq.heappop(end_heap)
            heapq.heappush(end_heap, (min_end + (end - start), room))
            occupied_rooms[room] += 1
            start_index += 1

    return occupied_rooms.index(
        max(occupied_rooms)
    )  # return room number of max number of meetings scheduled


def solve():
    n: int = 2
    meetings: list[list[int]] = [[0, 10], [1, 5], [2, 7], [3, 4]]
    # Expected: 0
    print(
        f"most booked room for n ={n} for meetings = {meetings} is result {most_booked(n, meetings)}"
    )

    n: int = 3
    meetings: list[list[int]] = [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]
    # Expected: 1
    print(
        f"most booked room for n ={n} for meetings = {meetings} is result {most_booked(n, meetings)}"
    )

    n: int = 1
    meetings: list[list[int]] = [[0, 5], [10, 15], [20, 25]]
    # Expected: 0
    print(
        f"most booked room for n ={n} for meetings = {meetings} is result {most_booked(n, meetings)}"
    )

    n: int = 2
    meetings: list[list[int]] = [[0, 2], [1, 10], [3, 4], [5, 6]]
    # Expected: 0
    print(
        f"most booked room for n ={n} for meetings = {meetings} is result {most_booked(n, meetings)}"
    )


solve()
