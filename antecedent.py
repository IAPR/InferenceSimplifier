from statement import Statement

class Antecedent(Statement):
    def __init__(self, st):
        super(Antecedent, self).__init__(st)

    @staticmethod
    def fromLeaf(leaf):
        new_leaf, new_tree = leaf.DuplicateTree()
        ant = Antecedent(None)
        ant.tree = new_tree
        ant.root = new_leaf
        return ant 

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

    def Branch(self):
        def FindBranches(ant):
            antl = []
            if(ant == None):
                return []
            elif(ant.symbol.code == "OP_OR" and ant.sign):
                if(ant.left.symbol.code == "OP_OR" and ant.left.sign):
                    antl = antl + FindBranches(ant.left)
                else:
                    antl.append(ant.left)
                if(ant.right.symbol.code == "OP_OR" and ant.right.sign):
                    antl = antl + FindBranches(ant.right)
                else:
                    antl.append(ant.right)
            return antl

        # Get list of nodes that can create a new antecedent
        ant_list = FindBranches(self.root)
        # Generate list if new antecedents
        new_antecedents = []
        for an in ant_list:
            new_ant = Antecedent.fromLeaf(an)
            new_antecedents.append(new_ant)
        return new_antecedents
