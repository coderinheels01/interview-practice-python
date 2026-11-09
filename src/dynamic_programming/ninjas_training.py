"""125. Ninja's Training

A ninja has planned an n-day training schedule. Each day, he must perform
exactly one of three activities: running, stealth training, or fighting
practice. He cannot perform the same activity on two consecutive days.

Given an n x 3 matrix, matrix[i][0], matrix[i][1], and matrix[i][2] are the
merit points for running, stealth training, and fighting practice on day
i + 1, respectively. Return the maximum total merit points he can earn.

Example 1:
    Input: matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    Output: 210
    Explanation:
        Day 1: fighting practice earns 70.
        Day 2: stealth training earns 50.
        Day 3: fighting practice earns 90.
        Total: 70 + 50 + 90 = 210, the maximum possible.

Example 2:
    Input: matrix = [[70, 40, 10], [180, 20, 5], [200, 60, 30]]
    Output: 290
    Explanation:
        Day 1: running earns 70.
        Day 2: stealth training earns 20.
        Day 3: running earns 200.
        Total: 70 + 20 + 200 = 290, the maximum possible.

Now Your Turn:
    Input: matrix = [[20, 10, 10], [20, 10, 10], [20, 30, 10]]
    Choose the correct maximum total: 70, 50, 40, or 60.

Constraints:
    - 1 <= n <= 10^4
    - n == len(matrix)
    - Each row contains exactly 3 values.
    - 0 <= matrix[i][j] <= 1000

https://www.youtube.com/watch?v=AE39gJYuRog&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY&index=8
"""


def ninjas_training_recursion(matrix: list[list[int]]) -> int:
    """Return the maximum points without repeating an activity on adjacent days.

    Approach: Naive Recursion
        1. Count the days and activities. Define train(day,
        last_task_performed) to find the best total for days 0 through
        day. Because we work backward, last_task_performed is the activity
        already chosen for the following day. We must avoid it today.
        2. At day 0, try every activity except last_task_performed and return
        the largest available score. There are no earlier days to process.
        3. On any later day, start the best total at 0. Try each activity
        that differs from last_task_performed.
        4. Add today's activity points to the best total for the earlier
        days. Ask train(day - 1, task) for that earlier total: passing
        today's task prevents the previous day from choosing the same one.
        5. Keep the largest total among the allowed activities, then return it.
        Each call makes its own choices; choosing today's best activity
        alone might not produce the best total schedule.
        6. Start at the final day with last_task_performed = cols. Valid
        activity indexes are 0, 1, and 2, so cols = 3 matches none of them.
        This allows all activities on the final day.

        Example: matrix = [[10, 9, 0], [100, 0, 0]].
            Choose running on day 1 (the second day): earn 100.
            The earlier day cannot use running, so its best score is 9.
            Total: 100 + 9 = 109.
            Choosing 10 on the first day instead would block running on
            the second day and give only 10 overall. Return 109.

    Parameters:
        matrix: An n x 3 list of activity scores. Each row is a day;
            columns 0, 1, and 2 mean running, stealth, and fighting.

    Returns:
        Maximum points from exactly one activity per day, with no activity
        repeated on consecutive days. For one day, returns its largest score.

    Mutation Behavior:
        Reads matrix without changing it or any other caller-owned data.

    Time Complexity: O(2^n)
        Here n is the number of days. The first call tries three activities,
        and later calls each try two, repeating earlier calculations.
        This exponential approach is too slow for 10,000 days.

    Space Complexity: O(n)
        Up to n recursive calls can be waiting at once. The input matrix is
        excluded from extra space; it is shared rather than copied.

    Assumptions:
        1 <= n <= 10000, each row has exactly three scores, and scores are
        between 0 and 1000. Starting maxima at 0 relies on nonnegative scores.
        Python needs enough recursion depth; large inputs can exceed its
        recursion limit. Arithmetic is treated as constant cost.
    """
    # Step 1: Count the days and activity choices.
    rows: int = len(matrix)
    cols: int = len(matrix[0])

    # Step 1: Find the best earlier schedule given the following day's task.
    def train(day: int, last_task_performed: int) -> int:

        # Step 2: On the first day, return the best allowed activity score.
        if day == 0:
            day_zero_max: int = 0
            for task in range(cols):
                if task != last_task_performed:
                    day_zero_max = max(day_zero_max, matrix[day][task])

            return day_zero_max

        # Step 3: Try each activity that differs from the neighboring day.
        current_max: int = 0
        for task in range(cols):
            if task != last_task_performed:
                # Step 4: Add today's points to the best compatible earlier days.
                current_points: int = matrix[day][task] + train(
                    day=day - 1, last_task_performed=task
                )
                # Step 5: Keep the best complete schedule found so far.
                current_max = max(current_max, current_points)

        # Step 5: Return the best total across the allowed choices.
        return current_max

    # Step 6: Start at the last day with no activity excluded.
    return train(day=rows - 1, last_task_performed=cols)


