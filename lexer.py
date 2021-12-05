#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import chain
import re
from string import whitespace
import sys

import common as c


ID_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
OPERATORS = "+-*/="
DELIMITERS = "();"

RESERVED_WORDS = {
    "print",
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
    Return a stream of tokens
    """
    tokens = []
    for i, line in enumerate(program):
        tokens.append(lex(line, i))
    tokens.append(_tokenize("EOF", TOKEN_TYPES["EOF"], -1, -1))
    return list(chain.from_iterable(tokens))


def lex(line: str, line_number: int) -> dict:
    """
    Get tokens from a line
    """
    tokens = []
    token = []
    for char in enumerate(line):
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
            return _tokenize(lexeme, TOKEN_TYPES['reserved'], line)
        if lexeme.isdigit():
            return _tokenize(int(lexeme), TOKEN_TYPES['intnum'], line)
        if ID_REGEX.match(lexeme) and not is_reserved(lexeme):
            return _tokenize(lexeme, TOKEN_TYPES['id'], line)
        return _tokenize(lexeme, TOKEN_TYPES[lexeme], line)
    return {}


def _tokenize(lexeme: str, ttype: str, line: int) -> dict:
    """
    Return token dictionary
    """
    return {
        'type': ttype,
        'lexeme': str(lexeme),
        'literal': lexeme,
        'line': line
    }


def is_reserved(token: str) -> bool:
    """
    Is token a reserved word (upper or lower, zero tolerance)
    """
    if token.strip().lower() in RESERVED_WORDS:
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


def illegal_chars_in_program(program: list) -> list:
    """
    Report syntax errors at line and position
    """
    errors = []
    for i, line in enumerate(program):
        if c.string_legal(line):
            continue
        illegal_chars = c.illegal_chars_in_string(line)
        for ic in illegal_chars:
            for idx in get_indices(ic, line):
                errors.append(f"Line {i}: illegal char '{ic}' at index {idx}")
    return errors


def main(filename: str) -> int:
    """
    Main function for testing tokenizer when run as a script
    Prints a stream of tokens and returns an error code to the terminal
    """
    program = c.load_program(filename)
    errors = illegal_chars_in_program(program)
    if errors:
        print("Syntax error: Illegal characters in program\n-------------")
        for error in errors:
            print(f"{error}\n---")
        return len(errors)

    tokens = lexer(program)
    if tokens:
        for i, token in enumerate(tokens):
            print(f"Line {i}: {token}")
    return 0


if __name__ == "__main__":
    args = c.argparser("Tiny Language Lexer").parse_args()
    if c.file_exists(args.filename):
        sys.exit(main(args.filename))
    sys.exit(-1)
