from symbol import Symbol
from tree import Tree, Leaf

class Compiler:
    def __init__(self):
        self.tree = []
        self.par_stack = []
        self.next_sign = True
        self.root = None

    def CreateTree(self):
        pass

#
# Rules:
#  - If symbol is operator, it becomes the new root. Old root becomes the
#    left side of the root.
#  - If symbol is identifier, it is placed on the right of the new root.
#  - If there is a parentheses, next symbol is taken as an identifier and
#    that identifier becomes the new local root (root is kept intact). When
#    parentheses end, the local root reverts to previous).
#
# Requirements:
#  - Where to store the past roots
#  - A way to know how many parentheses have been opened
#  - A buffer to keep the symbol when it is going to get swapped
#
    def AddToTree(self, symbol):
        if(self.tree == []):
            new_leaf = Leaf(symbol, self.next_sign)
            self.tree.append(new_leaf)
            self.par_stack.append(self.tree[0])
            self.root = self.tree[0]

        elif(symbol.code == "PAR_BEGIN"):
            new_leaf = Leaf(symbol, self.next_sign, upper=self.root)
            self.tree.append(new_leaf)
            self.root.right = self.tree[-1]
            self.par_stack.append(self.tree[-1])
            self.root = self.tree[-1]

        elif(symbol.code == "PAR_END"):
            self.par_stack.pop()
            self.root = self.par_stack[-1]

        elif(symbol.code == "NEGATION"):
                    self.next_sign = False

        elif(symbol.code == "IDENTIFIER"):
            new_leaf = Leaf(symbol, self.next_sign, upper=self.root)
            self.next_sign = True
            self.tree.append(new_leaf)
            self.root.right = self.tree[-1]

        else:
            new_leaf = Leaf(symbol, self.next_sign, upper=self.root.upper, left=self.root)
            self.next_sign = True
            self.tree.append(new_leaf)

            up = self.root.upper
            if(up is not None):
                if(up.left is self.root):
                    up.left = self.tree[-1]
                else:
                    up.right = self.tree[-1]

            self.root.upper = self.tree[-1]
            self.root = self.tree[-1]

    def PrintTree(self):
        # PRINT ALL THE TREE
        prnt_str = "::TREE::"
        for i in self.tree:
            prnt_str += "\nSYM" + str(i)
            prnt_str += "\nSI" + str(i.sign)
            prnt_str += "\n\tUP" + str(i.upper)
            prnt_str += "\n\tLEFT" + str(i.left)
            prnt_str += "\n\tRIGHT" + str(i.right)
        prnt_str += "\n"
        return prnt_str

    def ParseStatement(self, statement):
        if(statement == ""):
            raise ValueError
        print("Statement:", statement)
        i = 0
        while(i < len(statement)):
            psym = statement[i]
            if(psym == "-"):
                psym = statement[i:i+2]
                i += 1
            elif(psym == "<"):
                psym = statement[i:i+3]
                i += 2
            elif(psym.isalpha() and psym not in Symbol.symbol_table.values()):
                u = 1
                while(i+u < len(statement) and statement[i+u].isalpha() and statement[i+u] != 'v'):
                    psym = statement[i:i+u]
                    u += 1
                psym = statement[i:i+u]
                i = i+u

            # Check fo empty string
            if( psym.strip() == ""):
                i += 1
                continue

            new_symbol = Symbol(psym)
            print(new_symbol.code, new_symbol.mask)
            self.AddToTree(new_symbol)
            i += 1

        self.NormalizeTree()
        self.SetRoot()

        print("REAL ROOT:", self.root)
        self.PrintTree()

    def SetRoot(self):
        roots = []
        for leaf in self.tree:
            if(leaf.upper == None):
                roots.append(leaf)
        if( len(roots) == 1):
            self.root = roots[0]
        else:
            raise LookupError

    def NormalizeTree(self):
        for leaf in self.tree:
            if(leaf.symbol.code == "PAR_BEGIN"):
                if(leaf.left is not None):
                    raise Exception

                if(leaf.right is not None):
                    leaf.symbol = leaf.right.symbol
                    self.tree.pop( self.tree.index(leaf.right) )
                    leaf.right = None
                else:
                    raise Exception

