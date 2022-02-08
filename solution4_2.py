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
from collections import defaultdict


class Vertex(object):
    """A graph node with height and excess capacity information.

    Attributes:
      h:  The integer height of the vertex.
      e:  The integer excess of the vertex.
    """
    __slots__ = ("h", "e")

    def __init__(self, h=0, e=0):
        # type: (Vertex, int, int) -> None
        """Initialize a Vortex object.

        Args:
          h: int
            The height of the vertex.  Defaults to 0 height.
          e: int
            The excess flow at the vertex.  Defaults to 0 excess.
        """
        self.h = h
        self.e = e

    def __repr__(self):
        # type: () -> str
        return "Vertex(h={}, e={})".format(self.h, self.e)


class Arc(object):
    """A graph edge with capacity and flow information.

    Attributes:
      v:  A Union[str, int] vertex id
      u:  A Union[str, int] vertex id
      capacity: The integer max flow between vertices (u, v).
      flow: The integer current flow between vertices (u, v).  The default
        value of flow is 0.
    """
    __slots__ = ("u", "v", "flow", "capacity")

    def __init__(self, u, v, capacity, flow=0):
        # type: (Arc, Union[int, str], Union[int, str], int, int) -> None
        """Initialize an arc connecting vertex u and vertex v.

        Args:
          v:  A Union[str, int] vertex id.
          u:  A Union[str, int] vertex id.
          capacity: The integer max flow between vertices (u, v).
          flow: The integer current flow between vertices (u, v).  The default
            value of flow is 0.

        Return:
          None
        """
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow

    def __repr__(self):
        # type: () -> str
        return "Arc(u={}, v={}, flow={}, capacity={})".format(self.u,
                                                              self.v,
                                                              self.flow,
                                                              self.capacity)


class Graph(object):
    """A flow network graph.

     Attributes:
       arc:  dict[Union[int, str], dict[Union[int, str], Arc]]
         A dict of vertex id's mapped to their adjacent vertices and arc
         values.
       vertex:  dict[Union[int, str], Vertex]
        A dict of vertex id's and their associated vertex values.
    """
    __slots__ = ("arc", "vertex")

    def __init__(self):
        self.vertex = {}
        self.arc = defaultdict(dict)

    def add_arc(self, u, v, capacity):
        # type: (Graph, Union[int, str], Union[int, str], int) -> None
        """Add an arc connecting vertex u and vertex v to the graph.

        Args:
        u:  Union[int, str]
          The vertex u.
        v:  Union[int, str]
          The vertex v.
        Capacity: int
          The capacity of flow for arc(u, v).

        Returns:
          None
        """
        self.arc[u][v] = Arc(u, v, capacity)
        for node in (u, v):
            if node not in self.vertex:
                self.vertex[node] = Vertex(0, 0)

    def get_max_flow(self):
        # type: () -> int
        """Get the max flow for this graph.

        Return: int
          Return the max flow for this graph.
        """

        self._preflow()

        while self._overflow_vertex() >= 0:
            u = self._overflow_vertex()
            if not self._push(u):
                self._relabel(u)

        return self.vertex['t'].e

    def _push(self, u):
        # type: (Graph, Union[int, str]) -> bool
        """Push flow downhill from vertex u.

        Args:
          u: Union[int, str]
            The node from which to push excess flow.

        Returns:  bool
          Return True if excess flow can be pushed to another Vertex and False
            if not.
        """
        for v in self.arc[u]:
            if self.arc[u][v].flow == self.arc[u][v].capacity:
                continue

            if self.vertex[u].h > self.vertex[v].h:
                flow = min(self.arc[u][v].capacity - self.arc[u][v].flow,
                           self.vertex[u].e)
                self.vertex[u].e -= flow
                self.vertex[v].e += flow
                self.arc[u][v].flow += flow

                # update reverse edge flow
                if u in self.arc[v]:
                    self.arc[v][u].flow -= flow
                else:
                    self.arc[v][u] = Arc(v, u, capacity=flow, flow=0)

                return True
        return False

    def _relabel(self, u):
        # type: (Graph, int) -> None
        """Relabel the given vertex.

        Increment the height of the given vertex to the minimum height that
          allows for a future push action.

        Args:
            u: Union[int, str]
              The node whose height is to be incremented.

        Return:
            None
        """
        min_height = float("inf")
        for v in self.arc[u]:
            if (self.arc[u][v].flow != self.arc[u][v].capacity) \
                    and (self.vertex[v].h < min_height):
                min_height = self.vertex[v].h
                self.vertex[u].h = min_height + 1

    def _preflow(self):
        # type: () -> None
        """Preflow the graph.

        Set the source vertex to the height n-vertices and saturate all edges
        adjacent to the source.

        Returns:
          None
        """
        self.vertex['s'].h = len(self.vertex)
        for adjacent in self.arc['s']:
            self.arc['s'][adjacent].flow = self.arc['s'][adjacent].capacity
            self.vertex[adjacent].e += self.arc['s'][adjacent].flow
            self.arc[adjacent]['s'] = Arc(u=adjacent,
                                          v='s',
                                          capacity=0,
                                          flow=-self.arc['s'][adjacent].flow)

    def _overflow_vertex(self):
        # type: () -> int
        """Find an overflowing vertex.

        Return:
             Returns an overflowing vertex if found, otherwise returns -1.
        """
        for u in self.vertex:
            if u not in ('s', 't') and self.vertex[u].e > 0:
                return u
        else:
            return -1


def solution(entrances, exits, path):
    # type: (list[int], list[int], list[list[int]]) -> int
    """
    Find the max flow in the given graph.

    Find the max flow of the supplied path using a push-relabel max flow
      algorithm.  A synthetic source and synthetic sink are supplied to account
      for multiple-entrances and multiple-exits.

    Args:
      entrances: list[int]
        The list of source locations on the path.
      exits:  list[int]
        The list of sink locations on the path.
      path:  list[list[int]]
        The list of corridors with their flow capacity (int) to the
          corridor (int index value).  For example path[A][B] = C is equivalent
          to edge (a, b) having capacity C.

    Returns:
      Integer max flow

    """
    g = Graph()

    max_capacity = sum([sum(path[idx]) for idx in entrances])
    for idx in entrances:
        g.add_arc('s', idx, capacity=max_capacity)

    for idx in exits:
        g.add_arc(idx, 't', capacity=max_capacity)

    for u, corridor in enumerate(path):
        for v, capacity in enumerate(corridor):
            g.add_arc(u, v, capacity=capacity)

    max_flow = g.get_max_flow()
    return max_flow


def _test_max_flow():
    g = Graph()
    g.add_arc("s", 1, 16)
    g.add_arc("s", 2, 13)
    g.add_arc(1, 2, 10)
    g.add_arc(2, 1, 4)
    g.add_arc(1, 3, 12)
    g.add_arc(2, 4, 14)
    g.add_arc(3, 2, 9)
    g.add_arc(3, "t", 20)
    g.add_arc(4, 3, 7)
    g.add_arc(4, "t", 4)
    max_flow = g.get_max_flow()
    print max_flow == 23

    g = Graph()
    g.add_arc("s", 1, 1)
    g.add_arc("s", 2, 100)
    g.add_arc(1, 2, 100)
    g.add_arc(2, 1, 1)
    g.add_arc(1, "t", 100)
    g.add_arc(2, "t", 1)
    max_flow = g.get_max_flow()
    print max_flow == 3


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
    _test_max_flow()
    _test_solution()
