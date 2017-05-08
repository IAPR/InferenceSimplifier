from statement import Statement

class CNFStatement(Statement):
    def __init__(self, st):
        super(CNFStatement, self).__init__(st)
        self.SimplifyFNC()

    @staticmethod
    def fromLeaf(leaf):
        new_leaf, new_tree = leaf.DuplicateTree()
        cnf = CNFStatement(None)
        cnf.tree = new_tree
        cnf.root = new_leaf
        return cnf

    def Branch(self):
        def FindBranches(cnf):
            cnf_list = []        
            if(cnf == None): 
                pass       
            elif(cnf.symbol.code == "OP_AND" and cnf.sign):
                if(cnf.left.symbol.code == "OP_AND" and cnf.left.sign):
                    cnf_list = cnf_list + FindBranches(cnf.left)                 
                else:                                                
                    cnf_list.append(cnf.left)             
                if(cnf.right.symbol.code == "OP_AND" and cnf.right.sign):
                    cnf_list = cnf_list + FindBranches(cnf.right)                  
                else:                                                  
                    cnf_list.append(cnf.right)             
            return cnf_list

        print("Branching CNF Statement:", self)
        print("Tree:", self.tree)
        # Get list of node that generate new cnfsequents
        cnf_lst = FindBranches(self.root)
        if(cnf_lst == []):
            cnf_lst.append(self.root)
        # Generate that new cnfsequents
        new_cnf_list = []
        for cn in cnf_lst:
            new_cnf = CNFStatement.fromLeaf(cn)
            new_cnf_list.append(new_cnf)
        print("NEW CONS:", new_cnf_list)
        return new_cnf_list
