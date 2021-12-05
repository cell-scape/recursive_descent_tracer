#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import common as c
import lexer as l
from syntax_tree import *
from tokens import *



def parser(tokens: list, statements=StmtList([])):
    """
    Parse the token stream
    """
    head, tail = c.first(tokens), c.rest(tokens)
    if head['type'] == "ID":
        peek = c.first(tail)
        if peek['type'] == "EQ":
            expr_tokens, semicolon, tokens_left = advance_statement(c.rest(tail))
            assign_node = AssignStmt(id=head, eq=peek, semicolon=semicolon)
            if not semicolon:
                statements.list.append("Syntax Error")
                return statements
            assign_node.expr = expr(expr_tokens)
            statements.list.append(assign_node)
            return parser(tokens_left, statements)
        statements.list.append("Syntax Error")
        return statements

    if head['type'] == "RESERVED":
        if head['lexeme'] == "print":
            expr_tokens, semicolon, tokens_left = advance_statement(tail)
            print_node = PrintStmt(prnt=head, semicolon=semicolon)
            if not semicolon:
                statements.list.append("Syntax Error")
                return statements
            print_node.expr = expr(expr_tokens)
            statements.list.append(print_node)
            return parser(tokens_left, statements)
        statements.list.append("Syntax Error")
        return statements
    return statements


def advance_statement(tokens: list) -> tuple:
    """
    Advance to the next semicolon, return expr list, semicolon token, and tail
    """    
    expr = []
    semicolon = None
    for token in tokens:
        if token['type'] == "SEMICOLON":
            semicolon = token
            break
        expr.append(token)
    return expr, semicolon, tokens[len(expr)+1:]


def expr(tokens: list, expr: Expr()):
    """
    Get expr ast node
    """
    head, peek, tail = c.first(tokens), c.next(tokens) c.rest(tokens)
    if head['type'] == "ID":
        term_node, _ = term([head])
    if head['type'] == "INTNUM":
        term_node, _ = term([head])
        if peek['type'] in ("PLUS", "MINUS"):
            ExprBinOp()
        if peek['type'] in ("MUL", "DIV"):
            
    if head['type'] in ("PLUS", "MINUS"):
        ExprUnaryOp()
    if head['type'] == "MINUS":
        
    if head['type'] == "LPAREN":

    if head['type'] == "RPAREN":

    if head['type'] = "SEMICOLON":
        

def term(tokens: list, ): 


def stmt(tokens):
    pass


def expr(tokens):
    pass


def term(tokens):
    pass


def factor(tokens):
    pass



def main(filename: str) -> int:
    """
    Test parser when run as a script
    """
    program = c.load_program(filename)
    tokens = l.lexer(program)

    return 0


if __name__ == "__main__":
    args = c.argparser("Abstract Syntax Tree").parse_args()
    for f in args.files:
        if not c.file_exists(f):
            sys.exit(-1)
        rc = main(f)
    sys.exit(rc)