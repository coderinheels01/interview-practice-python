def to_camel_case(char_list: list[str]) -> str:
    """
    Converts a snake_case string (passed as a list of characters) to camelCase
    in-place using a two-pointer approach, then returns the result as a string.

    Time:  O(n) — single pass over the character list to do the in-place
                  rewrite (O(n)), followed by "".join() which is also O(n).
                  Overall O(n) where n is the length of char_list.
    Space: O(n) — the input char_list is mutated in-place so no extra list is
                  allocated, but "".join(char_list[:write_next]) builds a new
                  string of length at most n, giving O(n) output space.
                  If we count only auxiliary (extra) space, it's O(1) since the
                  slice and string are the required output, not scratch space.
    """
    capitalize_next = False
    write_next = 0

    for c in char_list:
        if c == "_":
            if write_next != 0:
                capitalize_next = True
        else:
            if capitalize_next:
                char_list[write_next] = c.upper()
                capitalize_next = False
            else:
                char_list[write_next] = c
            write_next += 1

    return "".join(char_list[:write_next])


# Write your solution here
def solve():
    s: str = "hello_world"
    print(to_camel_case(list(s)))
    s: str = "foo__bar"
    print(to_camel_case(list(s)))
    s: str = "_leading"
    print(to_camel_case(list(s)))


solve()
