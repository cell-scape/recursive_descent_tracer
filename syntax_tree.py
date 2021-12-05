from tokens import *


class Factor:
    pass


class Term:
    def __init__(self, factor=None):
        self.left = factor


class Expr:
    def __init__(self, term=None):
        self.left = term


class Stmt:
    def __init__(self, expr=None, semicolon=None):
        self.expr = expr
        self.semicolon = semicolon


class StmtList:
    def __init__(self, stmt_list=[]):
        self.statements = stmt_list


class Var(Factor):
    def __init__(self, name=None, value=None):
        self.id = name
        self.value = value


class IntNum(Factor):
    def __init__(self, value=None):
        self.value = value


class Grouping(Factor):
    def __init__(self, lparen=None, expr=None, rparen=None):
        self.lparen = lparen
        self.expr = expr
        self.rparen = rparen


class TermOp(Term):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right
        

class ExprBinOp(Expr):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right


class ExprUnaryOp(Expr):
    def __init__(self, op=None, operand=None):
        self.op = op
        self.operand = operand


class AssignStmt(Stmt):
    def __init__(self, id=None, eq=None, **kwds):
        self.id = id
        self.eq = eq
        super().__init__(**kwds)


class PrintStmt(Stmt):
    def __init__(self, prnt=None, **kwds):
        self.print = prnt
        super().__init__(**kwds)



