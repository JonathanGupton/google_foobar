# coding=utf-8
from math import sqrt


def compute_largest_square(num):
    return int(sqrt(num))**2


def solution(area):
    if area == 0:
        return []
    else:
        n_area = compute_largest_square(area)
        return [n_area] + solution(area - n_area)


def area_tests():
    print solution(15324) == [15129, 169, 25, 1]
    print solution(12) == [9, 1, 1, 1]
    print solution(1) == [1]
    print solution(1000000) == [1000000]
    print solution(9) == [9]


if __name__ == '__main__':
    area_tests()