def ninjas_training_memoization(matrix: list[list[int]]) -> int:
    """Find the best training total by saving answers for day/task states.

    Approach: Top-Down Dynamic Programming (Memoization)
        1. Count the days and activities, then prepare a cache. Each day
        needs states for activity indexes 0, 1, and 2, plus state 3,
        which means no activity is excluded. A -1 marks an unsaved answer.
        2. Define train(day, last_task_performed) as the best total for days
        0 through day. We work backward: last_task_performed is the task
        chosen for the following day, so it cannot be chosen today.
        3. If this day/task state has a saved answer, return it immediately
        instead of repeating the earlier calculations.
        4. At day 0, return the largest score among activities other than
        last_task_performed. There are no earlier days to process.
        This base-case answer is returned directly without being cached.
        5. On a later day, try each allowed task. Add today's score to
        train(day - 1, task). Passing today's task prevents the previous
        day from choosing that same activity.
        6. Keep the largest total. After checking all allowed tasks, save
        this day/task state's answer and return it.
        7. Start at the last day with last_task_performed = cols (3).
        No real activity has index 3, so all three choices are allowed.

        Example: matrix = [[10, 9, 0], [100, 0, 0]].
            Choose running on the second day: earn 100.
            The first day must avoid running, so its best score is 9.
            This schedule earns 109. Compare the other choices and return 109.
            If the same day/task question appears again, reuse its saved answer.

    Parameters:
        matrix: An n x 3 list of scores. Columns 0, 1, and 2 represent
            running, stealth training, and fighting practice respectively.

    Returns:
        Maximum total for exactly one activity per day without repeating
        the same activity on consecutive days.

    Mutation Behavior:
        Updates only its local cache; matrix is not modified.

    Time Complexity: O(n) for the intended memoized algorithm
        Each day has four possible task states, each checking three activities.
        Those counts are fixed, so total work grows with the number of days.

    Space Complexity: O(n) for the intended memoized algorithm
        The cache and recursion stack both grow with the number of days.
        The input matrix is excluded from extra space.

    Assumptions and Current Limitation:
        The input has 1 through 10000 days, three scores per day, and scores
        from 0 through 1000. Nonnegative scores allow maxima to start at 0.
        The current cache expression [-1] * cols + 1 raises TypeError before
        training begins; the steps and complexity above describe the algorithm
        once the cache provides cols + 1 entries per row. Large day counts
        can also exceed Python's recursion limit. Arithmetic is constant cost.
    """
    # Step 1: Count the days and activities and prepare the state cache.
    rows: int = len(matrix)
    cols: int = len(matrix[0])

    max_points: list[list[int]] = [[-1] * (cols + 1) for _ in range(rows)]

    # Step 2: Find the best earlier schedule given the following day's task.
    def train(day: int, last_task_performed: int) -> int:

        # Step 3: Reuse a saved answer for this exact day/task state.
        if max_points[day][last_task_performed] != -1:
            return max_points[day][last_task_performed]
        # Step 4: On the first day, choose the best allowed activity.
        if day == 0:
            day_zero_max: int = 0
            for task in range(cols):
                if task != last_task_performed:
                    day_zero_max = max(day_zero_max, matrix[day][task])

            return day_zero_max

        # Step 5: Try today's allowed tasks with compatible earlier schedules.
        current_max: int = 0
        for task in range(cols):
            if task != last_task_performed:
                current_points: int = matrix[day][task] + train(
                    day=day - 1, last_task_performed=task
                )
                # Step 6: Keep the best complete schedule.
                current_max = max(current_max, current_points)
        # Step 6: Save the best answer after all choices have been checked.
        max_points[day][last_task_performed] = current_max
        return current_max

    # Step 7: Start at the last day with all activities available.
    return train(day=rows - 1, last_task_performed=cols)


