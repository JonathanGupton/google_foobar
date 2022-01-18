"""Working solution"""


from collections import deque


def solution(map):
    """
    Find the shortest path from start to end with one optional wall removal.

    Args:
      map: list[list[int]] Representation of halls 0 and walls 1

    Returns:
        The minimum integer distance from the start position (0, 0) to the end
          position (w-1,h-1) with one optional wall removal.
    """
    def neighbours(x, y):
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    removals_available = 1

    start = (0, 0)
    walls_removed = 0
    steps = 1
    queue = deque([(start, walls_removed, steps)])

    goal_y, goal_x = len(map), len(map[0])
    visited = set()

    while queue:
        (y, x), walls_removed, steps = queue.popleft()
        if walls_removed > removals_available:
            continue
        if (y, x) == (goal_y - 1, goal_x - 1):
            return steps
        for neighbor_y, neighbor_x in neighbours(y, x):
            if not 0 <= neighbor_y < goal_y or not 0 <= neighbor_x < goal_x \
                    or (neighbor_y, neighbor_x, walls_removed) in visited \
                    or walls_removed > removals_available:
                continue
            queue.append(
                (
                    (neighbor_y, neighbor_x),
                    walls_removed + map[neighbor_y][neighbor_x],
                    steps + 1
                )
            )
            visited.add((neighbor_y, neighbor_x, walls_removed))


def _test_solution():
    s = solution(
        [
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 0]
        ]
    )
    print s, s == 7

    s = solution([
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0]]
    )
    print s, s == 11

    s = solution([[0, 1], [1, 0]])
    print s, s == 3

    s = solution([[0, 0], [0, 0]])
    print s, s == 3

    s = solution([
        [0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]]
    )
    print s, s == 11

    s = solution([
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    ])
    print s, s == 23


_test_solution()
