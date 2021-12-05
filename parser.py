#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import common as c
import lexer as lx


def parse(tokens: tuple):
    """
    Parse the token stream
    """
    pass


def stmt_list(tokens):
    pass


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
    tokens = lx.lexer(program)

    return 0


if __name__ == "__main__":
    args = c.argparser("Tiny Parser").parse_args()
    if c.file_exists(args.filename):
        sys.exit(main(args.filename))
    sys.exit(-1)