def ninjas_training_tabulation(matrix: list[list[int]]) -> int:
    """Return the best training total without repeating tasks on adjacent days.

    Approach: Bottom-Up Dynamic Programming (Tabulation)
        1. Create one table row per day with four columns. A cell
           max_points[day][last_task_performed] means the best total through
           that day when that task is excluded on that day. Columns 0, 1,
           and 2 exclude running, stealth, and fighting respectively.
           Column 3 excludes nothing; it is not a fourth activity.
        2. Fill day 0's four answers directly. For each excluded activity,
           choose the better of the other two scores. For column 3, choose
           the best of all three. Only one activity is performed that day.
        3. Visit the remaining days in order. Calculate an answer for each
           of the four restriction states, including the unrestricted state.
        4. Try each of the three real activities. Skip the one matching
           last_task_performed. When it is 3, all activities are allowed.
        5. Add today's task score to max_points[day - 1][task]. That earlier
           answer excludes today's task on the previous day, preventing
           repetition. It already contains the best compatible earlier schedule.
        6. Keep the largest total in the current day/restriction cell.
        7. Return the final day's column 3, allowing any final activity.
           For one day, this directly returns the initialized maximum.

        Example: matrix = [[10, 9, 0], [100, 0, 0]].
            Day 0's row is [9, 10, 10, 10]. The first entry is 9 because
            running is excluded there; the unrestricted entry is 10.
            On day 1, choosing running gives 100 + max_points[0][0] = 109.
            The other choices give 10 each. The unrestricted answer is 109.

    Parameters:
        matrix: An n x 3 list. Each row is a day, with scores for running,
            stealth training, and fighting practice, in that order.

    Returns:
        Maximum points from exactly one activity per day, without choosing
        the same activity on consecutive days.

    Mutation Behavior:
        Changes only its local table; matrix is not modified.

    Time Complexity: O(n)
        Each of n days has four states, each checking three activities.
        Four and three are fixed counts, so work grows linearly with days.

    Space Complexity: O(n)
        The table has four entries per day. The input matrix is excluded
        from extra space, and no recursion stack is needed.

    Assumptions:
        There are 1 through 10000 days, exactly three activities, and scores
        from 0 through 1000. Nonnegative scores allow table entries to start
        at 0. Arithmetic is treated as constant cost.
    """
    # Step 1: Reserve four restriction states per day.
    rows: int = len(matrix)
    cols: int = len(matrix[0])
    max_points: list[list[int]] = [[0] * (cols + 1) for _ in range(rows)]

    # Step 2: Fill the first day for each restriction and for no restriction.
    max_points[0][0] = max(matrix[0][1], matrix[0][2])
    max_points[0][1] = max(matrix[0][0], matrix[0][2])
    max_points[0][2] = max(matrix[0][1], matrix[0][0])
    max_points[0][3] = max(matrix[0][0], matrix[0][1], matrix[0][2])

    # Step 3: Build each later day from the already completed previous day.
    for day in range(1, rows):
        for last_task_performed in range(cols + 1):
            # Step 4: Try each real activity except the excluded one.
            for task in range(cols):
                if last_task_performed != task:
                    # Step 5: Add a compatible earlier schedule to today's score.
                    current_points: int = matrix[day][task] + max_points[day - 1][task]
                    # Step 6: Keep the best total for this restriction.
                    max_points[day][last_task_performed] = max(
                        max_points[day][last_task_performed], current_points
                    )

    # Step 7: Return the final day with no activity excluded.
    return max_points[rows - 1][cols]


