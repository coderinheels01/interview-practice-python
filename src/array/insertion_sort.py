"""
Insertion Sort with Intermediate States

Implement Insertion Sort and return intermediate states.

Insertion Sort is a simple sorting algorithm that builds the sorted list one
element at a time, from left to right. It works by repeatedly taking an element
from the unsorted portion and inserting it into its correct position in the
sorted portion of the list.

Objective:
Given a list of key-value pairs, sort the list by key using Insertion Sort.
Return a list of lists showing the state of the array after each insertion.
If two key-value pairs have the same key, maintain their relative order in
the sorted list (stable sort).

Input:
    pairs - a list of key-value pairs, where each key-value has an integer key
            and a string value. (0 <= pairs.length <= 100).

Example 1:
    Input:  pairs = [(5, "apple"), (2, "banana"), (9, "cherry")]
    Output: [[(5, "apple"), (2, "banana"), (9, "cherry")],
             [(2, "banana"), (5, "apple"), (9, "cherry")],
             [(2, "banana"), (5, "apple"), (9, "cherry")]]

Example 2:
    Input:  pairs = [(3, "cat"), (3, "bird"), (2, "dog")]
    Output: [[(3, "cat"), (3, "bird"), (2, "dog")],
             [(3, "cat"), (3, "bird"), (2, "dog")],
             [(2, "dog"), (3, "cat"), (3, "bird")]]
    Note: pairs with key=3 ("cat" and "bird") maintain their relative order,
    illustrating the stability of the algorithm.
"""




def insertion_sort(input:list[tuple[int, str]]) -> list[tuple[int, str]]:
    """
    Approach: for each element at temp_index, walk it backward (via while loop)
    swapping with its left neighbour until it reaches its correct sorted position.
    The left portion (0..temp_index) is always sorted after each outer iteration.

    Time:  O(n^2)
        - Outer for loop runs n-1 times
        - Inner while loop in the worst case runs up to temp_index times per iteration
          (1 + 2 + ... + n-1 = n(n-1)/2 swaps)
        - Worst case: reverse-sorted input e.g. [(3,"c"),(2,"b"),(1,"a")]
          Every element has to travel all the way to index 0, so the inner loop
          does the maximum number of iterations every time.

    Space: O(1)
        - Sorts in place, only a few integer variables (n, temp_index, j) are allocated
        - No extra arrays or data structures used regardless of input size
    """
    n:int = len(input)

    if n < 2:
        return input

    def swap(index1:int, index2:int):
        temp:int = input[index2]
        input[index2] = input[index1]
        input[index1] =temp

    temp_index:int = 1

    for temp_index in range(1, n):
        j: int = temp_index
        while j > 0 and input[j - 1][0] > input[j][0]:
            swap(j, j - 1)
            j -= 1

    return input

def solve() -> None:
    example1: list[tuple[int, str]] = [(5, "apple"), (2, "banana"), (9, "cherry")]
    expected1: list[tuple[int, str]] = [(2, "banana"), (5, "apple"), (9, "cherry")]
    result1: list[tuple[int, str]] = insertion_sort(example1)
    print("Example 1:")
    print(f"expected={expected1} got={result1}")

    example2: list[tuple[int, str]] = [(3, "cat"), (3, "bird"), (2, "dog")]
    expected2: list[tuple[int, str]] = [(2, "dog"), (3, "cat"), (3, "bird")]
    result2: list[tuple[int, str]] = insertion_sort(example2)
    print("\nExample 2:")
    print(f"expected={expected2} got={result2}")

    # Already sorted — no swaps should occur
    example3: list[tuple[int, str]] = [(1, "a"), (2, "b"), (3, "c")]
    expected3: list[tuple[int, str]] = [(1, "a"), (2, "b"), (3, "c")]
    result3: list[tuple[int, str]] = insertion_sort(example3)
    print("\nExample 3 (already sorted):")
    print(f"expected={expected3} got={result3}")

    # Reverse sorted — maximum swaps
    example4: list[tuple[int, str]] = [(3, "c"), (2, "b"), (1, "a")]
    expected4: list[tuple[int, str]] = [(1, "a"), (2, "b"), (3, "c")]
    result4: list[tuple[int, str]] = insertion_sort(example4)
    print("\nExample 4 (reverse sorted):")
    print(f"expected={expected4} got={result4}")

    # Single element
    example5: list[tuple[int, str]] = [(42, "only")]
    expected5: list[tuple[int, str]] = [(42, "only")]
    result5: list[tuple[int, str]] = insertion_sort(example5)
    print("\nExample 5 (single element):")
    print(f"expected={expected5} got={result5}")

    # Empty list
    example6: list[tuple[int, str]] = []
    expected6: list[tuple[int, str]] = []
    result6: list[tuple[int, str]] = insertion_sort(example6)
    print("\nExample 6 (empty):")
    print(f"expected={expected6} got={result6}")

    # All same keys — stability check
    example7: list[tuple[int, str]] = [(1, "x"), (1, "y"), (1, "z")]
    expected7: list[tuple[int, str]] = [(1, "x"), (1, "y"), (1, "z")]
    result7: list[tuple[int, str]] = insertion_sort(example7)
    print("\nExample 7 (all same keys):")
    print(f"expected={expected7} got={result7}")

solve()
