from tokens import *


class Factor:
    def __init__(self):
        pass


class Term:
    def __init__(self, factor=None):
        self.factor = factor

    def __repr__(self):
        return f"Term: {self.factor}"


class Expr:
    def __init__(self, term=None):
        self.term = term

    def __repr__(self):
        return f"Expr: {self.term}"


class Stmt:
    def __init__(self, expr=None, semicolon=None):
        self.expr = expr
        self.semicolon = semicolon


class StmtList:
    def __init__(self, stmt_list=[]):
        self.list = stmt_list

    def __repr__(self):
        return f"{self.list}"

class Var(Factor):
    def __init__(self, name=None, value=None):
        self.id = name
        self.value = value

    def __repr__(self):
        return self.value


class IntNum(Factor):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return self.value


class Grouping(Factor):
    def __init__(self, lparen=None, expr=None, rparen=None):
        self.lparen = lparen
        self.expr = expr
        self.rparen = rparen

    def __repr__(self):
        return f"({self.expr})"


class TermOp(Term):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"


class ExprBinOp(Expr):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"


class ExprUnaryOp(Expr):
    def __init__(self, op=None, operand=None):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"{self.op}{self.operand}"


class AssignStmt(Stmt):
    def __init__(self, id=None, eq=None, **kwds):
        self.id = id
        self.eq = eq
        super().__init__(**kwds)
    
    def __repr__(self):
        return f"{self.id} = {self.expr};"


class PrintStmt(Stmt):
    def __init__(self, prnt=None, **kwds):
        self.print = prnt
        super().__init__(**kwds)

    def __repr__(self):
        return f"print {self.expr};"
