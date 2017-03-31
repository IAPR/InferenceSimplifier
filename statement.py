from symbol import Symbol
from copy import deepcopy,copy
from leaf import Leaf

class Statement:
    def __init__(self, statement):
        self.tree = []
        self.par_stack = []
        self.next_sign = True
        self.root = None

        # Creating empty tree
        if(statement is None):
            return
        if(statement == ""):
            raise ValueError
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
                i = i+u-1

            # Check fo empty string
            if( psym.strip() == ""):
                i += 1
                continue

            new_symbol = Symbol(psym)
            print("SYMBOL", repr(new_symbol))
            self.AppendSymbol(new_symbol)
            self.tree = list(set(self.tree))
            i += 1

        self.NormalizeTree()
        self.FindRealRoot()

    def __str__(self):
        return self.root.GetTreeString()

    def __repr__(self):
        return self.GetTreeInfo()
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
    def AppendSymbol(self, symbol):
        if(self.tree == []):
            new_leaf = Leaf(symbol, self.next_sign)
            self.tree.append(new_leaf)
            self.par_stack.append(self.tree[0])
            self.root = self.tree[0]

            if(symbol.code == "PAR_BEGIN"):
                self.par_stack.append(self.tree[0])
            return

        if(symbol.code == "PAR_BEGIN"):
            new_leaf = Leaf(symbol, self.next_sign, upper=self.root)
            self.tree.append(new_leaf)
            self.root.right = self.tree[-1]
            self.par_stack.append(self.tree[-1])
            self.root = self.tree[-1]

        elif(symbol.code == "PAR_END"):
            oldroot = self.par_stack.pop()
            self.root = self.par_stack[-1]
            if(self.root.symbol.code == "PAR_BEGIN" and self.root.upper != None):
                self.root = self.root.upper
            print("OLDROOT:", repr(oldroot), "\tNEWROOT:", repr(self.root))

        elif(symbol.code == "NEGATION"):
            self.next_sign = False

        elif(symbol.code == "IDENTIFIER"):
            last_symbol = self.tree[-1].symbol
            if(last_symbol.code == "PAR_BEGIN"):
                new_leaf = Leaf(symbol, True, upper=self.root)
            else:
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

    def FindRealRoot(self):
        roots = []
        for leaf in self.tree:
            if(leaf.upper == None):
                roots.append(leaf)
        if( len(roots) == 1):
            self.root = roots[0]
        else:
            raise LookupError

    def NormalizeTree(self):
        # Eliminate rogue PAR_BEGIN symbols on tree
        for leaf in self.tree:
            if(leaf.symbol.code == "PAR_BEGIN"):
                # When there is par_begin, left will always be null
                if(leaf.left is not None or leaf.right is None):
                    raise Exception

                u = leaf.upper
                r = leaf.right
                if(id(u.left) == id(leaf)):
                    u.left = r
                elif(id(u.right) == id(leaf)):
                    u.right = r
                else:
                    raise Exception
                r.upper = u
                self.tree.pop( self.tree.index(leaf) )

    def PropagateInTree(self, variable, value):
        leaf.root.ReplaceInTree(variable, value)
        self.SimplifyToMinimum()

    def GetTreeInfo(self):
        prnt_str = ""
        for root in self.tree:
            prnt_str += "\nSYM " + repr(root)
            prnt_str += "\nSYMS" + str(id(root.symbol))
            prnt_str += "\nSI " + repr(root.sign)
            prnt_str += "\nUP " + repr(root.upper)
            prnt_str += "\nLEFT " + repr(root.left)
            prnt_str += "\nRIGHT " + repr(root.right)
            prnt_str += "\n"
        return prnt_str

