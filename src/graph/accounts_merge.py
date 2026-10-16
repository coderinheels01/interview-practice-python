"""82. Accounts merge

Given a list of accounts, merge accounts that belong to the same person.
Each accounts[i] is a list of strings: accounts[i][0] is the person's name,
and the remaining entries are email addresses belonging to that account.

Two accounts definitely belong to the same person if they share an email.
Connections can be indirect: if A shares an email with B, and B shares an
email with C, all three accounts belong to the same person.

Accounts with the same name do not necessarily belong to the same person.
A person can initially have any number of accounts, but all their accounts
have the same name.

Return the merged accounts. Each result contains the person's name first,
followed by their distinct email addresses in sorted order. The merged
accounts themselves may appear in any order.

Example 1:
    Input: N = 4,
        accounts = [
            ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
            ["John", "johnsmith@mail.com", "john00@mail.com"],
            ["Mary", "mary@mail.com"],
            ["John", "johnnybravo@mail.com"],
        ]
    Output: [
        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    Explanation: The first two accounts share johnsmith@mail.com and merge.
    Mary's account and the last John's account remain separate. Reordering
    these three output accounts is also valid.

Example 2:
    Input: N = 6,
        accounts = [
            ["John", "j1@com", "j2@com", "j3@com"],
            ["John", "j4@com"],
            ["Raj", "r1@com", "r2@com"],
            ["John", "j1@com", "j5@com"],
            ["Raj", "r2@com", "r3@com"],
            ["Mary", "m1@com"],
        ]
    Output: [
        ["John", "j1@com", "j2@com", "j3@com", "j5@com"],
        ["John", "j4@com"],
        ["Raj", "r1@com", "r2@com", "r3@com"],
        ["Mary", "m1@com"],
    ]
    Explanation: The first and fourth accounts share j1@com. The third and
    fifth accounts share r2@com. Merge each of these pairs.

Practice question:
    Input: N = 3,
        accounts = [
            ["Alice", "alice@mail.com", "alice_work@mail.com"],
            ["Bob", "bob@gmail.com"],
            ["Alice", "alice_personal@mail.com", "alice@mail.com"],
        ]
    Choose the correct output:
    A. [["Alice", "alice@mail.com", "alice_personal@mail.com"],
        ["Alice", "alice_personal@mail.com", "alice_work@mail.com"],
        ["Bob", "bob@gmail.com"]]
    B. [["Alice", "alice@mail.com", "alice_personal@mail.com"],
        ["Alice", "alice_work@mail.com"], ["Bob", "bob@gmail.com"]]
    C. [["Alice", "alice@mail.com", "alice_personal@mail.com", "alice_work@mail.com"],
        ["Bob", "bob@gmail.com"]]
    D. [["Alice", "alice@mail.com"],
        ["Alice", "alice_personal@mail.com", "alice_work@mail.com"],
        ["Bob", "bob@gmail.com"]]

Constraints:
    - 1 <= N <= 1000, where N = len(accounts)
    - 2 <= len(accounts[i]) <= 15
    - 1 <= len(accounts[i][j]) <= 30
    - accounts[i][0] consists of English letters.

https://www.youtube.com/watch?v=FMwpt_aQOGw&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn&index=50

"""

from dataclasses import dataclass, field


