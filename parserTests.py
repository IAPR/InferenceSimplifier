#!/usr/bin/env python3
from statement import Statement
from antecedent import Antecedent
from consequent import Consequent

st = Consequent("A -> ( (d v o) ^ c ) ^ (iA v iP)")
print("\n=== BRANCHING... ===")
sd = st.Branch()
print("\n========================= BRANCHES ==============================")
for s in sd:
    print(s)

#st = Statement("p v ( q ^ r)")
#st.SimplifyToMinimum()
#st1 = Statement("p ^ ( q v r)")
#st.SimplifyToMinimum()