###############################################################################
##################   Simplification steps #####################################
###############################################################################

    def SimplifyToMinimum(self):
        try:
            hc = True
            while(hc):
                for l in self.tree:
                    hc = False
                    if( self.GetSign(l) ):
                        print("GS", self)
                        hc = True
                    if( self.ChangeOREquals(l) ):
                        print("CO", self)
                        hc = True
                    elif( self.ChangeANDEquals(l) ):
                        print("CA", self)
                        hc = True
                    elif( self.TrueOnOR(l) ):
                        print("FA", self)
                        hc = True
                    elif( self.FalseOnOR(l) ):
                        print("FO", self)
                        hc = True
                    elif( self.TrueOnAND(l) ):
                        print("TA", self)
                        hc = True
                    elif( self.FalseOnAND(l) ):
                        print("FA", self)
                        hc = True
        except AttributeError:
            print("ERROR TREE:")
            print(self.__repr__())
            raise AttributeError


    # p <-> q -> (p -> q)^(q -> p)
    def MaterialEquivalence(self, leaf):
        if(leaf.symbol.code == "OP_IF_ONLY_IF"):
            leaf.symbol = Symbol('^')
            lbranch = leaf.left
            rbranch = leaf.right
            lbranch2,ltree = lbranch.DuplicateTree()
            self.tree += ltree
            rbranch2,rtree = rbranch.DuplicateTree()
            self.tree += rtree

            leaf.left = Leaf( Symbol('->'), True, leaf, lbranch, rbranch)
            self.tree.append(leaf.left)
            leaf.right = Leaf( Symbol('->'), True, leaf, rbranch2, lbranch2)
            self.tree.append(leaf.right)
            return True
        return False

    # p -> q -> !p v q
    def MaterialImplication(self, leaf):
        if(leaf.symbol.code == "OP_THEN"):
            leaf.symbol = Symbol("v")
            leaf.left.sign = not leaf.left.sign
            return True
        return False

    # !(p ^ q) -> (!p) v (!q)
    def DeMorganAND(self, leaf):
        if(leaf.symbol.code == "OP_AND" and not leaf.sign):
            leaf.symbol = Symbol("v")
            leaf.sign = not leaf.sign
            leaf.left.sign = not leaf.left.sign
            leaf.right.sign = not leaf.right.sign
            return True
        return False

    # !(p v q) -> (!p) ^ (!q)
    def DeMorganOR(self, leaf):
        if(leaf.symbol.code == "OP_OR" and not leaf.sign):
            leaf.symbol = Symbol("v")
            leaf.sign = not leaf.sign
            leaf.left.sign = not leaf.left.sign
            leaf.right.sign = not leaf.right.sign
            return True
        return False

    def GetSign(self,leaf):
        if(not leaf.sign):
            if(leaf.symbol.mask == "T"):
                leaf.symbol = Symbol("F")
                leaf.sign = True
            elif(leaf.symbol.mask == "F"):
                leaf.symbol = Symbol("T")
                leaf.sign = True

    def ChangeANDEquals(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_AND"):
            l = leaf.left
            r = leaf.right
            if(l.symbol.code != "IDENTIFIER" or r.symbol.code != "IDENTIFIER"):
                return False
            if(l.symbol.mask == r.symbol.mask):
                if(l.sign == r.sign):
                    u = leaf.upper
                    if(id(u.left) == id(leaf)):
                        u.left = l
                    elif(id(u.right) == id(leaf)):
                        u.right = l
                    l.upper = u
                    l.sign =not (l.sign ^ leaf.sign)
                    self.tree.pop(self.tree.index(leaf))
                else:
                    leaf.symbol = Symbol("F")
                    self.tree.pop(self.tree.index(leaf.left))
                    self.tree.pop(self.tree.index(leaf.right))
                    leaf.left = None
                    leaf.right = None
                has_changed = True
        return has_changed

    def ChangeOREquals(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_OR"):
            l = leaf.left
            r = leaf.right
            if(l.symbol.code != "IDENTIFIER" or r.symbol.code != "IDENTIFIER"):
                return False
            if(l.symbol.mask == r.symbol.mask):
                if(l.sign == r.sign):
                    u = leaf.upper
                    if(id(u.left) == id(leaf)):
                        u.left = l
                    elif(id(u.right) == id(leaf)):
                        u.right = l
                    l.upper = u
                    l.sign = not (l.sign ^ leaf.sign)
                    self.tree.pop(self.tree.index(leaf))
                else:
                    leaf.symbol = Symbol("F")
                    self.tree.pop(self.tree.index(leaf.left))
                    self.tree.pop(self.tree.index(leaf.right))
                    leaf.left = None
                    leaf.right = None
                has_changed = True
        return has_changed

    # (pvT) -> T
    def TrueOnOR(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_OR"):
            if(leaf.left.symbol.mask == "T"):
                has_changed = True
            elif(leaf.right.symbol.mask == "T"):
                has_changed = True
            if(has_changed):
                leaf.symbol = Symbol("T")
                self.tree.pop(self.tree.index(leaf.left))
                self.tree.pop(self.tree.index(leaf.right))
                leaf.left = None
                leaf.right = None
        return has_changed

    # (pvF) -> p
    def FalseOnOR(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_OR"):
            if(leaf.left.symbol.mask == "F"):
                has_changed = True
                sym = leaf.right
                dlt = leaf.left
            elif(leaf.right.symbol.mask == "F"):
                has_changed = True
                sym = leaf.left
                dlt = leaf.right
            if(has_changed):
                u = leaf.upper
                if(u != None):
                    if(id(u.left) == id(leaf)):
                        u.left = sym
                    elif(id(u.right) == id(leaf)):
                        u.right = sym
                else:
                    self.root = sym
                sym.upper = u
                sym.sign = not (sym.sign ^ leaf.sign)
                self.tree.pop(self.tree.index(leaf))
                self.tree.pop(self.tree.index(dlt))
                del(leaf)
                del(dlt)
        return has_changed

    # (p^T) -> p
    def TrueOnAND(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_AND"):
            if(leaf.left.symbol.mask == "T"):
                has_changed = True
                sym = leaf.right
                dlt = leaf.left
            elif(leaf.right.symbol.mask == "T"):
                has_changed = True
                sym = leaf.left
                dlt = leaf.right
            if(has_changed):
                u = leaf.upper
                if(u != None):
                    if(id(u.left) == id(leaf)):
                        u.left = sym
                    elif(id(u.right) == id(leaf)):
                        u.right = sym
                else:
                    self.root = sym
                sym.upper = u
                sym.sign = not (sym.sign ^ leaf.sign)
                self.tree.pop(self.tree.index(leaf))
                self.tree.pop(self.tree.index(dlt))
                del(leaf)
                del(dlt)
        return has_changed

    # (p^F) -> F
    def FalseOnAND(self, leaf):
        has_changed = False
        if(leaf.symbol.code == "OP_AND"):
            if(leaf.left.symbol.mask == "F"):
                has_changed = True
            elif(leaf.right.symbol.mask == "F"):
                has_changed = True
            if(has_changed):
                leaf.symbol = Symbol("F")
                self.tree.pop(self.tree.index(leaf.left))
                self.tree.pop(self.tree.index(leaf.right))
                leaf.left = None
                leaf.right = None
        return has_changed

    def DistribAND(self,leaf):
        if(leaf.symbol.code == "OP_AND"):
            l = leaf.left
            r = leaf.right
            if(l.symbol.code == "OP_OR" and r.symbol.code == "OP_OR" ):
                leaf.symbol = Symbol("v")

                ll1 = l.left
                lr1 = l.right
                rl1 = r.left
                rr1 = r.right

                ll2,llt = ll1.DuplicateTree()
                self.tree += llt
                lr2,lrt = lr1.DuplicateTree()
                self.tree += lrt
                rl2,rlt = rl1.DuplicateTree()
                self.tree += rlt
                rr2,rrt = rr1.DuplicateTree()
                self.tree += rrt

                nsym = Symbol("^")

                nll = Leaf(nsym, True, l, ll1, rl1)
                self.tree.append(nll)
                ll1.upper = nll
                rl1.upper = nll

                nlr = Leaf(nsym, True, l, ll2, rr1)
                self.tree.append(nlr)
                ll2.upper = nlr
                rr1.upper = nlr

                nrl = Leaf(nsym, True, r, lr1, rl2)
                self.tree.append(nrl)
                lr1.upper = nrl
                rl2.upper = nrl

                nrr = Leaf(nsym, True, r, lr2, rr2)
                self.tree.append(nrr)
                lr2.upper = nrr
                rr2.upper = nrr

                l.left = nll
                l.right = nlr
                r.left = nrl
                r.right = nrr

                return True
        return False
    
    def DistribOR(self,leaf):
        if(leaf.symbol.code == "OP_OR"):
            l = leaf.left
            r = leaf.right
            if(l.symbol.code == "OP_AND" and r.symbol.code == "OP_AND" ):
                leaf.symbol = Symbol("^")

                ll1 = l.left
                lr1 = l.right
                rl1 = r.left
                rr1 = r.right

                ll2,llt = ll1.DuplicateTree()
                self.tree += llt
                lr2,lrt = lr1.DuplicateTree()
                self.tree += lrt
                rl2,rlt = rl1.DuplicateTree()
                self.tree += rlt
                rr2,rrt = rr1.DuplicateTree()
                self.tree += rrt

                nsym = Symbol("v")

                nll = Leaf(nsym, True, l, ll1, rl1)
                self.tree.append(nll)
                ll1.upper = nll
                rl1.upper = nll

                nlr = Leaf(nsym, True, l, ll2, rr1)
                self.tree.append(nlr)
                ll2.upper = nlr
                rr1.upper = nlr

                nrl = Leaf(nsym, True, r, lr1, rl2)
                self.tree.append(nrl)
                lr1.upper = nrl
                rl2.upper = nrl

                nrr = Leaf(nsym, True, r, lr2, rr2)
                self.tree.append(nrr)
                lr2.upper = nrr
                rr2.upper = nrr

                l.left = nll
                l.right = nlr
                r.left = nrl
                r.right = nrr

                return True
        return False

