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

# parse output
CSTNode = namedtuple('CSTNode', 'token line column children')

# optimize output
ASTNode = namedtuple('ASTNode', 'name value children')
