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
    """
    Return a tscl AST starting at a CST root node.
    """
    if isinstance(node, CST.Node):
        # leaf 1:1
        return ast_leaf(node)
    elif isinstance(node, tuple):
        # branch 1:n
        return ast_branch(nodes=node)


def ast_branch(nodes) -> "AST.*":
    """
    Return the AST node for the corresponding CST branch.
    """
    # Function: (fn [] ...)
    if (nodes[0].name, getattr(nodes[1], 'name', '')) == ('LPAREN', 'KEYWORD') and nodes[1].value in ('λ', 'fn'):
        return AST.Function(
            parameters=tree(nodes[2]),
            expressions=tuple(filter(None, map(tree, nodes[3:]))),
        )
    # If: (if test true false)
    if (nodes[0].name, getattr(nodes[1], 'name', '')) == ('LPAREN', 'KEYWORD') and nodes[1].value == 'if':
        return AST.If(
            expression=tree(nodes[2]),
            then_expression=tree(nodes[3]),
            else_expression=tree(nodes[4]),
        )
    # Let: (let [] ...)
    if (nodes[0].name, getattr(nodes[1], 'name', '')) == ('LPAREN', 'KEYWORD') and nodes[1].value == 'let':
        return AST.Let(
            bindings=tree(nodes[2]),
            expressions=tuple(filter(None, map(tree, nodes[3:]))),
        )
    # Call: (...)
    if nodes[0].name == 'LPAREN':
        return AST.Call(
            expression=tree(nodes[1]),
            expressions=tuple(filter(None, map(tree, nodes[2:]))),
        )
    # List: [...]
    elif nodes[0].name == 'LBRACKET':
        return AST.List(
            expressions=tuple(filter(None, map(tree, nodes))),
        )


def ast_leaf(cst_node) -> "AST.* | None":
    """
    Return the AST node for the corresponding CST node, or None.
    """
    if cst_node.name == 'BOOLEAN':
        return AST.Boolean(cst_node.value)
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
