# [Effective Unit Testing](https://www.youtube.com/watch?v=fr1E9aVnBxw)

### Why do we write unit tests?
+ Because we want out code to work
+ Because we want it to **keep** working
+ Because we want to develop faster with more confidence and few regressions
+ Because we make mistakes

### The Fundamental Principle of Unit Testing
Code that...**verify that a known, fixed input produces a known, fixed output.** Known and fixed are very important. We want to avoid where we are sending in random data or time. Test the square root of 9 not 17.

### Eliminate everything that makes input or output unclear or contingent
+ Never generate random input. Alway used **fixed** values.
+ Don't use named constants from the model code. Prefer literal strings and numbers.
+ Don't access network and preferably not the file system.
+ Control time so you are not dependant on things outside your control

### Write you tests first
+ It's not just about testing, it's about software development.
+ You start with the user rather than the used code.
+ If you wrote tests before code, it shouldn't be coupled with the code

### Why *Unit* Test
+ Unit means **One**. Each test tests exactly one thing.
+ Each test method is one test.
+ Best practice; one assert per test method
+ Share the setup in a fixture, not the same method
+ Do not share data between tests or global state

### *Unit* also means **Independent**
+ Tests can (and do) run in any order
+ Tests can (and do) run in parallell in mutliple threads
+ Tests should not interfer with each other

### Speed
+ A single test should run in a second or less
+ A complete test suite should run in a minute or less
+ Separate larger tests into addition suites
+ This is for ease of development
+ Fail fast. Run slow tests last

### Passing tests should produce no output
+ Maybe a Green Bar or "Test Passed"
+ If everything's good, they should be quiet.
+ If necessary silence loggers in tests

### Failing tests should produce clear output
+ Failing tests should give clear, unambigious error message.
+ Rotate your test data, don't use the same data in every tests. Don't use int(3) for every int.

### Flakiness
+ Sometimes the test pass, sometimes not. This is **flakiness**. Work really, really hard to avoid. Source: Time dependance, Network availability, Explicit Randomness, Multithreding

### System Skem
+ Tests pass on my machine but not your coworkers. Check assumptions about underlying OS, floating point roundoff, Integer width, default character set

### Avoid Condition Logic in Tests
+ if/else and loops, should be seperate. Conditional logic may not run

### Debugging
+ Write a failing test before you fix the bug. **Good idea**
+ If the test passes, the bug isn't what you think it is.
+ Prevents future bugs from re-entering in same code.

### Refactoring
+ Break the code before you refactor it
+ Check your code coverage
+ If necessary, write additional tests before doing unsafe refactorings

### Development Practices
+ Use continuous integration (e.g. Travis)
+ Use a submit queue (not many in the audiance used this)
+ Never, ever allow a check in with a failing test
+ If it does happen, rollback fast, ask questions later.
+ A red test block all mergers. No further check ins until the build is green.

## Final Thoughts
+ Write your tests first
+ Make all tests unambigous and reproducible
