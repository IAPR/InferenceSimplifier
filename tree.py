from symbol import Symbol

class Tree:
    def __init__(self):
        leaves_list = []

    def __str__(self):
        pass

class Leaf:
    def __init__(self, symbol, isNeg, upper=None, left=None, right=None):
        self.symbol = symbol
        self.upper = upper
        self.left = left
        self.right = right
        self.sign = isNeg

    def __str__(self):
        ret_str = "[{1}]({0})".format( id(self) % 10000, self.symbol )
        return ret_str
