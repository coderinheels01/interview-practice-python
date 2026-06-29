# Python Data Structures - Methods & Operations

## Linear Structures

### List
**Initialize:**
```python
my_list: list = []                                          # Empty list
my_list: list[int] = [1, 2, 3]                            # List with elements
my_list: list[int] = list()                               # Using constructor
my_list: list[int] = list(range(5))                       # [0, 1, 2, 3, 4]
my_list: list[int] = [0] * 5                              # [0, 0, 0, 0, 0] (repeated element)
my_list: list[int] = [i for i in range(5)]               # List comprehension
my_list: list[str] = []                                   # List of strings
```

**Methods:**
- `append(x)` - Add element to end [O(1), O(1)]
- `extend(iterable)` - Add multiple elements to end [O(k), O(1)]
- `insert(i, x)` - Insert element at index [O(n), O(1)]
- `remove(x)` - Remove first occurrence of element [O(n), O(1)]
- `pop(i)` - Remove and return element at index (default: last) [O(n), O(1)]
- `clear()` - Remove all elements [O(n), O(1)]
- `index(x)` - Return index of first occurrence [O(n), O(1)]
- `count(x)` - Count occurrences of element [O(n), O(1)]
- `sort()` - Sort list in place [O(n log n), O(n)]
- `reverse()` - Reverse list in place [O(n), O(1)]
- `copy()` - Create shallow copy [O(n), O(n)]

**Notes:** Ordered, mutable, allows duplicates. Access by index with `list[i]`

### Tuple
**Initialize:**
```python
my_tuple: tuple = ()                                      # Empty tuple
my_tuple: tuple[int, int, int] = (1, 2, 3)              # Tuple with elements
my_tuple: tuple[int, ...] = (1,)                         # Single element tuple (comma required!)
my_tuple: tuple = tuple()                                # Using constructor
my_tuple: tuple[int, ...] = tuple([1, 2, 3])            # Convert list to tuple
my_tuple: tuple[int, ...] = tuple(range(5))             # (0, 1, 2, 3, 4)
```

**Methods:**
- `index(x)` - Return index of first occurrence [O(n), O(1)]
- `count(x)` - Count occurrences of element [O(n), O(1)]

