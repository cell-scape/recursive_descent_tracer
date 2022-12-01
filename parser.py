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
    def __init__(self, token={'type': "", "lex": ""}):
        self.type = token['type']
        self.lexeme = token['lex']
        if self.type == "NUMBER":
            self.literal = int(self.lexeme)
        else:
            self.literal = str(self.lexeme)

    def __repr__(self):
        return f"{self.type} Token: {self.literal}"


class Lexer:
    def __init__(self, program: list):
        self.program = program
        self.tokens = []
        self.errors = []
        self.lex()

    def lex(self):
        program_tokens = []
        for i, stmt in enumerate(self.program):
            tokens = []
            if not ID.match(stmt[0]):
                self.errors.append(f"Syntax error on line {i}: statement must begin with valid identifier or 'print'")
            elif stmt[0] != PRINT and ID.match(stmt[0]) and stmt[1] != "=":
                self.errors.append(f"Syntax error on line {i}: statement must begin with assigment '<ident> = '  or 'print'")
            elif stmt[0] == PRINT and stmt[1] == "=":
                self.errors.append(f"Syntax error on line {i}: 'print' is a reserved word and cannot be used for assignment")
            if stmt[-1] != ";" and not stmt[-1].endswith(";"):
                self.errors.append(f"Syntax error on line {i}: statement must end with semicolon")
            for lexeme in stmt:
                token = {"lex": lexeme}
                if lexeme == "print":
                    token["type"] = TOKEN_TYPES[lexeme]
                elif ID.match(lexeme):
                    token["type"] = TOKEN_TYPES["id"]
                elif lexeme.isdigit():
                    token["type"] = TOKEN_TYPES["int"]
                else:
                    token["type"] = TOKEN_TYPES[lexeme]
                tokens.append(Token(token))
            program_tokens.append(tokens)
        self.tokens = program_tokens

    def get_errors(self):
        return self.errors

    def get_tokens(self, flatten=True):
        if flatten:
            self.flatten()
        return self.tokens

    def flatten(self):
        self.tokens = list(chain.from_iterable(self.tokens))


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.cur_tok = -1
        self.state = {}
        self.output = []
        self.tracing = []
        self.errors = []

    def parse(self):
        if self.stmt_list():
            self.errors.append("Error: stmt_list returned False for a statement")
        if self.cur_tok != len(self.tokens)-1:
            self.errors.append(f"Syntax error - Token {self.cur_tok} of {len(self.tokens)}: {self.tokens[self.cur_tok]}")
        return self.output, self.tracing, self.errors, self.state

    def peek(self):
        if self.cur_tok < (len(self.tokens)-1):
            return self.tokens[self.cur_tok+1]
        return self.tokens[self.cur_tok]

    def prev(self):
        if self.cur_tok > 0:
            return self.tokens[self.cur_tok-1]
        return None

    def match(self, next_tok):
        peek = self.peek()
        if peek and peek.type == next_tok:
            self.cur_tok += 1
            self.tracing.append(f"Token {self.cur_tok:<4}\t|\tToken advanced by match()")
            return True
        return False

    def stmt_list(self):
        if (len(self.tokens)-1) > self.cur_tok:
            stmt_ret = self.stmt()
            if stmt_ret:
                self.output.append(stmt_ret)
                self.tracing.append(f"Token {self.cur_tok:<4}\t|\tstmt() return value: {stmt_ret}")
                self.stmt_list()
            return False
        return True

    def stmt(self):
        if self.match("PRINT"):
            expr = self.expr()
            if expr:
                if self.match("SEMICOLON"):
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tPrint stmt() return: {expr}")
                    return expr
                return False
            return False
        elif self.match("ID"):
            var = self.tokens[self.cur_tok]
            if self.match("ASSIGN"):
                value = self.expr()
                if value:
                    if self.match("SEMICOLON"):
                        self.state[var.literal] = value
                        self.tracing.append(f"Token {self.cur_tok:<4}\t|\tAssign stmt() return: {value}")
                        return value
                    return False
                return False
            return False
        return True

    def expr(self):
        term_ret = self.term()
        if term_ret:
            expr_ret = self.expr_pr()
            if expr_ret and isinstance(expr_ret, tuple):
                if expr_ret[0] == "PLUS":
                    value = term_ret + expr_ret[1]
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tPLUS expr() return value: {value}")
                    return value
                elif expr_ret[0] == "MINUS":
                    value = term_ret - expr_ret[1]
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tMINUS expr() return value: {value}")
                    return value
                else:
                    return False
                return False
            self.tracing.append(f"Token {self.cur_tok:<4}\t|\texpr() return value: {term_ret}")
            return term_ret
        return False

    def expr_pr(self):
        op = self.peek().type
        if self.match("PLUS") or self.match("MINUS"):
            term_ret = self.term()
            if term_ret:
                expr_ret = self.expr_pr()
                if expr_ret:
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\texpr_pr() return value: {op}, {term_ret}")
                    return op, term_ret
                return False
            return False
        return True

    def term(self):
        factor_ret = self.factor()
        if factor_ret:
            term_ret = self.term_pr()
            if term_ret and isinstance(term_ret, tuple):
                if term_ret[0] == "MULTIPLY":
                    value =  factor_ret * term_ret[1]
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tMULTIPLY term() return value: {value}")
                    return value
                elif term_ret[0] == "DIVIDE":
                    value = factor_ret // term_ret[1]
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tDIVIDE term() return value: {value}")
                    return value
                else:
                    return False
                return False
            self.tracing.append(f"Token {self.cur_tok:<4}\t|\tterm() return value: {factor_ret}")
            return factor_ret
        return False

    def term_pr(self):
        op = self.peek().type
        if self.match("MULTIPLY") or self.match("DIVIDE"):
            factor_ret = self.factor()
            if factor_ret:
                term_ret = self.term_pr()
                if term_ret:
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tterm_pr() return value: {op}, {factor_ret}")
                    return op, factor_ret
                return False
            return False
        return True

    def factor(self):
        if self.match("LPAREN"):
            expr_ret = self.expr()
            if expr_ret:
                if self.match("RPAREN"):
                    self.tracing.append(f"Token {self.cur_tok:<4}\t|\tPAREN factor() return value: {expr_ret}")
                    return expr_ret
                return False
            return False
        elif self.match("NUMBER"):
            value = self.num()
            self.tracing.append(f"Token {self.cur_tok:<4}\t|\tNUMBER factor() return value: {value}")
            return value
        elif self.match("ID"):
            value = self.id()
            self.tracing.append(f"Token {self.cur_tok:<4}\t|\tID factor() return value: {value}")
            return value
        return False

    def num(self):
        return self.tokens[self.cur_tok].literal

    def id(self):
        return self.state[self.tokens[self.cur_tok].literal]


