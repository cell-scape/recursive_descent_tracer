# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from string import ascii_letters, digits, whitespace


ALPHABET = ascii_letters + digits + whitespace + "_-=+*/();"


def argparser(desc: str):
    ap = argparse.ArgumentParser(prog=__name__, description=desc, epilog="---")
    ap.add_argument("-f, --files",
                    type=str,
                    default="",
                    dest="files",
                    required=False,
                    metavar="FILE",
                    nargs="+",
                    help="Tiny language file(s) to process")
    return ap


def file_exists(filename: str) -> bool:
    fp = Path(filename)
    return fp.exists() and fp.is_file()


def load_program(filename: str) -> tuple:
    """
    Read the program into a list of all lowercase strings
    """
    with open(filename) as f:
        return tuple(map(lambda line: line.lower().strip(), f.readlines()))


def program_legal(program: tuple) -> bool:
    """
    check if all chars in program are legal
    """
    return all(map(lambda stmt: stmt_legal(stmt), program))


def stmt_legal(stmt: str) -> bool:
    """
    Check if all chars in statement are legal
    """
    return all(map(lambda char: char_legal(char), stmt))


def char_legal(char: str) -> bool:
    """
    Check if char is in alphabet
    """
    return char in ALPHABET


def illegal_chars(stmt: str) -> tuple:
    """
    Return illegal chars in a stmt
    """
    return set(filter(lambda char: not char_legal(char), stmt))


def first(lst: list) -> list:
    if len(lst) < 2:
        return lst
    return lst[0]


def rest(lst: list) -> list:
    if len(lst) < 2:
        return []
    return lst[1:]


def take(lst: list, n=1) -> list:
    if n < 1:
        return []
    if len(lst) < 2:
        return lst
    if n > len(lst):
        return lst
    return lst[:n]