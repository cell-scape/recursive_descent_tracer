# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from string import ascii_letters, digits, whitespace


ALPHABET = ascii_letters + digits + whitespace + "_-=+*/();"


def argparser(desc: str):
    ap = argparse.ArgumentParser(prog=__name__, description=desc, epilog="---")
    ap.add_argument("-f, --file",
                    type=str,
                    default="",
                    required=False,
                    metavar="FILE",
                    nargs="*",
                    help="Tiny language file(s) to process")
    return ap


def file_exists(filename: str) -> bool:
    fp = Path(filename)
    return fp.exists() and fp.is_file()


def load_program(filename: str) -> tuple:
    """
    Read the program into a list of strings
    """
    with open(filename) as f:
        return tuple(map(lambda line: line.strip(), f.readlines()))


def program_legal(program: tuple) -> bool:
    """
    check if all chars in program are legal
    """
    return all(map(lambda l: string_legal(l), program))


def string_legal(s: str) -> bool:
    """
    Check if all chars in string are legal
    """
    return all(map(lambda c: char_legal(c), s))


def char_legal(c: str) -> bool:
    """
    Check if char is in alphabet
    """
    return c in ALPHABET


def illegal_chars_in_string(s: str) -> tuple:
    """
    Return illegal chars in a string
    """
    return set(filter(lambda c: not char_legal(c), s))
