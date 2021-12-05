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


def read(program: list, n=0):
    """
    Lex and parse statements into AST for evaluation
    """
    for stmt in program:
        if not c.stmt_legal(stmt):
            errors = l.lexical_errors(stmt)
            raise Exception(errors)
    tokens =  l.lex(stmt, n)



def repl(program=[]) tuple:
    """
    Read-Eval-Print Loop for Tiny language
    """
    state = {}
    if program:
        for stmt in program:
            try:
                output, state = evaluate(read(program), state)
            except Exception as e:
                return e.args[0], 1
        return output, 0
    
    pgm = "Tiny Lanugage Interpreter"
    print(f"{pgm}\n{'-'*len(pgm)}\n")
    
    output = None
    n = 0
    while True:
        try:
            stmt = input(">>> ")
            if stmt:
                ir = read(stmt, n)                
                output, state = evaluate(ir, state)
                print(output)
        except Exception as e:
            return f"Exception: {e}", 1
    n += 1
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
