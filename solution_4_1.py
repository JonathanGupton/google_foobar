"""
You will set up simultaneous thumb wrestling matches. In each match, two
trainers will pair off to thumb wrestle. The trainer with fewer bananas will
bet all their bananas, and the other trainer will match the bet. The winner
will receive all of the bet bananas. You don't pair off trainers with the same
number of bananas (you will see why, shortly). You know enough trainer
psychology to know that the one who has more bananas always gets over-confident
and loses. Once a match begins, the pair of trainers will continue to thumb
wrestle and exchange bananas, until both of them have the same number of
bananas. Once that happens, both of them will lose interest and go back to
supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas,
after the first round of thumb wrestling they will have 6 and 2 (the one with
3 bananas wins and gets 3 bananas from the loser). After the second round,
they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point
they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the
trainers had started with 1 and 4 bananas, then they keep thumb wrestling!
1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the
maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers
depicting the amount of bananas the each trainer starts with, returns the
fewest possible number of bunny trainers that will be left to watch the
workers. Element i of the list will be the number of bananas that trainer i
(counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the
number of bananas each trainer starts with will be a positive integer no more
than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(1,1)
Output:
    2

Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0

"""
from collections import Counter
from fractions import gcd
from itertools import combinations
import heapq


def is_looping_pair(n1, n2):  # int, int -> bool
    """
    Classify if a pair of trainers will loop or break

    Args:
        n1: int
        n2: int

    Returns:
        bool

    """
    seen = set()

    while True:
        _min, _max = min(n1, n2), max(n1, n2)

        # Reduce the banana count when able
        denominator = gcd(_min, _max)
        _min, _max = _min/denominator, _max/denominator

        if (_min + _max) % 2 != 0 or (_min, _max) in seen:
            return True

        if _min == _max:
            return False

        seen.add((_min, _max))
        n1, n2 = _min + _min, _max - _min



def solution(banana_list):
    loop_status = {}  # dict[tuple[int, int], int] {(n_bananas, n_bananas): loop_bool}
    banana_groups = {}  # dict[frozenset[int,..], int]

    def search_pairs(banana_slice):
        if not banana_slice:
            return 0
        if tuple(banana_slice) in banana_groups:
            return banana_groups[tuple(banana_slice)]

        min_trainers = len(banana_slice)
        t1 = banana_slice[0]
        for t2 in range(1, len(banana_slice)):
            pair = (t1, banana_slice[t2])
            if pair not in loop_status:
                loop_status[pair] = is_looping_pair(*pair)
            n_trainers = 0 if loop_status[pair] else 2
            combination = n_trainers + search_pairs(banana_slice[1:t2] + banana_slice[t2+1:])
            min_trainers = combination if combination < min_trainers else min_trainers
        banana_groups[tuple(banana_slice)] = min_trainers
        return min_trainers

    ret_val = search_pairs(banana_list)
    return ret_val



def _test_is_looping_pair():
    print is_looping_pair(1, 4) == True
    print is_looping_pair(1, 3) == False
    print is_looping_pair(3, 5) == False
    print is_looping_pair(1, 7) == False
    print is_looping_pair(1, 13) == True
    print is_looping_pair(1, 21) == True
    print is_looping_pair(1, 19) == True
    print is_looping_pair(7, 3) == True
    print is_looping_pair(7, 21) == False
    print is_looping_pair(7, 13) == True
    print is_looping_pair(3, 21) == False
    print is_looping_pair(7, 19) == True
    print is_looping_pair(3, 13) == False
    print is_looping_pair(3, 19) == True
    print is_looping_pair(13, 19) == False


def _test_solution(solution_fxn):
    print solution_fxn([1, 1]) == 2
    print solution_fxn([1, 1, 1, 1, 1, 7, 3, 21, 13, 19]) == 2
    print solution_fxn([1, 7, 3, 21, 13, 19]) == 0
    print solution_fxn([1, 27, 41, 52, 74, 99])
    print solution_fxn([1, 1, 1, 1, 1, 7, 3, 21])
    # print solution_fxn([i for i in range(1, 101)])

# l1 = solution([1, 1])
# l2 = solution([1, 7, 3, 21, 13, 19])
# l = [1, 7, 3, 21, 13, 19]
#
#
# def all_pairs(lst):
#     a = lst[0]
#     for i in range(1, len(lst)):
#         pair = (a, lst[i])
#         for rest in all_pairs(lst[1:i] + lst[i + 1:]):
#             yield [pair] + rest
#
_test_solution(solution)
#
# l = [1, 7, 3, 21, 13, 19]
# l = solution2(l)

# s = solution([1, 1, 1, 7, 3, 21, 13, 19])
