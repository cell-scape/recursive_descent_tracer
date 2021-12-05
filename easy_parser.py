#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from itertools import chain
from pathlib import Path
import re
from string import whitespace, ascii_letters, digits
import sys

ALPHABET = whitespace + ascii_letters + digits + "+-*=();"
ID = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
OPERATORS = "+-*/="
PRECEDENCE = ("=", "+", "-", "*", "/")
DELIMITERS = "();"
PRINT = "print"
TOKEN_TYPES = {
    "id": "ID",
    "print": "PRINT",
    "int": "NUMBER",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "=": "ASSIGN",
    ";": "SEMICOLON",
    "(": "LPAREN",
    ")": "RPAREN",
}


class Token:
    def __init__(self, token={'ttype': "", "lex": "", "loc": (-1, -1, -1)}):
        self.type = token['ttype']
        self.lexeme = token['lex']
        self.line = token['loc'][0]
        self.pos= token['loc'][1]
        self.index = token['loc'][2]
        if self.type == "NUMBER":
            self.literal = int(self.lexeme)
        else:
            self.literal = str(self.lexeme)
        
    def __repr__(self):
        return "".join([f"({self.line}, {self.pos}, {self.index}) -",
                f"{self.type} Token: {self.lexeme}"])


class Lexer:
    def __init__(self, program: list):
        self.program = program
        self.lex()
    
    def __repr__(self):
        return f"Lexer: {self.program_tokens}"

    def lex(self):
        program_tokens = []
        k = 0
        for i, stmt in enumerate(self.program):
            tokens = []    
            if not ID.match(stmt[0]):
                print(f"Syntax error on line {i}: statement must begin with valid identifier or 'print'")
            elif stmt[0] != PRINT and ID.match(stmt[0]) and stmt[1] != "=":
                print(f"Syntax error on line{i}: statement must begin with assigment '<ident> = '  or 'print'")
            elif stmt[0] == PRINT and stmt[1] == "=":
                print(f"Syntax error on line {i}: 'print' is a reserved word and cannot be used for assignment")
            if stmt[-1] != ";" and not stmt[-1].endswith(";"):
                print(f"Syntax error on line {i}: statement must end with semicolon")
            for j, lexeme in enumerate(stmt):
                token = {"lexeme": lexeme}
                if lexeme == "print":
                    token["type"] = TOKEN_TYPES[lexeme]
                elif ID.match(lexeme):
                    token["type"] = TOKEN_TYPES["id"]
                elif lexeme.isdigit():
                    token["type"] = TOKEN_TYPES["int"]
                else:
                    token["type"] = TOKEN_TYPES[lexeme]
                token["loc"] = (i, j, k)
                tokens.append(Token(token))
                k += 1
            program_tokens.append(tokens)
        self.program_tokens = program_tokens
    
    def get_tokens(self, flatten=False):
        if not self.program_tokens:
            self.lex()
        if flatten: 
            if not self.flat_tokens:
                self.flatten()
            return self.flat_tokens
        return self.program_tokens

    def flatten(self):
        if not self.program_tokens:
            self.lex()
        self.flat_tokens = chain.from_iterable(self.program_tokens)
    



class StmtList:
    def __init__(self, program_tokens: list):
        self.program = program_tokens
        self.statement_list()

    def __repr__(self):
        return f"{self.stmt_list}"

    def statement_list(self):
        stmt_list = []
        for stmt in self.program:
            stmt_list.append(Stmt(stmt))
        self.stmt_list = stmt_list

    def get_stmt_list(self):
        return self.stmt_list


class Stmt:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.format_statement()

    def __repr__(self):
        return f"{self.tokens}"

    def format_statement(self):
        if self.tokens[0]["type"] == "ID":
            self.type = "ASSIGNMENT"
            self.expr_tokens = self.tokens[2-1]
            self.var = self.tokens[0]['lexeme']
            self.value = None

        elif self.tokens[0]["type"] == "PRINT":
            self.type = "PRINT"
            self.expr_tokens: self.tokens[1:-1]
            self.value = None


class Assign(Stmt):
    def __init__(self, var: str, **kwds):
        self.var = var
        self.value = None
        super().__init__(**kwds)

    def __repr__(self):
        if self.value:
            return f"{self.var} = {self.value}"
        return f"{self.var} = {self.tokens}"


class Print(Stmt):
    def __init__(self, **kwds):
        self.value = None
        super().__init__(**kwds)

    def __repr__(self):
        if self.value:
            return f"{self.tokens} = {self.value}"
        return f"{self.tokens}"


class Expr:
    def __init__(self, tokens: list):
        self.tokens = tokens

    def __repr__(self):
        return f"{self.tokens}"


class BinaryExpr(Expr):
    def __init__(self, left: Expr, op: Token, right: Expr):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

class Term:
    def __init__(self, tokens: list):
        self.tokens = tokens




class Parser:
    def __init__(self, program: list):
        self.tokens = program
        self.current_statement = 0
        self.current_token = 0


def repl():
    """
    Interactive mode
    """
    pass


def file_exists(filename: str) -> bool:
    """
    Check if the file exists and is a file
    """
    fp = Path(filename)
    return fp.exists() and fp.is_file()


def load_program(filename: str) -> list:
    """
    Returns list of program statements split into lexemes
    """
    with open(filename) as f:
        stmts = f.readlines()
        if all(map(lambda s: legal_chars(s), stmts)):
            return list(map(lambda s: s.strip().split(), stmts))


def legal_chars(stmt: str) -> bool:
    """
    Checks if characters are legal
    """
    return all(map(lambda ch: ch in ALPHABET, stmt))


def argparser(desc=""):
    ap = argparse.ArgumentParser(prog="parser", description=desc, epilog="---")
    ap.add_argument("-i", "--interactive",
                    action="store_true",
                    dest="repl",
                    required=False,
                    help="Starts Tiny Language REPL")
    ap.add_argument("-f", "--files",
                    type=str,
                    dest="files",
                    default="",
                    nargs="+",
                    metavar="FILE",
                    help="Tiny Language file(s)",
                    required=False)
    return ap


def main(filename: str) -> int:
    """
    Executes Tiny Language code from command line
    Prints only last output to the terminal, or
    starts interactive mode with -i option
    """
    return 0


if __name__ == "__main__":
    args = argparser().parse_args()
    if args.repl:
        sys.exit(repl())

    for f in args.files:
        if not file_exists(f):
            sys.exit(-1)
        rc = main(f)