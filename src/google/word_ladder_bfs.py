"""
Word Ladder (LeetCode #127)

You're given two words, beginWord and endWord, plus a list of words wordList. Find the length of the shortest transformation sequence from beginWord to endWord, following these rules:

Each step, you may change exactly one letter of the current word.
Every intermediate word produced this way must exist in wordList.
endWord is guaranteed to have the same length as beginWord, and all words are lowercase.
If no such transformation sequence exists, return 0.
Note: beginWord does not need to be in wordList, but it's still counted as the first word in the sequence length.

Example:

beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5 (hit → hot → dot → dog → cog)

Constraints (typical):

1 ≤ beginWord.length ≤ 10
endWord.length == beginWord.length
1 ≤ wordList.length ≤ 5000
All words consist of lowercase English letters only
beginWord != endWord
All words in wordList are unique
"""

from collections import defaultdict
import string
import pprint
from collections import deque

def build_neighbors(begin_word: str, word_list: list[str]) -> defaultdict[str, list[str]]:
    # For each word, try swapping every position with every letter a-z.
    # If the resulting word exists in the list (and isn't the same word), it's a neighbor.
    # This builds an adjacency map: word → [words reachable in one letter change]
    neighbors: defaultdict[str, list[str]] = defaultdict(list)

    word_list = word_list if begin_word in word_list else word_list + [begin_word]
    for word in word_list:
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                new_word: str = word[:i] + c + word[i + 1:]
                if new_word in word_list and new_word != word:
                    neighbors[word].append(new_word)

    return neighbors


def word_ladder_bfs(begin_word: str, end_word: str, word_list: list[str]) -> tuple[list[str], int]:
    # If end_word isn't reachable at all, return early
    if end_word not in word_list:
        return 0

    # Pre-build the neighbor graph so BFS just follows edges
    neighbors: defaultdict[str, list[str]] = build_neighbors(begin_word=begin_word, word_list=word_list)

    # Each queue entry is (word, steps_taken_to_reach_it)
    # begin_word is step 0 — we haven't transformed anything yet
    queue: deque[tuple[str, int]] = deque([(begin_word, 0)])

    # Track visited words to avoid revisiting nodes in the BFS tree
    visited: set[str] = {begin_word}

    # Track each word's parent so we can reconstruct the path at the end
    parents: dict[str, str] = dict()

    count: int = 0

    while queue:
        word, count = queue.popleft()

        # Found the target — count holds the number of steps to get here
        if word == end_word:
            break

        for neighbor in neighbors[word]:
            if neighbor not in visited:
                visited.add(neighbor)
                # Pass count + 1 so each neighbor knows its own depth
                queue.append((neighbor, count + 1))
                parents[neighbor] = word

    # Reconstruct the path by walking backwards through parents
    parent: str = end_word
    result: list[str] = [end_word]

    while parent != begin_word:
        parent = parents[parent]
        result.append(parent)

    result.reverse()
    return (result, count)


"""

space optimized method by saving path, so result doesn't need to be stored in a 
separate list andresult.reverse() isn't needed

# Word Ladder BFS trace: `hot` → `cog`

| Step | Queue before pop | We pop | Word | Check neighbors of | New words added to visited |
|---|---|---|---|---|---|
| 1 | `[ ["hot"] ]` | `["hot"]` | `hot` | `hot`'s neighbors: `dot`, `lot` | `dot`, `lot` |
| 2 | `[ ["hot","dot"], ["hot","lot"] ]` | `["hot","dot"]` | `dot` | `dot`'s neighbors: `hot`, `lot`, `dog` | `dog` (`hot`, `lot` already visited) |
| 3 | `[ ["hot","lot"], ["hot","dot","dog"] ]` | `["hot","lot"]` | `lot` | `lot`'s neighbors: `hot`, `dot`, `log` | `log` (`hot`, `dot` already visited) |
| 4 | `[ ["hot","dot","dog"], ["hot","lot","log"] ]` | `["hot","dot","dog"]` | `dog` | `dog`'s neighbors: `dot`, `cog`, `log` | `cog` (`dot`, `log` already visited) |
| 5 | `[ ["hot","lot","log"], ["hot","dot","dog","cog"] ]` | `["hot","lot","log"]` | `log` | `log`'s neighbors: `lot`, `dog`, `cog` | *(none — all three already visited)* |
| 6 | `[ ["hot","dot","dog","cog"] ]` | `["hot","dot","dog","cog"]` | `cog` | `cog == end_word` → return path | — |

**Result:** `["hot", "dot", "dog", "cog"]`
"""
def word_ladder_bfs_space_optimized(begin_word: str, end_word: str, word_list: list[str]) -> tuple[list[str], int]:
    neighbors:defaultdict[str, list[str]] = build_neighbors(begin_word=begin_word, word_list=word_list)
    queue:deque[list[str]] = deque([[begin_word]])
    visited: set[str] = {begin_word}
    

    while queue:
        path: list[str] = queue.popleft()
        word: str = path[-1]

        if word == end_word:
            return [path, len(path)] 

        for neighbor in neighbors[word]:
            if neighbor in word_list and neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    
    return []


        


def solve():
    word_list: list[str] = ["hot","dot","dog","lot","log","cog"]
    print(f"total words and count = {word_ladder_bfs(begin_word="hot", end_word ="cog", word_list=word_list)}")
    print(f"total words and count space optimized= {word_ladder_bfs_space_optimized(begin_word="hot", end_word ="cog", word_list=word_list)}")

solve()