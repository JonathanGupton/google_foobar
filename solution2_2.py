from UserString import UserString
from itertools import izip_longest


"""
You've been assigned the onerous task of elevator maintenance -- ugh! It
wouldn't be so bad, except that all the elevator documentation has been lying
in a disorganized pile at the bottom of a filing cabinet for years, and you
 don't even know what elevator version numbers you'll be working on.

Elevator versions are represented by a series of numbers, divided up into major,
minor and revision integers. New versions of an elevator increase the major
number, e.g. 1, 2, 3, and so on. When new features are added to an elevator
 without being a complete new version, a second number named "minor" can be
used to represent those new additions, e.g. 1.0, 1.1, 1.2, etc. Small fixes or
maintenance work can be represented by a third number named "revision",
e.g. 1.1.1, 1.1.2, 1.2.0, and so on. The number zero can be used as a major for
pre-release versions of elevators, e.g. 0.1, 0.5, 0.9.2, etc
(Commander Lambda is careful to always beta test her new technology,
with her loyal henchmen as subjects!).

Given a list of elevator versions represented as strings, write a
function solution(l) that returns the same list sorted in
ascending order by major, minor, and revision number so that you can
identify the current elevator version. The versions in list l will always
contain major numbers, but minor and revision numbers are optional.
If the version contains a revision number, then it will also have a minor
number.

For example, given the list l as
["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"],
the function solution(l) would return the list
["1.0", "1.0.2", "1.0.12", "1.1.2", "1.3.3"].

If two or more versions are equivalent but one version contains more
numbers than the others, then these versions must be sorted ascending based
on how many numbers they have, e.g ["1", "1.0", "1.0.0"].

The number of elements in the list l will be at least 1 and will not exceed 100.

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
solution.solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"])
Output:
    0.1,1.1.1,1.2,1.2.1,1.11,2,2.0,2.0.0

Input:
solution.solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"])
Output:
    1.0,1.0.2,1.0.12,1.1.2,1.3.3

-- Java cases --
Input:
Solution.solution({"1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"})
Output:
    0.1,1.1.1,1.2,1.2.1,1.11,2,2.0,2.0.0

Input:
Solution.solution({"1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"})
Output:
    1.0,1.0.2,1.0.12,1.1.2,1.3.3

Constraints
==========

Your code will run inside a Python 2.7.13 sandbox. All tests will be run by
calling the solution() function.

Standard libraries are supported except for bz2, crypt, fcntl, mmap, pwd,
pyexpat, select, signal, termios, thread, time, unicodedata, zipimport, zlib.

Input/output operations are not allowed.

Your solution must be under 32000 characters in length including new lines
and other non-printing characters.

"""


class Version(UserString):
    def __init__(self, seq):
        super(Version, self).__init__(seq)

    def __lt__(self, other):
        for l, r in izip_longest(self.data.split('.'),
                                 other.data.split('.')):
            if l and r:
                if int(l) == int(r):
                    continue
                elif int(l) < int(r):
                    return True
                else:
                    return False
            elif l and not r:
                return False
            else:
                return True
        return True

    def __str__(self):
        return self.data


def solution(l):
    return map(str, sorted(map(Version, l)))



if __name__ == '__main__':
    # l = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]
    # m = map(Version, l)
    # b = m[0] < m[1]
    # l, r = Version("2.0"), Version("2")
    # l, r = Version("2"), Version("2.0.0")
    # b = l < r


    # print solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"])
    # print solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"])

    print solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]) \
    == ["0.1", "1.1.1", "1.2", "1.2.1", "1.11", "2", "2.0", "2.0.0"]

    print solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]) \
    == ["1.0", "1.0.2", "1.0.12", "1.1.2", "1.3.3"]

    print solution(["0", "0.0", "0.0.0", "0"]) == ["0", "0", "0.0", "0.0.0"]

