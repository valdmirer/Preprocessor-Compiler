##
## [ Prep version 01 ]
##

from decimal import Decimal
import string, sys, os, time

## Parser
#from src.parser import *

## Tests
from tests import *

#     ┌─────.
#     │ └──┘ │
#     │  ()  │   Free OPEN FLOPPY-PREP
#     └──────┘
#  
#     ▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
#     ▐                                            ▌
#     ▐                                            ▌
#     ▐     888 88e  888 88e  888'Y88 888 88e      ▌
#     ▐     888 888D 888 888D 888 ,'Y 888 888D     ▌
#     ▐     888 88"  888 88"  888C8   888 88"      ▌
#     ▐     888      888 b,   888 ",d 888          ▌
#     ▐     888      888 88b, 888,d88 888          ▌
#     ▐                                            ▌
#     ▐                                            ▌
#     ▐────────────────────────────────────────────▌
#     ▐          INSERT (COPYRIGHTS AMOIZ)         ▌
#     ▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌


# \\033(.?..)m

# constants are more optimized.
# than self.<whatever> in our case.

# number, type, version
#   00      0      1 (depending on prep version)

# version 1
#  -> errors_1.csv
#             <- number ->
#         ~ | 01 | 02 | 03
#    ↑    1  ...   ...  ...
#   type  2  ...   ...  ...
#    ↓    3  ...   ...  ...

# 5 = missings..

#Parser:
# DMAS
# D: 3, M: 2, A: 1, S: 0
class Pratt:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def insert(self, data):
        if self.left is None:
            self.left = Pratt(data)
        elif self.right is None:
            self.right = Pratt(data)
        elif self.right:
            self.right.insert(data)
        elif self.left:
            self.left.insert(data)
        
        #if data < self.data:
        #    if self.left is None:
        #        self.left = Pratt(data)
        #    else:
        #        self.left.insert(data)
        #elif data > self.data:
        #    if self.right is None:
        #        self.right = Pratt(data)
        #    else:
        #        self.right.insert(data)
        if not self.data:
            self.data = data

    def printTree(self):
        if self.left:
            self.left.printTree()
        print(self.data)
        if self.right:
            self.right.printTree()

a = Pratt(2)
a.insert(5)
a.insert(12)
a.insert(19)
#a.printTree()
#exit(0)

#
#   putting everything togeather
#   >>


#no-use

# undefined is not used in preprocessing. 
#ASSERT(isprep == True, f"undefined: '{line.replace("_;_", '\n')}'")

#enum

from src.runtime.rte import main

if __name__ == '__main__':
    main(*sys.argv) #->
