class Symbol:
    symbol_table = {
        "OP_AND" : "^",
        "OP_OR" : "v",
        "OP_THEN" : "->",
        "OP_IF_ONLY_IF" : "<->",
        "PAR_BEGIN" : "(",
        "PAR_END" : ")",
        "NEGATION" : "!"
    }

    def __init__(self, sym):
        self.code = "UNKNOWN"
        self.mask = sym

        if(sym.strip() == ""):
            self.code = "SPACE"
            return

        for code,symbol in self.symbol_table.items():
            if(sym == symbol):
                self.code = code
                return
        if(sym.isalpha()):
            self.code = "IDENTIFIER"

    def __repr__(self):
        return self.mask

    def __str__(self):
        return self.__repr__()
