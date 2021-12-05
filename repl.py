#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import common as c
import lexer as l
import parser as p


def evaluate(ir, state={}):
    """
    Evaluate IR
    """
    pass


def read(stmt: str) -> dict:
    """
    Lex and parse a statement into IR for evaluation
    """
    tokens = l.lexer(stmt)


def repl(program=[]) -> tuple:
    """
    Read-Eval-Print Loop for Tiny language
    """
    state = {}
    if program:
        for line in program:
            output, state = evaluate(read(program), state)
        for 
            try:
                output.append((f"{evaluate(read(stmt))}"))
            except Exception as e:
                output.append(f"{e}")
                return "\n".join(output), 1
        return "\n".join(output), 0
    
    pgm = "Tiny Lanugage Interpreter"
    print(f"{pgm}\n{'-'*len(pgm)}\n")
    
    output = ""
    
    while True:
        try:
            stmt = input(">>> ")
            if stmt:
                ir = read(stmt)                
                output, state = evaluate(ir, state)
                print(output)
            break
        except Exception as e:
            return f"Exception: {e}", 1
    return output, 0


def main(filename="") -> int:
    """
    Launch REPL
    """
    if filename:
        if c.file_exists(filename):
            program = c.load_program(filename)
            out, rc = repl(program)
            print(out)
            return rc
        print(f"could not interpret {filename}")
        return -1
    _, rc = repl()
    print("Goodbye!")
    return rc


if __name__ == "__main__":
    args = c.argparse("Tiny Language REPL").parse_args()
    sys.exit(main(args.filename))
