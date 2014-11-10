"""
Generate Python 3 AST
"""
import ast as python
from functools import singledispatch

from lib import AST as tscl

__all__ = [
    'generate',
]


@singledispatch
def generate(node):
    raise NotImplementedError('Python AST Generation Error: %r' % node)


# root

@generate.register(tscl.Program)
def _(node) -> "python.Expression":
    """
    Transform a tscl AST into an compilable Python AST.
    """
    return python.fix_missing_locations(
        python.Module(
            body=[expr(generate(node)) for node in node.expressions],
        )
    )


# values

@generate.register(tscl.Integer)
def _(node):
    return python.Num(
        n=int(node.value),
    )


@generate.register(tscl.Float)
def _(node):
    return python.Num(
        n=float(node.value),
    )


@generate.register(tscl.List)
def _(node):
    return python.List(
        elts=[generate(node) for node in node.expressions],
        ctx=python.Load(),
    )


# reference

@generate.register(tscl.Identifier)
def _(node):
    return python.Name(
        id=node.value,
        ctx=python.Load(),
    )


# call

@generate.register(tscl.Call)
def _(node):
    return python.Call(
        func=generate(node.expression),
        args=[generate(node) for node in node.expressions],
        keywords=[],
        starargs=None,
        kwargs=None,
    )


# helpers

def expr(node):
    return python.Expr(
        value=node,
    )
