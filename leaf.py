from symbol import Symbol
from copy import deepcopy,copy

class Leaf:
    def __init__(self, symbol, isNeg, upper=None, left=None, right=None):
        self.symbol = symbol
        self.upper = upper
        self.left = left
        self.right = right
        self.sign = isNeg

    def __repr__(self):
        ret_str = "[{1}][{2}]({0})".format( id(self) % 1000, self.symbol, self.sign )
        return ret_str

    def __str__(self):
        return str(self.symbol)
    
    def DuplicateTree(self):
        new_tree = []

        # Add To Real Tree of symbols
        def A2T(l):
            if(l == None):
                return
            new_tree.append(l)
            A2T(l.left)
            A2T(l.right)

        new_leaf = deepcopy(self)
        A2T(new_leaf)
        return (new_leaf, new_tree)
