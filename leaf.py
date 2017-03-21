from symbol import Symbol

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
