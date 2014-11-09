"""
Because it's convenient for the different compiler parts to share some simple data structures.
"""
from collections import namedtuple

__all__ = [
    'Token',
    'CST',
    'AST',
]


# scan (string) -> (Token,)

Token = namedtuple('Token', 'name value length')


# parse (Token,) -> (CST.Node,): concrete syntax tree

class CST:
    Node = namedtuple('Node', 'name value location')
    Location = namedtuple('Location', 'pos_start pos_end line_start col_start line_end col_end')


# abstract (CST.Node,) -> AST.Program: abstract syntax tree

class AST:
    Program = namedtuple('Program', '')
