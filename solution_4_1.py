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

from collections import defaultdict
from fractions import gcd
from itertools import combinations


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
    """
    Strategy:  Pack as many pairs into the found set as will fit, swapping
    as necessary
    """
    unpaired_set = set(range(len(banana_list)))  # set[int]
    pairings = {i : None for i in unpaired_set}  # dict[int, int]
    pair_map = defaultdict(set)  # dict[int, set(int)]

    for i, j in combinations(range(len(banana_list)), 2):
        if is_looping_pair(banana_list[i], banana_list[j]):
            pair_map[i].add(j)
            pair_map[j].add(i)

    for k, pairable_set in pair_map.items():
        if pairings[k] is None:
            if pairable_set & unpaired_set:
                for pairable_value in pairable_set & unpaired_set:
                    pairings[k] = pairable_value
                    pairings[pairable_value] = k
                    unpaired_set.difference_update({k, pairable_value})
                    break
            else:
                # swap logic
                other_unpaired = unpaired_set - {k}
                if other_unpaired:
                    for i in pair_map[k]:
                        if pair_map[i] & other_unpaired:
                            for j in pair_map[i] & other_unpaired:
                                if pairings[i] in pair_map[j]:
                                    temp = pairings[i]
                                    pairings[k], pairings[i] = i, k
                                    pairings[j], pairings[temp] = temp, j
                                    unpaired_set.difference_update({k, j})
                                    break
                            break

    return len(unpaired_set)



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
    from random import randint
    print solution_fxn([1]) == 1
    print solution_fxn([1, 1]) == 2
    print solution_fxn([1, 1, 1]) == 3
    print solution_fxn([1, 1, 1, 1]) == 4
    print solution_fxn([1, 3, 7, 13, 19, 21]) == 0
    print solution_fxn([1, 7, 3, 19, 13, 21]) == 0
    print solution_fxn([3, 7, 3, 7, 3, 7]) == 0
    print solution_fxn([1, 1, 1, 1, 1, 3, 7, 13, 19, 21]) == 2
    print solution_fxn([1, 27, 41, 52, 74, 99])
    print solution_fxn([1, 1, 1, 1, 1, 7, 3, 21])
    print solution_fxn([i for i in range(1, 101)])
    print solution_fxn([randint(1, 1073741823) for _ in range(100)])

    # come up with recursive match where multiple swaps are required???
    print solution_fxn([1, 3, 7, 13, 19, 21, 1, 3, 7, 13, 19, 21]) == 0


if __name__ == '__main__':


    _test_solution(solution)