@dataclass
class DisjointSet:
    vertices: int
    parents: list[int] = field(init=False)
    ranks: list[int] = field(init=False)

    def __post_init__(self) -> None:
        # Step 1: Each account begins in its own set, with rank zero.
        self.parents = list(range(self.vertices))
        self.ranks = [0] * self.vertices

    def _find_parent(self, node: int) -> int:
        # Steps 2 and 3: A root points to itself.
        if self.parents[node] == node:
            return node

        # Compress the visited path to the ultimate root for future lookups.
        self.parents[node] = self._find_parent(node=self.parents[node])
        return self.parents[node]

    def union_by_rank(self, node1: int, node2: int) -> bool:
        # Step 2: Merge entire account groups by finding their roots first.
        root1: int = self._find_parent(node=node1)
        root2: int = self._find_parent(node=node2)

        # Duplicate connections need no additional merge.
        if root1 == root2:
            return False

        # Attach the lower-rank root; only equal ranks increase the winner's rank.
        if self.ranks[root1] == self.ranks[root2]:
            self.parents[root2] = root1
            self.ranks[root1] += 1

        elif self.ranks[root1] > self.ranks[root2]:
            self.parents[root2] = root1
        else:
            self.parents[root1] = root2

        return True


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """Merge accounts connected by shared emails and sort each group's emails.

    Args:
        accounts: Lists containing a name followed by at least one email.
            Accounts connected by shared emails are assumed to have the same
            name, as guaranteed by the problem. Names alone do not establish
            a connection. Email strings are compared exactly as supplied.

    Returns:
        New lists containing a name followed by sorted, unique emails for
        each connected group. The order of groups is unrestricted. The input
        accounts and their nested lists are not modified; only newly created
        email buckets are sorted. Duplicate email entries appear once in the
        result. An empty input returns an empty list, although the problem
        requires at least one account.

    Approach:
        Disjoint Set Union (Union-Find) with union by rank and path compression,
        followed by sorting the emails within each merged group.

        1. Treat each account index as a vertex. Initialize a separate set for
           every account, a dictionary mapping emails to their first observed
           account index, and one empty email bucket per account.
        2. Visit each account's emails, skipping the name at position zero.
           Store the current account index for a previously unseen email.
           If the email was seen before, union the stored account index with
           the current account index. These are account indices, not positions
           of emails inside an account. The stored index need not be a root:
           union finds both roots before merging. Union by rank keeps trees
           shallow, and path compression shortens future root lookups.
           Shared emails also merge accounts transitively. Equal names with
           no connecting email remain in separate sets.
        3. After all unions finish, visit each dictionary entry exactly once.
           Find the final root of its stored account index and append the
           email to that root's bucket. Dictionary keys are unique, so this
           removes duplicate emails automatically. Waiting until all unions
           finish ensures that buckets use final roots, not earlier roots.
        4. Skip empty buckets. Sort each nonempty bucket and prepend the name
           from the root account. All accounts in that group have the same
           name, so any representative's name is valid. Append the new list
           to the output. Group order follows bucket indices and need not be
           sorted by name.

    Time Complexity:
        Let N be the number of accounts, T the total number of input email
        occurrences, U the number of distinct emails, and k_i the number of
        distinct emails in output group i, so sum(k_i) = U.
        O(N + (T + U) * alpha(N) + sum(k_i * log(k_i + 1))) amortized,
        assuming expected O(1) dictionary operations and bounded string costs.
        Initialization and bucket scanning take O(N). Processing input emails
        performs at most T unions, and bucketing performs U root lookups.
        Union by rank and path compression give O(alpha(N)) amortized per
        operation; alpha is the extremely slowly growing inverse Ackermann
        function. Sorting costs O(k_i * log(k_i + 1)) for each bucket, and
        constructing output lists takes O(U + N). A simpler upper bound is
        O(N + T * alpha(N) + U * log(U + 1)).
        Strings have length at most 30 here. If their maximum length L were
        variable, hashing and string comparisons could each cost O(L), so
        the dictionary and sorting terms would need to account for that.

    Space Complexity:
        O(N + U) additional space. Parent and rank arrays and the collection
        of buckets use O(N), while the email dictionary and bucket contents
        use O(U). Sorting may require O(U) temporary space in the largest
        bucket. Recursive root lookup uses O(log N) stack space at most with
        union by rank. The returned lists contain O(U + N) references, so
        including the output does not change the bound. Existing strings
        are referenced rather than copied, and input storage is excluded.
    """
    # Step 1: Initialize one DSU vertex and email bucket per account.
    email_to_account_map: dict[str, int] = {}
    vertices: int = len(accounts)
    ds = DisjointSet(vertices=vertices)
    merged_accounts: list[list[str]] = [[] * 1 for _ in range(vertices)]
    mapped_merged_accounts: list[list[str]] = []

    # Step 2: Shared emails connect account indices, even through other accounts.
    for index in range(vertices):
        for email_index in range(len(accounts[index])):
            if email_index == 0:
                continue
            email = accounts[index][email_index]
            if email in email_to_account_map:
                parent_index: int = email_to_account_map[email]
                ds.union_by_rank(node1=parent_index, node2=index)
                continue
            email_to_account_map[email] = index

    # Step 3: Assign each unique email to its account's final root.
    for email, account_index in email_to_account_map.items():
        parent_index: int = ds._find_parent(node=account_index)
        merged_accounts[parent_index].append(email)

    # Step 4: Sort each group's emails and prepend its representative's name.
    for index, account_emails in enumerate(merged_accounts):
        if not account_emails:
            continue
        account_emails.sort()
        mapped_merged_accounts.append([accounts[index][0]] + account_emails)

    return mapped_merged_accounts


