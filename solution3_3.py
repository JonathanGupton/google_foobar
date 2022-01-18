"""
Write a function called solution(n) which takes a positive integer as a string
and returns the minimum number of operations needed to transform the number of
pellets to 1. The fuel intake control panel can only display a number up to 309
digits long, so there won't ever be more pellets than you can express in that
many digits.

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy
   released when a quantum antimatter pellet is cut in half, the safety controls
   will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string
and returns the minimum number of operations needed to transform the number of
pellets to 1.

The fuel intake control panel can only display a number up to 309 digits long,
so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

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
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2

"""
import heapq


def generate_next_positions(n):
    if n % 2 == 0:
        yield n // 2
    else:
        yield n + 1
        yield n - 1


def solution(n):
    n = int(n)
    goal = 1
    pq = []
    heapq.heappush(pq, (0, n))
    came_from = {n: None}
    cost_so_far = {n: 0}

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            break
        for position in generate_next_positions(current):
            new_cost = cost_so_far[current] + 1
            if position not in cost_so_far or new_cost < cost_so_far[position]:
                cost_so_far[position] = new_cost
                heapq.heappush(pq, (new_cost, position))
                came_from[next] = current
    return cost_so_far[1]



def _test_solution():
    n = "15"
    s = solution(n)
    print n, s, s == 5

    n = "4"
    print solution(n) == 2
    print solution("30") == 6
    n = str(2 ** 1024 + 1)
    print solution(n) == 1025

_test_solution()