def ninjas_training_tabulation_space_optimized(matrix: list[list[int]]) -> int:
    """Return the best training total while keeping only two days of answers.

    Approach: Bottom-Up Dynamic Programming (Space-Optimized Tabulation)
        1. Prepare four answers for the first day. Slots 0, 1, and 2 hold
           the best score when running, stealth, or fighting is excluded,
           respectively. Slot 3 holds the best score with nothing excluded.
           These are four restriction states, not four activities.
        2. For each later day, create a fresh four-slot current_day_points
           list. The previous day's answers remain available separately.
        3. Calculate each restriction state by trying the three activities.
           Skip the task matching last_task_performed. When that value is
           3, every task is allowed because real task indexes are 0 to 2.
        4. Add today's task score to previous_day_points[task]. That earlier
           answer excludes today's task on the previous day, preventing
           consecutive days from using the same activity.
        5. Keep the largest total in the current restriction's slot.
        6. After finishing all four states, assign current_day_points to
           previous_day_points. Assignment shares the list rather than
           copying it. This is safe: the next day creates a fresh current
           list, so it will not overwrite the saved previous day's answers.
        7. Return slot 3, allowing any activity on the final day. With one
           day, the loop is skipped and the initialized answer is returned.

        Example: matrix = [[10, 9, 0], [100, 0, 0]].
            First day's answers: [9, 10, 10, 10].
            On the second day, choosing running gives 100 + 9 = 109.
            Stealth gives 0 + 10 = 10; fighting also gives 10.
            The unrestricted slot stores 109. Return 109.

    Parameters:
        matrix: An n x 3 list of daily scores for running, stealth training,
            and fighting practice, in that order.

    Returns:
        Maximum total from exactly one activity per day without repeating
        an activity on consecutive days.

    Mutation Behavior:
        Updates only local lists; matrix is not modified.

    Time Complexity: O(n)
        Each of n days checks four states and three activities per state.
        These are fixed counts, so work grows linearly with days.

    Space Complexity: O(1)
        At most two four-slot answer lists are needed at once, regardless
        of the number of days. The input matrix is excluded from extra space.

    Assumptions:
        The matrix has 1 through 10000 rows, exactly three columns, and
        scores from 0 through 1000. Nonnegative scores allow maxima to
        start at 0. Arithmetic is treated as constant cost.
    """
    # Step 1: Save the first day's answer for each of the four restrictions.
    rows: int = len(matrix)
    previous_day_points: list[int] = [0] * 4
    previous_day_points[0] = max(matrix[0][1], matrix[0][2])
    previous_day_points[1] = max(matrix[0][0], matrix[0][2])
    previous_day_points[2] = max(matrix[0][0], matrix[0][1])
    previous_day_points[3] = max(matrix[0][0], matrix[0][1], matrix[0][2])

    # Step 2: Start a fresh four-slot answer list for each later day.
    for day in range(1, rows):
        current_day_points: list[int] = [0] * 4
        # Step 3: Try the allowed activities for each restriction.
        for last_task_performed in range(4):
            for task in range(3):
                if last_task_performed != task:
                    # Step 4: Add today's score to a compatible earlier schedule.
                    current_points: int = matrix[day][task] + previous_day_points[task]
                    # Step 5: Keep the best total for this restriction.
                    current_day_points[last_task_performed] = max(
                        current_day_points[last_task_performed], current_points
                    )
        # Step 6: Save this completed day; the next day gets a fresh list.
        previous_day_points = current_day_points
    # Step 7: Return the final total with no activity excluded.
    return previous_day_points[3]


