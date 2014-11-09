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

Location = namedtuple('Location', 'pos_start pos_end line_start col_start line_end col_end')


class CSTNode:
    CSTNodeState = namedtuple('CSTNodeState', 'name value location')

    def __init__(self, name, value, location):
        self._state = CSTNode.CSTNodeState(name, value, location)

    def __getattr__(self, item):
        return getattr(self._state, item)

# optimize output
ASTNode = namedtuple('ASTNode', 'name value children')
