"""
Abstract Syntax Tree
"""
from lib import CST
from lib import AST

__all__ = [
    'ast',
]


def ast(cst):
    return AST.Program(expressions=tuple(filter(None, map(tree, cst))))


def tree(node) -> "(lib.ASTNode)":
    if isinstance(node, CST.Node):
        # 1:1
        return ast_node(node)
    elif isinstance(node, tuple):
        # branch
        if (node[0].name, getattr(node[1], 'name', '')) == ('LPAREN', 'KEYWORD') and node[1].value in ('λ', 'fn'):
            return AST.Function(
                parameters=tree(node[2]),
                expressions=tuple(filter(None, map(tree, node[3:]))),
            )
        if node[0].name == 'LPAREN':
            return AST.Call(
                expression=tree(node[1]),
                expressions=tuple(filter(None, map(tree, node[2:]))),
            )
        elif node[0].name == 'LBRACKET':
            return AST.List(
                expressions=tuple(filter(None, map(tree, node))),
            )


def ast_node(cst_node) -> "AST.* | None":
    """
    Return the AST node for the corresponding CST node, or None.
    """
    if cst_node.name == 'INTEGER':
        return AST.Integer(cst_node.value)
    if cst_node.name == 'FLOAT':
        return AST.Float(cst_node.value)
    if cst_node.name == 'ATOM':
        return AST.Atom(cst_node.value)
    if cst_node.name == 'IDENTIFIER':
        return AST.Identifier(cst_node.value)
    if cst_node.name == 'KEYWORD':
        return AST.Keyword(cst_node.value)