def solve() -> None:
    matrix: list[list[int]] = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected: int = 210
    result: int = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum days and points.
    matrix = [[0, 0, 0]]
    expected = 0
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One day; running is best.
    matrix = [[1000, 0, 0]]
    expected = 1000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One day; stealth is best.
    matrix = [[0, 1000, 0]]
    expected = 1000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One day; fighting is best.
    matrix = [[0, 0, 1000]]
    expected = 1000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # One day with tied choices.
    matrix = [[5, 5, 5]]
    expected = 5
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Cannot repeat the best activity.
    matrix = [[100, 1, 1], [100, 1, 1]]
    expected = 101
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Skipping the first day maximum improves total.
    matrix = [[10, 9, 0], [100, 0, 0]]
    expected = 109
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Zero-point activities still permit a schedule.
    matrix = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum points and tied activities.
    matrix = [[1000, 1000, 1000], [1000, 1000, 1000]]
    expected = 2000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Activity may repeat after one intervening day.
    matrix = [[1000, 0, 0], [0, 1000, 0], [1000, 0, 0]]
    expected = 3000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # First question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second question example.
    matrix = [[70, 40, 10], [180, 20, 5], [200, 60, 30]]
    expected = 290
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Your turn example.
    matrix = [[20, 10, 10], [20, 10, 10], [20, 30, 10]]
    expected = 60
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Several days with equal choices.
    matrix = [[5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5, 5]]
    expected = 25
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Optimal schedule uses all three activities.
    matrix = [[0, 0, 1000], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000]]
    expected = 4000
    result = ninjas_training_recursion(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: the first question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Minimum days and points.
    matrix = [[0, 0, 0]]
    expected = 0
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Running is best on one day.
    matrix = [[1000, 0, 0]]
    expected = 1000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Stealth is best on one day.
    matrix = [[0, 1000, 0]]
    expected = 1000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Fighting is best on one day.
    matrix = [[0, 0, 1000]]
    expected = 1000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Tied choices on one day.
    matrix = [[5, 5, 5]]
    expected = 5
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Cannot repeat best activity.
    matrix = [[100, 1, 1], [100, 1, 1]]
    expected = 101
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Greedy first-day choice is suboptimal.
    matrix = [[10, 9, 0], [100, 0, 0]]
    expected = 109
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Multiple zero-point days.
    matrix = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Maximum points and ties.
    matrix = [[1000, 1000, 1000], [1000, 1000, 1000]]
    expected = 2000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Reuse activity after an intervening day.
    matrix = [[1000, 0, 0], [0, 1000, 0], [1000, 0, 0]]
    expected = 3000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: First question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Second question example.
    matrix = [[70, 40, 10], [180, 20, 5], [200, 60, 30]]
    expected = 290
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Your turn example.
    matrix = [[20, 10, 10], [20, 10, 10], [20, 30, 10]]
    expected = 60
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Repeated tied states.
    matrix = [[5, 5, 5] for _ in range(5)]
    expected = 25
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Memoization: Use all three activities.
    matrix = [[0, 0, 1000], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000]]
    expected = 4000
    result = ninjas_training_memoization(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: the first question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Minimum days and points.
    matrix = [[0, 0, 0]]
    expected = 0
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Running is best.
    matrix = [[1000, 0, 0]]
    expected = 1000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Stealth is best.
    matrix = [[0, 1000, 0]]
    expected = 1000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Fighting is best; unrestricted final state.
    matrix = [[0, 0, 1000]]
    expected = 1000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Single day with ties.
    matrix = [[5, 5, 5]]
    expected = 5
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Cannot repeat the best activity.
    matrix = [[100, 1, 1], [100, 1, 1]]
    expected = 101
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Greedy choice is suboptimal.
    matrix = [[10, 9, 0], [100, 0, 0]]
    expected = 109
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Multiple zero days.
    matrix = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum score and ties.
    matrix = [[1000, 1000, 1000], [1000, 1000, 1000]]
    expected = 2000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Reuse activity after an intervening day.
    matrix = [[1000, 0, 0], [0, 1000, 0], [1000, 0, 0]]
    expected = 3000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: First example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Second example.
    matrix = [[70, 40, 10], [180, 20, 5], [200, 60, 30]]
    expected = 290
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Your turn example.
    matrix = [[20, 10, 10], [20, 10, 10], [20, 30, 10]]
    expected = 60
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Repeated tied scores.
    matrix = [[5, 5, 5] for _ in range(5)]
    expected = 25
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Use all activities.
    matrix = [[0, 0, 1000], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000]]
    expected = 4000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum days with zeros.
    matrix = [[0, 0, 0] for _ in range(10000)]
    expected = 0
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Tabulation: Maximum days and points.
    matrix = [[1000, 1000, 1000] for _ in range(10000)]
    expected = 10000000
    result = ninjas_training_tabulation(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: the first question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Minimum days and points.
    matrix = [[0, 0, 0]]
    expected = 0
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: One day; running is best.
    matrix = [[1000, 0, 0]]
    expected = 1000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: One day; stealth is best.
    matrix = [[0, 1000, 0]]
    expected = 1000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: One day; fighting is best.
    matrix = [[0, 0, 1000]]
    expected = 1000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: One day with tied choices.
    matrix = [[5, 5, 5]]
    expected = 5
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Cannot repeat the best activity.
    matrix = [[100, 1, 1], [100, 1, 1]]
    expected = 101
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Greedy choice is suboptimal.
    matrix = [[10, 9, 0], [100, 0, 0]]
    expected = 109
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Multiple zero-point days.
    matrix = [[0, 0, 0], [0, 0, 0]]
    expected = 0
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum points with ties.
    matrix = [[1000, 1000, 1000], [1000, 1000, 1000]]
    expected = 2000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Reuse an activity after an intervening day.
    matrix = [[1000, 0, 0], [0, 1000, 0], [1000, 0, 0]]
    expected = 3000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: First question example.
    matrix = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
    expected = 210
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Second question example.
    matrix = [[70, 40, 10], [180, 20, 5], [200, 60, 30]]
    expected = 290
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Your turn example.
    matrix = [[20, 10, 10], [20, 10, 10], [20, 30, 10]]
    expected = 60
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Repeated tied states.
    matrix = [[5, 5, 5] for _ in range(5)]
    expected = 25
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Optimal schedule uses all activities.
    matrix = [[0, 0, 1000], [1000, 0, 0], [0, 1000, 0], [0, 0, 1000]]
    expected = 4000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum days with zeros.
    matrix = [[0, 0, 0] for _ in range(10000)]
    expected = 0
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Space-optimized tabulation: Maximum days and points.
    matrix = [[1000, 1000, 1000] for _ in range(10000)]
    expected = 10000000
    result = ninjas_training_tabulation_space_optimized(matrix)

    assert result == expected
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
