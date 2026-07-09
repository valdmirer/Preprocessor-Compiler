# Importing tests;
from tests.tests import *

# GOOD'OLD EXPECT
def Expect(BOOLEAN, MESSAGE):
    if not BOOLEAN:
        print(MESSAGE)
        exit(1)
        return 1, MESSAGE
    return 0, ""

# A1 for: simple func, Regex
class A1:
    def __init__(self):
        self.reg = reg

    def FIGOUTTEST(target):
        # figure it out.
        def decorator(func):
            def wrapper(*args, **kwargs):
                _func = reg[binarySearch(HASHash(target).hash(), reg)][1]
                a = _func(*func(*args))
                #for i in range(len(args)):
                #    EXPECT(a[i] != args[i], "test Fail: result was unchanged")

                return a
            return wrapper
        return decorator

def binarySearch(target, l: list):
    Expect(type(l) == list, f"BinarySearch-ERROR: type: {type(l)} is not a list.")
    if type(l[0]) == list:
        low, high = 0, len(l) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if l[mid][0] == target:
                return mid
            elif l[mid][0] < target:
                low = mid + 1
            else:
                high = mid - 1
    else:
        low, high = 0, len(l) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if l[mid] == target:
                return mid
            elif l[mid] < target:
                low = mid + 1
            else:
                high = mid - 1

    return -1


def bubbleSort(l :list = []):
    Expect(type(l) == list, f"BubbleSort-ERROR: type: {type(l)} is not a list.")
    a = l
    if len(l) != 0 and type(l[0]) == list:
        for o in range(len(l)-1, 0, -1):
            for i in range(o):
                if l[i][0] > l[i+1][0]:
                    l[i], l[i+1] = l[i+1], l[i]
    else:
        for o in range(len(l)-1, 0, -1):
            for i in range(o):
                if a[i] > a[i+1]:
                    a[i], a[i+1] = a[i+1], a[i]
        return a

#BUBBLESORT(reg)

if __name__ == '__main__':
    @A1.FIGOUTTEST("clstest1")
    def fig(a, b, c):
        print("performing")
        return "HEY HOW ARE YOU DOING?", ["1__LINE__\u200BNice", "2__LINE__\u200Byess"], " and 3"
    print(fig("a-yay", "b-yay", "c-yay"))
