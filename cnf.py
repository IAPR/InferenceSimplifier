from statement import Statement

class Consequent(Statement):
    def __init__(self, st):
        super(Consequent, self).__init__(st)

    @staticmethod
    def fromLeaf(leaf):
        new_leaf, new_tree = leaf.DuplicateTree()
        con = Consequent(None)
        con.tree = new_tree
        con.root = new_leaf
        return con

    def SimplifyFNC(self):
        # Simplify tree
        # Order: <-> >> -> >> v >> ^
        has_changed = True
        while(has_changed):
            has_changed = False
            for leaf in self.tree:
                if( leaf == None ):
                    raise Exception
                elif( self.MaterialEquivalence(leaf) ):
                    has_changed = True
                elif( self.MaterialImplication(leaf) ):
                    has_changed = True
                elif( self.DeMorganAND(leaf) ):
                    has_changed = True
                elif( self.DeMorganOR(leaf) ):
                    has_changed = True
                elif( self.DistribOR(leaf) ):
                    has_changed = True
                    self.SimplifyToMinimum()

    def Branch(self):
        def FindBranches(con):
            con_list = []        
            if(con == None): 
                pass       
            elif(con.symbol.code == "OP_AND" and con.sign):
                if(con.left.symbol.code == "OP_AND" and con.left.sign):
                    con_list = con_list + FindBranches(con.left)                 
                else:                                                
                    con_list.append(con.left)             
                if(con.right.symbol.code == "OP_AND" and con.right.sign):
                    con_list = con_list + FindBranches(con.right)                  
                else:                                                  
                    con_list.append(con.right)             
            return con_list

        print("Branching consequent:", self)
        print("Tree:", self.tree)
        # Get list of node that generate new consequents
        con_lst = FindBranches(self.root)
        if(con_lst == []):
            con_lst.append(self.root)
        # Generate that new consequents
        new_consequents = []
        for cn in con_lst:
            new_con = Consequent.fromLeaf(cn)
            new_consequents.append(new_con)
        print("NEW CONS:", new_consequents)
        return new_consequents
