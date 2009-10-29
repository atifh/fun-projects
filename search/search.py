#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>

import time

def print_timing(func):
    """A decorator to calculate the time taken by a function
    to execute.
    """
    def wrapper(*arg):
        t1 = time.clock()
        res = func(*arg)
        t2 = time.clock()
        print '%s took %0.3fms' % (func.func_name, (t2 - t1) * 1000.0)
        return res
    return wrapper


@print_timing
def search_item(item, lst, low=0, high=None):
    """Uses BinarySearch algo. to retrieve item 
    from a list"""

    # low and high initialised as index
    lst.sort() # Sort the list first
    if high is None:
        high = len(lst)

    while low < high:
        mid = (low + high) / 2
        midval = lst[mid]

        if midval < item:
            low = mid + 1
        elif midval > item:
            high = mid
        else:
            return midval


@print_timing
def search_item2(item, l):
    if item in l:
        return item


# Tests
# >>> search_item(9900, range(10000000))
# search_item took 340.000ms
# 9900

# >>> search_item2(9900, range(10000000))
# search_item2 took 0.000ms
# 9900
