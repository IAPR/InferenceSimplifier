from symbol import Symbol
from copy import deepcopy,copy
from tree import Tree, Leaf

class Compiler:
    def __init__(self):
        self.tree = []
        self.par_stack = []
        self.next_sign = True
        self.root = None

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

    def ListTree(self):
        prnt_str = ""
        for root in self.tree:
            prnt_str += "\nSYM " + repr(root)
            prnt_str += "\nSYMS" + str(id(root.symbol))
            prnt_str += "\nSI " + repr(root.sign)
            prnt_str += "\n\tUP " + repr(root.upper)
            prnt_str += "\n\tLEFT " + repr(root.left)
            prnt_str += "\n\tRIGHT " + repr(root.right)
            prnt_str += "\n"
            prnt_str += self.DebugTree(root.left)
            prnt_str += self.DebugTree(root.right)
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
                i = i+u-1

            # Check fo empty string
            if( psym.strip() == ""):
                i += 1
                continue

            new_symbol = Symbol(psym)
            print(new_symbol.code, new_symbol.mask)
            self.AddToTree(new_symbol)
            self.tree = list(set(self.tree))
            print("CURRENT ROOT:", repr(self.root))
            print("TREE CREATED\n", self.PrintDebugTree(self.root))
            i += 1

        self.NormalizeTree()
        self.SetRoot()

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

    def SimplifyFNC(self):
        # Simplify tree
        # Order: <-> >> -> >> v >> ^
        print("Simplifying tree:", self.ConvertToString(self.root))
        has_changed = True
        while(has_changed):
            has_changed = False
            for leaf in self.tree:
                if( leaf == None ):
                    raise Exception
                elif( self.MaterialEquivalence(leaf) ):
                    print("MatE:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.MaterialImplication(leaf) ):
                    print("MatI:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DeMorganAND(leaf) ):
                    print("MAND:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DeMorganOR(leaf) ):
                    print("MoOR:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DistribOR(leaf) ):
                    print("DiOR:", self.ConvertToString(self.root))
                    has_changed = True
                    self.SimplifyToMinimum()

    def SimplifyFND(self):
        # Simplify tree
        # Order: <-> >> -> >> v >> ^
        print("Simplifying tree:", self.ConvertToString(self.root))
        has_changed = True
        while(has_changed):
            has_changed = False
            for leaf in self.tree:
                if( leaf == None ):
                    raise Exception
                elif( self.MaterialEquivalence(leaf) ):
                    print("MatE:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.MaterialImplication(leaf) ):
                    print("MatI:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DeMorganAND(leaf) ):
                    print("MAND:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DeMorganOR(leaf) ):
                    print("MoOR:", self.ConvertToString(self.root))
                    has_changed = True
                elif( self.DistribAND(leaf) ):
                    print("DAND:", self.ConvertToString(self.root))
                    has_changed = True
                    self.SimplifyToMinimum()

    def SimplifyToMinimum(self):
        hc = True
        while(hc):
            for l in self.tree:
                hc = False
                if( self.ChangeOREquals(l) ):
                    print("CORE:", self.ConvertToString(self.root))
                    hc = True
                elif( self.ChangeANDEquals(l) ):
                    print("CAND:", self.ConvertToString(self.root))
                    hc = True
                elif( self.TrueOnOR(l) ):
                    print("ToOR:", self.ConvertToString(self.root))
                    hc = True
                elif( self.FalseOnOR(l) ):
                    print("FoOR:", self.ConvertToString(self.root))
                    hc = True
                elif( self.TrueOnAND(l) ):
                    print("TAND:", self.ConvertToString(self.root))
                    hc = True
                elif( self.FalseOnAND(l) ):
                    print("FAND:", self.ConvertToString(self.root))
                    hc = True


    def PrintDebugTree(self, root, level = 0):
        print( ("  " * level) + str(root) )
        if(root != None):
            self.PrintDebugTree(root.left, level + 1)
            self.PrintDebugTree(root.right, level + 1)

    def DebugTree(self, root):
        if(root == None):
            return ""

        prnt_str = ""
        prnt_str += "\nSYM " + repr(root)
        prnt_str += "\nSYMS" + str(id(root.symbol))
        prnt_str += "\nSI " + repr(root.sign)
        prnt_str += "\n\tUP " + repr(root.upper)
        prnt_str += "\n\tLEFT " + repr(root.left)
        prnt_str += "\n\tRIGHT " + repr(root.right)
        prnt_str += "\n"
        prnt_str += self.DebugTree(root.left)
        prnt_str += self.DebugTree(root.right)
        return prnt_str

    def ConvertToString(self, leaf, level = 0):
        if(leaf == None):
            raise Exception

        ret_str = ""
        # Print left side
        if(leaf.left != None):
            if(leaf.left.symbol.code != "IDENTIFIER"):
                if(not leaf.left.sign):
                    ret_str += Symbol.symbol_table["NEGATION"]
                ret_str += Symbol.symbol_table["PAR_BEGIN"] + " "
            ret_str += self.ConvertToString(leaf.left, level + 1)
            if(leaf.left.symbol.code != "IDENTIFIER"):
                ret_str += Symbol.symbol_table["PAR_END"] + " "
        # Print leaf content
        if(not leaf.sign and leaf.symbol.code == "IDENTIFIER"):
            ret_str += Symbol.symbol_table["NEGATION"]
        ret_str += str(leaf) + " "
        # Print right side
        if(leaf.right != None):
            if(leaf.right.symbol.code != "IDENTIFIER"):
                if(not leaf.right.sign):
                    ret_str += Symbol.symbol_table["NEGATION"]
                ret_str += Symbol.symbol_table["PAR_BEGIN"] + " "
            ret_str += self.ConvertToString(leaf.right, level + 1)
            if(leaf.right.symbol.code != "IDENTIFIER"):
                ret_str += Symbol.symbol_table["PAR_END"] + " "
        # Problem solving for level 0
        if(level == 0 and not leaf.sign and leaf.symbol.code != "IDENTIFIER"):
            ret_str = "!( " + ret_str + " )"
        return ret_str

###############################################################################
##################   Simplification steps #####################################
###############################################################################

    def DuplicateTree(self,leaf):
        if(leaf == None):
            return None

        # Add To Real Tree of symbols
        def A2T(br):
            if(br == None):
                return
            self.tree.append(br)
            A2T(br.left)
            A2T(br.right)

        leaf2 = deepcopy(leaf)
        A2T(leaf2)
        return leaf2

    # p <-> q -> (p -> q)^(q -> p)
    def MaterialEquivalence(self, leaf):
        if(leaf.symbol.code == "OP_IF_ONLY_IF"):
            leaf.symbol = Symbol('^')
            lbranch = leaf.left
            rbranch = leaf.right
            lbranch2 = self.DuplicateTree(lbranch)
            rbranch2 = self.DuplicateTree(rbranch)

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
                if(id(u.left) == id(leaf)):
                    u.left = sym
                elif(id(u.right) == id(leaf)):
                    u.right = sym
                sym.upper = u
                sym.sign = not (sym.sign ^ leaf.sign)
                self.tree.pop(self.tree.index(leaf))
                self.tree.pop(self.tree.index(dlt))
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
                if(id(u.left) == id(leaf)):
                    u.left = sym
                elif(id(u.right) == id(leaf)):
                    u.right = sym
                sym.upper = u
                sym.sign = not (sym.sign ^ leaf.sign)
                self.tree.pop(self.tree.index(leaf))
                self.tree.pop(self.tree.index(dlt))
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

                ll2 = self.DuplicateTree(ll1)
                lr2 = self.DuplicateTree(lr1)
                rl2 = self.DuplicateTree(rl1)
                rr2 = self.DuplicateTree(rr1)

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

                ll2 = self.DuplicateTree(ll1)
                lr2 = self.DuplicateTree(lr1)
                rl2 = self.DuplicateTree(rl1)
                rr2 = self.DuplicateTree(rr1)

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


    def Distribution(self, leaf):
        if(leaf.symbol.code == "OP_AND"):
            main_sym = ("OP_AND", "^")
            sec_sym = ("OP_OR", "v")
        elif(leaf.symbol.code == "OP_OR"):
            sec_sym = ("OP_AND", "^")
            main_sym = ("OP_OR", "v")
        else:
            return False

        has_changed = False
        if(leaf.symbol.code == main_sym[0]):
            l = leaf.left
            r = leaf.right
            if(l.symbol.code == sec_sym[0] and r.symbol.code == sec_sym[0] ):
                ll = l.left
                lr = l.right
                rl = r.left
                rr = r.right
                if(ll.symbol.mask == rl.symbol.mask and ll.sign == rl.sign):
                    has_changed = True
                    # Change first node to v
                    leaf.symbol = Symbol(sec_sym[1])
                    # Change left node of leaf
                    ll.upper = leaf
                    leaf.left = ll
                    # Change right node of leaf
                    r.symbol = Symbol(main_sym[1])
                    r.left = lr
                    lr.upper = r
                elif(ll.symbol.mask == rr.symbol.mask and ll.sign == rr.sign):
                    has_changed = True
                    # Change first node to v
                    leaf.symbol = Symbol(sec_sym[1])
                    # Change left node of leaf
                    ll.upper = leaf
                    leaf.left = ll
                    # Change right node of leaf
                    r.symbol = Symbol(main_sym[1])
                    r.right = lr
                    lr.upper = r
                elif(lr.symbol.mask == rl.symbol.mask and lr.sign == rl.sign):
                    has_changed = True
                    # Change first node to v
                    leaf.symbol = Symbol(sec_sym[1])
                    # Change left node of leaf
                    lr.upper = leaf
                    leaf.left = lr
                    # Change right node of leaf
                    r.symbol = Symbol(main_sym[1])
                    r.left = ll
                    ll.upper = r
                elif(lr.symbol.mask == rr.symbol.mask and lr.sign == rr.sign):
                    has_changed = True
                    # Change first node to v
                    leaf.symbol = Symbol(sec_sym[1])
                    # Change left node of leaf
                    lr.upper = leaf
                    leaf.left = lr
                    # Change right node of leaf
                    r.symbol = Symbol(main_sym[1])
                    r.right = ll
                    ll.upper = r
        return has_changed
