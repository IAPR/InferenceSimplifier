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

    def GetTreeString(self, level = 0):
        ST = Symbol.symbol_table
        ret_str = ""
        # Print left side
        if(self.left != None):
            # Creates parentheses if left side is negative AND it is not an identifier
            if(self.left.symbol.code != "IDENTIFIER"):
                ret_str += " "
                if(not self.left.sign):
                    ret_str += ST["NEGATION"]
                ret_str += ST["PAR_BEGIN"] + " " + self.left.GetTreeString(level + 1) + " " + ST["PAR_END"] + " "
            else:
                ret_str += self.left.GetTreeString(level + 1)
        if(self.symbol.code == "IDENTIFIER"):
            if(not self.sign):
                ret_str += ST["NEGATION"]
            ret_str += self.__str__()
        else:
            ret_str += " " + self.__str__() + " "
        if(self.right != None):
            # Creates parentheses if left side is negative AND it is not an identifier
            if(self.right.symbol.code != "IDENTIFIER"):
                ret_str += " "
                if(not self.right.sign):
                    ret_str += ST["NEGATION"]
                ret_str += ST["PAR_BEGIN"] + " " + self.right.GetTreeString(level + 1) + " " + ST["PAR_END"] + " "
            else:
                ret_str += self.right.GetTreeString(level + 1)

        # Problem solving for level 0
        if( (level == 0) and (not self.sign) and (self.symbol.code != "IDENTIFIER") ):
            ret_str += " " + ST["NEGATION"] + ST["PAR_BEGIN"] + " " + ret_str + " " + ST["PAR_END"] + " "
        return ret_str

    def ReplaceInTree(self, mask, value):
        if(self.symbol.mask == mask):
            if(not self.sign):
                if(value == "T"):
                    sym = Symbol("F")
                elif(value == "F"):
                    sym = Symbol("T")
                else:
                    sym = Symbol(value)
            else:
                sym = Symbol(value)
            self.symbol = sym
        if(self.left != None):
            self.left.ReplaceInTree(mask, value)
        if(self.right != None):
            self.right.ReplaceInTree(mask, value)

