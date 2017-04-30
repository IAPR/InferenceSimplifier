#!/usr/bin/env python3
from statement import Statement

print("None ID", id(None) % 1000)
st = Statement("( ( ( !p v !q ) v !r ) v !s ) v g")
print("None ID", id(None) % 1000)
for leaf in st.tree:
    print( repr(leaf) )
