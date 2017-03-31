from antecedent import Antecedent
from consequent import Consequent

class Rule:
    def __init__(self, ant_str, con_str):
        self.antecedent = Antecedent(ant_str)
        print("ANTECEDENT:", str(self.antecedent))
        self.consequent = Consequent(con_str)
        print("CONSEQUENT:", str(self.consequent))

    def __str__(self):
        return str(self.antecedent) + " -> " + str(self.consequent)

    def __repr__(self):
        s =  "ANTECEDENT" + str(self.antecedent) + "\n\t"
        s += str(self.antecedent.tree) + "\n"
        s += "CONSEQUENT" + str(self.consequent) + "\n\t" 
        s += str(self.consequent.tree) + "\n"
        return s

    def __eq__(self, other):
        ant_st1 = str(self.antecedent)
        con_st1 = str(self.consequent)
        ant_st2 = str(other.antecedent)
        con_st2 = str(other.consequent)
        return ant_st1 == ant_st2 and con_st1 == con_st2

    def Verify(self):
        # Check if consequent is an identifier
        pass

    @staticmethod
    def TranslateToRules(antecedent, consequent):
        separator = Antecedent( str(consequent) )
        sep_list = separator.Branch()

        con_list = []
        for sep in sep_list:
            newcon = Consequent( str(sep) )
            con_list.append( newcon )

        rule_list = []
        i = 0
        while(i < len(con_list)):
            ant_str = str(antecedent)
            buf_lst = con_list.copy()
            buf_lst.pop(i)
            for buf in buf_lst:
                ant_str += " ^ " + str(buf)
            new_rule = Rule(ant_str, str(con_list[i]) )
            rule_list.append(new_rule)
            i += 1
        return rule_list
