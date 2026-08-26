# Coding Preferences

## Existing code changes

Never change, rewrite, refactor, optimize, or fix my existing solution code
without my explicit permission. When I ask for documentation, comments, tests,
or advice, limit changes strictly to what I requested and leave the solution
implementation exactly as written.

## Recommendation requests

Whenever I use the word "recommendation" followed by a function definition or
function name, review that function and give recommendations based on relevant
best practices, including correctness, edge cases, readability, naming, type
annotations, mutation behavior, time complexity, and space complexity. Do not
update, rewrite, refactor, optimize, or fix the code directly. Explain suggested
changes in the chat only, and clearly state that no files were changed.

## Approach requests

Whenever I ask to add an "Approach" to a solution:

1. Add a clear, explanatory function docstring with a clearly labeled
   `Approach` section. Explain the function's purpose, important behavior,
   parameters, return value, mutation behavior, and any assumptions or
   constraints needed to use it correctly.
2. If the solution uses a recognized algorithm, include its canonical name in
   the `Approach` section, such as `Boyer-Moore Majority Vote Algorithm` or
   `Dutch National Flag Algorithm`. Do not invent an algorithm name when the
   solution does not use a known named algorithm.
3. Explain the algorithm thoroughly in numbered, step-by-step order.
4. Add a `Time Complexity` section that states the Big-O complexity and explains
   why it has that complexity based on the loops, operations, and input size.
5. Add a `Space Complexity` section that states the Big-O complexity and explains
   exactly which variables or data structures use the additional memory.
6. Add step-by-step inline comments to the implementation so the comments match
   the numbered steps in the approach.
7. Keep every complexity claim accurate for the implementation. Mention when the
   implementation does not satisfy a complexity requirement from the prompt.

## Test-case format

Write each test as a separate block with `expected` above `result`, followed by
an assertion and output. Do not create a `test_cases` collection or loop over
test cases.

Whenever I ask to "add a test," "add tests," or "add test cases," append every
new test block to the bottom of the existing test section in `solve()`, directly
before the end of `solve()`. Never insert a new test between existing test
blocks.

Whenever I ask to "add a test," "add tests," or "add test cases," comment out
every pre-existing test block and leave only the newly added test block or
blocks active. Comment out the complete old blocks, including their input
setup, `expected`, `result`, assertions, and print statements. Do not delete
the old tests.

Whenever I ask to "add tests" or "add test cases," cover all relevant edge cases
allowed by the problem's constraints, in addition to normal examples. Before
finishing, explicitly check every minimum and maximum constraint, each boundary
value, and every important algorithm-specific transition or branch. Consider
minimum and maximum input sizes and values, empty inputs only when allowed,
single-element inputs, duplicates, all-identical values, already-valid inputs,
negative values, zero, and parameters that are zero, equal to the input size, or
larger than the input size when applicable. Include tests for matches or valid
results at the beginning, middle, and end of the input when position matters.
Include only edge cases relevant to the specific problem, and keep every test in
the separate-block format above. Do not claim coverage is complete until this
checklist has been verified against the problem's stated constraints.

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
