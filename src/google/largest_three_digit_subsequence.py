# PROBLEM:
# There is an array, named digits, consisting of N digits. Choose at most three
# digits (not necessarily adjacent) and merge them into a new integer without
# changing the order of the digits. What is the biggest number that can be obtained
# this way?
#
# Write a function:
#   def solution(digits) that, given an array of N digits, returns the biggest
#   number that can be built.
#
# Examples:
#   Given digits = [7, 2, 3, 3, 4, 9], the function should return 749.
#   Given digits = [0, 0, 5, 7], the function should return 57.
#
# Constraints:
#   N is an integer within the range [3..50]
#   each element of array digits is an integer within the range [0..9]
#
# Note: focus on correctness, not performance.


def largest_three_digit_subsequence_brute_force(input: list[int]) -> int:
    """
    Brute force approach: try every possible combination of 1, 2, or 3 digits
    (in order) and return the maximum value found.

    Strategy:
      - Start with the best single digit.
      - Try all pairs (i, j) where i < j to form two-digit numbers.
      - Try all triples (i, j, k) where i < j < k to form three-digit numbers.
      - Track the running maximum throughout.

    Time complexity: O(N^3) due to the triple nested loop.
    Space complexity: O(1)
    """
    # Start with the best single-digit candidate
    best: int = input[0]

    size: int = len(input)

    # Check all single digits for the current best
    for i in range(1, size):
        if input[i] > best:
            best = input[i]

    # Try all two-digit combinations: pick index i then j (i < j)
    # Combine as: first_digit * 10 + second_digit
    for i in range(0, size):
        first_digit: int = input[i]
        for j in range(i + 1, size, 1):
            second_digit: int = first_digit * 10 + input[j]
            if second_digit > best:
                best = second_digit

    # Try all three-digit combinations: pick indices i < j < k
    # Combine as: (first * 10 + second) * 10 + third
    for i in range(0, len(input)):
        first_digit: int = input[i]
        for j in range(i + 1, size, 1):
            second_digit = first_digit * 10 + input[j]
            for k in range(j + 1, size, 1):
                third_digit = second_digit * 10 + input[k]
                if third_digit > best:
                    best = third_digit

    return best


def largest_three_digit_subsequence_optimized(input: list[int]) -> int:
    """
    Greedy approach: pick the best digit greedily, left to right, while
    leaving at least enough remaining digits to complete the triple.

    Strategy:
      1. Find the maximum digit in input[0..size-3] (leave room for 2 more).
      2. From that position onward, find the maximum digit in [pos+1..size-2]
         (leave room for 1 more).
      3. From that position onward, find the maximum digit in [pos+1..size-1].
      4. Combine the three chosen digits into the result.

    NOTE: This greedy is correct for maximising a 3-digit number because
    the most significant digit dominates — picking the largest available
    first digit (with positions remaining for two more) is always optimal.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    size: int = len(input)

    # Step 1: Find the best first digit. Search up to index size-3 so there
    # are always at least 2 more digits available after the chosen position.
    best_index: int = 0
    for i in range(1, size - 2):
        if input[i] > input[best_index]:
            best_index = i

    result = input[best_index]

    # Step 2: Find the best second digit after best_index, up to size-2 so
    # there is still at least one digit left for the third pick.
    second_start = best_index + 1
    second_best_index = second_start
    for i in range(second_start, size - 1):
        if input[i] > input[second_best_index]:
            second_best_index = i

    result = result * 10 + input[second_best_index]

    # Step 3: Find the best third digit after second_best_index, no upper
    # restriction since this is the final pick.
    third_start = second_best_index + 1
    third_best_index = third_start
    for i in range(third_start, size):
        if input[i] > input[third_best_index]:
            third_best_index = i

    result = result * 10 + input[third_best_index]

    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def run_tests():
    """
    Run a suite of test cases against both the brute-force and optimised
    solutions. Raises AssertionError on the first failure.
    """
    test_cases = [
        # (input, expected, description)
        ([7, 2, 3, 3, 4, 9], 749, "Basic example from problem: pick 7, 4, 9"),
        ([0, 0, 5, 7], 57, "Leading zeros stripped: pick 5, 7 (two digits best)"),
        ([9, 9, 9], 999, "All nines: only one possible triple"),
        ([1, 2, 3], 123, "Ascending order: only one possible triple"),
        ([3, 2, 1], 321, "Descending order: only one possible triple"),
        ([0, 0, 0], 0, "All zeros"),
        ([5, 1, 1, 9], 519, "Best triple skipping middle low values"),
        ([1, 9, 1, 9, 1, 9], 999, "Alternating pattern: pick three 9s"),
        ([0, 9, 0, 9, 0, 9], 999, "Zero-padded nines: pick three 9s"),
        ([1, 2, 9, 3], 293, "9 is best first digit in middle, then pick 3"),
        ([9, 1, 2, 3], 923, "9 at start: pick 9, 2, 3"),
        ([1, 2, 3, 9], 239, "9 at end but forced to choose best triple left to right"),
        (
            [5, 3, 8, 2, 7],
            827,
            "Non-trivial: pick 8, 2, 7 — 8 dominates as first digit",
        ),
    ]

    print("Running tests...\n")
    all_passed = True

    for digits, expected, description in test_cases:
        bf_result = largest_three_digit_subsequence_brute_force(digits)
        opt_result = largest_three_digit_subsequence_optimized(digits)

        bf_ok = bf_result == expected
        opt_ok = opt_result == expected

        status = "PASS" if (bf_ok and opt_ok) else "FAIL"
        if status == "FAIL":
            all_passed = False

        print(
            f"[{status}] {description}\n"
            f"        input={digits}, expected={expected}, "
            f"brute_force={bf_result} ({'✓' if bf_ok else '✗'}), "
            f"optimized={opt_result} ({'✓' if opt_ok else '✗'})\n"
        )

    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests FAILED — see above for details.")


run_tests()