def solve() -> None:
    # Original example.
    accounts: list[list[str]] = [
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    expected: list[list[str]] = [
        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    result: list[list[str]] = accounts_merge(accounts)

    # # Allow any account order while still checking the email order within each.
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single account with one email.
    accounts: list[list[str]] = [["A", "a@x.com"]]
    expected: list[list[str]] = [["A", "a@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Single account needs email sorting.
    accounts: list[list[str]] = [["Alice", "z@x.com", "a@x.com", "m@x.com"]]
    expected: list[list[str]] = [["Alice", "a@x.com", "m@x.com", "z@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Same name without shared email stays separate.
    accounts: list[list[str]] = [["John", "a@x.com"], ["John", "b@x.com"]]
    expected: list[list[str]] = [["John", "a@x.com"], ["John", "b@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Different names and disjoint emails.
    accounts: list[list[str]] = [["Alice", "a@x.com"], ["Bob", "b@x.com"]]
    expected: list[list[str]] = [["Alice", "a@x.com"], ["Bob", "b@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Identical accounts merge once.
    accounts: list[list[str]] = [["John", "a@x.com"], ["John", "a@x.com"]]
    expected: list[list[str]] = [["John", "a@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Duplicate email within a single account.
    accounts: list[list[str]] = [["Alice", "a@x.com", "a@x.com"]]
    expected: list[list[str]] = [["Alice", "a@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shared email in the middle of the later account.
    accounts: list[list[str]] = [
        ["Alice", "shared@x.com"],
        ["Alice", "a@x.com", "shared@x.com", "z@x.com"],
    ]
    expected: list[list[str]] = [["Alice", "a@x.com", "shared@x.com", "z@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Shared email at the end of the later account.
    accounts: list[list[str]] = [
        ["Alice", "shared@x.com"],
        ["Alice", "a@x.com", "shared@x.com"],
    ]
    expected: list[list[str]] = [["Alice", "a@x.com", "shared@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Transitive chain.
    accounts: list[list[str]] = [
        ["John", "a@x.com", "b@x.com"],
        ["John", "b@x.com", "c@x.com"],
        ["John", "c@x.com", "d@x.com"],
    ]
    expected: list[list[str]] = [["John", "a@x.com", "b@x.com", "c@x.com", "d@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Late bridge joins two earlier groups.
    accounts: list[list[str]] = [
        ["John", "a@x.com"],
        ["John", "b@x.com"],
        ["John", "a@x.com", "b@x.com"],
    ]
    expected: list[list[str]] = [["John", "a@x.com", "b@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Repeated connections form a cycle.
    accounts: list[list[str]] = [
        ["John", "a@x.com", "b@x.com"],
        ["John", "b@x.com", "c@x.com"],
        ["John", "c@x.com", "a@x.com"],
    ]
    expected: list[list[str]] = [["John", "a@x.com", "b@x.com", "c@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Separate person between merging accounts.
    accounts: list[list[str]] = [
        ["Alice", "a@x.com"],
        ["Bob", "b@x.com"],
        ["Alice", "a@x.com", "c@x.com"],
    ]
    expected: list[list[str]] = [["Alice", "a@x.com", "c@x.com"], ["Bob", "b@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Second supplied example.
    accounts: list[list[str]] = [
        ["John", "j1@com", "j2@com", "j3@com"],
        ["John", "j4@com"],
        ["Raj", "r1@com", "r2@com"],
        ["John", "j1@com", "j5@com"],
        ["Raj", "r2@com", "r3@com"],
        ["Mary", "m1@com"],
    ]
    expected: list[list[str]] = [
        ["John", "j1@com", "j2@com", "j3@com", "j5@com"],
        ["John", "j4@com"],
        ["Raj", "r1@com", "r2@com", "r3@com"],
        ["Mary", "m1@com"],
    ]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum name and email string lengths.
    accounts: list[list[str]] = [
        [
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "zzzzzzzzzzzzzzzzzzzzzzzz@x.com",
            "aaaaaaaaaaaaaaaaaaaaaaaa@x.com",
        ]
    ]
    expected: list[list[str]] = [
        [
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "aaaaaaaaaaaaaaaaaaaaaaaa@x.com",
            "zzzzzzzzzzzzzzzzzzzzzzzz@x.com",
        ]
    ]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Minimum string length per supplied constraints; emails treated as opaque identifiers.
    accounts: list[list[str]] = [["A", "x"]]
    expected: list[list[str]] = [["A", "x"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum emails in a single account.
    accounts: list[list[str]] = [
        ["Alice"] + [f"e{i:02}@x.com" for i in range(13, -1, -1)]
    ]
    expected: list[list[str]] = [["Alice"] + [f"e{i:02}@x.com" for i in range(14)]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum accounts, all disjoint with maximum account size.
    accounts: list[list[str]] = [
        ["John"] + [f"e{i:04}_{j:02}@x.com" for j in range(13, -1, -1)]
        for i in range(1000)
    ]
    expected: list[list[str]] = [
        ["John"] + [f"e{i:04}_{j:02}@x.com" for j in range(14)] for i in range(1000)
    ]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum accounts in a transitive chain.
    accounts: list[list[str]] = [
        ["John", f"e{i:04}@x.com", f"e{i + 1:04}@x.com"] for i in range(1000)
    ]
    expected: list[list[str]] = [["John"] + [f"e{i:04}@x.com" for i in range(1001)]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")

    # Maximum accounts all identical.
    accounts: list[list[str]] = [["John", "same@x.com"] for _ in range(1000)]
    expected: list[list[str]] = [["John", "same@x.com"]]
    result: list[list[str]] = accounts_merge(accounts)
    assert sorted(result) == sorted(expected)
    print(f"Expected: {expected}")
    print(f"Result: {result}")


if __name__ == "__main__":
    solve()
