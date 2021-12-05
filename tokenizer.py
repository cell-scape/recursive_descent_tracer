#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from string import whitespace
import sys

import common as c


ID_REGEX = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9_]*$")
OPERATORS = "+-*/="
DELIMITERS = "();"

RESERVED_WORDS = {
    "print",
}

TOKEN_TYPES = {
    "_empty": "EMPTY",
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
}


def lexer(program: tuple) -> tuple:
    """
    Return a stream of tokens
    """
    token_stream = []
    for line in program:
        token_stream.append(lex(line))
    return token_stream


def lex(line: str) -> dict:
    """
    Get from a line
    """
    tokens = []
    token = []
    for char in line:
        if not char and not token:
            tokens.append(tokenize(""))
            continue
        if not token and char in whitespace:
            continue
        if token and char in whitespace:
            tokens.append(tokenize("".join(token)))
            token = []
            continue
        if char in "".join(OPERATORS + DELIMITERS):
            tokens.append(tokenize("".join(token)))
            tokens.append(tokenize(char))
            token = []
            continue
        token.append(char)
    return tokens


def tokenize(token: str) -> dict:
    """
    Return token objects for each token
    """
    if token:
        if is_reserved(token):
            return {TOKEN_TYPES['reserved']: token}
        if token.isdigit():
            return {TOKEN_TYPES['intnum']: int(token)}
        elif ID_REGEX.match(token) and not is_reserved(token):
            return {TOKEN_TYPES['id']: token}
        return {TOKEN_TYPES[token]: token}
    return {TOKEN_TYPES['_empty']: token}


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


def illegal_chars_in_program(program: tuple) -> tuple:
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
