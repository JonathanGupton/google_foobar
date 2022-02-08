# start 1/23/2022 12:00 AM
# end 2/14/2022 12:00 AM

"""
Disorderly Escape
=================

Oh no! You've managed to free the bunny workers and escape Commander Lambdas
exploding space station, but Lambda's team of elite starfighters has flanked
your ship. If you dont jump to hyperspace, and fast, youll be shot out of the
sky!

Problem is, to avoid detection by galactic law enforcement, Commander Lambda
planted the space station in the middle of a quasar quantum flux field. In
order to make the jump to hyperspace, you need to know the configuration of
celestial bodies in the quadrant you plan to jump through. In order to do
*that*, you need to figure out how many configurations each quadrant could
possibly have, so that you can pick the optimal quadrant through which youll
make your jump.

There's something important to note about quasar quantum flux fields'
configurations: when drawn on a star grid, configurations are considered
equivalent by grouping rather than by order. That is, for a given set of
configurations, if you exchange the position of any two columns or any two rows
some number of times, youll find that all of those configurations are
equivalent in that way -- in grouping, rather than order.

Write a function solution(w, h, s) that takes 3 integers and returns the
number of unique, non-equivalent configurations that can be found on a star
grid w blocks wide and h blocks tall where each celestial body has s possible
states. Equivalency is defined as above: any two star grids with each celestial
body in the same state where the actual order of the rows and columns do not
matter (and can thus be freely swapped around). Star grid standardization
means that the width and height of the grid will always be between 1 and 12,
inclusive. And while there are a variety of celestial bodies in each grid,
the number of states of those bodies is between 2 and 20, inclusive. The
solution can be over 20 digits long, so return it as a decimal string.  The
intermediate values can also be large, so you will likely need to use at least
64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial
body is either in state 0 (for instance, silent) or state 1 (for instance,
noisy).  We can examine which grids are equivalent by swapping rows and
columns.

00
00

In the above configuration, all celestial bodies are "silent" - that is, they
have a state of 0 - so any swap of row or column would keep it in the same
state.

00 00 01 10
01 10 00 00

1 celestial body is emitting noise - that is, has a state of 1 - so swapping
rows and columns can put it in any of the 4 positions.  All four of the above
configurations are equivalent.

00 11
11 00

2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves
them unchanged, and swapping rows simply moves them between the top and bottom.
In both, the *groupings* are the same: one row with two bodies in state 0, one
row with two bodies in state 1, and two columns with one of each state.

01 10
01 10

2 noisy celestial bodies adjacent vertically. This is symmetric to the
side-by-side case, but it is different because there's no way to transpose the
grid.

01 10
10 01

2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have
one of each state, so they are equivalent to each other.

01 10 11 11
11 11 01 10

3 noisy celestial bodies, similar to the case where only one of four is noisy.

11
11

4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so solution(2, 2, 2) would
return 7.

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.


-- Python cases --
Input:
solution.solution(2, 3, 4)
Output:
    430

Input:
solution.solution(2, 2, 2)
Output:
    7

"""
import fractions
from fractions import Fraction
from itertools import product
from math import factorial


def make_permutation_groups(degree,
                            max_val=None,
                            permutation_head=None,
                            permutation_groups=None):
    if permutation_head is None:
        permutation_head = []

    if permutation_groups is None:
        permutation_groups = []

    if degree == 0:
        permutation_groups.append(permutation_head)
        return

    if max_val is None:
        max_val = degree

    for length in range(max_val, 0, -1):
        if length == 1:  # short circuit unnecessary recursion
            permutation_head.append((length, degree))
            make_permutation_groups(0, 0, permutation_head, permutation_groups)
            continue
        else:
            length_count_max = degree // length
            for count in range(length_count_max, 0, -1):
                new_permutation_head = list(permutation_head)
                new_permutation_head.append((length, count))
                new_remaining = degree - (length * count)
                if new_remaining >= length:
                    new_max_val = length - 1
                else:
                    new_max_val = length
                make_permutation_groups(new_remaining, new_max_val, new_permutation_head, permutation_groups)
    return permutation_groups


