#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import chain
import re
from string import whitespace
import sys

import common as c
from tokens import *


ID_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
OPERATORS = "+-*/="
DELIMITERS = "();"

RESERVED_WORDS = {
    "print",
    "exit",
    "quit"
}

TOKEN_TYPES = {
    "intnum": "INTNUM",
    "id": "ID",
    "reserved": "RESERVED",
    "+": "PLUS",
    "-": "MINUS",
    "/": "DIV",
    "*": "MUL",
    "(": "LPAREN",
    ")": "RPAREN",
    "=": "ASSIGN",
    ";": "SEMICOLON",
    "EOF": "EOF",
}


def lexer(program: list) -> list:
    """
    Return a stream of tokens for a program
    """
    tokens = []
    for i, line in enumerate(program):
        tokens.append(lex(line, i))
    tokens.append([Token("EOF", TOKEN_TYPES["EOF"], -1)])
    return list(chain.from_iterable(tokens))


def lex(line: str, line_number: int) -> dict:
    """
    Return a stream of tokens from a line
    """
    tokens = []
    token = []
    for char in line:
        if not token and char in whitespace:
            continue
        if token and char in whitespace:
            tokens.append(tokenize("".join(token), line_number))
            token = []
            continue
        if char in "".join(OPERATORS + DELIMITERS):
            tokens.append(tokenize("".join(token), line_number))
            tokens.append(tokenize(char, line_number))
            token = []
            continue
        token.append(char)
    return list(filter(lambda t: t, tokens))


def tokenize(lexeme: str, line: int) -> dict:
    """
    Return token objects for each lexeme
    """
    if lexeme:
        if is_reserved(lexeme):
            return Reserved(lexeme, lexeme=lexeme, ttype=TOKEN_TYPES['reserved'], line=line)
        if lexeme.isdigit():
            return Number(int(lexeme), lexeme=lexeme, ttype=TOKEN_TYPES['intnum'], line=line)
        if ID_REGEX.match(lexeme) and not is_reserved(lexeme):
            return Id(lexeme, lexeme=lexeme, ttype=TOKEN_TYPES['id'], line=line)
        if lexeme in DELIMITERS:
            return Delimiter(lexeme, lexeme=lexeme, ttype=TOKEN_TYPES[lexeme], line=line)
        if lexeme in OPERATORS:
            return Operator(lexeme, lexeme=lexeme, ttype=TOKEN_TYPES[lexeme], line=line)
        return Token(lexeme, TOKEN_TYPES[lexeme], line)
    return {}


def is_reserved(token: str) -> bool:
    """
    Is token a reserved word
    """
    if token.lower() in RESERVED_WORDS:
        return True
    return False


def get_indices(item, seq, idxs=[]) -> list:
    """
    Get all the index locations of a repeated item in a sequence
    """
    start = 0
    if idxs:
        start = idxs[-1] + 1
    if item in seq:
        offset = seq.index(item)
        return get_indices(item, seq[offset+1:], idxs + [start+offset])
    return idxs


def lexical_errors(stmt: str) -> list:
    """
    Get lexical errors in a statement
    """
    errors = []
    illegal_chars = c.illegal_chars_in_stmt(stmt)
    for char in illegal_chars:
        for index in get_indices(char, stmt):
            errors.append(f"Illegal character '{char}' at index '{index}'")
    return errors


def program_lexical_errors(program: list) -> list:
    """
    Get syntax errors at line and position
    """
    errors = {}
    for i, line in enumerate(program):
        if c.stmt_legal(line):
            continue
        errors[i] = lexical_errors(line)
    return errors


def report_lexical_errors(errors: dict) -> int:
    """
    Displays lexical errors and returns the count
    """
    print("Lexical Errors:\n---------------")
    for line, error in sorted(errors.items(), key=lambda k: errors.keys()):
        print(f"Line {line}: {error}")
    return len(errors)


def main(filename: str) -> int:
    """
    Main function for testing tokenizer when run as a script
    Prints a stream of tokens and returns an error code to the terminal
    """
    program = c.load_program(filename)
    errors = program_lexical_errors(program)
    if errors:
        return report_lexical_errors(errors)

    tokens = lexer(program)
    if tokens:
        for i, token in enumerate(tokens):
            print(f"{i}: {token}")
    return 0


if __name__ == "__main__":
    args = c.argparser("Tiny Language Lexer").parse_args()
    for f in args.files:
        if not c.file_exists(f):
            sys.exit(-1)
        rc = main(f)
    sys.exit(rc)
