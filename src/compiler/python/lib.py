"""
Because it's convenient for the different compiler parts to share some simple data structures.
"""
from collections import namedtuple

__all__ = [
    'Token',
    'CSTNode',
    'ASTNode',
]

# scan output
Token = namedtuple('Token', 'name value length')

Location = namedtuple('Location', 'pos_start pos_end line_start col_start line_end col_end')

# parse output
CSTNode = namedtuple('CSTNode', 'name value location')

# optimize output
ASTNode = namedtuple('ASTNode', 'name value children')
