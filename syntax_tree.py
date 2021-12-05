#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import typing as t

import common as c
import lexer as l


Token = t.Dict['type': str, 'lexeme': str, 'literal': t.Union[str, int], 'line': int]
Factor = t.Union[int, str, t.list[Token]]
Term = t.Union[Factor, t.list[Token]]
StmtList = list
Statement = dict
Expr = dict
Term = t.Union


def stmt_list(statements: list, state={}) -> int:
    """
    Evaluate a statement list
    """
    while statements:
        


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


def main(filename: str) -> int:
    """
    Test abstract syntax tree when run as a script
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