def compute_cycle_index_coefficient(permutation_group):
    denominator = 1
    for length, count in permutation_group:
        denominator *= length ** count * factorial(count)
    return Fraction(1, denominator)


def symmetric_cycle_index(degree):
    groups = make_permutation_groups(degree)
    cycle_index = [(compute_cycle_index_coefficient(group), group) for group in groups]
    return cycle_index


def least_common_multiple(a, b):
    return abs(a * b) // fractions.gcd(a, b)


def solution(h, w, s):
    rows, cols = symmetric_cycle_index(h), symmetric_cycle_index(w)
    output = 0
    for row, col in product(rows, cols):
        result = 1
        coefficient = row[0] * col[0]
        for l, r in product(row[1], col[1]):
            exponent = (l[0] * l[1] * r[0] * r[1]) / least_common_multiple(l[0], r[0])
            result *= s ** exponent
        output += coefficient * result
    return str(output)


def _test_make_permutation_groups():
    print make_permutation_groups(1) == [[(1, 1)],
                                         ]
    print make_permutation_groups(2) == [[(2, 1)],
                                         [(1, 2)]
                                         ]
    print make_permutation_groups(3) == [[(3, 1)],
                                         [(2, 1), (1, 1)],
                                         [(1, 3)]
                                         ]
    print make_permutation_groups(4) == [[(4, 1)],
                                         [(3, 1), (1, 1)],
                                         [(2, 2)],
                                         [(2, 1), (1, 2)],
                                         [(1, 4)],
                                         ]
    print make_permutation_groups(5) == [[(5, 1)],
                                         [(4, 1), (1, 1)],
                                         [(3, 1), (2, 1)],
                                         [(3, 1), (1, 2)],
                                         [(2, 2), (1, 1)],
                                         [(2, 1), (1, 3)],
                                         [(1, 5)],
                                         ]


def _test_symmetric_cycle_index():
    """
    Results from https://mathworld.wolfram.com/SymmetricGroup.html
    """
    print symmetric_cycle_index(1) == [
        (Fraction(1, 1), [(1, 1)])
    ]

    print symmetric_cycle_index(2) == [
        (Fraction(1, 2), [(2, 1)]),
        (Fraction(1, 2), [(1, 2)])
    ]

    print symmetric_cycle_index(3) == [
        (Fraction(1, 3), [(3, 1)]),
        (Fraction(1, 2), [(2, 1), (1, 1)]),
        (Fraction(1, 6), [(1, 3)])
    ]

    print symmetric_cycle_index(4) == [
        (Fraction(1, 4), [(4, 1)]),
        (Fraction(1, 3), [(3, 1), (1, 1)]),
        (Fraction(1, 8), [(2, 2)]),
        (Fraction(1, 4), [(2, 1), (1, 2)]),
        (Fraction(1, 24), [(1, 4)])
    ]
    print symmetric_cycle_index(5) == [
        (Fraction(1, 5), [(5, 1)]),
        (Fraction(1, 4), [(4, 1), (1, 1)]),
        (Fraction(1, 6), [(3, 1), (2, 1)]),
        (Fraction(1, 6), [(3, 1), (1, 2)]),
        (Fraction(1, 8), [(2, 2), (1, 1)]),
        (Fraction(1, 12), [(2, 1), (1, 3)]),
        (Fraction(1, 120), [(1, 5)]),
    ]


def _test_solution():
    print solution(2, 2, 2) == "7"
    print solution(2, 3, 1) == "1"
    print solution(2, 3, 2) == "13"
    print solution(2, 3, 3) == "92"
    print solution(2, 3, 4) == "430"
    print solution(12, 12,
                   20) == "97195340925396730736950973830781340249131679073592360856141700148734207997877978005419735822878768821088343977969209139721682171487959967012286474628978470487193051591840"


if __name__ == '__main__':
    _test_symmetric_cycle_index()
    _test_make_permutation_groups()
    _test_solution()
