from functools import reduce


def addnumbers(a, b):
    return a + b


def addnumbers(arr):
    return reduce(lambda a, b: a + b, arr)
