#!/usr/bin/env python3
from statement import Statement

print("None ID", id(None) % 1000)
st = Statement("( ( ( ( T v q ) v a ) v b ) v o ) v f")
st.SimplifyToMinimum()
print("None ID", id(None) % 1000)
for leaf in st.tree:
    print( repr(leaf) )
