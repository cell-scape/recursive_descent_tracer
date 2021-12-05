#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import typing as t
import sys

import common as c
import lexer as l
from syntax_tree import *
from tokens import *



def parser(tokens: t.list[Token], stmt_list=StmtList([])):
    """
    Parse the token stream
    """
    if tokens:
        token, tokens = tokens[0], tokens[1:]
    if token['type'] == "ID":
        pass




def statement(tokens: t.list[Token], state: dict) -> tuple:
    """
    Evaluate a statement, return value and state
    Assignments will return the assigned value
    """
    if tokens[0]['type'] == "ID":
        return assignment(tokens, state)
    if tokens[0]['type'] == "RESERVED":
        return builtin(tokens, state)
    else:



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