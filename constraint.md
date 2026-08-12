# Coding Preferences

## Existing code changes

Never change, rewrite, refactor, optimize, or fix my existing solution code
without my explicit permission. When I ask for documentation, comments, tests,
or advice, limit changes strictly to what I requested and leave the solution
implementation exactly as written.

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

## New problem-file requests

Whenever I ask to "make a file" for a coding problem:

1. Place the file in the folder most relevant to the problem's algorithm or
   topic, and use a descriptive snake_case filename.
2. Put the complete, cleanly formatted question at the top of the file inside a
   module docstring.
3. Add a typed function template with a descriptive name and the correct
   parameters and return type.
4. Leave the function unimplemented with `pass`.
5. Never provide or add a solution unless I explicitly ask for one.
6. Always add a typed `solve()` function containing exactly one test case from
   the question.
7. In that test case, put `expected` above `result`, then include an assertion
   and print both values.
8. Add an `if __name__ == "__main__":` guard that calls `solve()`.
