"""
Parse tokens into a parse tree (concrete syntax tree) representing tscl's formal grammar.
"""
from lib import CST
from parse import tree

__all__ = [
    'parse',
]


def parse(tokens) -> "(lib.CSTNode)":
    """
    Transform tokens into an iterable of concrete syntax trees.
    """
    return tree.cst(syntax(nodes(tokens)))


#
# Passes over flat `tokens`
#

def nodes(tokens) -> "(lib.CSTNode,)":
    """
    Generate flat CST nodes with source location information from tokens.
    """
    cursor = CST.Location(0, 0, 0, 0, 0, 0)
    previous_token = None

    for token in tokens:
        pos_start = cursor.pos_end
        pos_end = pos_start + token.length
        line_start = cursor.line_end + (1 if (previous_token and previous_token.name == 'NEWLINE') else 0)
        line_end = cursor.line_end + (1 if (previous_token and previous_token.name == 'NEWLINE') else 0)  # not right
        col_start = 0 if (previous_token and previous_token.name == 'NEWLINE') else cursor.col_end
        col_end = col_start + token.length  # which means this is wrong, too

        cursor = CST.Location(pos_start, pos_end, line_start, col_start, line_end, col_end)
        node = CST.Node(
            name=token.name,
            value=token.value,
            location=cursor,
        )

        previous_token = token
        yield node


#
# Passes over flat `nodes`
#

def syntax(nodes):
    """
    Filter nodes that are not part of the language syntax.
    """
    return filter(lambda node: node.name not in ('WS', 'NEWLINE', 'COMMENT'), nodes)
