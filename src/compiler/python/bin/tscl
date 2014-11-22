#!/usr/local/bin/python3
import os
import argparse

from preprocess import preprocessor
from lex import lexer
from parse import parser
from abstract import tree
from generate import python_ast


def compilef(path):
    """
    Compile a source file at the given path.
    """
    with open(path, 'r', encoding='utf-8') as source_file:
        return compiles(
            source=source_file.read(),
            name=os.path.basename(path),
        )


def compiles(source, name):
    """
    Compile a source string.
    """
    source = preprocessor.preprocess(source)
    tokens = lexer.lexs(source)
    cst = parser.parse(tokens)
    ast = tree.ast(cst)
    target = python_ast.generate(ast)
    return compile(target, name, 'exec')


if __name__ == '__main__':
    """
    Run this script from the command line passing a source file path as the first argument.
    """
    args = argparse.ArgumentParser(prog='tscl')
    args.add_argument('source', help='The tscl source file to run.')
    eval(compilef(args.parse_args().source))