**Notes:** Ordered, immutable (can't change after creation), allows duplicates. No add/remove operations.

### Deque
**Initialize:**
```python
from collections import deque

my_deque: deque[int] = deque()                           # Empty deque
my_deque: deque[int] = deque([1, 2, 3])                 # Deque with elements
my_deque: deque[int] = deque(maxlen=5)                  # Max length (circular when full)
```

**Methods:**
- `append(x)` - Add element to right end [O(1), O(1)]
- `appendleft(x)` - Add element to left end [O(1), O(1)]
- `pop()` - Remove and return from right end [O(1), O(1)]
- `popleft()` - Remove and return from left end [O(1), O(1)]
- `extend(iterable)` - Add multiple elements to right [O(k), O(1)]
- `extendleft(iterable)` - Add multiple elements to left [O(k), O(1)]
- `clear()` - Remove all elements [O(n), O(1)]
- `rotate(n)` - Rotate elements n steps [O(n), O(1)]

**Import:** `from collections import deque`

**Notes:** Double-ended queue. Fast O(1) operations at both ends. Better than list for queue operations.

## Hash-based Structures

### Dictionary
**Initialize:**
```python
my_dict: dict = {}                                       # Empty dict
my_dict: dict[str, int] = {'a': 1, 'b': 2}            # Dict with key-value pairs
my_dict: dict[str, int] = dict()                       # Using constructor
my_dict: dict[str, int] = dict(a=1, b=2)              # Keyword arguments
my_dict: dict[str, int] = dict([('a', 1), ('b', 2)])  # From list of tuples
my_dict: dict[int, int] = {i: i*2 for i in range(3)}  # Dict comprehension {0: 0, 1: 2, 2: 4}
```

**Methods:**
- `get(key, default)` - Retrieve value, return default if not found [O(1)*, O(1)]
- `pop(key, default)` - Remove and return value [O(1)*, O(1)]
- `popitem()` - Remove and return arbitrary key-value pair [O(1)*, O(1)]
- `update(dict)` - Update with key-value pairs from another dict [O(k), O(1)]
- `clear()` - Remove all items [O(n), O(1)]
- `copy()` - Create shallow copy [O(n), O(n)]
- `keys()` - Return dict_keys object [O(1), O(n)]
- `values()` - Return dict_values object [O(1), O(n)]
- `items()` - Return dict_items object (key-value pairs) [O(1), O(n)]
- `setdefault(key, default)` - Get value or set default if not found [O(1)*, O(1)]

**Access:** `dict[key]` or `dict.get(key)`

**Insert:** `dict[key] = value`

**Notes:** Key-value pairs. Python 3.7+: insertion ordered. Mutable.

### Set
**Initialize:**
```python
my_set: set = set()                                     # Empty set (NOT {} - that's a dict!)
my_set: set[int] = {1, 2, 3}                          # Set with elements
my_set: set[int] = set([1, 2, 3])                     # Convert list to set
my_set: set[int] = set(range(5))                      # {0, 1, 2, 3, 4}
my_set: set[int] = {i for i in range(5)}              # Set comprehension
```

**Methods:**
- `add(x)` - Add element [O(1)*, O(1)]
- `remove(x)` - Remove element (raises KeyError if not found) [O(1)*, O(1)]
- `discard(x)` - Remove element (does nothing if not found) [O(1)*, O(1)]
- `pop()` - Remove and return arbitrary element [O(1)*, O(1)]
- `clear()` - Remove all elements [O(n), O(1)]
- `copy()` - Create shallow copy [O(n), O(n)]
- `union(set)` - Return union (also: `set1 | set2`) [O(n + m), O(n + m)]
- `intersection(set)` - Return intersection (also: `set1 & set2`) [O(min(n, m)), O(min(n, m))]
- `difference(set)` - Return difference (also: `set1 - set2`) [O(n), O(n)]
- `issubset(set)` - Check if subset [O(n), O(1)]
- `issuperset(set)` - Check if superset [O(m), O(1)]

**Search:** `x in set`

**Notes:** Unordered, unique elements only. Mutable. No duplicates allowed.

### Frozenset
**Initialize:**
```python
my_frozenset: frozenset = frozenset()                  # Empty frozenset
my_frozenset: frozenset[int] = frozenset([1, 2, 3])   # Convert list to frozenset
my_frozenset: frozenset[int] = frozenset({1, 2, 3})   # Convert set to frozenset
my_frozenset: frozenset[int] = frozenset(range(5))    # frozenset({0, 1, 2, 3, 4})
```

**Methods:**
- `union(set)` - Return union [O(n + m), O(n + m)]
- `intersection(set)` - Return intersection [O(min(n, m)), O(min(n, m))]
- `difference(set)` - Return difference [O(n), O(n)]
- `issubset(set)` - Check if subset [O(n), O(1)]
- `issuperset(set)` - Check if superset [O(m), O(1)]

**Notes:** Immutable version of set. Can be used as dict key or in a set.

## Stack & Queue (Abstract Data Types)

### Stack (LIFO - Last In, First Out)
**Initialize:**
```python
# Stack is implemented using a list
stack: list[int] = []
stack: list[int] = [1, 2, 3]
```

**Implementation:** Use list
- `append(x)` - Push (add to top) [O(1), O(1)]
- `pop()` - Pop (remove from top) [O(1), O(1)]
- `list[-1]` - Peek (view top) [O(1), O(1)]

### Queue (FIFO - First In, First Out)
**Initialize:**
```python
from collections import deque

# Queue is implemented using deque (faster than list)
queue: deque[int] = deque()
queue: deque[int] = deque([1, 2, 3])
```

**Implementation:** Use deque (faster than list for this)
- `append(x)` - Enqueue (add to back) [O(1), O(1)]
- `popleft()` - Dequeue (remove from front) [O(1), O(1)]
- `list[0]` - Peek (view front) [O(1), O(1)]

## Tree Structures

### Heap (heapq module)
**Initialize:**
```python
import heapq

# Heap is a list with special structure
my_heap: list[int] = []
my_heap: list[int] = [3, 2, 1]
heapq.heapify(my_heap)                # Transform into min-heap: [1, 2, 3]

# Or build incrementally
my_heap: list[int] = []
heapq.heappush(my_heap, 5)
heapq.heappush(my_heap, 3)
heapq.heappush(my_heap, 7)            # [3, 5, 7]
```

**Methods:**
- `heappush(heap, item)` - Add item to heap [O(log n), O(1)]
- `heappop(heap)` - Remove and return smallest item [O(log n), O(1)]
- `heapify(list)` - Transform list into heap in-place [O(n), O(1)]
- `heappushpop(heap, item)` - Push item and pop smallest [O(log n), O(1)]
- `heapreplace(heap, item)` - Pop smallest and push item [O(log n), O(1)]

**Import:** `import heapq`

**Notes:** Min-heap by default. Create with list, then use heapq functions. Access min with `heap[0]` in O(1).

### Binary Search Tree (Custom Implementation)
**Initialize:**
```python
# BST requires custom implementation
# Basic structure:
class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Node | None = None
        self.right: Node | None = None

class BST:
    def __init__(self) -> None:
        self.root: Node | None = None
    
    def insert(self, value: int) -> None:
        # Custom insert logic
        pass

# Usage:
bst: BST = BST()
bst.insert(10)
bst.insert(5)
bst.insert(15)
```

**Methods:**
- `insert(value)` - Insert value [O(log n) avg / O(n) worst, O(1)]
- `search(value)` - Find value [O(log n) avg / O(n) worst, O(1)]
- `delete(value)` - Remove value [O(log n) avg / O(n) worst, O(1)]
- `inorder()` - In-order traversal [O(n), O(n)]
- `preorder()` - Pre-order traversal [O(n), O(n)]
- `postorder()` - Post-order traversal [O(n), O(n)]

**Notes:** No built-in BST in Python. Typically implemented as custom class with Node objects.

## Graph Structures

### Adjacency List (Custom Implementation)
**Initialize:**
```python
# Using dict of lists
graph: dict[int, list[int]] = {}
graph: dict[int, list[int]] = {
    1: [2, 3],
    2: [1, 4],
    3: [1],
    4: [2]
}

# Or using defaultdict
from collections import defaultdict
graph: defaultdict[int, list[int]] = defaultdict(list)
graph[1].append(2)
graph[1].append(3)
```

**Methods:**
- `add_vertex(v)` - Add vertex [O(1), O(1)]
- `add_edge(u, v)` - Add edge between vertices [O(1), O(1)]
- `neighbors(v)` - Get adjacent vertices [O(degree(v)), O(1)]
- `remove_vertex(v)` - Remove vertex [O(V + E), O(1)]
- `remove_edge(u, v)` - Remove edge [O(degree(u)), O(1)]

**Implementation:** Dict of lists
```python
graph = {
    1: [2, 3],
    2: [1, 4],
    3: [1],
    4: [2]
}
```

### Union-Find (Disjoint Set Union)
**Initialize:**
```python
# Union-Find requires custom implementation with path compression and union by rank
class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> None:
        # Union by rank logic
        pass

# Usage:
uf: UnionFind = UnionFind(5)
uf.union(1, 2)
uf.find(2)
```

**Methods:**
- `find(x)` - Find root/representative of element [O(α(n))*, O(1)]
- `union(x, y)` - Union two sets [O(α(n))*, O(1)]

**Notes:** Used for connectivity problems. Manual implementation with path compression and union by rank for O(α(n)) performance.

## Quick Reference: What to Use

| Goal | Use | Method |
|------|-----|--------|
| Stack (LIFO) | `list` | `.append()`, `.pop()` |
| Queue (FIFO) | `deque` | `.append()`, `.popleft()` |
| Fast lookups | `dict` or `set` | `.get()`, `.add()` |
| Unique elements | `set` | `.add()`, `.remove()` |
| Min/Max extraction | `heapq` | `heappush()`, `heappop()` |
| Prefix search | `Trie` | Custom class |
| Connectivity | `Union-Find` | Custom class |

## Complexity Notation Legend

Each method shows `[Time Complexity, Space Complexity]`

- **n** = number of elements
- **m** = number of elements in second set/dict
- **k** = size of input (for extend, update operations)
- **V** = number of vertices
- **E** = number of edges
- **α(n)** = inverse Ackermann function (essentially constant)
- **\*** = amortized or average case; worst case can be O(n) with poor hash function