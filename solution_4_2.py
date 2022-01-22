# start time 4:00 1/18
# # end time 4:00 2/2

"""
You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their
work duties -- and now you need to escape from the space station as quickly and
as orderly as possible! The bunnies have all gathered in various locations
throughout the station, and need to make their way towards the seemingly
endless amount of escape pods positioned in other parts of the station. You
need to get the numerous bunnies through the various rooms to the escape pods.
Unfortunately, the corridors between the rooms can only fit so many bunnies at
a time. What's more, many of the corridors were resized to accommodate the
LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of
the escape pods, and how many bunnies can fit through at a time in each
direction of every corridor in between, figure out how many bunnies can safely
make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of
integers denoting where the groups of gathered bunnies are, an array of
integers denoting where the escape pods are located, and an array of an array
of integers of the corridors, returning the total number of bunnies that can
get through at each time step as an int. The entrances and exits are disjoint
and thus will never overlap. The path element path[A][B] = C describes that
the corridor going from A to B can fit C bunnies at each time step.  There are
at most 50 rooms connected by the corridors and at most 2000000 bunnies that
will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each
time step.  (Note that in this example, room 3 could have sent any variation
of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains
the same.)

Languages
=========

To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(
    [0],
    [3],
    [
        [0, 7, 0, 0],
        [0, 0, 6, 0],
        [0, 0, 0, 8],
        [9, 0, 0, 0]
    ]
    )
Output:
    6

Input:
solution.solution(
    [0, 1],
    [4, 5],
    [
        [0, 0, 4, 6, 0, 0],
        [0, 0, 5, 2, 0, 0],
        [0, 0, 0, 0, 4, 4],
        [0, 0, 0, 0, 6, 6],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    )
Output:
    16

"""


class Vertex(object):
    __slots__ = ("height", "excess")

    def __init__(self, height=0, excess=0):
        self.height = height  # int
        self.excess = excess  # int

    def __repr__(self):
        return "Vertex(height={}, excess={})".format(self.height, self.excess)


class Edge(object):
    __slots__ = ("u", "v", "flow", "capacity")

    def __init__(self, u, v, capacity, flow=0):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow

    def __repr__(self):
        return "Edge(u={}, v={}, flow={}, capacity={})".format(self.u,
                                                               self.v,
                                                               self.flow,
                                                               self.capacity)


class Graph(object):
    __slots__ = ("n_vertices", "edge", "vertex")

    def __init__(self, n_vertices):
        self.n_vertices = n_vertices
        self.vertex = [Vertex(0, 0) for _ in range(n_vertices)]
        self.edge = []

    def add_edge(self, u, v, capacity):
        self.edge.append(Edge(u, v, capacity))

    def get_max_flow(self, s, t):
        self._preflow(s)

        while self._overflow_vertex() >= 0:
            u = self._overflow_vertex()
            if not self._push(u):
                self._relabel(u)

        return self.vertex[t].excess

    def _push(self, u):
        for i, edge in filter(lambda e: e[1].u == u, enumerate(self.edge)):
            if edge.flow == edge.capacity:
                continue

            if self.vertex[u].height > self.vertex[edge.v].height:
                flow = min(edge.capacity - edge.flow, self.vertex[u].excess)
                self.vertex[u].excess -= flow
                self.vertex[edge.v].excess += flow
                edge.flow += flow
                self._update_reverse_edge_flow(i, flow)
                return True
        return False

    def _relabel(self, u):
        min_height = float("inf")
        for edge in filter(lambda e: (e.u == u) and (e.flow != e.capacity),
                           self.edge):
            if self.vertex[edge.v].height < min_height:
                min_height = self.vertex[edge.v].height
                self.vertex[u].height = min_height + 1

    def _preflow(self, s):  # int
        """
        args:
          s:  int source index

        returns:
          None
        """
        self.vertex[s].height = self.n_vertices
        for edge in filter(lambda e: e.u == s, self.edge):
            edge.flow = edge.capacity
            self.vertex[edge.v].excess += edge.flow
            self.edge.append(Edge(u=edge.v, v=s, capacity=0, flow=-edge.flow))

    def _update_reverse_edge_flow(self, i, flow):
        u, v = self.edge[i].v, self.edge[i].u
        for edge in filter(lambda e: e.v == v and e.u == u, self.edge):
            edge.flow -= flow
            break
        else:
            self.edge.append(Edge(u, v, capacity=flow, flow=0))

    def _overflow_vertex(self):
        for vertex_idx, vertex in enumerate(self.vertex[1:-1], 1):
            if vertex.excess > 0:
                return vertex_idx
        else:
            return -1


def _test_max_flow():
    vertices = 6
    g = Graph(vertices)
    g.add_edge(0, 1, 16)
    g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 10)
    g.add_edge(2, 1, 4)
    g.add_edge(1, 3, 12)
    g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7)
    g.add_edge(4, 5, 4)
    s = 0
    t = 5
    max_flow = g.get_max_flow(s, t)
    print max_flow == 23

    vertices = 4
    g = Graph(vertices)
    g.add_edge(0, 1, 1)
    g.add_edge(0, 2, 100)
    g.add_edge(1, 2, 100)
    g.add_edge(2, 1, 1)
    g.add_edge(1, 3, 100)
    g.add_edge(2, 3, 1)
    s = 0
    t = 3
    max_flow = g.get_max_flow(s, t)
    print max_flow == 3


def solution(entrances, exits, path):
    pass


def _test_solution():
    print solution([0, 1], [4, 5], [
        [0, 0, 4, 6, 0, 0],
            [0, 0, 5, 2, 0, 0],
            [0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]) == 16

    print solution([0], [3],
                   [[0, 7, 0, 0],
                    [0, 0, 6, 0],
                    [0, 0, 0, 8],
                    [9, 0, 0, 0]
                    ]) == 6


if __name__ == '__main__':
    a = solution([0, 1], [4, 5], [
        [0, 0, 4, 6, 0, 0],
        [0, 0, 5, 2, 0, 0],
        [0, 0, 0, 0, 4, 4],
        [0, 0, 0, 0, 6, 6],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ])
