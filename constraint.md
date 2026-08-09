# Coding Preferences

## Approach requests

Whenever I ask to add an "Approach" to a solution:

1. Add a clearly labeled `Approach` section to the function's docstring.
2. Explain the algorithm thoroughly in numbered, step-by-step order.
3. Add a `Time Complexity` section that states the Big-O complexity and explains
   why it has that complexity based on the loops, operations, and input size.
4. Add a `Space Complexity` section that states the Big-O complexity and explains
   exactly which variables or data structures use the additional memory.
5. Add step-by-step inline comments to the implementation so the comments match
   the numbered steps in the approach.
6. Keep every complexity claim accurate for the implementation. Mention when the
   implementation does not satisfy a complexity requirement from the prompt.

## Test-case format

Write each test as a separate block with `expected` above `result`, followed by
an assertion and output. Do not create a `test_cases` collection or loop over
test cases.
