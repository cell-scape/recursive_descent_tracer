


class Token:
    def __init__(self, lexeme=None, ttype=None, line=None):
        self.type = ttype
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return (f"{self.type} Token: {self.lexeme}")


class Operator(Token):
    def __init__(self, op: str, **kwds):
        self.op = op
        if op in ("/", "*"):
            self.operand = "Factor"
        elif op in ("+", "-"):
            self.operand = "Term"
        elif op == "=":
            self.operand = "Stmt"
        super().__init__(**kwds)


class Delimiter(Token):
    def __init__(self, delim: str, **kwds):
        self.delim = delim
        if delim in ("(", ")"):
            self.delimits = "Expr"
        elif delim == ";":
            self.delimits = "Stmt"
        super().__init__(**kwds)


class Reserved(Token):
    def __init__(self, name: str, **kwds):
        self.name = name
        super().__init__(**kwds)


class Id(Token):
    def __init__(self, name: str, **kwds):
        self.name = name
        super().__init__(**kwds)


class Number(Token):
    def __init__(self, value: int, **kwds):
        self.value = value
        super().__init__(**kwds)