def repl(verbose=False, tracing=False):
    print("Welcome to Recursive Descent REPL ('quit' or 'exit', to exit)")
    print("---------------------------------------------------------")
    if verbose:
        print("verbose mode enabled")
    if tracing:
        print("tracing enabled")
    print("Toggle verbose or detailed tracing with 'verbose' and 'tracing' options")
    print("Valid statements are assignments or print statements")
    print("Example assignment:  id = 1 + 3 * 4 ;")
    print("Example print:       print 1 + 3 * 4 ;")
    print("---")
    state = {}
    verbose = verbose
    tracing = tracing
    while True:
        userin = input(">>> ")

        if userin.lower() in ("exit", "quit", "stop", "break"):
            print("Goodbye!")
            return 0
        if userin.lower() in ("verbose", "v"):
            if verbose:
                verbose = False
                print("verbose mode disabled")
            else:
                verbose = True
                print("verbose mode enabled")
            continue
        if userin.lower() in ("tracing", "trace"):
            if tracing:
                tracing = False
                print("tracing disabled")
            else:
                tracing = True
                print("tracing enabled")
            continue
        if not legal_chars(userin):
            print(f"You can only use chars in {ALPHABET}")
            continue

        stmt = userin.strip().split()
        if stmt:
            if not ID.match(stmt[0]):
                print(f"Invalid input {userin}: statements start with an identifier or 'print'")
                continue
            if not stmt[-1] == ";":
                print(f"Invalid input {userin}: statements end with a space separated semicolon ';'")
                continue
        else:
            continue

        lex = Lexer([stmt])
        tokens = lex.get_tokens()   
        if lex.errors:
            print(f"Tokens: {tokens}\n")
            _ = report_output(lex.errors, "Lexer Errors")
            continue

        if verbose or tracing:
            print(f"Tokens: {tokens}\n")

        p = Parser(tokens)
        p.parse()
        if verbose or tracing:
            if p.output:
                _ = report_output(p.output, "Output")
            if p.errors:
                _ = report_output(p.errors, "Errors")
            if p.state:
                state.update(p.state)
                print(f"Variables bound in parser: {state}")
        else:
            if p.output:
                print(p.output[0])
            continue
        if tracing:
            _ = report_output(p.tracing, "Tracing")
        continue


def report_output(output, title: str) -> int:
    """
    Formats parser output
    """
    print(f"{title}\n---\n")
    for i, message in enumerate(output):
        print(f"{i:<4} :  {message}")
    print("\n---\n")
    return len(output)


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


def argparser(desc="Top Down Recursive Descent Parser"):
    ap = argparse.ArgumentParser(prog="parser.py", description=desc, epilog="---")
    ap.add_argument("-i", "--interactive",
                    action="store_true",
                    dest="repl",
                    required=False,
                    help="Starts Tiny Language REPL")
    ap.add_argument("-t", "--tracing",
                    action="store_true",
                    dest="tracing",
                    required=False,
                    help="Adds extra output detail")
    ap.add_argument("-v", "--verbose",
                    action="store_true",
                    dest="verbose",
                    required=False,
                    help="Adds verbose reporting to REPL")
    ap.add_argument("-f", "--files",
                    type=str,
                    dest="files",
                    default="",
                    nargs="+",
                    metavar="FILE",
                    help="Tiny Language file(s)",
                    required=False)
    return ap


def main(filename: str, tracing=False):
    """
    Executes Tiny Language code from command line
    """
    program = load_program(filename)
    lexer = Lexer(program)
    if lexer.errors:
        _ = report_output(lexer.errors, "Lexer Errors")
    tokens = lexer.get_tokens()
    p = Parser(tokens)
    _ = p.parse()
    rc = 0
    if p.output:
        _ = report_output(p.output, "Parser Output")
    if p.errors:
        rc = report_output(p.errors, "Parser Errors")
    if p.state:
        print(f"Variable State:\n---\n\nvariables bound in parser: {p.state}\n")
    if tracing and p.tracing:
        _ = report_output(p.tracing, "Tracing Output")
    return rc


if __name__ == "__main__":
    args = argparser().parse_args()
    if args.repl:
        sys.exit(repl(verbose=args.verbose, tracing=args.tracing))

    for f in args.files:
        if not file_exists(f):
            sys.exit(-1)
        _ = main(f, tracing=args.tracing)
