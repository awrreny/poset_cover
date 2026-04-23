# Poset Cover Solver

This tool takes a set of permutations, and returns a compact set of conditions that characterise them. That is, a permutation is in the input set if and only if it satisfies the conditions.

Equivalently, we can say that given a set of total orders, this produces a small set of partial orders such that the input is exactly the union of linear extensions of the partial orders.

### Algorithm

Each pair of elements `(i, j)` is treated as a boolean variable representing whether `i < j`. 

1. The set of permutations is converted to a boolean expression in disjunctive normal form.
2. A truth table is constructed. Valuations that fail transitivity are marked with "don't-care" states.
3. The tool uses the `espresso` heuristic minimiser  (via `pyeda`) to find a compressed DNF representation.

The minimiser used is heuristic so the output is not guaranteed to be minimal, but is usually small.

The size of the truth table used internally is 2^(nC2), where n is the number of elements in the set. This runs instantly for n<7, and takes ~1min for n=7.

### Usage

This tool requires the `pyeda` library: https://pypi.org/project/pyeda/

Example:

```bash
python simplifyqueues.py -i testinput.txt -o out.txt -s '\n'
```

- `-i`: Input file path. (See `testinput.txt` for format).

- `-o`: Output file path (omit to print to stdout).

- `-s`: Input separator. For example, use `-s '|'` for `ABC|ACB`.

### Notation

This tool was initially made for Tetris research, so some of the notation may resemble Tetris notation, however the core.py file works with general permutations.

In the final output, `X<YZ` is shorthand for `X<Y & X<Z`, and similarly `XY<Z` is shorthand for `X<Z & Y<Z`.

